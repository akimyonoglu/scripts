#!/usr/bin/python
# ---------------------------------------------------------------------------
# common_prefix.py - Returns the common prefix of the arguments

# Copyright 2014, Armagan Kimyonoglu <akimyonoglu@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License at <http://www.gnu.org/licenses/> for
# more details.

# Usage: ./common_prefix.py asd asde a -> a
# ---------------------------------------------------------------------------

import sys


def usage():
    print "Usage: ./common_prefix.py asd asde a -> a"


def common_prefix(*args):
    """
    Returns the common prefix of the arguments
    """
    if len(args) < 1:
        usage()
    common_prefix = args[0]
    for arg in args[1:]:
        if common_prefix == "":
            break
        length = min(len(common_prefix), len(arg))
        common_prefix = common_prefix[:length]
        for i in range(0, length):
            if common_prefix[i] != arg[i]:
                common_prefix = arg[:i]
                break
    return common_prefix


def main(args):
    print common_prefix(*args[1:])

if __name__ == "__main__":
    main(sys.argv)
