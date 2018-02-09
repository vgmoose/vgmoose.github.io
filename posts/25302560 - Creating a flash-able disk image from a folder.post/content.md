---
layout: post
title: Creating a flash-able disk image from a folder
date: 2018-02-09 00:20:24
comments: true
categories: linux, dd
id: 7951774518
---

First, create an empty file of the desired size that the disk image will be, using `dd`. The below will create a 1GB file (count*bs)
```
dd if=/dev/zero of=disk.img bs=512M count=2
```

Then, use `losetup` and the -P flag to use the newly created image as a loopback device.
```
losetup -P /dev/loop0 disk.img
```

Once the loopback device is created, you should be able to create a partition map on it using `fdisk`. (If you don't want to use fdisk, another disk partitioning program should work)
```
fdisk /dev/loop0
```

Inside of fdisk, you can now create your partitions. For instance, `g` will create a GPT map, and `n` will add a new partition to it. When you are done, type `write`.

Once the partition map is created, the system will reload the partitions, and you should now at least have a `/dev/loop0p1` device, representing the first partition. We can run whichever `mkfs` we want on this partition now:
```
mkfs.ext4 /dev/loop0p1
```

Once the filesystem is created, it can be mounted into an empty folder as if it were a real device.
```
mkdir /mnt/diskimage
mount /dev/loop0p1 /mnt/diskimage
```

You can put files or folders inside of the mount point now, and they will be written to the `disk.img` file as you write to the folder. When you're done, you can unmount the filesystem, and disconnect the loopback device.
```
umount /mnt/diskimage
losetup -d /dev/loop0
```

Now the `disk.img` file should contain the exact desired filesystem, and can be flashed to one or more target devices using `dd` on unix/linux or a program like [win32diskimager](https://sourceforge.net/projects/win32diskimager/) for windows.
```
dd if=disk.img of=/dev/sdX bs=500M
```