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
        from yapsy.PluginManager import PluginManager
        self.manager = PluginManager()
        self.manager.setPluginPlaces(["formats"])
        self.manager.collectPlugins()

    def teardown(self):
        self.manager = None

    def test_read_scores(self):
        import os, inspect

        correct = [
            {'score': 84, 'name': 'Computer'},
            {'score': 47, 'name': 'MobyGamer'},
            {'score': 39, 'name': 'Moby Game'},
            {'score': 35, 'name': 'MobyGamer'},
            {'score': 27, 'name': 'Moby Game'},
            {'score': 26, 'name': 'tiny'},
            {'score': 1, 'name': 'rascal'}
        ]

        plugin = self.manager.getPluginByName("Archery (DOS)").plugin_object
        
        actual = plugin.read_scores(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), "test_archery_a"))
        
        assert actual == correct

    def test_write_scores(self):
        import os, inspect

        plugin = self.manager.getPluginByName("Archery (DOS)").plugin_object

        with open (os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), "test_archery_a", "ARCHERY.SCR"), 'rb') as infile:
            correct = infile.read()
        
        scores = plugin.read_scores(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), "test_archery_a"))

        actual = plugin.write_scores(scores)
        
        assert actual == correct
