#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from labyrinthe.window import Window

class Test_window():

    def setup(self):
        pass

    def teardown(self):
        pass
    
    def test_init(self):
        new = Window()
        assert new.window.get_size() == (640,480)
        
