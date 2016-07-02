---
layout: post
title: Leaving Ubuntu for Fedora
date: 2016-07-02 10:15:34
comments: true
categories: linux, fedora, ubuntu
id: 5574192608
---

Despite having literally [worked at Red Hat](http://vgmoose.com/blog/day-03-cubicle-sweet-cubicle-4154581713/), I've actually always been a Debian/Ubuntu guy. There are three common reasons that I would give for this preference: stability, ease-of-use, and support. I don't usually blog about personal computing either, but I feel like I need to vent some frustration here!

![Fedora 24 desktop](desktop.png)
Above: The default Fedora 24 gnome-3 desktop ([larger](https://i.imgur.com/GnmY4sT.png))

When I started my next job, I made the decision to install Ubuntu on the work laptop rather than Fedora. I believed that, since it was a laptop, Ubuntu has better drivers, and on top of that apt-get "felt" less intrusive to use. I was also under the impression that it would be easier to find support online due to the popularity of Ubuntu.

## The situation
I ran Ubuntu on this laptop for a full year, with minimal issues, besides the occasional rare graphical bug. At a certain point, however, I wanted to install a tool called [openconnect](http://www.infradead.org/openconnect/). Of course, ```apt-get install openconnect``` works with no issues. Problems arose though, in that I wanted to use it with ```--juniper```, a flag that is only in a later version-- a version not on Canonical's repositories. This is because the latest openconnect depended on something else that was also too new. Anyway, I decided that I should upgrade anyway.

In the past, I've performed Debian upgrades by simply adding the new version repositories and performing ```apt-get dist-upgrade```. I'm told that that isn't how Ubuntu does things however. Instead, you are supposed to use the ```do-release-upgrade``` command. Okay, no worries. So, I execute that command and leave the system alone to upgrade. 

Here's mistake number 2, which is, as far as I'm aware, the only second mistake that I made during this whole process. Although, it is a pretty big one. I went to lunch, and absent mindedly shut the laptop. I immediately opened it once I had realized what had done, but it was completely frozen (and sleep had worked prior to this.) Okay, this was unfortunate, but I chalked it up to perhaps some driver was in mid-upgrade. It's not unreasonable that the machine would have issues if it suspended while upgrading. 

## The problem
Not surprisingly, the computer failed to boot. It was in a strange halfa-state, where the glibc library wasn't installed. And most things depend on glibc! Fortunately, although bash wouldn't work, the recovery mode in Ubuntu jumps to busybox, which isn't linked against glibc. From here I was able to fetch and manually install some .deb files that provided glibc. Then I couldn't boot, but I could get to bash, and apt was working.

Now I know, perhaps I should cut my losses at this point. Machine lost power mid-upgrade, it's over. Reinstall. But apt is working! If I could repair the packages, surely, I should be fine. I obtained a slew of errors whenever I tried to get apt-get to do anything that I wanted. Most of them seemed to be related to dependency problems. For instance, it would say that it couldn't install something because of something else being a newer version, and that it wouldn't downgrade. 

Let me save you some time if you ever run into apt-get troubles. Everything you ever google and look up online will always recommend the following advice:

```
apt-get clean
apt-get update
apt-get install -f
```

Sounds so simple. Well I've never had that work... ever. Never has that resolved apt-get dependency issues I've had in the past, not just now. It doesn't prevent people from continuing to recommend it, however. I wish I could tell you the specific error messages that I came across, but I don't have access to them right now.

Probably a mix between something like "you have held broken packages" and "dependency conflict could not be resolved". When you dig deeper into apt-get support, people will eventually recommend using aptitude, dpkg (```dpkg --configure -a```), or running synaptics and using "Fix broken packages". Well, none of these worked this time. I was just in a jam. As a last resort (and perhaps out of frustration with apt-get), I removed the dpkg package directory (/etc/dpkg/). This makes apt believe that zero packages are installed. I was free!

Feeling smug, I happily issued ```apt-get install unity```, and it pulled down and re-installed/configured many many packages. For a time, I thought I was getting away from this mishap without needing to do a reinstall. Unforuntately, apt-get eventually errored out, citing more dependency issues. I thought this strange, as I just now started from a "blank slate" from an installed-packages point of view. The error now was something about Python3 dependencies or something. Out of desperation I issued a reboot.

To my shock, unity actually installed successfully, and I was greeted with a login screen. logging in as my own user wouldn't work, but I was able to use ```startx``` from the [VT tty](https://en.wikipedia.org/wiki/Virtual_console). After logging in, the unity sidebar was still missing, but I could ctrl-alt-T to a Terminal and run apps. Everything was that wasn't unity was working fine, and due to laziness I probably carried on working this way much longer than I should've. Trying to install any package resulted in apt-get errors, so my package manager was basically completely borked at this point.

## The solution
This isn't the first time I've had a slew of issues with apt-get, but it is the first time that I wasn't able to fix them. And yes, again, I am aware that it died during upgrade, a situation that is infamous for being unrecoverable. But I don't like the issues that I encountered regardless, and I especially don't like the "attitude" of how apt-get responds to failure. "You have held broken packages. Sucks to be you."

Fedora recently switched to a new package manager called [dnf](https://en.wikipedia.org/wiki/DNF_(software)), which uses [libsolv](https://github.com/openSUSE/libsolv), which to quote the readme, states: "The sat-solver code has been written to aim for the newest packages, record the decision tree to provide introspection, **and also allows to provide the user with suggestions on how to deal with unsolvable problems.**" That half of that sentence is huge. No longer should the advice to blindly "try clean, update, install -f".

I don't know if dnf addresses, or could handle the situation that I described above. I haven't even looked into how it's dependency satisfaction differs from apt-get. Although that's not for lack of trying-- trying to search up anything dependency-related and "apt" results in only people asking for how to solve their issues, and more likely, people asking them if they've tried clean; update; install -f. It's a bit like asking someone if they've tried rebooting. Just blindly hope that your package manager can resolve whatever [ridiculous problems have developed](https://en.wikipedia.org/wiki/Dependency_hell), and if not, reinstall. 

Like I said, I have no reason to believe that dnf is the end all be all, nor do I have any evidence. All I know is, that it's different. And different is all I need right now. Goodbye Ubuntu and apt.
