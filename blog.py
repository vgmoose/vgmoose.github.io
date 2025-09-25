import sys, os, time, random, re, shutil, json
import unicodedata
import urllib

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
            self.gfm = markdown.markdown(self.content, extensions=['gfm'], output_format='html5', safe_mode=False)
        except UnicodeDecodeError:
            self.gfm = markdown.markdown(unidecode.unidecode(self.content.decode("utf-8")), extensions=['gfm'], output_format='html5', safe_mode=False)
        
def stripTime(datestr):
    # read it as a datetime
    date_struct = time.strptime(datestr, '%Y-%m-%d %H:%M:%S')
    # return just the actual date
    return time.strftime('%Y-%m-%d', date_struct)

def generate_page(page_type, template_path, output_path, replacements, subdirectory_level=0):
    """Standardized page generation function"""
    with open(template_path, "r", encoding='utf-8') as f:
        template = f.read()
    
    # maually adjust some paths based on subdirectory level
    if (subdirectory_level > 0):
        prefix = "../" * subdirectory_level
        template = template.replace("href=\"", f"href=\"{prefix}")
        template = template.replace("src=\"", f"src=\"{prefix}")
        template = template.replace(f"href=\"{prefix}http", "href=\"http")
        template = template.replace(f"src=\"{prefix}http", "src=\"http")
    
    conditional_comments = [
        # ("<!-- entry_group", "entry_group -->"),
        # ("<!-- search_group", "search_group -->"),
        # ("<!-- single_entry", "single_entry -->")
    ]
    start, end = "<!-- " + page_type, page_type + " -->"
    template = template.replace(start, "")
    template = template.replace(end, "")
    
    for key, value in replacements.items():
        template = template.replace(key, value)
    
    # create output directories if not in root
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(template)

if action == "compile":
    
    posts = []
    
    with open("projects.json", "r") as f:
        projects_data = json.load(f)
    
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
    archived_groups = []  # For posts before 2016
    
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
    
    # keep track of post metadata for search results
    postmeta = {}

    # build all md files in posts
    for e in all_posts:
        if not e.endswith(".post"):
            continue
    
        # open the content markdown file        
        content = Content("posts/"+e+"/content.md", e)
        e = content.folder 
        
        if "hidden" not in content.prop or content.prop["hidden"] != "true":
            # store post metadata for search
            preview_img = "/layout/titleblog.png"
            has_image = False
            post_folder = "posts/" + content.folder
            if os.path.exists(post_folder):
                for f in os.listdir(post_folder):
                    if f.lower().endswith((".jpg", ".png", ".gif", ".jpeg")):
                        preview_img = "/" + post_folder + "/" + f
                        has_image = True
                        break
            
            postmeta[content.prop["id"]] = {
                "title": content.prop["title"],
                "date": stripTime(content.prop["date"]),
                "preview": preview_img,
                "hasImage": has_image,
                "description": content.minicontent,
                "archived": int(content.prop["date"][:4]) < 2016,
                "dirname": None  # Will be set later
            }
            
            # if post is from before 2016 archive it
            post_year = int(content.prop["date"][:4])
            if post_year < 2016:
                archived_groups.append(content)
            else:
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

        tdate = stripTime(content.prop["date"])

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
        
        previewUrl = "/layout/titleblog.png" # default icon if there's no applicable image in the folder
        for f in os.listdir("posts/"+e):
            f = f.lower()
            if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".gif") or f.endswith(".jpeg"):
                print(f)
                previewUrl = "posts/"+e+"/"+f
                break # just take the first one TODO: allow specifying one
            
        temp_template = temp_template.replace("$categories", content.prop["categories"])
        temp_template = temp_template.replace("$id", content.prop["id"])
        temp_template = temp_template.replace("$title", content.prop["title"])
        temp_template = temp_template.replace("$description", content.minicontent.replace("\n", " ").replace("\"", "\\\""))
        temp_template = temp_template.replace("$previewUrl", urllib.parse.quote(previewUrl))
        temp_template = temp_template.replace("$adcode", appropriate_ad)

        dirname = dash_phrase(content.prop["title"]) + "-" + content.prop["id"]
        
        content.dirname = dirname
        
        # store dirname for  later
        try:
            postmeta[content.prop["id"]]["dirname"] = dirname
        except:
            print("[WARNING] Post ID missing in postmeta: " + content.prop["id"])
        
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
    template = template.replace("$description", "Musings from the individual known as VGMoose")
    template = template.replace("$url", "https://vgmoose.dev")
    template = template.replace("$previewUrl", "/layout/titleblog.png")
    
    # build entry (homepage) group with thumbnails
    entry_html = []
    for x in range(0, len(groups)):
        post = groups[x]
        
        # Find preview image for this post - use absolute paths from root
        preview_img = None
        has_image = False
        post_folder = "posts/" + post.folder
        if os.path.exists(post_folder):
            for f in os.listdir(post_folder):
                if f.lower().endswith((".jpg", ".png", ".gif", ".jpeg")):
                    preview_img = "/" + post_folder + "/" + f
                    has_image = True
                    break
        
        # only show thumbnail if post has images
        thumbnail_html = ""
        if has_image:
            thumbnail_html = f'<img src="{preview_img}" alt="Preview" class="blog-thumbnail">'
        
        # create HTML with conditional thumbnail
        entry_item = f'''<div class="blog-entry{'' if has_image else ' no-image'}">
            {thumbnail_html}
            <div class="blog-content">
                <div class="blog-header">
                    <a href="{post.dirname}/">{post.prop["title"]}</a>
                    <span class="blog-date">{stripTime(post.prop["date"])}</span>
                </div>
                <div class="minidescription">{post.minicontent}</div>
            </div>
        </div>'''
        entry_html.append(entry_item)
    
    template = template.replace("$entry_group", ''.join(entry_html))

    # generate all projects HTML for use in listing page
    all_projects_html = []
    for project in projects_data["projects"]:
        thumbnail_html = ""
        if os.path.exists(f"projects/{project['id']}.png"):
            thumbnail_html = f'''<img src="/projects/{project['id']}.png" alt="{project['title']}" class="project-thumbnail">'''
        project_item = f'''<div class="project-entry{'' if thumbnail_html else ' no-image'}">
            {thumbnail_html}
            <div class="project-content">
                <div class="project-header">
                    <a href="{project['url'] if 'url' in project else project['source']}" target="_blank">{project['title']}</a>
                    <a href="{project['source']}" target="_blank" class="source-link">[source]</a>
                </div>
                <div class="project-description">{project['description']}</div>
            </div>
        </div>'''
        all_projects_html.append(project_item)

    # the left/right layout columns for the home page
    latest_posts_html = []
    posts_with_images = []
    
    # collect only posts that have images
    for post in groups:
        post_folder = "posts/" + post.folder
        if os.path.exists(post_folder):
            for f in os.listdir(post_folder):
                if f.lower().endswith((".jpg", ".png", ".gif", ".jpeg")):
                    posts_with_images.append(post)
                    break
    
    # take the first 4 posts with images
    # TODO: don't check fs again
    for x in range(0, min(4, len(posts_with_images))):
        post = posts_with_images[x]
        preview_img = None
        post_folder = "posts/" + post.folder
        if os.path.exists(post_folder):
            for f in os.listdir(post_folder):
                if f.lower().endswith((".jpg", ".png", ".gif", ".jpeg")):
                    preview_img = "/" + post_folder + "/" + f
                    break
        
        # TODO: a lot of hardcoded html in this script, which should be sub-template-ized
        entry_item = f'''<div class="blog-entry-small">
            <img src="{preview_img}" alt="Preview" class="blog-thumbnail-small">
            <div class="blog-content-small">
                <div class="blog-header-small">
                    <a href="blog/{post.dirname}">{post.prop["title"]}</a>
                    <span class="blog-date-small">{stripTime(post.prop["date"])}</span>
                </div>
                <div class="minidescription-small">{post.minicontent[:150]}...</div>
            </div>
        </div>'''
        latest_posts_html.append(entry_item)

    featured_projects = [p for p in projects_data["projects"] if p.get("featured", False)][:6]  # Show 6 projects
    featured_projects_html = []
    for project in featured_projects:
        project_item = f'''<div class="project-entry-small">
            <img src="/projects/{project['id']}.png" alt="{project['title']}" class="project-thumbnail-small">
            <div class="project-content-small">
                <div class="project-header-small">
                    <a href="{project['url'] if 'url' in project else project['source']}" target="_blank">{project['title']}</a>
                </div>
                <div class="project-description-small">{project['description']}</div>
            </div>
        </div>'''
        featured_projects_html.append(project_item)

    home_content_parts = [
        '<div class="home-intro">',
        '<h2>Hi, I\'m VGMoose!</h2>',
        '<p>I\'m an open-source developer and software engineer who enjoys creating niche tools, apps, and sites! This page contains info about my active and older projects, as well as any dev notes or random research. See my Socials page to follow me elsewhere!</p>',
        '</div>',
        '<div class="home-columns">',
        '<div class="home-left">',
        '<h3>Featured Projects</h3>'
    ]
    home_content_parts.extend(featured_projects_html)
    home_content_parts.extend([
        '<div class="view-all-link"><a href="projects/">View all projects →</a></div>',
        '</div>',
        '<div class="home-right">',
        '<h3>Latest Blog Posts</h3>'
    ])
    home_content_parts.extend(latest_posts_html)
    home_content_parts.extend([
        '<div class="view-all-link"><a href="blog/">View all blog posts →</a></div>',
        '</div>',
        '</div>'
    ])

    home_replacements = {
        "$title": "VGMoose - Home",
        "$description": "Software engineer and open-source developer", 
        "$url": "https://vgmoose.dev",
        "$previewUrl": "/layout/titleblog.png",
        "$entry_group": ''.join(home_content_parts)
    }
    generate_page("entry_group", "layout/template.html", "index.html", home_replacements, subdirectory_level=0)

    blog_replacements = {
        "$title": "VGMoose's Blog",
        "$description": "Musings from the individual known as VGMoose",
        "$url": "https://vgmoose.dev/blog",
        "$previewUrl": "/layout/titleblog.png", 
        "$entry_group": "<h2>Blog Posts</h2>" + ''.join(entry_html)
    }
    generate_page("entry_group", "layout/template.html", "blog/index.html", blog_replacements, subdirectory_level=1)

    projects_replacements = {
        "$title": "VGMoose - Projects",
        "$description": "Open source projects and tools by VGMoose",
        "$url": "https://vgmoose.dev/projects", 
        "$previewUrl": "/layout/titleblog.png",
        "$entry_group": f'<h2>Projects Index</h2>{"".join(all_projects_html)}'
    }
    generate_page("entry_group", "layout/template.html", "projects/index.html", projects_replacements, subdirectory_level=1)

    # nuild archived posts content
    archived_entry_html = []
    archived_groups = archived_groups[::-1]  # reverse chronological
    for post in archived_groups:
        preview_img = None
        post_folder = "posts/" + post.folder
        if os.path.exists(post_folder):
            for f in os.listdir(post_folder):
                if f.lower().endswith((".jpg", ".png", ".gif", ".jpeg")):
                    preview_img = "../../" + post_folder + "/" + f
                    break
        
        thumbnail_html = ""
        if preview_img:
            thumbnail_html = f'<img src="{preview_img}" alt="Preview" class="blog-thumbnail">'
        entry_item = f'''<div class="blog-entry{'' if preview_img else ' no-image'}">
            {thumbnail_html}
            <div class="blog-content">
                <div class="blog-header">
                    <a href="../../blog/{post.dirname}">{post.prop["title"]}</a>
                    <span class="blog-date">{stripTime(post.prop["date"])} <span class="archived-tag">[ARCHIVED]</span></span>
                </div>
                <div class="minidescription">{post.minicontent}</div>
            </div>
        </div>'''
        archived_entry_html.append(entry_item)

    archive_replacements = {
        "$title": "VGMoose - Archive",
        "$description": "Archive of older content and previous versions of this site",
        "$url": "https://vgmoose.dev/archive",
        "$previewUrl": "/layout/titleblog.png",
        "$entry_group": '''<h2>Archive</h2>
<p>Links to older content and previous versions of this site:</p>

<div class="archive-links">
    <h3>Blog Archive</h3>
    <p><a href="archive-posts/">View all archived blog posts (pre-2016)</a></p>
    
    <h3>Previous Sites</h3>
    <p><a href="https://backpack.vgmoose.com" target="_blank">VGMoose's Backpack</a></p>
    <p><a href="https://backpack.vgmoose.com/2008" target="_blank">Old 2008 Site</a></p>
</div>'''
    }
    generate_page("entry_group", "layout/template.html", "archive/index.html", archive_replacements, subdirectory_level=1)

    archived_posts_replacements = {
        "$title": "VGMoose - Archived Posts",
        "$description": "Archived blog posts from before 2016",
        "$url": "https://vgmoose.dev/archive/archive-posts",
        "$previewUrl": "/layout/titleblog.png",
        "$entry_group": "<h2>Archived Posts</h2>" + ''.join(archived_entry_html)
    }
    generate_page("entry_group", "layout/template.html", "archive/archive-posts/index.html", archived_posts_replacements, subdirectory_level=2)

    socials_replacements = {
        "$title": "VGMoose - Socials",
        "$description": "Find VGMoose on various social platforms",
        "$url": "https://vgmoose.dev/socials",
        "$previewUrl": "/layout/titleblog.png",
        "$entry_group": '''<h2>Socials</h2>
<p>Find me on these platforms:</p>

<div class="socials-grid">
    <a class="social-item" href="https://github.com/vgmoose" target="_blank">
        <div class="social-icon github-icon"></div>
        <div class="social-content">
            <h3>GitHub</h3>
            <p>Open source code and repositories</p>
        </div>
    </a>
    
    <a class="social-item" href="https://bsky.app/profile/vgmoose.dev" target="_blank">
        <div class="social-icon bluesky-icon"></div>
        <div class="social-content">
            <h3>Bluesky</h3>
            <p>Social media updates and thoughts</p>
        </div>
    </a>
    
    <a class="social-item" href="https://youtube.com/@vgmoose" target="_blank">
        <div class="social-icon youtube-icon"></div>
        <div class="social-content">
            <h3>YouTube</h3>
            <p>Video content and tutorials</p>
        </div>
    </a>
    
    <a class="social-item" href="https://ko-fi.com/vgmoose" target="_blank">
        <div class="social-icon kofi-icon"></div>
        <div class="social-content">
            <h3>Ko-fi</h3>
            <p>Support my work and projects</p>
        </div>
    </a>

    <a class="social-item" href="https://github.com/sponsors/vgmoose" target="_blank">
        <div class="social-icon githubsponsors-icon"></div>
        <div class="social-content">
            <h3>Github Sponsors</h3>
            <p>An alternate way to support me</p>
        </div>
    </a>
</div>'''
    }
    generate_page("entry_group", "layout/template.html", "socials/index.html", socials_replacements, subdirectory_level=1)

    # load the template
    tfile = open("layout/template.html", "r")
    template = tfile.read()
    tfile.close()
    
    template = template.replace("<!-- search_group", "")
    template = template.replace("search_group -->", "")
    template = template.replace("$title", "VGMoose.com Search")
    template = template.replace("$search_vocab", json.dumps(vocab, cls=SetEncoder, sort_keys=True, indent=4, separators=(',', ': ')))
    template = template.replace("$search_lookup", json.dumps(humanmap, cls=SetEncoder, sort_keys=True, indent=4, separators=(',', ': ')))
    template = template.replace("$search_postmeta", json.dumps(postmeta, cls=SetEncoder, sort_keys=True, indent=4, separators=(',', ': ')))
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
