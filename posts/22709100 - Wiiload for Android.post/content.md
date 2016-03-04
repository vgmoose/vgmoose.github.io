---
layout: post
title: Wiiload for Android
date: 2013-03-06 00:00:00
comments: true
categories: apps, android, java, wii, release
id: 2007493297
---

Wiiload for Android is a graphical interface for the Wiiload client for Android. Wiiload is an application that sends bootable ELF or DOL files over the network to a Wii running the Homebrew Channel mod. This allows for one to boot native Wii code and applications without using a computer at all, only using a phone and the Wii.

Wiiload for Android is possible, as Android applications are programmed in Java, so JWiiload for Android is a port of [JWiiload](http://vgmoose.com/9909702342), a project of mine that was also written from the ground up. In fact, it was written with the intent of releasing Wiiload for Android, and eliminating the need of a computer from the homebrew scene on the Wii.

####Requirements

- Android Device (1.5+) with WiFi capabilities
- Be on the same network as your Wii

####Usage

The application can launch itself from intents (from .zip, .elf, or .dol from other file browser’s open with… dialogs) or through the own built in filebrowser which isn’t as simple as it appears. It displays images and contains filetype filtering, and support of a home directory and new file support. The application checks if the user’s wifi is on, and if it’s not, requests it to be enabled. The scan option should locate the Wii if it is on the same Wi-Fi network as the phone, usually returning the IP address of the Wii in seconds, assuming the Wii has been put on the Homebrew Channel. Arguments and port can be specified from the menu on the main screen. There is an ad at the bottom of the screen, but it can be disabled by entering “I love you” under the “Make New Folder” dialog in the file browser. Please report any errors!

####Screen shots

![Android](300px-Screenshot_2012-06-12-20-50-47.png) ![Android](300px-Screenshot_2012-06-12-20-51-32.png) ![Android](300px-Screenshot_2012-06-12-20-51-46.png)

For more information, see the [WiiBrew page](http://wiibrew.org/wiki/JWiiload#Wiiload_for_Android) on Wiiload for Android.