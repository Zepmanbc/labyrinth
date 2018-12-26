#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import os
from labyrinthe.labygenerator import LabyGenerator

class Test_generator():
    DATA_FILE = LabyGenerator.DATA_FILE

    def setup(self):
        if os.path.exists(self.DATA_FILE):
            os.rename(self.DATA_FILE, self.DATA_FILE + '.bak')
        pass

    def teardown(self):
        if os.path.exists(self.DATA_FILE + '.bak'):
            os.rename(self.DATA_FILE + '.bak', self.DATA_FILE)
        pass
    
    
    def test_length_matrix(self):
        self.laby = LabyGenerator()
        code, longuest = self.laby.generate(10, 10)
        assert len(code) == 10

    def test_length_part_of_matrix(self):
        self.laby = LabyGenerator()
        code, longuest = self.laby.generate(10, 10)
        assert len(code[0]) == 10

    def test_if_DATA_FILE_exists(self):
        self.laby = LabyGenerator()
        assert os.path.exists(self.DATA_FILE) is True

    def test_read_laby_not_exists(self):
        self.laby = LabyGenerator()
        with pytest.raises(KeyError):
            self.laby.getout(5)

    def test_write_laby(self):
        self.laby = LabyGenerator()
        code, longuest = self.laby.generate(10, 10)
        self.laby.save_laby(5, code, longuest)
        assert type(self.laby.getout(5)) == type(list())
    