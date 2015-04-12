---
layout: post
title: Chromebook Screen Dimming Tip
date: 2015-03-15 16:37:47
comments: true
categories: chromebook, linux, bash
id: 2405391604
---

I was looking for an alternative to f.lux / screen filter (android) / shades (mac) to keep the screen more dim at night, and couldn't find one that I liked. A lot of them would just dim the webpage and not the whole system. However, on linux there's a trick you can do to write the brightness value directly from the terminal, and I wondered if the same trick would work on chromeos.
 
With developer mode on, from crosh (ctrl+alt+T):
```
shell
sudo su
cd $(dirname $(find /sys -name brightness))
```
 
This will bring you to a directory with brightness information. On my Samsung chromebook this was ```/sys/devices/backlight.12/backlight/backlight.12/```
 
From here, you can use the following commands to check the max brightness, current brightness, and then set your own.
 
This will display the current brightness value:
```
cat actual_brightness
```
 
This will display the maximum brightness value:
```
cat max_brightness
```
 
This will set the brightness value to whatever number you put there (in this case, 7):
```
echo 7 > brightness
```
 
My chromebook, using just the buttons would allow me to go as low as 18, and so using this trick I was able to make it 1/3 as the dimmest settings the buttons would go!
 
This may have gotten a little technical, but it isn't using crouton or any other linux things, just out of the box developer mode. I was very impressed to see this linux trick still work on chromeos.