---
layout: post
title: Using iPhone Data Connection wth a Computer Hotspot (Reverse Tethering)
date: 2016-11-26 11:20:16
comments: true
categories: iphone, ssh, tethering, hotspot, ios
id: 4414683578
---

So recently I've stumbled upon a pretty neat "one weird trick" that can be done to access the iPhone's data connection from any wifi-enabled device. This is still important if your carrier doesn't allow tethering (of which, a surprising amount the US seem to not, [despite some court rulings](https://en.wikipedia.org/wiki/Tethering#United_States). The same trick can probably work on Android phones as well but I haven't tried anything.

So the general idea is this:
1. Host a wifi-hostpot on your computer
2. Turn on wifi on your iPhone and connect to the hotspot
3. Tell the iPhone to use its data connection despite being connected to Wifi

I'm not sure if (3) is a networking trick, or a lesser known feature of iOS, but it's accomplished as follows:
1. Go to Settings -> General -> Wifi
2. Connect to the Hotspot that you hosted on your computer
3. Tap the blue arrow next to the name of the Wifi network to view more settings
4. Note the IP that you have been assigned from the Hotspot, then choose the "static" tab
5. Input the IP from earlier as the IP, and enter 255.255.0.0 as the subnet mask
6. **Leave everything else blank** (Router, DNS, Search Domains). This tells it to route traffic over the cellular network.

As for (1), most PC operating systems have some variation of this built-in. Gnome3 network-manager has an option that straight up says "Host wifi hotspot".

At this point, your computer is able to access your iPhone directly, and your iPhone is able to access its network directly, despite being connected over wifi. So for example, you can do the following:

```
ssh mobile@10.42.0.40
```
And then:
```
wget google.com
```
And get whatever files you need. In this case, I am taking advantage of the fact that my iPhone is jailbroken and is running an sshd server. In theory though, the same can be done with any App Store apps that allow you to download and host files, such as [this one](https://itunes.apple.com/us/app/downloader/id835382053?mt=8). Using xcode tools, someone could make something to host an sshd server on a nonjailbroken iPhone or even host an http proxy, which could be done completely without root.

Even though I am jailbroken, I've always found that the jailbroken tether apps are either very poor or cost a lot of money. And since I usually just need ssh access anyway, being able to ssh into the iPhone and have an internet connection from that is good enough for me on the go. (So usually I ssh into the phone, and then ssh into another computer, like work or home).


