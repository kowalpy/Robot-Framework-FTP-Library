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

#to generate libdoc documentation run:
#   python -m robot.libdoc FtpLibrary FtpLibrary.html

import ftplib
import os
import socket
from robot.api import logger

class FtpLibrary(object):

    """
This library provides functionality of FTP client.

Version 1.9 released on 27th of February 2020

What's new in release 1.9:
- active mode added by Alexander Klose (scathaig)

FTP communication provided by ftplib.py

Author: [https://github.com/kowalpy|Marcin Kowalczyk]

Website: https://github.com/kowalpy/Robot-Framework-FTP-Library

Installation:
- run command: pip install robotframework-ftplibrary

OR
- download, unzip and run command: python setup.py install

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

To run library remotely execute: python FtpLibrary.py <ipaddress> <portnumber>
(for example: python FtpLibrary.py 192.168.0.101 8222)
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

    def __isTlsConnection(self, connObject):
        if not isinstance(connObject, ftplib.FTP_TLS):
            raise FtpLibraryError("Keyword should be used only with TLS connection")

    def __isRegularConnection(self, connObject):
        if not isinstance(connObject, ftplib.FTP):
            raise FtpLibraryError("Non regular connection")

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

    def ftp_connect(self, host, user='anonymous', password='anonymous@', port=21, timeout=30, connId='default', tls=False, mode='passive'):
        """
        Constructs FTP object, opens a connection and login. TLS support is optional.
        Call this function before any other (otherwise raises exception).
        Returns server output.
        Parameters:
            - host - server host address
            - user(optional) - FTP user name. If not given, 'anonymous' is used.
            - password(optional) - FTP password. If not given, 'anonymous@' is used.
            - port(optional) - TCP port. By default 21.
            - timeout(optional) - timeout in seconds. By default 30.
            - connId(optional) - connection identifier. By default equals 'default'
            - tls(optional) - TLS connections flag. By default False
            - mode(optional) - set the transfer mode to 'active' or 'passive'. By default 'passive'
            
        Examples:
        | ftp connect | 192.168.1.10 | mylogin | mypassword |  |  |
        | ftp connect | 192.168.1.10 |  |  |  |  |
        | ftp connect | 192.168.1.10 | mylogin | mypassword | connId=secondConn |  |
        | ftp connect | 192.168.1.10 | mylogin | mypassword | 29 | 20 |
        | ftp connect | 192.168.1.10 | mylogin | mypassword | 29 |  |
        | ftp connect | 192.168.1.10 | mylogin | mypassword | timeout=20 |  |
        | ftp connect | 192.168.1.10 | port=29 | timeout=20 |  |  |
        | ftp connect | 192.168.1.10 | port=29 | timeout=20 | mode=active |  |
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
                newFtp = None
                if tls:
                    newFtp = ftplib.FTP_TLS()
                else:
                    newFtp = ftplib.FTP()
                outputMsg += newFtp.connect(host, port, timeout)
                self.__addNewConnection(newFtp, connId)
                outputMsg += newFtp.login(user, password)
                
                # set mode depending of "mode" value. if it is not "active" or "passive" default to passive
                newFtp.set_pasv({'passive': True, 'active': False}.get(mode, True))
                
            except socket.error as se:
                raise FtpLibraryError('Socket error exception occured.')
            except ftplib.all_errors as e:
                if connId in self.ftpList:
                    self.ftp_close(connId)
                raise FtpLibraryError(str(e))
            except Exception as e:
                raise FtpLibraryError(str(e))
            if self.printOutput:
                logger.info(outputMsg)

    def clear_text_data_connection(self, connId='default'):
        """
        Switches to a clear text data connection.
        Only usable with an FTP TLS connection. No effect if used with a regular ftp connection.
        Parameters:
        - connId(optional) - connection identifier. By default equals 'default'
        """
        outputMsg = ""
        thisConn = self.__getConnection(connId)
        self.__isTlsConnection(thisConn)
        try:
            thisConn.prot_c()
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    def secure_data_connection(self, connId='default'):
        """
        Switches to a secure data connection.
        Only usable with an FTP TLS connection. No effect if used with a regular ftp connection.
        Parameters:
        - connId(optional) - connection identifier. By default equals 'default'
        """
        outputMsg = ""
        thisConn = self.__getConnection(connId)
        self.__isTlsConnection(thisConn)
        try:
            thisConn.prot_p()
        except ftplib.all_errors as e:
            raise FtpLibraryError(str(e))
        if self.printOutput:
            logger.info(outputMsg)
        return outputMsg

    def get_welcome(self, connId='default'):
        """
        Returns welcome message of FTP server.
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
        Returns list of raw lines returned as contens of current directory.
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

    def dir_names(self, connId='default'):
        """
        Returns list of files (and/or directories) of current directory.
        Parameters:
        - connId(optional) - connection identifier. By default equals 'default'
        """
        files_list = []
        thisConn = self.__getConnection(connId)
        try:
            files_list = thisConn.nlst()
        except:
            files_list = []
        return files_list

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
            with open(localPath, 'wb') as localFile:
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
            thisConn.quit()
            self.__removeConnection(connId)
        except Exception as e:
            try:
                thisConn.close()
                self.__removeConnection(connId)
            except ftplib.all_errors as x:
                raise FtpLibraryError(str(x))

    def __del__(self):
        self.ftpList = {}

class FtpLibraryError(Exception):
    def __init__(self,msg):
        self.msg = msg

    def __str__(self):
        return self.msg

def main():
    import sys
    from robotremoteserver import RobotRemoteServer
    print("Starting Robot Framework Ftp Library as a remote server ...")
    RobotRemoteServer(library=FtpLibrary(), host=sys.argv[1], port=sys.argv[2])

if __name__ == '__main__':
    main()
