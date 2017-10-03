# filescout
A command line tool used to perform log investigation based on the timestamps of an input file.

Filescout is a utility created to determine the origin of a malicious file based on the modified or change time (whichever is more recent) of a given file. It was developed exclusively for a cPanel environment, running on CentOS/CloudLinux/RHEL 6 and 7. 

Filescout solves a number of potential problems, and can save time when investigating the source of a malicious file.


### Installation:
Create the /root/bin directory, if it doesn't already exist:

```
 mkdir -p /root/bin
```
And grab the script:
```
wget -O /root/bin/filescout http://mattjung.net/filescout
```
And give it execute permissions:
```
chmod +x /root/bin/filescout
```
### Usage:
Usage is very simple, you just call filescout, and give it a file that you want to to investigate. There are also optional flags that can be used. 

```
filescout somefile.php
```

Flags:
```     
        -h  Displays the help menu.
        -v  Displays the version of Filescout
        -m  Force use of the Modified timestamp.
        -c  Force use of the Change timestamp.
        -b  Force use of the file's CREATION timestamp (Only available on ext4 filesystems)        
        -r  [Experimental] Enables recursive searching. Lets you investigate a file that uploaded a file that uploaded a file....and so on.
        -t 'STAT TIMESTAMP' USER
             Example usage with -t:
             filescout -t '2017-06-26 16:25:26.473000000 -0400' myuser 
             (The timestamp MUST be in quotes)
```

### What it does:
* When given an input file, filescout will get a stat of the absolute path of the file.
* It then searches the apache domlogs (daily and archived) for signs of an HTTP POST request based off either the modified or change time (whichever is more recent) of your input file, which indicates a possible point of entry for your original input file.
* It then checks for a possible FTP upload, based off the timestamp of the modified or change time.
* It then converts the timestamp to UTC and searches for a possible cPanel file manager upload from the cPanel user.
* The last thing it checks is for a SSH/SFTP login from that user on the day of modification or change of the original input file. This last search is very broad, only because uploads via SFTP aren't explicitly logged in /var/log/secure.

### Example output:

```
[root@web.mattjung.net /home/mattjung/public_html/script-test]# filescout malicious_shell1.php 
============================================
          Stats and timestamps            
============================================

The change time is equal to, or more recent than the modified time. Using the change time going forward.
Heres a stat of malicious_shell1.php: (With the full file path!!)

  File: ‘/home/mattjung/public_html/script-test/malicious_shell1.php’
  Size: 25        	Blocks: 8          IO Block: 4096   regular file
Device: fd03h/64771d	Inode: 432515      Links: 1
Access: (0644/-rw-r--r--)  Uid: ( 1003/mattjung)   Gid: ( 1003/mattjung)
Access: 2017-06-26 16:28:35.087000000 -0400
Modify: 2017-06-26 16:28:35.087000000 -0400
Change: 2017-06-26 16:28:35.087000000 -0400

============================================
               Log diving                 
============================================

Found HTTP POST entry when searching the Apache domlogs for the following domain(s): mattjung.net

/usr/local/apache/domlogs/mattjung/mattjung.net-ssl_log:55.30.55.31 - - [26/Jun/2017:16:28:35 -0400] "POST /script-test/upload.php HTTP/1.1" 200 151 "https://mattjung.net/script-test/data1.php" "Mozilla/5.0 (X11; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0"

The above POST request was directed at this file: /home/mattjung/public_html/script-test/data1.php
You should review the above file if you have not already done so.


 You should review the file that was POST-ed to, and re-run filescout on that file if it is malicious.
 Repeat this process until:
	 -You've found the original source of the compromise.
	 -You've run out of logs to look through.
	 -The trail of logs goes cold.

Don't forget to  chmod 000 /home/mattjung/public_html/script-test/malicious_shell1.php  if it's malicious! 

```
 
