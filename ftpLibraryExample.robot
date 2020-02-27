*** Settings ***
Library           FtpLibrary
Library           Collections

*** Variables ***
${public_address}    speedtest.tele2.net
${public_file_name}    1KB.zip
${local_ftp_addr_1}    10.1.4.21
${local_ftp_addr_2}    10.1.4.120
${local_ftp_addr_3}    10.1.4.87
${fake_ftp_addr}    10.244.17.36
${user_1}         marcin
${pass_1}         marcin
${user_2}         marcin
${pass_2}         marcin
${user_3}         marcin
${pass_3}         marcin
${test_file_name}    test.txt

*** Test Cases ***
the_simplest_example_public_ftp
    public example

the_simplest_example_public_ftp_looped
    FOR    ${i}    IN RANGE    0    3
        public example

get_connections
    [Documentation]    Testing new keyword "get all ftp connections"
    ${connections}=    get all ftp connections
    ftp connect    ${local_ftp_addr_1}    ${user_1}    ${pass_1}
    ftp connect    ${local_ftp_addr_2}    ${user_2}    ${pass_2}    connId=secondConn
    ftp connect    ${local_ftp_addr_3}    ${user_3}    ${pass_3}    connId=thirdConn
    ${connections}=    get all ftp connections
    @{connectionKeys}=    get dictionary keys    ${connections}
    @{connectionValues}=    get dictionary values    ${connections}
    FOR    ${k}    IN    @{connectionKeys}
        Log    ${k}
    FOR    ${c}    IN    @{connectionValues}
        Log    ${c}
    ftp close
    ftp close    secondConn
    ftp close    thirdConn
    ${connections}=    get all ftp connections

full_test_3_connections
    [Documentation]    Testing all keywords in the library in 3 different parallel connections.
    ftp connect    ${local_ftp_addr_1}    ${user_1}    ${pass_1}
    ftp connect    ${local_ftp_addr_2}    ${user_2}    ${pass_2}    connId=secondConn
    ftp connect    ${local_ftp_addr_3}    ${user_3}    ${pass_3}    connId=thirdConn
    ${newDir1}=    set variable    w_szczebrzeszynie
    ${newDir2}=    set variable    chrzaszcz_brzmi
    ${newDir3}=    set variable    w_trzcinie
    ${newFIle1}=    set variable    stol_z_powylamywanymi_nogami
    ${newFIle2}=    set variable    suchaSzosaSaszaSzedl
    ${welcomeMsg}=    get welcome
    Log    ${welcomeMsg}
    ${welcomeMsg}=    get welcome    connId=secondConn
    Log    ${welcomeMsg}
    ${welcomeMsg}=    get welcome    connId=thirdConn
    Log    ${welcomeMsg}
    ${pwdMsg}=    pwd
    Log    ${pwdMsg}
    Log    mkd
    mkd    ${newDir2}    secondConn
    Log    dir
    @{dirResult}=    dir    secondConn
    Log    ${dirResult}
    rmd    ${newDir2}    secondConn
    @{dirResult}=    dir    secondConn
    Log    ${dirResult}
    send cmd    HELP
    mkd    ${newDir1}    thirdConn
    cwd    ${newDir1}    thirdConn
    ${currDir}=    pwd    thirdConn
    upload file    ${test_file_name}    connId=thirdConn
    upload file    ${test_file_name}    ${newFIle2}    thirdConn
    dir    thirdConn
    rename    ${test_file_name}    ${newFIle1}    thirdConn
    dir    thirdConn
    comment    ${size}=    size    ${newFIle1}    thirdConn
    comment    Log    ${size}
    download file    ${newFIle1}    connId=thirdConn
    download file    ${newFIle2}    connId=thirdConn
    download file    ${newFIle1}    tmp    connId=thirdConn
    download file    ${newFIle2}    tmp    connId=thirdConn
    delete    ${newFIle1}    thirdConn
    delete    ${newFIle2}    thirdConn
    dir    thirdConn
    pwd    secondConn
    pwd    thirdConn
    ftp close
    ftp close    secondConn
    ftp close    thirdConn

negative_tests
    [Documentation]    Testing handling of exceptions
    ftp connect    ${local_ftp_addr_1}    ${user_1}    ${pass_1}    connId=newConn
    ${passed}=    Run Keyword And Return Status    pwd    connId=newConn2
    Run Keyword Unless    ${passed}    Log    Fail as expected
    ${passed2}=    Run Keyword And Return Status    ftp connect    ${local_ftp_addr_1}    ${user_1}    ${pass_1}    connId=newConn    # already existing connection ID
    Run Keyword Unless    ${passed2}    Log    Fail as expected
    ${passed3}=    Run Keyword And Return Status    pwd    connId=newConn8    # not existing connection ID
    Run Keyword Unless    ${passed3}    Log    Fail as expected
    ${passed4}=    Run Keyword And Return Status    ftp connect    ${fake_ftp_addr}    ${user_1}    ${pass_1}    # wrong IP address
    Run Keyword Unless    ${passed4}    Log    Fail as expected
    ${passed5}=    Run Keyword And Return Status    upload file    shagdfqfcrtcfjwgakwrj    connId=newConn    # not existing file
    Run Keyword Unless    ${passed5}    Log    Fail as expected

tls keywords check with non tls connection
    ftp connect    ${public_address}
    Clear Text Data Connection
    Secure Data Connection
    ftp close

the_simplest_example_public_ftp_active_mode
    comment    Public FTP server IP address taken from http://stackoverflow.com/questions/7968703/is-there-a-public-ftp-server-to-test-upload-and-download
    Log    Example does not work because server seems not to accept active mode    WARN
    ftp connect    ${public_address}    mode=active
    @{dirResult}=    dir
    Log    ${dirResult}
    @{files}=    dir names
    Log    ${files}
    ${pwdMsg}=    pwd
    download file    ${public_file_name}
    ftp close

*** Keywords ***
public_example
    comment    Public FTP server IP address taken from http://stackoverflow.com/questions/7968703/is-there-a-public-ftp-server-to-test-upload-and-download
    ftp connect    ${public_address}
    @{dirResult}=    dir
    Log    ${dirResult}
    @{files}=    dir names
    Log    ${files}
    ${pwdMsg}=    pwd
    download file    ${public_file_name}
    ${connections}=    get all ftp connections
    @{connectionKeys}=    get dictionary keys    ${connections}
    @{connectionValues}=    get dictionary values    ${connections}
    ftp close
