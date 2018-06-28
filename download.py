"""
Downloads all emails in an imap account. Iterates through every mailbox on the account, saving every
email as JSON, with metadata for the flags and date, as well as the message content base64 encoded.

The downloaded files are structured as follows.
`<email>/<mailbox>/<uid>`
"""
import imaplib
import os
import os.path
import pathlib
import re
import json
import base64
import click


internal_date_pattern = re.compile(r'INTERNALDATE "(\d+\-[A-z]+\-\d+ \d+:\d+:\d+ ([\+\-]\d+)?)"')
flags_pattern = re.compile(r'FLAGS \((.+)\)')


def list_mailboxes(M):
    typ, data = M.list()
    for line in data:
        yield line.decode('utf-7').split('"."')[1].strip()


def download_folder(M, email, folder):
    path = os.path.join(email, folder)
    M.select(folder)
    os.makedirs(path)
    typ, data = M.search(None, 'ALL')
    for num in data[0].split():
        typ, data = M.fetch(num, '(FLAGS INTERNALDATE RFC822)')
        assert typ == "OK"
        email_path = os.path.join(path, num.decode('utf-7'))
        with open(email_path, 'w') as f:
            # first line contains flags and date.
            # Example: b'5 (FLAGS (\\Seen) INTERNALDATE "23-Jun-2014 21:17:54 +0200" RFC822 {542}'
            first_line = data[0][0].decode('utf-8')

            res = {
                "date": internal_date_pattern.search(first_line).group(1),
                "flags": flags_pattern.search(first_line).group(1)
            }
            body = b''
    
            for byt in data[0][1:]:
                body += byt
            
            res['body'] = base64.encodebytes(body).decode('utf-8')
            json.dump(res, f)
    M.close()    


def download(host, email, password):
    M = imaplib.IMAP4_SSL(host=host)
    try:
        M.login(email, password)
        print(f"[INFO] Logged in as {email}")
        folders = list(list_mailboxes(M))
        
        with click.progressbar(folders, label="[INFO] Downloading mailboxes", item_show_func=lambda x: x) as bar:
            for folder in bar:
                download_folder(M, email, folder)
    finally:
        M.logout()
    print("[INFO] Done :)")


@click.command(help=__doc__)
@click.argument("host")
@click.argument("email")
@click.option("--password", prompt=True, hide_input=True)
def cli(host, email, password):
    download(host, email, password)


if __name__ == "__main__":
    cli()

