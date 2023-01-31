---
layout: post
title: Creating a Windows 11 Install USB in 2022
date: 2022-09-28 19:48:51
comments: true
categories: usb, os, install, windows, tutorial, boot
id: 5071914005
original: https://gist.github.com/vgmoose/4e74aca92787e79661defc16960a10f3
---

I have been installing Windows for a long time. Does it get easier? I want to say it gets easier, but it seems like there's always some new wrinkle! These instructions are as much a note to my future self as they may be useful to anyone else.

For me, I was not able to get any exfat-based installs, or even any of the GUI helpers to make this process any more straightforward. Maybe on your target Windows / host OS those helpers will work, but the below process (as of current year) is consistent, and not overly complicated.

Overview:
  1. Downloading an official ISO image from MS:
     - https://www.microsoft.com/software-download/windows11
  2. Formatting the drive (at least 8GB) as GPT, and one **FAT-format** partition (aka **MS-DOS**)
     - Can use [Disks](https://www.ubuntubuzz.com/2020/02/how-to-format-disk-drive-as-gpt-on-ubuntu.html) or [Disk Utilty](https://support.apple.com/guide/disk-utility/format-a-disk-for-windows-computers-dskutl1010/mac) for this 
  3. Mounting the ISO either in a file browser (eg. Files or Finder)
  4. Copying over all the files _except_ `sources/install.wim`
  5. Using [wimsplit](https://wimlib.net/man1/wimsplit.html) from wimtools to split the `install.wim` file onto the destination drive
     - FAT-format filesystems have a limitation of 4GB per file, wimsplit creates two files in a format the Windows installer understands

## Commands
### Prereqs
Format the the target drive, as mentioned above. It should be at least 8GB, FAT/MS-DOS-formatted, and GPT partitioning scheme.

Install wimsplit on Ubuntu:
```
sudo apt install wimtools
```

On macOS (needs [brew](https://brew.sh/) first
```
brew install wimlib
```

### Usage
- Let's say `Downloads/Win11_22H2_English_x64.iso` is the Windows ISO.
  - Double click or right-click Open this file with "Disk Image Mounter" to mount it
- The USB drive is (FAT/MS-DOS formatted) mounted at `/Volumes/TheUSB`
  - (on Ubuntu, it's likely in `/media/<name>/<usb>`)
- The mounted Windows ISO is at `/Volumes/CCCOMA_X64FRE_EN-US_DV9` (say that 10 times fast)
  - (Ubuntu: `/media/<name>/CCCOMA_X64FRE_EN-US_DV9`)

The following command copies over all files except `install.wim`:
```
rsync -avP --exclude sources/install.wim /Volumes/CCCOMA_X64FRE_EN-US_DV9/* /Volumes/TheUSB
```

Then, this command splits and copies `install.wim` at 3000MB (Just under the FAT limit):
```
wimsplit /Volumes/CCCOMA_X64FRE_EN-US_DV9/sources/install.wim /Volumes/TheUSB/sources/install.swm 3000
```

Make sure to replace `/Volumes` with the path to where the files/drives are mounted in the above commands.

### Result
If successful, you should see `/Volumes/TheUSB` (your target USB) looks very similar to `/Volumes/CCCOMA_X64FRE_EN-US_DV9` (the mounted ISO), except that in the `sources` folder, the USB has `install.swm` and `install2.swm`. Again, these will be presented to the Windows installation environment as one file.

After this, put the USB in your target device, and boot off it from the boot menu.

Since we're using UEFI boot, it should _just appear_ in the boot menu of the computer.

If your computer hardwaare does not support UEFI boot, you can try reformatting the drive using MBR instead of GPT (But still using FAT). I can't vouch for this, but according to sources online it should Also Work.

## Bonus (Unsupported OS Workaround)
If you get the error "Unsupported OS" in Windows, this has to do with a deliberate attempt to make Windows 11 harder to install on platforms that Microsoft has not deemed worthy. Or something like that. And, to make this very clear, if you see this error, your platform is NOT worthy. (Again, according to the publicly traded company MSFT).

This worthiness is not an issue at this time, but if MS and Amazon merge or partner down the road, you could imagine you need the right hardware or you can't buy groceries (Or... something)

To fix it, you can follow [these steps](https://pureinfotech.com/install-windows-11-unsupported-pc/), to summarize:
1. At the install screen (Before you click Install) press **Shift+F10** to bring up a cmd prompt
   - (I hope you have F1 through F12 keys, otherwise you will need to get creative)
2. In cmd, type `regedit`, and press enter
   - This is the Windows Registry Editor. It's an old program that allows you to modify different system and user config files. This is kind of similar to editing `plist` files in `~/Library` on macOS.
3. On the left, navigate to `HKEY_LOCAL_MACHINE` then `SYSTEM` then `Setup`
   - Inside that `Setup` folder should be these three "Keys": `AllowStart`, `Pid`, `SETUPCL`
4. Right click the `Setup` folder, and create a new Key, named: `LabConfig`
5. Enter the `LabConfig` key, and on the right-hand-side, right click to create a new `DWORD (32-bit)` value. Do this three times, with the following names:
   - `BypassTPMCheck`
   - `BypassSecureBootCheck`
   - `BypassRAMCheck`
6. After creating each of those, double click or right-click -> Modify them, so that each of their values is `1`.
7. Now continue with the installation

Note: If you are using Virtualbox (AKA, you probbaly aren't on this page?) You should use [these settings](https://blogs.oracle.com/virtualization/post/install-microsoft-windows-11-on-virtualbox) for Windows 11.

## Bonus 2 (UNMOUNTABLE_BOOT_VOLUME)
If, after installing, you get a bluescreen that occurs quickly with the code UNMOUNTABLE_BOOT_VOLUME, there are tutorials online that will have you run variations of the following commands:

```
bootrec /fixmbr
bootrec /fixboot
bootsect /nt60 sys
bootrec /fixboot (yes, again, after the bootsec)
bcdedit /rebuildbcd
```

If you mess around with those commands, but still nothing seems to fix it, I would suggest just completely deleting the EFI partition. Leave that space as unallocated, and allow the Windows installer to recreate it all on its own. I used to have a 1GB EFI partition manually created (FAT format) that housed both ubuntu and Windows boot folders. As of Windows 11, however, no matter what I did, the Windows bootloader refused to boot with this partition.

After deleting the partition, however (And backing up `EFI/ubuntu`), the Windows installer recreated the EFI partition as a 100MB partition, alongside 2 other recovery/unused partitions. I believe there's some issue with the boot logic where it expects these partitions to be present during UEFI boot, and if Linux created the EFI partition, it ends up in an unexpected state.

Once Windows 11 recreated them during the install, and boot normally, I just copied back the `EFI/ubuntu` folder, and was able to boot back into Linux. If you aren't able to back up this folder, you should be able to re-create the entries needed for Linux [like this](https://unix.stackexchange.com/a/169461):

(With the EFI partition mounted at `/boot/efi`):
```
grub-install --efi-directory=/boot/efi
```

UEFI booting is supposed to be simpler: just manage an entry on the EFI partition. The UNMOUNTABLE_BOOT_ERROR makes it seem more complicated, but I would mentally file this under "Microsoft just requiring some special sauce" category of issues. Copying and moving around the `/boot/efi/ubuntu` folder back and forth to the EFI partition, whether Windows create it or not, on my machine allowed me to consistently boot back into Linux.

As an aside, this is why some tutorials will suggest for dual boots to install Windows first, let it set up the partitions how it wants them, and then after that, install Ubuntu/Linux.

In case you are in a similar situation to me, here are some rough CMD analogues to some common unix commands:
- `cp [targ] [dest]` -> `xcopy [targ] [dest] /E /H /C /I`
- `mv [targ] [dest]` -> `ren [targ] [dest]` or `move [targ] [dest]`
- `rm [targ]` -> `del [targ]`
- `rm -rf [targ]` -> `rmdir /s [targ]`

And next time someone tells you DOS commands being arcane isn't an issue because Powershell or WSL exists, kindly remind them that these won't help you when it's 2am and you can't get your OS to boot.

## Bonus 3 (Offline install)
Wow, I did not expect to run into Yet Another problem before the OS is fully set up, but here we are. This one is a little more straightforwards, but if you don't want to sign into a Microsoft account during the initial Windows 11 setup, hit Shift+F10 and enter the following command:

```
oobe\bypassnro
```

All one command like that, no spaces. This will restart the computer but set the "Out of Box Experience" to allow you to configure it without connecting to the network. If you already entered your networking info and connected, expecting not to be held hostage to use a MS account, you can use `ipconfig /release` to disconnect first.