"""
    This file contains test cases for pokemon_base.py.
    This file is provided in template.
    Additional test cases for pokemon_base methods are in test_shared_methods.py

"""

from random_gen import RandomGen
from pokemon_base import PokemonBase, PokeType
from pokemon import Eevee, Gastly, Haunter
from tests.base_test import BaseTest

class TestPokemonBase(BaseTest):
    """Class containing test cases for methods in pokemon base provided in template"""
    def test_cannot_init(self):
        """Tests that we cannot initialise PokemonBase, and that it raises the correct error."""
        self.assertRaises(TypeError, lambda: PokemonBase(30, PokeType.FIRE))

    def test_level(self):
        """Test case for getting level and level up mechanics on Eevee"""
        e = Eevee()
        self.assertEqual(e.get_level(), 1)
        e.level_up()
        self.assertEqual(e.get_level(), 2)
    
    def test_hp(self):
        """Test case for getting current hp and losing hp mechanics on Eevee"""
        e = Eevee()
        self.assertEqual(e.get_hp(), 10)
        e.lose_hp(4)
        self.assertEqual(e.get_hp(), 6)
        e.heal()
        self.assertEqual(e.get_hp(), 10)

    def test_status(self):
        """Test case for setting status and status effect implementation on Eevees"""
        RandomGen.set_seed(0)
        e1 = Eevee()
        e2 = Eevee()
        e1.attack(e2)
        # e2 now is confused.
        e2.attack(e1)
        # e2 takes damage in confusion.
        self.assertEqual(e1.get_hp(), 10)

    def test_evolution(self):
        """Test case for getting evolved pokemon for Gastly"""
        g = Gastly()
        self.assertEqual(g.can_evolve(), True)
        self.assertEqual(g.should_evolve(), True)
        new_g = g.get_evolved_version()
        self.assertIsInstance(new_g, Haunter)
