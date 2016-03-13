---
layout: post
title: How To: Host a File Locally
date: 2016-03-13 13:35:41
comments: true
categories: python, tutorial
id: 4370481922
---
Here's a quick guide on how to host a file over the network. 

There are three basic parts to this:
1. Knowing your local IP
2. Knowing where the files to host are
3. Running a server to serve it over HTTP

Every single website that you see and visit in your browser is done over the [HyperText Transfer Protocol](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol). These websites are hosted on remote servers, which distribute content to you via this protocol. So to host a file, we will need to run a server on your machine, to be visited by the other machine.

After step 3. is accomplished on the hosting computer that is running the server, any machine on your network will be able to visit the content that is being hosted by navigating to http://YOUR_IP:port. The default port is 80. This is true for any website: for example [this](http://serebii.net) vs [this](http://serebii.net:80).

### Installing a server
The host will require a server. There are many different types of http servers for many various operating systems. For this guide, I will be demonstrating how to host it using a built-in module in [python](https://www.python.org/).

Python is included on most modern operating systems, but not on some of the most *popular* operating systems. Open up a terminal (or CMD on Windows) and run: ```python --version``` If you get back "no command found" or something similar, you will have to [install python](https://www.python.org/downloads/). This guide uses the 2.7.x version. Also if on Windows, you'll want to add the python binaries to your path, [instructions here](https://docs.python.org/2/using/windows.html#configuring-python).

When it's all setup and configured properly, you should get output like this from your terminal:
```
>> python --version
Python 2.7.6
```

### Finding your local IP
Now we need to find your local IP. This is different from your public one that you can get from the Internet. The local IP refers to an IP that you have within your sub-network only. In order to get it, we will need to retrieve the information from your computer. [Here is an article](http://lifehacker.com/5833108/how-to-find-your-local-and-external-ip-address) with detailed steps for Mac and Windows. On Linux and Mac you can also run ```ifconfig``` and look for the IP next to your interface. 

It's very common for your local IP to be one of the following formats: 192.168.x.x or 10.x.x.x, so you can expect it to look lke that.

### Getting the files to host
Now that we are ready to run the server, we need files to actually host. cd into the folder ([Windows](http://ss64.com/nt/cd.html)) ([Other](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/3/html/Step_by_Step_Guide/s1-navigating-cd.html)) with the files you want to host, and run the folliowing:
```
>> python -m SimpleHTTPServer
Serving HTTP on 0.0.0.0 port 8000 ...
```
This command will run until you hit Ctrl+C. While it's running, you should be able to go to http://YOUR_IP:8000/ in your browser **on any computer on your network**. Upon visiting, you should see a list of files in the current directory. If you put html files in this folder, you will also be able to see them rendered on screen.

If you are using python 3, the command is as follows:
```
>> python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 ...
```

At this point you can now go to another machine and check it to make sure it works!

### Troubleshooting
#### Cannot find terminal/cmd
Search for it on your computer or google how to run/open one.

#### Cannot find python
Install python, or make sure that the python binaries are on your path. Google it if you continue to have issues.

#### It says serving on port 8000, but cannot access it
Make sure the computer you are trying to access it from is on the same network as you. If that fails, check your firewall setting or anti-virus to make sure it isn't being blocked. Try googling the specific issues with "python simplehttpserver" in your search query.

### Soapbox
Python does not come preinstalled or configured on Windows. This is one reason why I might recommend switching to a unix/linux operating system, even just for a little while. Once you get comfortable with the terminal a lot more possibilities open up for what you can do with your device.
