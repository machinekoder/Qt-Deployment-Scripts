#!/usr/bin/python
'''
Part of the Qt-Deployment scripts

@package qt-release
'''
import github3
import sys
import getpass
import os
import mimetypes
import re
import argparse
import ConfigParser


def printInfo(text):
    sys.stdout.write(text)
    sys.stdout.flush()


class QtRelease:
    def __init__(self):
        self.gh = None
        self.repository = None
        self.name = ''
        self.platform = ''
        self.release = None
        self.version = None
        self.releaseTag = None
        self.releaseName = ''
        self.releaseDescription = ''
        self.descriptionFile = ''
        self.prerelease = False
        self.draft = False
        self.repoUser = ''
        self.repoName = ''
        self.zipName = ''
        self.pkgName = ''
        self.pkgPattern = ''
        self.authorize = False
        self.debug = False
        self.configFile = ''
        self.credentialsFile = os.path.expanduser('~/.qt-release/github.token')

    def parseConfig(self):
        if self.debug:
            printInfo('parsing config file')

        if self.version:
            defaults = {'version': self.version}
        else:
            defaults = None
        config = ConfigParser.SafeConfigParser(defaults)
        config.read(self.configFile)
        self.name = config.get('DEFAULT', 'name').strip('"')
        try:
            if not self.version:
                self.version = config.get('DEFAULT', 'version').strip('"')
        except:
            self.version = None
        try:
            if not self.releaseTag:
                self.releaseTag = config.get('DEFAULT', 'tag').strip('"')
        except:
            self.releaseTag = None

        self.platform = config.get('Deployment', 'platform').strip('"')
        self.pkgName = os.path.expanduser(config.get('Deployment', 'pkgName').strip('"'))
        self.pkgPattern = config.get('Deployment', 'pkgPattern').strip('"')
        [self.repoUser, self.repoName] = config.get('GitHub', 'repo').strip('"').split('/')
        self.releaseName = config.get('Release', 'name').strip('"')
        self.descriptionFile = config.get('Release', 'description').strip('"')

    def parseArguments(self):
        parser = argparse.ArgumentParser(description='Component for easy release of Qt applications')
        parser.add_argument('-v', '--version', help='Version of the application', required=None)
        parser.add_argument('-t', '--tag', help='GitHub release tag', required=None)
        parser.add_argument('-dr', '--draft', help='Publish on GitHub as draft', action='store_true')
        parser.add_argument('-pr', '--prerelease', help='Publish on GitHub as pre-release', action='store_true')
        parser.add_argument('-d', '--debug', help='Whether debug output should be enabled or not', action='store_true')
        parser.add_argument('-a', '--authorize', help='Authorize the script at GitHub and generate a token', action='store_true')
        parser.add_argument('config', help='Config file', nargs='?', default=None)
        args = parser.parse_args()

        self.version = args.version
        self.releaseTag = args.tag
        self.draft = args.draft
        self.prerelease = args.prerelease
        self.debug = args.debug
        self.authorize = args.authorize
        self.configFile = args.config

        if self.debug:
            printInfo('parsed arguments')

        if not self.authorize and not self.configFile:
            printInfo('no config file specified\n')
            exit(1)

    def createVars(self):
        if self.debug:
            printInfo('creating variables')

        if (self.platform == 'windows_x86') or (self.platform == 'windows_x64'):
            self.zipName = self.pkgName + '.zip'
        elif (self.platform == 'linux_x86') or (self.platform == 'linux_x64'):
            self.zipName = self.pkgName + '.tar.gz'
        elif (self.platform == 'mac'):
            self.zipName = self.pkgName + '.dmg'
        else:
            printInfo('unknown platform\n')
            exit(1)

        self.releaseDescription = ''
        if os.path.exists(self.descriptionFile):
            f = open(self.descriptionFile)
            if f:
                self.releaseDescription = f.read()

    def createCredentials(self):
        user = raw_input('GitHub username: ')
        password = ''

        while not password:
            password = getpass.getpass('GitHub password: ')

        note = 'Qt-Deployment-Scripts'
        note_url = 'https://github.com/strahlex/Qt-Deployment-Scripts'
        scopes = ['repo']

        printInfo('requesting token...')
        auth = github3.authorize(user, password, scopes, note, note_url)

        directory = os.path.dirname(self.credentialsFile)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(self.credentialsFile, 'w') as fd:
            fd.write(auth.token + '\n')
            fd.write(str(auth.id))

        printInfo('done\n')

    def loginToGitHub(self):
        printInfo('loging in to GitHub...')

        token = ''
        with open(self.credentialsFile, 'r') as fd:
            token = fd.readline().strip()  # Can't hurt to be paranoid
        self.gh = github3.login(token=token)
        if not self.gh:
            printInfo('failed\n')
            exit(1)
        else:
            printInfo('done\n')

        self.repository = self.gh.repository(owner=self.repoUser, repository=self.repoName)
        if not self.repository:
            printInfo('Repository not found')
            exit(1)

    def getRelease(self):
        printInfo('getting release on GitHub...')

        self.release = None
        for r in self.repository.releases():
            if (r.tag_name == self.releaseTag):
                self.release = r
                printInfo('found\n')
                break

        if not self.release:
            printInfo('not found\n')
            printInfo('creating new release...')
            self.release = self.repository.create_release(tag_name=self.releaseTag,
                                                          name=self.releaseName,
                                                          body=self.releaseDescription,
                                                          draft=self.draft,
                                                          prereleae=self.prerelease)
            printInfo('done\n')

    def deleteAssets(self):
        for asset in self.release.assets():
            if re.match(self.pkgPattern, asset.name):
                printInfo('deleted ' + asset.name + '\n')
                asset.delete()

    def uploadAsset(self):
        printInfo('uploading file to GitHub...')

        if not self.release:
            raise Exception('You must first create a release')

        assetName = os.path.basename(self.zipName)
        assetType = mimetypes.guess_type(self.zipName)
        assetFile = open(self.zipName, 'r')

        asset = None
        if assetFile:
            try:
                asset = self.release.upload_asset(content_type=assetType,
                                            name=assetName,
                                            asset=assetFile)
            except:
                pass
            assetFile.close()

        if not asset:
            printInfo('uploading file failed\n')
            exit(1)

        printInfo('done\n')

    def run(self):
        self.parseArguments()
        if self.authorize:
            self.createCredentials()
        else:
            self.parseConfig()
            self.createVars()
            self.loginToGitHub()
            self.getRelease()
            self.deleteAssets()
            self.uploadAsset()


release = QtRelease()
release.run()
