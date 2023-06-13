"""
    This file contains test cases for pokemon.py.
    This file is provided in template.
    Additional test cases for pokemon class' shared methods are in test_shared_methods.py

"""

from pokemon import Venusaur
from tests.base_test import BaseTest

class TestPokemon(BaseTest):
    """Class containing test case for methods and attributes for Pokemon provided by template"""
    def test_venusaur_stats(self):
        """Test case for getting statistics for Venusaur after levelling up and losing hp in string format"""
        v = Venusaur()
        self.assertEqual(v.get_hp(), 21)
        self.assertEqual(v.get_level(), 2)
        self.assertEqual(v.get_attack_damage(), 5)
        self.assertEqual(v.get_speed(), 4)
        self.assertEqual(v.get_defence(), 10)
        v.level_up()
        v.level_up()
        v.level_up()
        self.assertEqual(v.get_hp(), 22)
        self.assertEqual(v.get_level(), 5)
        self.assertEqual(v.get_attack_damage(), 5)
        self.assertEqual(v.get_speed(), 5)
        self.assertEqual(v.get_defence(), 10)
        v.lose_hp(5)

        self.assertEqual(str(v), "LV. 5 Venusaur: 17 HP")
