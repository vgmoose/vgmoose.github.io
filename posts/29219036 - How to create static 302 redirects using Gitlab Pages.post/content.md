---
layout: post
title: How to create static 302 redirects using Gitlab Pages
date: 2025-07-21 19:56:04
comments: true
categories: website, development, redirects, gitlab
id: 9998756653
---

Website redirects can be annoying! The best thing to do is often a 302 (or 301) HTTP redirect, without having to use meta refresh tags or requiring the user to run JavaScript on the page.

Gitlab provides an extremely convenient offering with Gitlab Pages and also allows you to set up a single yml config file with some limited dynamic capabilities. See their [docs page on redirects](https://docs.gitlab.com/user/project/pages/redirects/).

In short, create a `.gitlab-ci.yml` in the root of your repo, and all that needs to be filled is:

```
variables:
  REDIRECT_DOMAIN: "example.com"

pages:
  stage: deploy
  script:
    - mkdir public
    - echo "/* https://$REDIRECT_DOMAIN/:splat 302" > public/_redirects
  
  artifacts:
    paths:
      - public
  
  only:
    - main
    - master
```

This will cover both main/master branches (depending on which your git client defaults too), and 302 redirect any requsts to the REDIRECT_DOMAIN. All that has to be changed is the 2nd line of the file.

The `:splat` component preserves the full path during the redirect! This is a great option for static sites and serverless environments, and it's one less thing that you have to worry about as a website maintainer.
