# -*- coding: utf-8 -*-
import unittest
import app
from unittest.mock import patch



class TestMyApp(unittest.TestCase):
    @patch('app.get_index', return_value=1)
    def test_my_index_after_start(self, get_index):
        app.start_presentation()
        result = app.get_index()
        self.assertEqual(result, 1)  # replace expected_result with the value you expect


    
if __name__ == '__main__':
    unittest.main()