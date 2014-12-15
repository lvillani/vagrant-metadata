# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2014 Lorenzo Villani
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

import collections
import hashlib
import os
import os.path
from os.path import join


class BoxCountError(Exception):
    pass


def process_directory(root, metadata, force=False):
    """Processes all boxes in the given directory.

    The initial metadata should either be loaded from an existing `metadata.json` file or,
    alternatively, seeded from command line arguments (or whatever, as long as it contains "name",
    "description" and "baseurl" keys).

    This function does update `metadata` in place but instead returns a new dictionary with the
    new fields.

    """
    ret = collections.OrderedDict([
        ("name", metadata["name"]),
        ("description", metadata["description"]),
        ("baseurl", metadata["baseurl"]),
        ("versions", []),
    ])

    for version_dir in sorted(all_directories_in(root)):
        version = os.path.basename(version_dir)
        version_data = get_version_data(version, metadata)
        version_ret = get_version_data(version, ret)

        for provider_dir in sorted(all_directories_in(version_dir)):
            box = box_in(provider_dir)
            provider = os.path.basename(provider_dir)
            provider_data = get_provider_data(provider, version_data).copy()

            if not provider_data["checksum"] and not force:
                provider_data["checksum"] = compute_sha1(box)
                provider_data["url"] = "%s/%s" % (metadata["baseurl"], os.path.relpath(box, root))

            version_ret["providers"].append(provider_data)

        ret["versions"].append(version_ret)

    return ret


def all_directories_in(path):
    return [join(path, d) for d in os.listdir(path) if os.path.isdir(join(path, d))]


def box_in(path):
    boxes = [join(path, f) for f in os.listdir(path) if f.endswith(".box") and os.path.isfile(join(path, f))]

    if len(boxes) != 1:
        raise BoxCountError("Was expecting exactly one box: %s" % path)
    else:
        return boxes[0]


def get_version_data(want_version, metadata):
    return find_in_collection(metadata["versions"], "version", want_version, collections.OrderedDict([
        ("version", want_version),
        ("providers", []),
    ]))


def get_provider_data(want_provider, version_data):
    return find_in_collection(version_data["providers"], "name", want_provider, collections.OrderedDict([
        ("name", want_provider),
        ("checksum_type", "sha1"),
        ("checksum", ""),
        ("url", ""),
    ]))


def find_in_collection(collection, primary_key, where, default):
    for item in collection:
        if item[primary_key] == where:
            return item
    else:
        return default


def compute_sha1(path):
    algo = hashlib.sha1()

    with open(path, 'rb') as f:
        buf = f.read(algo.block_size)

        while len(buf):
            algo.update(buf)

            buf = f.read(algo.block_size)

    return algo.hexdigest()
