Qt-Deployment-Scripts
=====================

Python scripts for deploying Qt applications to GitHub. This blog entry [Deploying Qt](http://www.tripleboot.org/?p=138) will help you specifying the correct dependencies.

## Install
To install the deployment scripts in Linux run

    sudo make install

## Examples
For up-to-date examples please take a look at the deployment scripts for [MachinekitClient and BBIOConfig](https://github.com/machinekoder/deployment-scripts).

## qt-deploy.py
This script can be used to deploy compiles Qt applications directly to GitHub. Example configurations can be found in the *examples* folder.

    usage: qt-deploy.py [-h] [-v VERSION] [-u USER] [-p PASSWORD] [-dr DRAFT]
                    [-pr PRERELEASE] [-t TAG] [--deploy] [--publish]
                    [--unpublish] [--clean] [-d]
                    [config]

    Component for easy deployment of Qt applications
    
    positional arguments:
      config                Config file
    
    optional arguments:
      -h, --help            show this help message and exit
      -v VERSION, --version VERSION
                            Version of the application
      -u USER, --user USER  GitHub user name
      -p PASSWORD, --password PASSWORD
                            GitHub password
      -dr DRAFT, --draft DRAFT
                            Publish on GitHub as draft
      -pr PRERELEASE, --prerelease PRERELEASE
                            Publish on GitHub as pre-release
      -t TAG, --tag TAG     Git tag of the release
      --deploy              Deploy the application to the output directory
      --publish             Upload the application to GitHub
      --unpublish           Remove the release from GitHub
      --clean               Cleanup the created files afterwards
      -d, --debug           Whether debug output should be enabled or not
