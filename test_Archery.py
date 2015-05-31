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
import logging

class Test_archery_a:

    def setup(self):
        import io
        import Archery

        self.Archery = Archery

        # This mock data is a copy of a real score file
        mock = (b'Computer   84MobyGamer  47Moby Game  39MobyGamer  35Moby '
                b'Game  27tiny       26rascal      1').ljust(256, b'\0')
        self.scorefile = io.BytesIO(mock)

    def teardown(self):
        self.plugin = None
        self.scorefile = None

    def test_extract_scores_from_path(self):
        """Test whether extract_scores opens the right file, given a path."""
        import os
        from unittest.mock import mock_open, patch
        with patch('builtins.open', mock_open(), create=True) as m:
            try:
                self.Archery.extract_scores("foo")
            except TypeError:
                # mock_open makes an object with a faulty read method (doing
                # read(n) returns the whole file rather than just the next n
                # bytes), so rather than try to fix that, just don't bother with
                # the actual data, and catch the error that causes.
                pass
            m.assert_called_once_with(os.path.join("foo", "ARCHERY.SCR"), 'rb')

    def test_extract_scores_from_scorepath(self):
        """Test whether extract_scores opens the scorepath given."""
        from unittest.mock import mock_open, patch
        with patch('builtins.open', mock_open(), create=True) as m:
            try:
                self.Archery.extract_scores(scorepath="foo")
            except TypeError:
                pass
            m.assert_called_once_with("foo", 'rb')

    def test_read_scores(self):
        """Test whether read_scores correctly interprets known scores."""
        correct = [
            {'score': 84, 'name': 'Computer'},
            {'score': 47, 'name': 'MobyGamer'},
            {'score': 39, 'name': 'Moby Game'},
            {'score': 35, 'name': 'MobyGamer'},
            {'score': 27, 'name': 'Moby Game'},
            {'score': 26, 'name': 'tiny'},
            {'score': 1, 'name': 'rascal'}
        ]

        actual = self.Archery.read_scores(self.scorefile)

        assert actual == correct

    def test_write_scores(self):
        """Roundtrip a score file with read_scores and write_scores."""
        scores = self.Archery.read_scores(self.scorefile)
        actual = self.Archery.write_scores(scores)

        assert actual == self.scorefile.getvalue()
