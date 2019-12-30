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

"""
To install Robot Framework Ftp Library execute command:
    run command: pip install robotframework-ftplibrary

    OR

    download, unzip and run command: python setup.py install
"""
from distutils.core import setup

setup(name='robotframework-ftplibrary',
      version='1.8',
      description='Robot Framework Ftp Library',
      author='Marcin Kowalczyk',
      license='GPLv3',
      url='http://sourceforge.net/projects/rf-ftp-py/',
      py_modules=['FtpLibrary'],
      data_files=[('Example RF script', ['ftpLibraryExample.robot']),
                  ('Keywords documentation', ['FtpLibrary.html']),
                  ('License file', ['LICENSE_lgpl-3.0.txt'])]
      )