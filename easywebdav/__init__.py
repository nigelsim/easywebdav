import sys
import os
import argparse
import urlparse
from easywebdav.client import Client


def connect(*args, **kwargs):
    """connect(host, port=0, auth=None, username=None, password=None, protocol='http', path="/")"""
    return Client(*args, **kwargs)


def cmd_connect(url, verify_ssl=True):
    """Connect to the remote server and return the Client object"""
    parts = urlparse.urlparse(url)

    return connect(parts.hostname, username=parts.username,
                   password=parts.password, protocol=parts.scheme,
                   path=parts.path, verify_ssl=verify_ssl), parts


def do_list(remote, verify_ssl):
    """Perform a listing of a folder"""
    con, parts = cmd_connect(remote, verify_ssl)
    for item in con.ls():
        print item


def do_mkdir(remote, verify_ssl):
    con, parts = cmd_connect(remote, verify_ssl)
    con.mkdir('/')
    print "Made", remote


def do_rmdir(remote, verify_ssl):
    con, parts = cmd_connect(remote, verify_ssl)
    con.rmdir('/')
    print "Deleted", remote


def do_upload(local, remote, verify_ssl):
    """Upload a file or directory to a remote location"""
    con, parts = cmd_connect(remote, verify_ssl)
    if os.path.isfile(local):
        try:
            con.upload(local, os.path.basename(local))
            print "Uploaded OK: " + local
        except:
            print "Upload failed: " + local
            raise
    else:
        # Uploading a directory
        os.path.walk(local, _do_upload_dir, (con, local))


def _do_upload_dir(args, dirname, files):
    """Callback for walking the directory tree and uploading files and folders.
    This overwrites any existing files"""
    con, basepath = args
    relpath = os.path.relpath(dirname, basepath)
    if not relpath.endswith('/'):
        relpath += '/'
    if not con.exists(relpath):
        con.mkdirs(relpath)
    for f_name in files:
        f_path = os.path.join(basepath, relpath, f_name)
        if not os.path.isfile(f_path):
            continue
        try:
            con.upload(f_path, relpath + f_name)
            print "Uploaded OK: " + (relpath + f_name)
        except:
            print "Upload failed: " + (relpath + f_name)
            raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help="ignore SSL errors")
    subparsers = parser.add_subparsers(dest='action')

    cmd_list = subparsers.add_parser('list')
    cmd_list.add_argument('url', help="remote URL")

    cmd_upload = subparsers.add_parser('upload')
    cmd_upload.add_argument('file', help="local file")
    cmd_upload.add_argument('url', help="remote directory URL")

    cmd_delete = subparsers.add_parser('delete')
    cmd_delete.add_argument('url', help="remote file URL")

    cmd_mkdir = subparsers.add_parser('mkdir')
    cmd_mkdir.add_argument('url', help="URL to create")

    cmd_rmdir = subparsers.add_parser('rmdir')
    cmd_rmdir.add_argument('url', help="remote dir URL to delete")

    args = parser.parse_args()

    if args.action == 'list':
        do_list(args.url, verify_ssl=args.i)
    elif args.action == 'upload':
        do_upload(args.file, args.url, verify_ssl=args.i)
    elif args.action == 'mkdir':
        do_mkdir(args.url, verify_ssl=args.i)
    elif args.action == 'rmdir':
        do_rmdir(args.url, verify_ssl=args.i)
    return 0

if __name__ == '__main__':
    sys.exit(main())
