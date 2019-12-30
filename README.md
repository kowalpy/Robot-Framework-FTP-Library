# Robot Framework FTP Library

This library provides functionality of FTP client. FTP communication provided by ftplib.

Starting from 3rd of Janury 2017, project is hosted at Github. 

## License

LGPL 3.0

## Keyword documentation

[FtpLibrary.html](https://kowalpy.github.io/Robot-Framework-FTP-Library/FtpLibrary.html)

## Version history

Version 1.3 released on 30th of January 2016.

What's new in release 1.3:
- multiple connections in parallel
- strongly refactored source code
- enabling/disabling printout of messages returned by ftp server

Version 1.4 released on 17th of May 2017  

What's new in release 1.4:
- running library remotely
- IronPython compatibility issue fixed by Jarkko Peltonen

Version 1.5 released on 25th of December 2017

What's new in release 1.5:
- Python 3 support by Dirk Richter
- New Keyword Dir Names

Version 1.6 released on 10th of January 2018

What's new in release 1.6:
- fixed session closing by Antonpaa

Version 1.7 released on 30th of December 2019

What's new in release 1.7:
- TLS support by Antonpaa
- one bugfix by Jarkko Peltonen

## Installation
- run command: **pip install robotframework-ftplibrary**

OR
- download, unzip and run command: python setup.py install

## Usage
	
The simplest example (connect, change working dir, print working dir, close):
```
 | ftp connect | 192.168.1.10             | mylogin | mypassword |
 | cwd         | /home/myname/tmp/testdir |         |            |
 | pwd         |                          |         |            |
 | ftp close   |                          |         |            |
```

It is possible to use multiple ftp connections in parallel. Connections are
identified by string identifiers:
```
 | ftp connect | 192.168.1.10             | mylogin  | mypassword  | connId=ftp1 |
 | ftp connect | 192.168.1.20             | mylogin2 | mypassword2 | connId=ftp2 |
 | cwd         | /home/myname/tmp/testdir | ftp1     |             |             |
 | cwd         | /home/myname/tmp/testdir | ftp2     |             |             |
 | pwd         | ftp2                     |          |             |             |
 | pwd         | ftp1                     |          |             |             |
 | ftp close   | ftp2                     |          |             |             |
 | ftp close   | ftp1                     |          |             |             |
```

During library import it is possible to disable logging of server messages.
By default logging is enabled:
```
 | Library | FtpLibrary.py |
```
 To disable logging of server messages, additional parameter must be added to import:
``` 
 | Library | FtpLibrary.py | False |
``` 

## Running remotely

To run library remotely execute: *python FtpLibrary.py ipaddress portnumber*
(for example: *python FtpLibrary.py 192.168.0.101 8222*)