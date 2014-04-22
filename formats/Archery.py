# Classic Game Resource Reader (CGRR): Parse resources from classic games.
# Copyright (C) 2014  Tracy Poff
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
import logging
import struct
import os

import yapsy

import utilities
from utilities import File, FileReader

class Archery(yapsy.IPlugin.IPlugin):
    """Parses Archery files."""
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

    @staticmethod
    def verify(path):
        """Verifies that the provided path is the supported game."""
        return utilities.verify(Archery.identifying_files, path)

    @staticmethod
    def read_scores(path):
        """Reads high score table."""
        scores = []
        with open(os.path.join(path, Archery.scorefile), "rb") as scorefile:
            for data in iter(lambda: scorefile.read(Archery.score_reader.struct.size), b"\0"*13):
                scores.append(Archery.score_reader.unpack(data))
        return scores

    @staticmethod
    def write_scores(scores):
        """Return a bytestring representing a scorefile containing scores."""
        data = bytes()
        for score in scores:
            data += Archery.score_reader.pack(score)
            logging.debug(data)
        return data.ljust(256, b"\0")
