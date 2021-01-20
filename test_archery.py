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
import pytest

class Test_archery_a:

    def setup(self):
        import io
        import archery

        self.archery = archery

        # This mock data is a copy of a real score file
        mock = (b'Computer   84MobyGamer  47Moby Game  39MobyGamer  35Moby '
                b'Game  27tiny       26rascal      1').ljust(256, b'\0')
        self.scorefile = io.BytesIO(mock)

        self.correct = [
            {'score': 84, 'name': 'Computer'},
            {'score': 47, 'name': 'MobyGamer'},
            {'score': 39, 'name': 'Moby Game'},
            {'score': 35, 'name': 'MobyGamer'},
            {'score': 27, 'name': 'Moby Game'},
            {'score': 26, 'name': 'tiny'},
            {'score': 1, 'name': 'rascal'}
        ]


    def teardown(self):
        self.plugin = None
        self.scorefile = None

    def test_extract_scores_from_path(self):
        """Test whether extract_scores opens the right file, given a path."""
        import os
        from unittest.mock import mock_open, patch
        with patch('builtins.open',
                   mock_open(read_data=self.scorefile.getvalue()),
                   create=True) as m:
            scores = self.archery.extract_scores("foo")
            m.assert_called_once_with(os.path.join("foo", "ARCHERY.SCR"), 'rb')

        assert scores == self.correct

    def test_extract_scores_from_scorepath(self):
        """Test whether extract_scores opens the scorepath given."""
        from unittest.mock import mock_open, patch
        with patch('builtins.open',
                   mock_open(read_data=self.scorefile.getvalue()),
                   create=True) as m:
            scores = self.archery.extract_scores(scorepath="foo")
            m.assert_called_once_with("foo", 'rb')

        assert scores == self.correct

    def test_read_scores(self):
        """Test whether read_scores correctly interprets known scores."""

        actual = self.archery.read_scores(self.scorefile)

        assert actual == self.correct

    def test_write_scores(self):
        """Roundtrip a score file with read_scores and write_scores."""
        scores = self.archery.read_scores(self.scorefile)
        actual = self.archery.write_scores(scores)

        assert actual == self.scorefile.getvalue()

    def test_extract_scores_without_path(self):
        with pytest.raises(ValueError) as e:
            self.archery.extract_scores()

        assert str(e.value) == "Either path or scorefile must be specified."

    def test_extract_scores_with_path_and_scorepath(self):
        with pytest.raises(ValueError) as e:
            self.archery.extract_scores(path='foo', scorepath='bar')

        assert str(e.value) == "Only one of path or scorefile may be specified."
