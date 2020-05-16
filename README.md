## vgmoose.com
The current iteration of my website, see [this blog post](http://vgmoose.com/blog/reinventing-the-wheel-2989095422/) for more information at my approach this time around.

It's similar to other static blog sites, in that you edit Markdown files and compiling them before committing. Although, there's a compelling argument that this can be moved to GitHub Actions now!

The other cool thing about this blogging engine is the static client-side search, which [is detailed here](https://vgmoose.com/blog/implementing-a-static-blog-search-clientside-in-js-6629164446/).

### Making a new entry
```
python3 blog.py new "Title of new blog post"
```

### Building
```
python3 blog.py compile
```
