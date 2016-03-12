---
layout: post
title: Implementing a Static Blog Search Clientside in JS
date: 2016-03-11 22:14:08
comments: true
categories: tutorial, javascript, python
id: 6629164446
---

One of the primary features of the blog on this website is the fact that it is compiled offline with a python script and then served as a static site by a "dumb" server. The advantage of this is less overhead for me when hosting, as well as the ability to leverage Github Pages to act as a [CDN](https://en.wikipedia.org/wiki/Content_delivery_network). More info about the decisions behind the script are detailed in [this post](http://vgmoose.com/blog/reinventing-the-wheel-2989095422).

However, there was something that the site had been lacking, and that was a way to go through and actually search through the posts that I had been made. I had a couple of ideas on how to go about this without having to add overhead with a backend.

### Idea #1 Searching Categories Only
My initial intent of the "categories" to the left of every blog post was to generate separate json blobs for every unique category to keep track of which posts were in which categories. Posts can already be referred to by their unique post IDs (seen in the URL). So for instance:
```
{
    "tutorial" : [1, 4, 7],
    "javascript" : [1, 2, 5, 6],
    ...
}
```
In my case post IDs are 10 digits, though. So the idea here is that a search can go through specified known tags and return the matches in the form of links to blog posts. This approach is okay, but only covers the tags, which is a small subset of the content in the posts obviously!

### Idea #2 Searching Everything
Scrapping the category-based search ont the grounds of being too limited, I wanted to provide the full powers of an actual search engine. Well there's one pretty straightforward way to accomplish that: provide every blog post in its entirety to the client all at once for manually searching in javascript. The JSON in this case would look like this:
```
{
   "6629164446" : "One of the primary features of the blog on this website is the fact that it is compiled offline with a python script and then served ... ",
   ...
}
```
The issue with this is twofold: firstly, I'm providing the entirty of the site just for the search page. The more blog posts, the more text this is going to be. The second issue is similar: every search query is going to to have to thumb through all the words in all the entries. This is probably actually never a real issue due to the size of my blog, but still it isn't very efficient

### Idea #3 Inverted Index
An [inverted index](https://en.wikipedia.org/wiki/Inverted_index) is a search engine teachnique to speed up the esponse time of a query. The term inverted index refers to the fac that it's the opposite of a [forward index](https://en.wikipedia.org/wiki/Search_engine_indexing#The_forward_index). A forward index is a mapping of the indentifier (post ID) to the set of unique words that are within it. An inverted index flips the key and the entry types, and uses the unique words as the key and the entries as the set of identifiers that the word is in. Below is an example:
```
{
    "permanent": [
        "4632920139"
    ],
    "persistent": [
        "5495631835"
    ],
    "person": [
        "4314069407",
        "9640693481",
        "1665286367",
        "0310593175",
        "3972771157"
    ],
    "personal": [
        "2989095422",
        "4632920139",
        "6547939220"
    ]
    ...
}
```
So now, it's easy to break the search query into unique words and then look those words up in that data structure. This results in a set of blog post IDs that match for each word in the query. It also means that the keyset of this dictionary is the set of unique words in all my blog posts, or in other words my blog's "vocabulary".

I went with the third approach, which you can see in action on the [Search page](http://vgmoose.com/search/). There's still a bit of overhead in sending the large json blob of search data, but I believe the benefits of being a static site overcome the download speed. It should never greatly exceed the file size of small images, let alone large ones.

Future upgrades to this mechanism include tagging frequencies of the words per page in order to "rank" them based on which matches the query more closely. Also, by tagging the frequencies, it should be possible to make one of those cool [word cloud](http://www.wordle.net) thingies.

If nothing else it's just interesting to see pure clientside javascript handle something like searching, which you'd expect to traditionally be done live on the server. This also means I don't ever have to worry about any kind of search shennanigans such as query injections or ddosing! Piece of mind!