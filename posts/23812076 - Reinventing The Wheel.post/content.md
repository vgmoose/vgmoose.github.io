---
layout: post
title: Reinventing The Wheel
date: 2015-04-10 23:56:01
comments: true
categories: javascript, python
id: 2989095422
---

Today marks the launch of YET ANOTHER VGMoose site redesign. The old site will remain available at [backpack.vgmoose.com](http://backpack.vgmoose.com). The current iteration of the site is built offline using python with [this script](https://github.com/vgmoose/vgmoose.com/blob/gh-pages/blog.py). Each post is stored in a .post directory as seen [here](https://github.com/vgmoose/vgmoose.com/tree/gh-pages/posts). This is very similar to the way my [personal site](http://rickyayoub.com) is built.

I've amassed a surprisingly large number of blogs throughout the last decade that I've spent on the interwebs! I've made blogs using [BlogDrive](http://moosebeta.blogdrive.com/), [Wordpress](https://vgmoose.wordpress.com/), [BlogSpot](http://vgmoose.blogspot.com/),[Tumblr](http://rickyayoub.tumblr.com), [iWeb](http://vgmoose.com/Blog/Blog.html), and [Octopress](http://vgmoose.github.io/deku-scrub/blag/). I haven't stuck with any of them, however...

One problem that I seem to inevitably have with most of the sites listed above is that they don't allow for an extremely detailed degree of control. That might sound CRAZY! After all, there are an abundance of Wordpress and Tumblr themes out there, and Octopress was even designed with programmers in mind specifically to address this problem! Why would I roll my own tools to generate a blog when software already exists that does it?

![xkcd](standards.png)

A big part of programming is being stumped. That is, encountering a problem, and being forced to debug it until you find a solution that makes the program behave the way you want it to. That goes doubly for visual things like web design. If you want a website to look the way it does in your head, you need to spend the time using the tools you have to try to make it look like that. And of course, there's generally a high after solving such problems.

However, if I'm relying on some cookie-cutter copy-and-paste blogging engine, the high doesn't seem to feel nearly as good. Maybe I happen to be particularly picky about the alignment of some of the words, or I'd prefer a different permalink structure, or I want ajax loading if javascript is enabled. To implement such things I would have to spent a good chunk of time learning very specific things about the blogging engine to make it do what I want. And the payoff would be minimal.

Perhaps I am being too preachy. After all, my design (compiling markdown files statically with python) isn't too dissimilar to the main idea behind Octopress. A key difference though is I understand every single part of my own implementation. If you see some glitches on here, that's my bad. On the other hand though, if the site looks nice you know who is responsible!