#Robot Framework FTP Library
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.



import ftplib
import os
import socket
from robot.api import logger

class FtpLibrary(object):

    """
This library provides functionality of FTP client.

Version 1.3 released on 30th of January 2016.

What's new in release 1.3:
- multiple connections in parallel
- strongly refactored source code
- enabling/disabling printout of messages returned by ftp server

Despite new features, 1.3 should be compatible with previous versions.

FTP communication provided by ftplib.py

Author: Marcin Kowalczyk

Website: http://sourceforge.net/projects/rf-ftp-py/

Installation:
- run command: pip install robotframework-ftplibrary

OR
- download, unzip and run command: python setup.py install

OR
- download, unzip and copy FtpLibrary.py file to a directory pointed by
    PYTHONPATH (for example ...\Python27\lib\site-packages).

The simplest example (connect, change working dir, print working dir, close):
 | ftp connect | 192.168.1.10 | mylogin | mypassword |
 | cwd | /home/myname/tmp/testdir |
 | pwd |
 | ftp close |

It is possible to use multiple ftp connections in parallel. Connections are
identified by string identifiers:
 | ftp connect | 192.168.1.10 | mylogin | mypassword | connId=ftp1 |
 | ftp connect | 192.168.1.20 | mylogin2 | mypassword2 | connId=ftp2 |
 | cwd | /home/myname/tmp/testdir | ftp1 |
 | cwd | /home/myname/tmp/testdir | ftp2 |
 | pwd | ftp2 |
 | pwd | ftp1 |
 | ftp close | ftp2 |
 | ftp close | ftp1 |

"""

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self, printOutput=True):
        """
        During library import it is possible to disable logging of server messages.
        By default logging is enabled:
        | Library | FtpLibrary.py |
        To disable logging of server messages, additional parameter must be added to
        import:
        | Library | FtpLibrary.py | False |
        """
        self.ftpList = {}
        if isinstance(printOutput, bool):
            self.printOutput = printOutput
        else:
            if printOutput == "False":
                self.printOutput = False
            else:
                self.printOutput = True

    def __getConnection(self, connId):
        if connId in self.ftpList:
            return self.ftpList[connId]
        else:
            errMsg = "Connection with ID %s does not exist. It should be created before this step." % connId
            raise FtpLibraryError(errMsg)

    def __addNewConnection(self, connObj, connId):
        if connId in self.ftpList:
            errMsg = "Connection with ID %s already exist. It should be deleted before this step." % connId
            raise FtpLibraryError(errMsg)
        else:
            self.ftpList[connId] = connObj

    def __removeConnection(self, connId):
        if connId in self.ftpList:
            self.ftpList.pop(connId)

    def getAllFtpConnections(self):
        """
        Returns a dictionary containing active ftp connections.
        """
        outputMsg = "Current ftp connections:\n"
        counter = 1
        for k in self.ftpList:
            outputMsg += str(counter) + ". " + k + " "
            outputMsg += str(self.ftpList[k]) + "\n"
            counter += 1
        if self.printOutput:
            logger.info(outputMsg)
        return self.ftpList

    def ftp_connect(self, host, user='anonymous', password='anonymous@', port=21, timeout=30, connId='default'):
        """
        Constructs FTP object, opens a connection and login.
        Call this function before any other (otherwise raises exception).
        Returns server output.
        Parameters:
            - host - server host address
            - user(optional) - FTP user name. If not given, 'anonymous' is used.
            - password(optional) - FTP password. If not given, 'anonymous@' is used.
            - port(optional) - TCP port. By default 21.
            - timeout(optional) - timeout in seconds. By default 30.
            - connId(optional) - connection identifier. By default equals 'default'
        Examples:
        | ftp connect | 192.168.1.10 | mylogin | mypassword |  |  |
        | ftp connect | 192.168.1.10 |  |  |  |  |
        | ftp connect | 192.168.1.10 | mylogin | mypassword | connId=secondConn |  |
        | ftp connect | 192.168.1.10 | mylogin | mypassword | 29 | 20 |
        | ftp connect | 192.168.1.10 | mylogin | mypassword | 29 |  |
        | ftp connect | 192.168.1.10 | mylogin | mypassword | timeout=20 |  |
        | ftp connect | 192.168.1.10 | port=29 | timeout=20 |  |  |
        """
        if connId in self.ftpList:
            errMsg = "Connection with ID %s already exist. It should be deleted before this step." % connId
            raise FtpLibraryError(errMsg)
        else:
            newFtp = None
            outputMsg = ""
            try:
                timeout = int(timeout)
                port = int(port)
                newFtp = ftplib.FTP()
                outputMsg += newFtp.connect(host, port, timeout)
                outputMsg += newFtp.login(user,password)
            except socket.error as se:
                raise FtpLibraryError('Socket error exception occured.')
            except ftplib.all_errors as e:
                raise FtpLibraryError(str(e))
            except Exception as e:
                raise FtpLibraryError(str(e))
            if self.printOutput:
                logger.info(outputMsg)
            self.__addNewConnection(newFtp, connId)

    def get_welcome(self, connId='default'):
        """
        Returns wlecome message of FTP server.
        Parameters:
        - connId(optional) - connection identifier. By default equals 'default'
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        try:
            outputMsg += thisConn.getwelcome()
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    def pwd(self, connId='default'):
        """
        Returns the pathname of the current directory on the server.
        Parameters:
        - connId(optional) - connection identifier. By default equals 'default'
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        try:
            outputMsg += thisConn.pwd()
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    def cwd(self, directory, connId='default'):
        """
        Changes working directory and returns server output. Parameters:
        - directory - a path to which working dir should be changed.
        - connId(optional) - connection identifier. By default equals 'default'
        Example:
        | cwd | /home/myname/tmp/testdir |  |
        | cwd | /home/myname/tmp/testdir | ftp1 |
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        try:
            outputMsg += thisConn.cwd(directory)
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    def dir(self, connId='default'):
        """
        Returns list of contents of current directory.
        Parameters:
        - connId(optional) - connection identifier. By default equals 'default'
        """
        dirList = []
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        try:
            thisConn.dir(dirList.append)
            for d in dirList:
                outputMsg += str(d) + "\n"
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return dirList

    def mkd(self, newDirName, connId='default'):
        """
        Creates new directory on FTP server. Returns new directory path.
        Parameters:
        - newDirName - name of a new directory
        - connId(optional) - connection identifier. By default equals 'default'
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        try:
            outputMsg += str(thisConn.mkd(newDirName))
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    def rmd(self, directory, connId='default'):
        """
        Deletes directory from FTP server. Returns server output.
        Parameters:
        - directory - path to a directory to be deleted
        - connId(optional) - connection identifier. By default equals 'default'
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        try:
            outputMsg += str(thisConn.rmd(directory))
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    def download_file(self, remoteFileName, localFilePath=None, connId='default'):
        """
        Downloads file from current directory on FTP server in binary mode. If
        localFilePath is not given, file is saved in current local directory (by
        default folder containing robot framework project file) with the same name
        as source file. Returns server output
        Parameters:
        - remoteFileName - file name on FTP server
        - localFilePath (optional) - local file name or path where remote file should be saved.
        - connId(optional) - connection identifier. By default equals 'default'
        localFilePath variable can have following meanings:
        1. file name (will be saved in current default directory);
        2. full path (dir + file name)
        3. dir path (original file name will be added)
        Examples:
        | download file | a.txt |  |  |
        | download file | a.txt | b.txt | connId=ftp1 |
        | download file | a.txt | D:/rfftppy/tmp |  |
        | download file | a.txt | D:/rfftppy/tmp/b.txt |  |
        | download file | a.txt | D:\\rfftppy\\tmp\\c.txt |  |
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        localPath = ""
        if localFilePath == None:
            localPath = remoteFileName
        else:
            localPath = os.path.normpath(localFilePath)
            if os.path.isdir(localPath):
                localPath = os.path.join(localPath, remoteFileName)
        try:
            localFile = open(localPath, 'wb')
            outputMsg += thisConn.retrbinary("RETR " + remoteFileName, localFile.write)
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    def upload_file(self, localFileName, remoteFileName=None, connId='default'):
        """
        Sends file from local drive to current directory on FTP server in binary mode.
        Returns server output.
        Parameters:
        - localFileName - file name or path to a file on a local drive.
        - remoteFileName (optional) - a name or path containing name under which file should be saved.
        - connId(optional) - connection identifier. By default equals 'default'
        If remoteFileName agument is not given, local name will be used.
        Examples:
        | upload file | x.txt | connId=ftp1 |
        | upload file | D:/rfftppy/y.txt |  |
        | upload file | u.txt | uu.txt |
        | upload file | D:/rfftppy/z.txt | zz.txt |
        | upload file | D:\\rfftppy\\v.txt |  |
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        remoteFileName_ = ""
        localFilePath = os.path.normpath(localFileName)
        if not os.path.isfile(localFilePath):
            raise FtpLibraryError("Valid file path should be provided.")
        else:
            if remoteFileName==None:
                fileTuple = os.path.split(localFileName)
                if len(fileTuple)==2:
                    remoteFileName_ = fileTuple[1]
                else:
                    remoteFileName_ = 'defaultFileName'
            else:
                remoteFileName_ = remoteFileName
            try:
                outputMsg += thisConn.storbinary("STOR " + remoteFileName_, open(localFilePath, "rb"))
            except ftplib.all_errors as e:
               raise FtpLibraryError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    def size(self, fileToCheck, connId='default'):
        """
        Checks size of a file on FTP server. Returns size of a file in bytes (integer).
        Parameters:
        - fileToCheck - file name or path to a file on FTP server
        - connId(optional) - connection identifier. By default equals 'default'
        Example:
        | ${file1size} = | size | /home/myname/tmp/uu.txt | connId=ftp1 |
        | Should Be Equal As Numbers | ${file1size} | 31 |  |

        Note that the SIZE command is not standardized, but is supported by many
         common server implementations.
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        try:
            tmpSize = thisConn.size(fileToCheck)
            outputMsg += str(tmpSize)
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    def rename(self, targetFile, newName, connId='default'):
        """
        Renames (actually moves) file on FTP server. Returns server output.
        Parameters:
        - targetFile - name of a file or path to a file to be renamed
        - newName - new name or new path
        - connId(optional) - connection identifier. By default equals 'default'
        Example:
        | rename | tmp/z.txt | /home/myname/tmp/testdir/z.txt |
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        try:
            outputMsg += str(thisConn.rename(targetFile, newName))
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    def delete(self, targetFile, connId='default'):
        """
        Deletes file on FTP server. Returns server output.
        Parameters:
        - targetFile - file path to be deleted
        - connId(optional) - connection identifier. By default equals 'default'
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        try:
            outputMsg += str(thisConn.delete(targetFile))
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    def send_cmd(self, command, connId='default'):
        """
        Sends any command to FTP server. Returns server output.
        Parameters:
        - command - any valid command to be sent (invalid will result in exception).
        - connId(optional) - connection identifier. By default equals 'default'
        Example:
        | send cmd | HELP |
        """
        thisConn = self.__getConnection(connId)
        outputMsg = ""
        try:
            outputMsg += str(thisConn.sendcmd(command))
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    def ftp_close(self, connId='default'):
        """
        Closes FTP connection. Returns None.
        Parameters:
        - connId(optional) - connection identifier. By default equals 'default'
        """
        thisConn = self.__getConnection(connId)
        try:
            thisConn.close()
            self.__removeConnection(connId)
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))

    def __del__(self):
        self.ftpList = {}

class FtpLibraryError(Exception):
    def __init__(self,msg):
        self.msg = msg

    def __str__(self):
        return self.msg

def main():
    mainMsg = "FtpLibrary is a functionality of FTP client for Robot Framework."
    mainMsg += " For instruction on how to use please visit "
    mainMsg += "http://sourceforge.net/projects/rf-ftp-py/"
    print mainMsg

if __name__ == '__main__':
    main()
