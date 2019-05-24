from pathlib import Path
from unittest import TestCase, main
from make_variables import MakeVariables


class VariablesSetUp(TestCase):
    def setUp(self):
        self.test_obj = MakeVariables('HTI', 2012)

    def test_object_instantiated(self):
        self.assertEqual(self.test_obj.country, 'HTI')
        self.assertEqual(self.test_obj.year, 2012)

    def test_correct_extent_selected(self):
        self.assertFalse(self.test_obj.extent == '75N060W')
        self.assertEqual(self.test_obj.extent, '75N180W')

    def test_key_error_raised(self):
        self.assertRaises(Exception, MakeVariables, 'BOX', 2000)

    def test_base_set(self):
        self.assertEqual(self.test_obj.BASEDIR, Path(__file__).resolve().parent.parent)

    

if __name__ == "__main__":
    main()