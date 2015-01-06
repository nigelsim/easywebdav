EasyWebDAV: A WebDAV Client in Python
=====================================

Features
--------

* Basic authentication
* Creating directories, removing directories and files
* Uploading and downloading files
* Directory listing
* Support for client side SSL certificates

Installation
------------

Install using distribute:

    easy_install easywebdav

Quick Start
-----------

    import easywebdav
    # Start off by creating a client object. Username and
    # password may be omitted if no authentication is needed.
    webdav = easywebdav.connect('webdav.your-domain.com', username='myuser', password='mypass')
    # Do some stuff:
    webdav.mkdir('some_dir')
    webdav.rmdir('another_dir')
    webdav.download('remote/path/to/file', 'local/target/file')
    webdav.upload('local/path/to/file', 'remote/target/file')

Client object API
-----------------

The API is pretty much self-explanatory:

    cd(path)
    ls(path=None)
    exists(remote_path)
    mkdir(path, safe=False)
    mkdirs(path)
    rmdir(path, safe=False)
    delete(file_path)
    upload(local_path_or_fileobj, remote_path)
    download(remote_path, local_path_or_fileobj)

Using clientside SSL certificate
--------------------------------

    webdav = easywebdav.connect('secure.example.net',
                                username='user',
                                password='pass',
                                protocol='https',
                                cert="/path/to/your/certificate.pem")
    # Do some stuff:
    print webdav.ls()

Please note that all options and restriction regarding the "cert" parameter from
[Requests API](http://docs.python-requests.org/en/latest/api/) apply here as the parameter is only passed through!

Developing EasyWebDAV
---------------------

Working with a virtual environment is highly recommended:

    virtualenv --no-site-packages easywebdav_dev
    source easywebdav_dev/bin/activate

Installing the library in development-mode:

    EASYWEBDAV_DEV=1 python setup.py develop

The first part of the command causes setup.py to install development dependencies, in addition to the normal dependencies.

Running the tests:

    nosetests --with-yanc --nologcapture --nocapture tests

Running the tests with WebDAV server logs:

    WEBDAV_LOGS=1 nosetests --with-yanc --nologcapture --nocapture -v tests

Command Line Usage
------------------

You can invoke the command line client either by calling teh easywebdav module:

    python -m easywebdav [opts] <command> [args]

or by using the entry point script that will be created when you install the library:

    easywebdav [opts] <command> [args]

CLI usage is as follows:

    easywebdav [opts] <command> [args]

    ops:
        -i                          disable verifing SSL (insecure)

    commands:
        upload <local> <remote>     uploads the file or folder
        list <remote>               list the remote folder
        ls <remote>                 list the remote folder

    Examples:
        easywebdav -i list https://username:password@myserver.com/path
