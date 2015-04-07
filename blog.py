import sys, os, time

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
    
class Content:
    def __init__(self, filename, foldername):
        lines = open(filename, "r").readlines()
        self.prop = {}
                 
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
        newfilename = str((int(time.mktime(time.strptime(self.prop['date'], '%Y-%m-%d %H:%M:%S')))-1428316490)/60)+" - "+self.prop['title']+".post"
        
        if newfilename != foldername:
            print "\trenaming to \""+newfilename+"\""
            os.rename("posts/"+foldername, "posts/"+newfilename)
            
    def buildHTML(self):
        # parse gfm to html
        self.gfm = markdown.markdown(self.content, ['gfm'])
        
if action == "compile":
    
    posts = []

    # build all md files in posts
    for e in os.listdir("posts"):
        if not e.endswith(".post"):
            continue
    
        # open the content markdown file        
        content = Content("posts/"+e+"/content.md", e)
        
        # write the contents to an index file
        index = open("posts/"+e+"/index.html", "w")
        index.write(content.gfm)
        
    # build the blog pages
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
    filename = str(int(init_time-1428316490)/60)+" - "+postname+".post"
        
    # make the directory of this post
    os.mkdir("posts/"+filename)
    
    # create the content file
    f = open("posts/"+filename+"/content.md", "w")
    
    f.write("---\n")
    f.write("layout: post\n")
    f.write("title: " + postname + "\n")
    f.write("date: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(init_time)) + "\n")
    f.write("comments: true\n")
    f.write("categories: \n")
    f.write("id: "+str(init_time)+"\n")
    f.write("---\n\n")
            