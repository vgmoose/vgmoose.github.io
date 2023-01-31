---
layout: post
title: Pokémon Red and Blue ROM Patches with Slowed Down Music
date: 2022-12-30 19:59:19
comments: true
categories: pokemon, hack, rom, patch, music
id: 6347114672
original: https://gist.github.com/vgmoose/9be2d9062e3992b4eaf399ae026ebd21
---

These are patches for Red/Blue that are built with their music tempo slowed down 2x and 4x. This is done by changing [this line](https://github.com/pret/pokered/blob/bbb0e7e82deb6741f75a12b48f81076d92f5d9dc/macros/scripts/audio.asm#L172) in the decompilation (to `HIGH(\1 * 2), LOW(\1 * 2)` or `HIGH(\1 * 4), LOW(\1) * 4`).

This creates a slightly better experience if you use 2x or 4x speed up / fast forwarding in an emulator, so that the sound isn't just a cacophony of sped up noises. It's not perfect though!

### Downloads
- 2x Slowed: [Red](https://gist.github.com/vgmoose/9be2d9062e3992b4eaf399ae026ebd21/raw/69cf8a76a13335e00070ef1152238c171b38820f/red_2x_slowed.ips), [Blue](https://gist.github.com/vgmoose/9be2d9062e3992b4eaf399ae026ebd21/raw/69cf8a76a13335e00070ef1152238c171b38820f/blue_2x_slowed.ips)
- 4x Slowed: [Red](https://gist.github.com/vgmoose/9be2d9062e3992b4eaf399ae026ebd21/raw/69cf8a76a13335e00070ef1152238c171b38820f/red_4x_slowed.ips), [Blue](https://gist.github.com/vgmoose/9be2d9062e3992b4eaf399ae026ebd21/raw/69cf8a76a13335e00070ef1152238c171b38820f/blue_4x_slowed.ips)

### How to Patch
Use https://www.marcrobledo.com/RomPatcher.js/ on the web to patch a rom.

### Video
- Running at 4x speed: https://twitter.com/VGMoose/status/1600975855542448129
- Running at "normal" speed: https://twitter.com/VGMoose/status/1600976002343399424