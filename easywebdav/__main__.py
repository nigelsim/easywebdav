import sys
import os
import getopt
import urlparse
import easywebdav

def print_help():
    print """
    %(cmd)s <ops> <command> [args]

    commands:
        upload <local> <remote>     uploads the file or folder
        list <remote>               list the remote folder
        ls <remote>                 list the remote folder
        """%{'cmd':sys.argv[0]}

def connect(url):
    """Connect to the remote server and return the Client object"""
    parts = urlparse.urlparse(url)

    return easywebdav.connect(parts.hostname, username=parts.username, password=parts.password, protocol=parts.scheme, path=parts.path)

def do_list(remote):
    """Perform a listing of a folder"""
    con = connect(remote)
    for item in con.ls():
        print item

def do_upload(local, remote):
    """Upload a file or directory to a remote location"""
    con = connect(remote)
    if os.path.isfile(local):
        try:
            client.upload(local, os.path.basename(local))
            print "Uploaded OK: " + local
        except:
            print "Upload failed: " + local
            raise
    else:
        # Uploading a directory
        os.path.walk(local, _do_upload_dir, (client, local))

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
        try:
            con.upload(os.path.join(basepath, relpath, f_name), relpath + f_name)
            print "Uploaded OK: " + (relpath + f_name)
        except:
            print "Upload failed: " + (relpath + f_name)
            raise


def main():
    opts, args = getopt.getopt(sys.argv[1:], '')

    if len(args) == 0:
        print_help()
        sys.exit(1)

    cmd = args.pop(0)

    if cmd in ('ls', 'list'):
        do_list(*args)
    elif cmd in ('upload'):
        do_upload(*args)
    else:
        print "Unknown command: %s"%(cmd,)
        print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
