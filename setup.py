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
    python setup.py install
"""
from distutils.core import setup

setup(name='robotframework-ftplibrary',
      version='1.3',
      description='Robot Framework Ftp Library',
      author='Marcin Kowalczyk',
      author_email='mkov80@gmail.com',
      license='GPLv3',
      url='http://sourceforge.net/projects/rf-ftp-py/',
      py_modules=['FtpLibrary'],
      data_files=[('Example RF script', ['ftpLibraryExample.txt']),
                  ('Keywords documentation', ['FtpLibrary.html']),
                  ('License file', ['LICENSE_gpl-3.0.txt'])]
      )