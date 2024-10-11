import sys, os, time, random, re, shutil, json
import unicodedata

try:
    import unidecode
    import markdown
    import gfm
    from progressbar import *
except:
    print("[ERROR] Some python modules are missing. Check requirements.txt and ensure all modules are installed.")
    exit()

def usage():
    print("usage: python blog.py compile")
    print("                      new [post title]")
    
    
try:
    action = sys.argv[1]
except:
    usage()
    exit()

def ascii(words):
    return unicodedata.normalize('NFD', words).encode('ascii', 'ignore').decode("utf-8")
    
def dash_phrase(phrase):
    phrase = ascii(phrase.lower())
    words = pattern.sub('', phrase)
    words = words.split()
    return '-'.join(words)
    
# match all non-whitespace and non-alphanumeric
pattern = re.compile(r'([^\s\w]|_)+')

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
    
class Content:
    def __init__(self, filename, foldername):
        outfile = open(filename, "r")
        lines = outfile.readlines()
        self.prop = {}
        self.folder = foldername
                 
        # we expect first line to be three dashes
        if lines[0] == "---\n":
            count = 1
            # keep reading until next ---
            while lines[count] != "---\n":
                colonpos = lines[count].find(":")
                prop = lines[count][:colonpos]
                self.prop[prop] = lines[count][colonpos+1:-1].strip()
                count += 1
                
        self.content = ''.join(lines[count+1:])
                
        outfile.close()
        
        self.buildHTML()
        self.minicontent = re.sub(r'<[^<]+?>', '', self.gfm)
        
        if len(self.minicontent) > 500:
            self.minicontent = self.minicontent[:500] + "..."
        
#        print "processing \""+filename+"\""
#        print "\tproperties: "+str(self.prop)
        
        # adjust folder filename if necessary
        newfilename = str((int(time.mktime(time.strptime(self.prop['date'], '%Y-%m-%d %H:%M:%S'))))//60)+" - "+self.prop['title']+".post"
        
        newfilename = ascii(newfilename.replace("?",""))
        self.prop["title"] = ascii(self.prop["title"])
        
        if newfilename != foldername:
            print("[INFO] Renaming \""+foldername+"\" to\""+newfilename+"\"")
            try:
                os.rename("posts/"+foldername, "posts/"+newfilename)
                self.folder = newfilename
            except:
                print("[WARNING] Could not rename \""+foldername+"\"! Skipping...")
                self.prop["hidden"] = "true"
                        
    def buildHTML(self):
        # parse gfm to html
        try:
            self.gfm = markdown.markdown(self.content, ['gfm'])
        except UnicodeDecodeError:
            self.gfm = markdown.markdown(unidecode.unidecode(self.content.decode("utf-8")), ['gfm'])
        
if action == "compile":
    
    posts = []
    
    # load the template
    tfile = open("layout/template.html", "r")
    template = tfile.read()
    tfile.close()
    
    template = template.replace("href=\"", "href=\"../../")
    template = template.replace("src=\"", "src=\"../../")
    template = template.replace("href=\"../../http", "href=\"http")
    template = template.replace("src=\"../../http", "src=\"http")
    template = template.replace("<!-- single_entry", "")
    template = template.replace("single_entry -->", "")
    
    # build the blog pages
    if os.path.isdir("blog"): 
        shutil.rmtree("blog")
    os.mkdir("blog")
    
    groups = []
    
    all_posts = os.listdir("posts")
    all_posts.sort()
    total_posts = len(all_posts)-1
    cur_count = 0
    
    widgets = ['Compiling ', Percentage(), ' ', Bar("*"), ' ', Counter(), '/', str(total_posts)]
    pbar = ProgressBar(widgets=widgets, maxval=total_posts).start()

    # keep track of all unique words and their post IDs
    vocab = {}
    
    # keep track of all uris (id -> uri)
    urimap = {}
    
    # keep track of all human readable titles (id -> title)
    humanmap = {}

    # build all md files in posts
    for e in all_posts:
        if not e.endswith(".post"):
            continue
    
        # open the content markdown file        
        content = Content("posts/"+e+"/content.md", e)
        e = content.folder 
        
        if "hidden" not in content.prop or content.prop["hidden"] != "true":
            groups.append(content)
            
#        if len(groups) > 10:
#            groups.pop(0)
        
        # write the contents to an index file
        index = open("posts/"+e+"/index.html", "w")
        index.write(content.gfm)
        index.close()
        		
        nopunc = re.sub(r'[?! -.:/]', ' ', content.gfm.lower()).replace("\n", " ")

        words = re.sub(r'<[^<]+?>', '', nopunc).split(" ")
        for word in words:
#            word = re.sub('[?! -.]', '', word.lower()).replace("\n",'')
            if not word in vocab:
                vocab[word] = set()
            vocab[word].add(content.prop["id"])
                
        tcontent = content.gfm

        tdate = content.prop["date"]
        if (tdate.endswith(" 00:00:00")):
            tdate = tdate[:-9]

        # for posts before 2024, we do a hackier way of replacing the src and href
        if (int(tdate[:4]) < 2024):
            tcontent = tcontent.replace("src=\"", "src=\"../../posts/"+e+"/")
        else:
            tcontent = tcontent.replace("src=\"./", "src=\"../../posts/"+e+"/")
        tcontent = tcontent.replace("href=\"./", "href=\"../../posts/"+e+"/")
        temp_template = template.replace("$content", tcontent)
            
        temp_template = temp_template.replace("$date", tdate)
        
        # get appropriately sized ad based on how long this entry is
        if len(tcontent) >= 1800:
            appropriate_ad = '<ins class="adsbygoogle" style="display:inline-block;width:120px;height:600px" data-ad-client="ca-pub-8148658375496745" data-ad-slot="5165595306"></ins>'
        else:
            appropriate_ad = '<ins class="adsbygoogle" style="display:inline-block;width:120px;height:240px" data-ad-client="ca-pub-8148658375496745" data-ad-slot="2990858106"></ins>'
            
        temp_template = temp_template.replace("$categories", content.prop["categories"])
        temp_template = temp_template.replace("$id", content.prop["id"])
        temp_template = temp_template.replace("$title", content.prop["title"])
        temp_template = temp_template.replace("$adcode", appropriate_ad)

        dirname = dash_phrase(content.prop["title"]) + "-" + content.prop["id"]
        
        content.dirname = dirname
        
        urimap[content.prop["id"]] = "/blog/"+dirname+"/"
        humanmap[content.prop["id"]] = content.prop["title"]
        
        os.mkdir("blog/"+dirname)
        blog = open("blog/"+dirname+"/index.html", "w")
        blog.write(temp_template)
        blog.close()
        
        # if this is the 404 page ID, hardcoded
        if (content.prop["id"] == "9298654889"):
            h404 = open("404.html", "w")
            h404.write(open("layout/404.html", "r").read())
            temp_template.replace("../../", "https://vgmoose.com/")
            h404.write(temp_template)
            h404.close()
        
        pbar.update(cur_count)
        cur_count+=1
    
    print("All Done!")
#    print json.dumps(vocab, cls=SetEncoder, sort_keys=True, indent=4, separators=(',', ': '))
    
    # build the category pages
    # load the template
    tfile = open("layout/template.html", "r")
    template = tfile.read()
    tfile.close()
    
    groups = groups[::-1]
    template = template.replace("<!-- entry_group", "")
    template = template.replace("entry_group -->", "")
    template = template.replace("<!-- home_page", "")
    template = template.replace("home_page -->", "")
    template = template.replace("$title", "VGMoose's Blog")
    template = template.replace("$entry_group", '<br>'.join([(groups[x].prop["date"][:4]+": <a href=\"blog/"+groups[x].dirname+"\">"+groups[x].prop["title"]+"</a> <div class='minidescription'>")+groups[x].minicontent+"</div>" for x in range(0, len(groups))]))
    main = open("index.html", "w")
    main.write(template)
    main.close()
    
    # load the template
    tfile = open("layout/template.html", "r")
    template = tfile.read()
    tfile.close()
    
    template = template.replace("<!-- search_group", "")
    template = template.replace("search_group -->", "")
    template = template.replace("$title", "VGMoose.com Search")
    template = template.replace("$search_vocab", json.dumps(vocab, cls=SetEncoder, sort_keys=True, indent=4, separators=(',', ': ')))
    template = template.replace("$search_lookup", json.dumps(humanmap, cls=SetEncoder, sort_keys=True, indent=4, separators=(',', ': ')))
    template = template.replace("href=\"", "href=\"../")
    template = template.replace("src=\"", "src=\"../")
    template = template.replace("../http", "http")
    
    # build the search page
    try:
        os.mkdir("search")
    except:
        pass
    search = open("search/index.html", "w")
    search.write(template)
    search.close()
    
    redirs = open("js/redirects.js", "w")
    redirs.write("all_posts = " + json.dumps(urimap, cls=SetEncoder, sort_keys=True, indent=4, separators=(',', ': ')) + ";")
    redirs.close()
    
    
if action == "new":
    
    # get the time we are making this post on
    init_time = time.time()
    
    # load a name for the post if necessary
    if sys.argv[2:] != []:
        postname = ' '.join(sys.argv[2:])
    else:
        postname = "Untitled Post"
        
    # set the post full name with the time offset
    filename = str(int(init_time)//60)+" - "+postname+".post"
        
    # make the directory of this post
    os.mkdir("posts/"+filename)
    
    # create the content file
    f = open("posts/"+filename+"/content.md", "w")
    
    # print out the path to the created file
    print("posts/"+filename+"/content.md")
    
    f.write("---\n")
    f.write("layout: post\n")
    f.write("title: " + postname + "\n")
    f.write("date: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(init_time)) + "\n")
    f.write("comments: true\n")
    f.write("categories: \n")
    f.write("id: %0.10d\n" % random.randint(0, 9999999999))
    f.write("---\n\n")
    f.close()
    
    # open it in the specified Editor
    os.system("open -a Visual\\ Studio\\ Code \""+"posts/"+filename+"/content.md\"")
