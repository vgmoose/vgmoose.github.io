---
layout: post
title: Fixing a Suddenly Read-only Flash Drive
date: 2017-08-07 17:28:34
comments: true
categories: usb, linux, silicon power, misc
id: 1847368734
---

A while back I purchased this [Silicon Power 64G USB3 flash drive](https://www.amazon.com/dp/B01LZETCQ3/) to put on my keychain. It was a great, durable flash drive for about 6 months... Then, it suddenly showed up as read-only on any device that I connected to it!

It was not a permission error, or something wrong with the partition map. The physical device was flat-out refusing to be read. Even gparted -> Create Partition Map would report back "/dev/sdb is read-only".

After some googling, a common belief is that this may be a sign that the drive is on its way out, and that it enters a read-only safemode to allow data to be copied off it without encouraging the user to keep using it. That might actually still be true.

The fact remains though, that something in the USB firmware/controller is preventing writes from occurring at a low level. I eventually came across [this program](https://www.silicon-power.com/web/download-USBrecovery) from Silicon Power. It was a rather sketchy program, and it downloaded another program before it ran. But when it did run, it restored the write-ability to my flash drive! So who am I to complain?

I'm making this post as I didn't see a solution like this recommended anywhere where people were complaining about their flash drives suddenly becoming read-only. So to sum up, if this has happened to your flash drive, the manufacturer may provide some (questionable) recovery software to fix the issue! Good luck.



