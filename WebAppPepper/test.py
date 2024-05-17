# -*- coding: utf-8 -*-
import unittest
import app
from mock import patch, mock_open

class TestMyApp(unittest.TestCase):
    def test_my_index__start_status(self):
        result = app.get_index()
        self.assertEqual(result, 0)

    
    def test_my_index_after_start(self):
        app.increment_index()
        result = app.get_index()
        self.assertEqual(result, 1) 

    @patch('app.open', mock_open(read_data='{"current_presentation": "TEST2"}')) #ici on utilise un mock pour simuler le champ current_presentation dans le fichier json
    def test_get_current_presentation(self):
        result = app.get_current_presentation()
        self.assertEqual(result, "TEST2") 

    def test_get_current_presentation(self):
        print(app.get_current_presentation())
        result = app.get_current_presentation()
        self.assertEqual(result, "PresentationUDM") 
    
if __name__ == '__main__':
    unittest.main()