import sys
import os
import getopt
import urlparse
import easywebdav

def print_help():
    print """
    %(cmd)s [opts] <command> [args]

    opts:
        -i                          disable verifing SSL (insecure)

    commands:
        upload <local> <remote>     uploads the file or folder
        list <remote>               list the remote folder
        ls <remote>                 list the remote folder

    Examples:
        %(cmd)s -i list https://username:password@myserver.com/path
        """%{'cmd':sys.argv[0]}

def connect(url, verify_ssl=True):
    """Connect to the remote server and return the Client object"""
    parts = urlparse.urlparse(url)

    return easywebdav.connect(parts.hostname, username=parts.username, \
                        password=parts.password, protocol=parts.scheme, \
                        path=parts.path, verify_ssl=verify_ssl)

def do_list(remote, verify_ssl):
    """Perform a listing of a folder"""
    con = connect(remote, verify_ssl)
    for item in con.ls():
        print item

def do_upload(local, remote, verify_ssl):
    """Upload a file or directory to a remote location"""
    con = connect(remote, verify_ssl)
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
    opts, args = getopt.getopt(sys.argv[1:], 'i')

    verify_ssl = True
    for k,v in opts:
        if k == '-i':
            verify_ssl = False

    if len(args) == 0:
        print_help()
        sys.exit(1)

    cmd = args.pop(0)

    if cmd in ('ls', 'list'):
        do_list(*args, verify_ssl=verify_ssl)
    elif cmd in ('upload'):
        do_upload(*args, verify_ssl=verify_ssl)
    else:
        print "Unknown command: %s"%(cmd,)
        print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
