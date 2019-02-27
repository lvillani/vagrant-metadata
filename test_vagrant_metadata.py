# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2019 Lorenzo Villani
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import json
import os
import os.path

import pytest

import vagrant_metadata as v


TEST_METADATA = {
    "baseurl": "http://example.com",
    "name": "hashicorp/precise64",
    "description": "This box contains Ubuntu 12.04 LTS 64-bit.",
    "versions": [{
        "version": "1.0.0",
        "providers": [{
            "name": "virtualbox",
            "url": "http://example.com/1.0.0/virtualbox/precise64_virtualbox.box",
            "checksum_type": "sha1",
            "checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
        },
        {
            "name": "vmware_desktop",
            "url": "http://example.com/1.0.0/vmware_desktop/precise64_vmware_desktop.box",
            "checksum_type": "sha1",
            "checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
        }]
    },
    {
        "version": "2.0.0",
        "providers": [{
            "name": "virtualbox",
            "url": "http://example.com/2.0.0/virtualbox/precise64_virtualbox.box",
            "checksum_type": "sha1",
            "checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
        },
        {
            "name": "vmware_desktop",
            "url": "http://example.com/2.0.0/vmware_desktop/precise64_vmware_desktop.box",
            "checksum_type": "sha1",
            "checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
        }]
    }]
}


def test_compute_sha1():
    assert v.compute_sha1("logo.svg") == "11800525056bdcacf47cfa9e9d40d0e28e07b23f"


def test_all_directories_in(boxtree):
    assert v.all_directories_in(boxtree['box_empty']) == []
    assert v.all_directories_in(boxtree['box_one']) == []
    assert v.all_directories_in(boxtree['box_dir']) == [os.path.join(boxtree['box_dir'], 'test.box')]

    dirs = sorted(v.all_directories_in(boxtree['root']))
    expected = [os.path.join(boxtree['root'], d) for d in ['box_dir', 'box_empty', 'box_multi', 'box_one']]

    assert dirs == expected


def test_box_in(boxtree):
    assert v.box_in(boxtree['box_one']) == os.path.join(boxtree['box_one'], 'test.box')


def test_box_in_no_boxes(boxtree):
    with pytest.raises(v.BoxCountError):
        v.box_in(boxtree['box_empty'])

    with pytest.raises(v.BoxCountError):
        v.box_in(boxtree['box_multi'])


@pytest.fixture
def boxtree(tmpdir):
    """Creates a test directory tree.

    The tree contains directories with and without (empty) '.box' files. Returns a dictionary
    which map to the full path of the temporary directory tree.

    """
    # Create several test directories, each containing a variable number of (empty) '.box' files.
    box_empty = makedirs(os.path.join(str(tmpdir), 'box_empty'))
    box_multi = makedirs(os.path.join(str(tmpdir), 'box_multi'))
    box_one = makedirs(os.path.join(str(tmpdir), 'box_one'))

    touch(os.path.join(box_one, 'test.box'))
    touch(os.path.join(box_multi, 'test1.box'))
    touch(os.path.join(box_multi, 'test2.box'))

    # Create a '.box' directory instead of a file.
    box_dir = makedirs(os.path.join(str(tmpdir), 'box_dir'))

    makedirs(os.path.join(box_dir, 'test.box'))

    return {
        'root': str(tmpdir),
        'box_dir': box_dir,
        'box_empty': box_empty,
        'box_multi': box_multi,
        'box_one': box_one,
    }


def test_find_in_collection():
    collection = [
        {
            "pkey": "a value",
            "data": "Satellite data",
        },
        {
            "pkey": "another value",
            "data": "Satellite data",
        },
    ]

    default = {"pkey": "default when missing"}

    assert v.find_in_collection(collection, "pkey", "a value", default) == {"pkey": "a value", "data": "Satellite data"}
    assert v.find_in_collection(collection, "pkey", "missing", default) == default


def test_get_version_data():
    assert v.get_version_data("bogus", TEST_METADATA) == {
        "version": "bogus",
        "providers": [],
    }

    assert v.get_version_data("1.0.0", TEST_METADATA) == {
        "version": "1.0.0",
        "providers": [{
            "name": "virtualbox",
            "url": "http://example.com/1.0.0/virtualbox/precise64_virtualbox.box",
            "checksum_type": "sha1",
            "checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
        },
        {
            "name": "vmware_desktop",
            "url": "http://example.com/1.0.0/vmware_desktop/precise64_vmware_desktop.box",
            "checksum_type": "sha1",
            "checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
        }]
    }


def test_get_provider_data():
    version_data = v.get_version_data("1.0.0", TEST_METADATA)

    assert v.get_provider_data("kvm", version_data) == {
        "name": "kvm",
        "checksum_type": "sha1",
        "checksum": "",
        "url": "",
    }

    assert v.get_provider_data("virtualbox", version_data) == {
        "name": "virtualbox",
        "url": "http://example.com/1.0.0/virtualbox/precise64_virtualbox.box",
        "checksum_type": "sha1",
        "checksum": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
    }


def test_process_directory(mktesttree):
    # Initial metadata
    metadata = {
        "baseurl": "http://example.com",
        "name": "hashicorp/precise64",
        "description": "This box contains Ubuntu 12.04 LTS 64-bit.",
        "versions": [],
    }

    # This is how we expect the metadata dictionary to look after calls to process_directory
    # (i.e.: it should be untouched)
    metadata_expected = {
        "baseurl": "http://example.com",
        "name": "hashicorp/precise64",
        "description": "This box contains Ubuntu 12.04 LTS 64-bit.",
        "versions": [],
    }

    new_metadata = v.process_directory(mktesttree, metadata)
    new_metadata_force = v.process_directory(mktesttree, new_metadata, True)

    assert metadata == metadata_expected
    assert new_metadata == TEST_METADATA
    assert new_metadata_force == TEST_METADATA


@pytest.fixture
def mktesttree(tmpdir):
    """Creates a test tree with two versions and two box providers."""
    root = str(tmpdir)

    for v in ["1.0.0", "2.0.0"]:
        version = makedirs(os.path.join(root, v))
        version_virtualbox = makedirs(os.path.join(version, "virtualbox"))
        version_virtualbox_box = touch(os.path.join(version_virtualbox, "precise64_virtualbox.box"))
        version_vmware_desktop = makedirs(os.path.join(version, "vmware_desktop"))
        version_vmware_desktop_box = touch(os.path.join(version_vmware_desktop, "precise64_vmware_desktop.box"))

    return root

#
# Utility functions
#

def print_dict(d):
    import pprint
    pprint.pprint(json.loads(json.dumps(d)))


def makedirs(path):
    """Like `os.makedirs` but also returns the given path."""
    os.makedirs(path)

    return path


def touch(path):
    """Creates an empty file (if missing) and updates its timestamp."""
    with open(path, 'w'):
        os.utime(path, None)
