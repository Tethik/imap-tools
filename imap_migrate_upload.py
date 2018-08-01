"""
Uploads a folder of previously imap-download-ed emails into an imap inbox.
For every subfolder it will create the subfolder/mailbox if it does not already exist 
in the root mailbox. 

Each email will be appended to the target imap mailbox. Meaning if you run this command multiple times,
you will end up with multiple copies of the same email in the inbox.
"""
import imaplib
import os
import os.path
import pathlib
import json
import base64
from datetime import datetime
import click


# 01-Jan-2014 23:20:11 +0100
date_format_str = "%d-%b-%Y %H:%M:%S %z"


def list_mailboxes(M):
    typ, data = M.list()
    for line in data:
        yield line.decode('utf-7').split('"."')[1].strip()


def upload_folder(M: imaplib.IMAP4_SSL, email, folder):
    path = os.path.join(email, folder)
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        with open(file_path) as f:            
            res = json.load(f)
        # msg = pathlib.Path(file).read_bytes()
        body = base64.b64decode(res["body"])
        internal_date = datetime.strptime(res["date"], date_format_str)
        M.append(folder, res["flags"], internal_date, body)


def upload(import_folder, host, to_email, password):
    M = imaplib.IMAP4_SSL(host=host)
    M.login(to_email, password)
    print(f"[INFO] Logged in as {to_email}")
    folders = set(list(list_mailboxes(M)))
    folders_to_upload = os.listdir(import_folder)
    with click.progressbar(folders_to_upload, label="[INFO] Uploading folders", item_show_func=lambda x: x) as bar:
        for folder in bar:
            if folder not in folders:
                M.create(folder)
            upload_folder(M, import_folder, folder)
    print("[INFO] Done!")
    M.logout()


@click.command(help=__doc__)
@click.argument('import_folder', help="Directory on your disk to import emails from")
@click.argument('host', help="hostname to the imap server you are uploading to, e.g. mail.example.com")
@click.argument('to_email', help="imap account you are uploading to.")
@click.option("--password", prompt=True, hide_input=True)
def cli(import_folder, host, to_email, password):
    upload(import_folder, host, to_email, password)


if __name__ == "__main__":
    cli()

