import sys, os, time, random, unidecode, re, shutil

try:
    import markdown
    import gfm
except:
    print "install py-gfm and markdown modules"

def usage():
    print "usage: python blog.py compile"
    print "                      new [post title]"
    
    
try:
    action = sys.argv[1]
except:
    usage()
    
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
        lines = open(filename, "r").readlines()
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
        
        self.buildHTML()
        
#        print "processing \""+filename+"\""
#        print "\tproperties: "+str(self.prop)
        
        # adjust folder filename if necessary
        newfilename = str((int(time.mktime(time.strptime(self.prop['date'], '%Y-%m-%d %H:%M:%S'))))/60)+" - "+self.prop['title']+".post"
        
        newfilename = unidecode.unidecode(newfilename.decode("utf-8"))
        
        if newfilename != foldername:
            print "\trenaming to \""+newfilename+"\""
            self.folder = newfilename
            os.rename("posts/"+foldername, "posts/"+newfilename)
                        
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
    
    # build the blog pages
    shutil.rmtree("blog")
    os.mkdir("blog")

    # build all md files in posts
    for e in os.listdir("posts"):
        if not e.endswith(".post"):
            continue
    
        # open the content markdown file        
        content = Content("posts/"+e+"/content.md", e)
        e = content.folder 
        
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

        dirname = dash_phrase(content.prop["title"]) + "-" + content.prop["id"]
        
        os.mkdir("blog/"+dirname)
        blog = open("blog/"+dirname+"/index.html", "w")
        blog.write(temp_template)
        blog.close()
    
    
    # build the category pages
    
    
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
    
    # open it in the finder
    os.system("open -a Brackets \""+"posts/"+filename+"/content.md\"")