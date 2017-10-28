---
layout: post
title: Using libnx to Compile Nintendo Switch binaries
date: 2017-09-20 18:23:02
comments: true
categories: nintendo, switch, homebrew, libnx, linux
id: 3632420593
original: https://gist.github.com/vgmoose/8844a812c4bf50889e3f2b65359a6930/
hidden: true
---

*Notice*: The below instructions were written on 9/22/17 and refer to an alpha build of devkitA64, libnx, and Mephisto. Take it with a grain of salt if the date has moved too far into the future since then.
*Double Notice*: The creator of devkitpro advises against these instructions in favor of using an automated installer, which as of 10/28/17 has not been released yet. Follow only as your own curiosity permits.

## Requirements
- [Devkit ARM64](https://sourceforge.net/projects/devkitpro/files/devkitA64/) for your OS
- unix-like environment
- git, make, 7zip
- lz4, lz4-devel ([Ubuntu](https://launchpad.net/ubuntu/+source/lz4), [Fedora](http://rpm.pbone.net/index.php3/stat/4/idpl/38018758/dir/fedora_25/com/lz4-devel-1.8.0-1.fc25.x86_64.rpm.html), [Github](https://github.com/lz4/lz4))

## Setup
0. Make a ```devkitpro``` folder (any directory is fine, but this guide will use ```~```)
```
mkdir ~/devkitpro
```
1. Extract the contents of [Devkit ARM64](https://sourceforge.net/projects/devkitpro/files/devkitA64/) to ```~/devkitpro/devkitA64```  
2. Clone the [libnx](https://github.com/switchbrew/libnx) library from github
```
cd ~
git clone https://github.com/switchbrew/libnx.git
```
3. Update the ```DEVKITPRO```, ```DEVKITA64```, and ```PATH``` environment variables
```
export DEVKITPRO=~/devkitpro
export DEVKITA64=$DEVKITPRO/devkitA64
export PATH=$PATH:$DEVKITA64/bin
export PATH=$PATH:~/libnx/tools
```
4. Compile libnx
```
cd ~/libnx
make install
make
```

## Compiling example binary
The [libnx switch example](https://github.com/switchbrew/switch-examples/blob/master/templates/simple/source/main.c#L8) example provided by libnx is called **simple**-- it waits for 5 seconds, and then exits. [svcSleepThread](http://switchbrew.org/index.php?title=SVC#svcSleepThread) is a native switch function, exposed by libnx.

[Here](https://github.com/switchbrew/libnx/tree/4fd0989bf348ffa04d342f12c4e285099df5d266/nx/include/switch) are all of the functions provided by the libnx library. In the future, some drawing functions may be RE'd and allow for simple homebrew games to be made.

An additional important thing to note, is that as of this time of writing there is no method to execute these binaries on the Switch. They can be executed using the [CageTheUnicorn](https://github.com/reswitched/CageTheUnicorn) emulator on an intel computer, however.

### Compiling
1. Clone the [switch-examples](https://github.com/switchbrew/switch-examples) project
```
cd ~
git clone https://github.com/switchbrew/switch-examples
```
2. Compile the simple example by running make (if you hit a devkit error here, redo the exports from **Setup** step #3)
```
cd ~/switch-examples/templates/simple
mkdir -p exefs_src/a
make
```
3. You should now have two files in the current folder, ```simple.nso``` and ```simple.pfs0```
```
hexdump -C simple.nso | head -20
```

```
00000000  4e 53 4f 30 00 00 00 00  00 00 00 00 3f 00 00 00  |NSO0........?...|
00000010  00 01 00 00 00 00 00 00  60 04 00 00 01 00 00 00  |........`.......|
00000020  1f 04 00 00 00 10 00 00  20 00 00 00 01 00 00 00  |........ .......|
00000030  2a 04 00 00 00 20 00 00  48 00 00 00 10 01 02 00  |*.... ..H.......|
00000040  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000060  1f 03 00 00 0b 00 00 00  21 00 00 00 00 00 00 00  |........!.......|
00000070  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
000000a0  cf db df 92 32 05 89 69  56 6a 04 14 04 80 f1 1c  |....2..iVj......|
000000b0  b7 18 75 4b 54 bd d8 60  6c 95 60 0f 97 09 9b bf  |..uKT..`l.`.....|
000000c0  66 68 7a ad f8 62 bd 77  6c 8f c1 8b 8e 9f 8e 20  |fhz..b.wl...... |
000000d0  08 97 14 85 6e e2 33 b3  90 2a 59 1d 0d 5f 29 25  |....n.3..*Y.._)%|
000000e0  0e b8 68 7c a3 25 a2 59  02 97 76 68 6b da c3 ac  |..h|.%.Y..vhk...|
000000f0  29 bd 61 28 44 21 83 66  34 28 9e d5 0a 82 07 e9  |).a(D!.f4(......|
00000100  fa 2f 03 00 00 94 48 4f  4d 45 42 52 45 57 dc 13  |./....HOMEBREW..|
00000110  00 d1 40 04 00 58 61 04  00 58 21 00 00 cb 21 1c  |..@..Xa..X!...!.|
00000120  00 91 21 f0 7d 92 02 00  80 d2 00 00 1c 8b 02 84  |..!.}...........|
00000130  00 f8 21 20 00 f1 c1 ff  ff 54 80 03 00 58 a1 03  |..! .....T...X..|
00000140  28 00 01 24 00 47 00 40  f9 42 2c 00 f3 0e 81 ff  |(..$.G.@.B,.....|
```
The ```exefs_src``` contains any files that should be copied to the executable filesystem. In the simple example, we don't need any files copied, so the ```mkdir -p exefs_src/a``` is just so that the [Makefile doesn't complain](https://github.com/switchbrew/switch-examples/blob/master/templates/simple/Makefile#L18).
