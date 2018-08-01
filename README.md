# README
Some scripts to help with migrating between imap servers. Use at your own risk!

## Install
Requires python 3.6.
```
pip3 install -U --user "git+https://github.com/Tethik/imap-tools#egg=imap-tools"
```

## Usage
Assuming you installed via pip.

Download an entire mailbox as follows (will ask for password via stdin):
```
imap-download <old server hostname> <email>
```
It will download all the emails into a folder `<email>`. 

Then upload to the new server as follows:
```
imap-upload <new server hostname> <email>
```
