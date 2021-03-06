# Classic Game Resource Reader (CGRR): Parse resources from classic games.
# Copyright (C) 2014-2015  Tracy Poff
#
# This file is part of CGRR.
#
# CGRR is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CGRR is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CGRR.  If not, see <http://www.gnu.org/licenses/>.
"""Parses Archery files."""
import os

import cgrr
from cgrr import File, FileReader

key = "archery_a"
title = "Archery"
developer = "Brian Blankenship"
description = "Archery (DOS)"

identifying_files = [
    File("ARCHERY.EXE", 31616,  "d8fae202edcc48d51a72026cbfbe7fa8"),
]

scorefile = "ARCHERY.SCR"

score_reader = FileReader(
    format = [
        ("name", "9s"),
        ("score", "4s"),
    ],
    massage_in = {
        "name"  : (lambda s: s.decode('ascii').strip()),
        "score" : (lambda s: int(s.decode('ascii'))),
    },
    massage_out = {
        "name"  : (lambda s: s.ljust(9).encode('ascii')),
        "score" : (lambda s: str(s).rjust(4).encode('ascii')),
    },
)

def verify(path):
    """Verifies that the provided path is the supported game."""
    return cgrr.verify(identifying_files, path)

def extract_scores(path=None, scorepath=None):
    if not (path or scorepath):
        raise ValueError("Either path or scorefile must be specified.")
    elif (path and scorepath):
        raise ValueError("Only one of path or scorefile may be specified.")
    if not scorepath:
        scorepath = os.path.join(path, scorefile)
    with open(scorepath, "rb") as sfile:
        scores = read_scores(sfile)
    return scores

def read_scores(scorefile):
    """Reads high score table."""
    scores = []
    for data in iter(lambda: scorefile.read(score_reader.struct.size), b"\0"*13):
        scores.append(score_reader.unpack(data))
    return scores

def write_scores(scores):
    """Return a bytestring representing a scorefile containing scores."""
    data = bytes()
    for score in scores:
        data += score_reader.pack(score)
    return data.ljust(256, b"\0") # null pad to 256 bytes
