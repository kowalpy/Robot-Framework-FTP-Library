*** Settings ***
Library           Remote    http://192.168.0.101:8222    WITH NAME    ftplib

*** Test Cases ***
theSimplestExample
    comment    FTP server IP address    taken from    http://stackoverflow.com/questions/7968703/is-there-a-public-ftp-server-to-test-upload-and-download
    ftplib.ftp connect    speedtest.tele2.net
    @{dirResult}=    dir
    ${pwdMsg}=    pwd
    ftplib.download file    1KB.zip
    ftplib.ftp close
