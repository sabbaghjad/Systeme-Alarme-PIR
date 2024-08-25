import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import patch, Mock
from controleur import Controleur


class TestCheckSensor(unittest.TestCase):
    @patch('controleur.time.sleep', return_value=None)
    def test_check_sensor(self, mock_sleep):
        mock_module = Mock()
        mock_vue = Mock()
        controleur = Controleur(mock_module, mock_vue)
        controleur.pir = Mock()
        controleur.detecter_mouvement = Mock()
        controleur.detecter = True
        
        controleur.pir.value = 1
        controleur.check_sensor()
        
        controleur.detecter_mouvement.assert_called_once()
    

    
    @patch('controleur.time.sleep', return_value=None)
    def test_check_sensor_no_movement(self, mock_sleep):
        mock_module = Mock()
        mock_vue = Mock()
        controleur = Controleur(mock_module, mock_vue)
        controleur.pir = Mock()
        controleur.detecter_mouvement = Mock()
        controleur.detecter = False
        
        controleur.pir.value = 0
        controleur.check_sensor()
        
        controleur.detecter_mouvement.assert_not_called()
        
if __name__ == '__main__':
    unittest.main()