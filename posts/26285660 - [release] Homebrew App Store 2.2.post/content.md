---
layout: post
title: [release] Homebrew App Store 2.2
date: 2019-12-23 17:20:55
comments: true
categories: homebrew, app store, release
id: 8378492338
---

### What's New?
This update should address a lot of the slowness and crashing that people have experienced. We have other infrastructure-related changes that we're still working on, but are publishing this now to make sure these client bugfixes are out there!

In July 2019, we passed our *third year* of hosting the Homebrew App Store service since starting on the Wii U! Thank you to everyone who has used the App Store or otherwise shown support for this project. You're the reason we keep doing this.

The App Store team is: [pwsincd](https://github.com/pwsincd), [rw-r-r_0644](https://github.com/rw-r-r-0644), [CompuCat](https://compucat.me), [crc32](https://crc32.dev), [vgmoose](https://vgmoose.com), [quarky](https://heyquark.com), [Whovian9369](https://cybre.space/@Whovian9369)
Our homepage: https://fortheusers.org
Chat with us on Discord: https://discord.fortheusers.org

### Download
For downloads, see the release on [Gitlab](https://gitlab.com/4TU/hb-appstore/-/releases)

### Changelog
**Wii U + Switch App Client**
Download: https://gitlab.com/4TU/hb-appstore/releases

- No more loading screen! Images and metadata are now downloaded on-the-fly, and you are dropped immediately into the app listing (by rw-r-r_0644!)
- Abstracted UI components into the standalone library [Chesto](https://gitlab.com/4TU/chesto)
    - Chesto is a declarative, element-based library for creating lightweight user interfaces in SDL2. Along with the App Store console client, it also powers [vgedit](https://github.com/vgmoose/vgedit).
    - Chesto uses [resinfs](https://gitlab.com/4TU/resinfs) rather than switch/wiiu romfs for storing and loading compressed assets from memory (by rw-r-r_0644)
    - Want to give it a try? Have a peek at CompuCat's example, [ChestoTesto](https://gitlab.com/4TU/chestotesto)!
- Shows progress while extracting files from the zip package
- Detailed Credits page to fairly highlight importance of people's contributions in the scene
- Recovery mode added, accessed by pressing repeatedly L/R immediately after launching
    - Can be used to clear all cached/config data, and install/remove packages without a GUI
- Bugfixes and Oversights
    - Fixes issues when package structure totally changes (libget#8)
    - Sorting button no longer occasionally crashes
    - Files download to disk to avoid being stored in memory (Thanks TotalJustice!)
    - Onscreen quit button added (Thanks jacquesCedric!)
- Platform Specific
    - Switch: Uses https for default Switch repo (sorry for dragging feet on this!)
    - Switch: Themes are now excluded from the "All Apps" category
    - Switch: If launched in applet mode, uses Wii U style banners
    - Wii U: Fix crackling/popping during music playback (by Quarktheawesome)
    - Wii U: Fix bug that duplicates appstore entries in HBL upon upgrading... (see Notice*)
        - TL;DR: after updating  on Wii U there will be *two* appstore apps in HBL. Launching either one will work, and it will clean up the extra one
- Move primary development from GitHub to GitLab
    - We’ll continue to upload releases to GitHub for the moment, but that repo will eventually be deprecated and direct users to GitLab. ↩︎

### Sources
- https://gitlab.com/4TU/hb-appstore
- https://gitlab.com/4TU/libget
- https://gitlab.com/4TU/chesto
- https://gitlab.com/4TU/resinfs

*Wii U Notice: The duplicate appstore entries in HBL was an oversight, but should resolve itself after launching *either* HBL app after the update. It has to do with old users migrating from .elf to .rpx, and me trying to consolidate it for each platform. After updating, the issue should not occur again in the future due to libget#8 being fixed.
