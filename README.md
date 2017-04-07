# vagrant-metadata

<img src="https://rawgit.com/lvillani/vagrant-metadata/master/logo.svg" align="right" width="200" height="200"/>

_Creates and updates Vagrant box metadata files (metadata.json)_

[![Build Status](https://img.shields.io/travis/lvillani/vagrant-metadata.svg?style=flat)](https://travis-ci.org/lvillani/vagrant-metadata)
[![Coverage Status](http://img.shields.io/coveralls/lvillani/vagrant-metadata.svg?style=flat)](https://coveralls.io/r/lvillani/vagrant-metadata)
[![License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://choosealicense.com/licenses/mit/)

--------------------------------------------------------------------------------

An utility program which creates and updates Vagrant
[box metadata files](http://docs.vagrantup.com/v2/boxes/format.html). This program is meant for
small-scale deployment and versioning of Vagrant base boxes to private servers. For large scale
deployment it always better to just use [Atlas](https://atlas.hashicorp.com/).


## Usage

### Installation

This program requires Python 2.7 and can be installed via PIP:

    pip install vagrant-metadata


### Publishing Your First Box

Now, let's suppose you have a base box called `precise64` in two flavors: one for Virtualbox and
the other for VMWare. `vagrant-metadata` follows the "convention over configuration" principle and
it expects a certain directory layout to do its magic. Let's start by creating the required
directory structure:

    mkdir -p precise64/1.0.0/virtualbox
    mkdir -p precise64/1.0.0/vmware_desktop

At this point you should have a directory tree like this:

    .
    └── precise64
        └── 1.0.0
            ├── virtualbox
            └── vmware_desktop

Now you should copy your boxes to their appropriate directory and end up with something like this:

    .
    └── precise64
        └── 1.0.0
            ├── virtualbox
            │   └── precise64.box
            └── vmware_desktop
                └── precise64.box

Now let's go into the `precise64` directory:

    cd precise64

Since this is the first time we run `vagrant-metadata` we'll have to tell it something about the
base box such as its URL, name and description:

    vagrant-metadata --name="lvillani/precise64" --description="Ubuntu 12.04 64-bit" \
        --baseurl="http://lorenzo.villani.me/vagrant/precise64"

After a while, when `vagrant-metadata` exits, you will find a fresh `metadata.json` file which
contains all the box metadata. At this point you can publish the whole `precise64` directory
somewhere.


### Updating a Box

Updating a box is easier than preparing a new one for publication. Let's suppose we want to
publish version `2.0.0` of the `precise64` box described before: create a new `2.0.0` directory
with the same layout as before and copy your boxes there ending up with something like:

    .
    └── precise64
        ├── 1.0.0
        │   ├── virtualbox
        │   │   └── precise64.box
        │   └── vmware_desktop
        │       └── precise64.box
        ├── 2.0.0
        │   ├── virtualbox
        │   │   └── precise64.box
        │   └── vmware_desktop
        │       └── precise64.box
        └── metadata.json

At this point go to the `precise64` directory and run `vagrant-metadata`:

    cd precise64
    vagrant-metadata

Notice that we don't even have to specify the box name, description or base URL.

Sync this directory with your remote server and you are done.

If you don't have all box files downloaded locally, and want to add new version
to existing metadata.json simply add `--append` (`-a`) option to only add new
version box to existing metadata
