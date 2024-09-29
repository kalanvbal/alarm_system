import unittest
from datetime import datetime
from modele import Model

class test_unitaire(unittest.TestCase):

    def test_initialization(self):
        action_text = "test_action"
        model_instance = Model(action=action_text)
        
        self.assertEqual(model_instance.action, action_text)
        self.assertTrue(isinstance(datetime.strptime(model_instance.date, "%Y-%m-%d %H:%M:%S"), datetime))

    def test_afficher(self):
        action_text = "test_action"
        model_instance = Model(action=action_text)
        
        expected_output = f"{model_instance.date}, {model_instance.action} "
        self.assertEqual(model_instance.afficher(), expected_output)

if __name__ == '__main__':
    unittest.main()
