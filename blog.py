import sys, os, time, random, re, shutil


try:
    import unidecode
    import markdown
    import gfm
    from progressbar import *
except:
    print "[ERROR] Some python modules are missing. Check requirements.txt and ensure all modules are installed."
    exit()

def usage():
    print "usage: python blog.py compile"
    print "                      new [post title]"
    
    
try:
    action = sys.argv[1]
except:
    usage()
    exit()
    
def dash_phrase(phrase):
    phrase = phrase.lower()
    phrase = unidecode.unidecode(phrase.decode("utf-8"))
    words = pattern.sub('', phrase)
    words = words.split()
    return '-'.join(words)
    
# match all non-whitespace and non-alphanumeric
pattern = re.compile('([^\s\w]|_)+')
    
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
        self.minicontent = re.sub('<[^<]+?>', '', self.gfm)
		
        if len(self.minicontent) > 500:
            self.minicontent = self.minicontent[:500] + "..."
        
#        print "processing \""+filename+"\""
#        print "\tproperties: "+str(self.prop)
        
        # adjust folder filename if necessary
        newfilename = str((int(time.mktime(time.strptime(self.prop['date'], '%Y-%m-%d %H:%M:%S'))))/60)+" - "+self.prop['title']+".post"
        
        newfilename = unidecode.unidecode(newfilename.decode("utf-8"))
        self.prop["title"] = unidecode.unidecode(self.prop["title"].decode("utf-8"))
        
        if newfilename != foldername:
            print "[INFO] Renaming \""+foldername+"\" to\""+newfilename+"\""
            try:
                os.rename("posts/"+foldername, "posts/"+newfilename)
                self.folder = newfilename
            except:
                print "[WARNING] Could not rename \""+foldername+"\"! Skipping..."
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

    # build all md files in posts
    for e in all_posts:
        if not e.endswith(".post"):
            continue
    
        # open the content markdown file        
        content = Content("posts/"+e+"/content.md", e)
        if "hidden" in content.prop and content.prop["hidden"] == "true":
            pbar.update(cur_count+1)
            cur_count+=1
            continue

        e = content.folder 
        
        groups.append(content)
            
#        if len(groups) > 10:
#            groups.pop(0)
        
        # write the contents to an index file
        index = open("posts/"+e+"/index.html", "w")
        index.write(content.gfm)
        index.close()
                
        tcontent = content.gfm
        tcontent = tcontent.replace("src=\"", "src=\"../../posts/"+e+"/")
        temp_template = template.replace("$content", tcontent)
            
        tdate = content.prop["date"]
        if (tdate.endswith(" 00:00:00")):
            tdate = tdate[:-9]
        temp_template = temp_template.replace("$date", tdate)
            
        temp_template = temp_template.replace("$categories", content.prop["categories"])
        temp_template = temp_template.replace("$id", content.prop["id"])
        temp_template = temp_template.replace("$title", content.prop["title"])

        dirname = dash_phrase(content.prop["title"]) + "-" + content.prop["id"]
        
        content.dirname = dirname
        
        os.mkdir("blog/"+dirname)
        blog = open("blog/"+dirname+"/index.html", "w")
        blog.write(temp_template)
        blog.close()
        
        pbar.update(cur_count+1)
        cur_count+=1
    
    print "All Done!"
    
    # build the category pages
    # load the template
    tfile = open("layout/template.html", "r")
    template = tfile.read()
    tfile.close()
    
    groups = groups[::-1]
    template = template.replace("<!-- entry_group", "")
    template = template.replace("entry_group -->", "")
    template = template.replace("$title", "VGMoose's Blog")
    template = template.replace("$entry_group", '<br>'.join([(groups[x].prop["date"][:4]+": <a href=\"blog/"+groups[x].dirname+"\">"+groups[x].prop["title"]+"</a> <div class='minidescription'>")+groups[x].minicontent+"</div>" for x in range(0, len(groups))]))
    main = open("index.html", "w")
    main.write(template)
    main.close()
    
    
if action == "new":
    
    # get the time we are making this post on
    init_time = time.time()
    
    # load a name for the post if necessary
    if sys.argv[2:] != []:
        postname = ' '.join(sys.argv[2:])
    else:
        postname = "Untitled Post"
        
    # set the post full name with the time offset
    filename = str(int(init_time)/60)+" - "+postname+".post"
        
    # make the directory of this post
    os.mkdir("posts/"+filename)
    
    # create the content file
    f = open("posts/"+filename+"/content.md", "w")
    
    # print out the path to the created file
    print "posts/"+filename+"/content.md"
    
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
    os.system("open -a Brackets \""+"posts/"+filename+"/content.md\"")
