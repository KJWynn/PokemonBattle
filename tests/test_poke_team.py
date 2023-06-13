"""
This file includes test cases added for testing methods in poke_team.py module alongside the provided tests in the original template.
Methods to be tested: __init__, random_team, return_pokemon, retrieve_pokemon, special, regenerate_team, is_empty, choose_battle_option

"""
__author__ = "Scaffold by Jackson Goerner, Code by Khor Jia Wynn"

from battle import Battle
from poke_team import Action, BM2SortedList, Criterion, PokeTeam
from queue_adt import CircularQueue
from random_gen import RandomGen
from pokemon import Bulbasaur, Charmander, Gastly, Squirtle, Eevee
from sorted_list import ListItem
from tests.base_test import BaseTest


class TestPokeTeam(BaseTest):
    """Class containing test cases provided in template"""
    def test_random(self):
        """Test random team generation"""
        RandomGen.set_seed(123456789)
        t = PokeTeam.random_team("Cynthia", 0)
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Squirtle, Gastly, Eevee, Eevee, Eevee, Eevee]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_regen_team(self):
        """Test regeneration of team generated randomly"""
        RandomGen.set_seed(123456789)
        t = PokeTeam.random_team("Cynthia", 2, team_size=4, criterion=Criterion.HP)
        # This should end, since all pokemon are fainted, slowly.
        while not t.is_empty():
            p = t.retrieve_pokemon()
            p.lose_hp(1)
            t.return_pokemon(p)
        t.regenerate_team()
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Bulbasaur, Eevee, Charmander, Gastly]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_battle_option_attack(self):
        """Test choose battle option method by PokeTeam with ai mode that always chooses attack option"""
        t = PokeTeam("Wallace", [1, 0, 0, 0, 0], 1, PokeTeam.AI.ALWAYS_ATTACK)
        p = t.retrieve_pokemon()
        e = Eevee()
        self.assertEqual(t.choose_battle_option(p, e), Action.ATTACK)

    def test_special_mode_1(self):
        """Test case for implementation of special mode for PokeTeam with battle mode 1"""
        t = PokeTeam("Lance", [1, 1, 1, 1, 1], 1, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        # C B S G E
        t.special()
        # S G E B C
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Squirtle, Gastly, Eevee, Bulbasaur, Charmander]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_string(self):
        """Test case for string representation of teams"""
        t = PokeTeam("Dawn", [1, 1, 1, 1, 1], 2, PokeTeam.AI.RANDOM, Criterion.DEF)
        self.assertEqual(str(t), "Dawn (2): [LV. 1 Gastly: 6 HP, LV. 1 Squirtle: 11 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Eevee: 10 HP, LV. 1 Charmander: 9 HP]")


class TestInit(BaseTest):
    """Tests arguments and poketeam ADT for __init__ of PokeTeam class"""

    def test_team_name(self):
        """Tests that correct error is raised when invalid team_name passed"""
        team_name = 4
        self.assertRaises(ValueError, lambda: PokeTeam(team_name, [1, 1, 1, 1, 1], 1, PokeTeam.AI.ALWAYS_ATTACK))

    def test_team_numbers(self):
        """Tests that correct error is raised when invalid team_numbers passed"""
        team_numbers = [1, 2, "4", 4, 1]
        self.assertRaises(ValueError, lambda: PokeTeam("John", team_numbers, 1, PokeTeam.AI.ALWAYS_ATTACK))

    def test_battle_mode(self):
        """Tests that correct error raised when invalid battle mode passed"""
        battle_mode = 3
        self.assertRaises(ValueError, lambda: PokeTeam("Jane", [1, 1, 1, 1, 1], battle_mode, PokeTeam.AI.ALWAYS_ATTACK))

    def test_ai_type(self):
        """Tests that correct error raised when invalid ai_type passed"""
        ai_type = "ALWAYS_ATTACK"
        self.assertRaises(ValueError, lambda: PokeTeam("John", [1, 1, 1, 1, 1], 3, ai_type))

    def test_criterion(self):
        """Tests that correct error raised when invalid criterion passed"""
        crit = "LV"
        self.assertRaises(ValueError, lambda: PokeTeam("Jane", [1, 1, 1, 1, 1], 2, PokeTeam.AI.ALWAYS_ATTACK, crit))

    def test_criterion_value(self):
        """Tests that correct error raised when invalid criterion_value passed"""
        crit_value = "6" 
        self.assertRaises(ValueError, lambda: PokeTeam("John", [1, 1, 1, 1, 1], 2, PokeTeam.AI.ALWAYS_ATTACK, Criterion.DEF, crit_value))

    def test_bm2_no_criterion(self):
        """Tests that correct error raised when no criterion passed for battle mode 2"""
        battle_mode = 2
        criterion = None
        self.assertRaises(ValueError, lambda: PokeTeam("Jane", [1, 1, 1, 1, 1], battle_mode, PokeTeam.AI.ALWAYS_ATTACK, criterion))

    def test_pokeTeamMembers_2(self):
        """Tests that pokeTeamMembers generated correctly"""
        t = PokeTeam("John", [1, 1, 1, 1, 1], 2, PokeTeam.AI.ALWAYS_ATTACK, Criterion.DEF)
        self.assertIsInstance(t.pokeTeamMembers, BM2SortedList)
        items = [item for item in t.pokeTeamMembers]
        expected_elems = [ListItem] * len(t.pokeTeamMembers)
        for item, elem in zip(items, expected_elems):
            self.assertIsInstance(item, elem)
        pokemon = [poke.value for poke in t.pokeTeamMembers]
        expected_classes = [Gastly, Squirtle, Bulbasaur, Eevee, Charmander]
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

    def test_pokeTeamMembers_0(self):
        """Tests that pokeTeamMembers generated correctly"""
        t = PokeTeam("John", [1, 1, 1, 1, 1], 0, PokeTeam.AI.ALWAYS_ATTACK)
        self.assertIsInstance(t.pokeTeamMembers, CircularQueue)
        items = []
        while not t.pokeTeamMembers.is_empty():
            item = t.pokeTeamMembers.serve()
            items.append(item)
        expected_elems = [ListItem] * len(t.pokeTeamMembers)
        for item, elem in zip(items, expected_elems):
            self.assertIsInstance(item, elem)

        pokemon = [poke.value for poke in items]
        expected_classes = [Charmander, Bulbasaur, Squirtle, Gastly, Eevee]
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)

class TestRandomTeam(BaseTest):
    """Test for 3 battle modes for random team generation"""

    def test_random_bm0(self):
        """Test for battle mode 0"""
        RandomGen.set_seed(123456789)
        t = PokeTeam.random_team("Jane", 0)
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Squirtle, Gastly, Eevee, Eevee, Eevee, Eevee]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)
        
    def test_random_bm1(self):
        """Test for battle mode 1"""
        RandomGen.set_seed(123456789)
        t = PokeTeam.random_team("Jane", 1, 6, PokeTeam.AI.RANDOM)
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Bulbasaur, Squirtle, Gastly, Eevee, Eevee, Eevee]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)    

    def test_random_bm2(self):
        """Test for battle mode 2"""
        RandomGen.set_seed(123456789) 
        t = PokeTeam.random_team("Jen", 2, 6, PokeTeam.AI.RANDOM, criterion = Criterion.HP) 
        pokemon = []
        while not t.is_empty():
            pokemon.append(t.retrieve_pokemon())
        expected_classes = [Bulbasaur, Squirtle, Eevee, Eevee, Eevee, Gastly]
        self.assertEqual(len(pokemon), len(expected_classes))
        for p, e in zip(pokemon, expected_classes):
            self.assertIsInstance(p, e)   

class TestRetrievePokemon(BaseTest):
    """Test retrieving from empty team, bm1 and bm2"""

    def test_retrieve_empty(self):
        """Test empty team, retrieves None"""
        RandomGen.set_seed(123456789)
        t = PokeTeam.random_team("Jen", 0, 0, PokeTeam.AI.RANDOM, criterion = Criterion.LV)
        poke = t.retrieve_pokemon()
        self.assertEqual(poke, None)
        after = "Jen (0): []"
        self.assertEqual(str(t), after)

    def test_retrieve_bm1(self):
        """Test retrieving from bm1 team sorted by pokedex"""
        RandomGen.set_seed(123456789)
        t = PokeTeam.random_team("John", 1, 4, PokeTeam.AI.RANDOM)
        poke = t.retrieve_pokemon()
        after = "John (1): [LV. 1 Bulbasaur: 13 HP, LV. 1 Gastly: 6 HP, LV. 1 Eevee: 10 HP]"
        self.assertIsInstance(poke, Charmander)   
        self.assertEqual(str(t), after)
        self.assertEqual(poke.status, "free")

    def test_retrieve_bm2(self):
        """Test retrieving from bm2 team sorted by criterion then pokedex"""
        RandomGen.set_seed(123456789)
        t = PokeTeam.random_team("Jane", 2, 6, PokeTeam.AI.RANDOM, criterion = Criterion.DEF)
        poke = t.retrieve_pokemon()
        after = "Jane (2): [LV. 1 Squirtle: 11 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Eevee: 10 HP, LV. 1 Eevee: 10 HP, LV. 1 Eevee: 10 HP]"
        self.assertIsInstance(poke, Gastly)    
        self.assertEqual(str(t), after)
        self.assertEqual(poke.status, "free")

class TestReturnPokemon(BaseTest):
    """Test fainted pokemon, paralysed pokemon and returning pokemon to a team sorted by criterion"""    

    def test_return_fainted(self):
        """Test returning a fainted pokemon"""
        RandomGen.set_seed(123456789)
        t = PokeTeam.random_team("Jane", 1, 6, PokeTeam.AI.RANDOM)
        p = t.retrieve_pokemon()
        before = str(t)
        p.is_fainted = True
        after = str(t)
        self.assertEqual(before, after)

    def test_return_paralysed(self):
        """Test paralysed pokemon when returned does not affect team ordering because its status is cleared when taken off the field"""
        RandomGen.set_seed(123456789)
        t = PokeTeam.random_team("Jane", 2, 4, PokeTeam.AI.RANDOM, criterion = Criterion.SPD)
        before = str(t)
        p = t.retrieve_pokemon()
        self.assertEqual(p.get_current_speed(), 8)
        p.status = "paralysis"
        p.paralysis()
        self.assertEqual(p.get_current_speed(), 4)
        t.return_pokemon(p)
        after = str(t)
        self.assertEqual(before, after)

    def test_return_bm2(self):
        """Test damaged pokemon returned to team sorted by hp"""
        RandomGen.set_seed(123456789)
        t = PokeTeam.random_team("Jane", 2, 4, PokeTeam.AI.RANDOM, criterion = Criterion.HP)
        p = t.retrieve_pokemon()
        p.lose_hp(4)
        t.return_pokemon(p)
        after = "Jane (2): [LV. 1 Eevee: 10 HP, LV. 1 Charmander: 9 HP, LV. 1 Bulbasaur: 9 HP, LV. 1 Gastly: 6 HP]"
        self.assertEqual(str(t), after)

class TestSpecial(BaseTest):
    """Test the 3 special modes"""

    def test_special_0(self):
        """Test battle mode 0"""
        t = PokeTeam("Jane", [1, 1, 1, 1, 1], 0, PokeTeam.AI.ALWAYS_ATTACK)
        t.special()
        after = str(t)
        self.assertEqual(after, "Jane (0): [LV. 1 Eevee: 10 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Squirtle: 11 HP, LV. 1 Gastly: 6 HP, LV. 1 Charmander: 9 HP]")

    def test_special_1(self):
        """Test battle mode 1"""
        t = PokeTeam("Jane", [2, 0, 0, 1, 1], 1, PokeTeam.AI.ALWAYS_ATTACK) 
        #Jane (1): [LV. 1 Charmander: 9 HP, LV. 1 Charmander: 9 HP, LV. 1 Gastly: 6 HP, LV. 1 Eevee: 10 HP]
        items = CircularQueue(len(t.pokeTeamMembers))
        # save the first two charmanders
        while len(t.pokeTeamMembers) > 0:
            item = t.pokeTeamMembers.serve()
            if len(t.pokeTeamMembers) == 3: # first
                first_charm = item
            elif len(t.pokeTeamMembers) == 2: # second
                second_charm = item
            items.append(item)
        t.pokeTeamMembers = items
        
        t.special() #Jane (1): [LV. 1 Gastly: 6 HP, LV. 1 Eevee: 10 HP, LV. 1 Charmander: 9 HP, LV. 1 Charmander: 9 HP]
        
        items = CircularQueue(len(t.pokeTeamMembers))
        # save the last two charmanders
        while len(t.pokeTeamMembers) > 0:
            item = t.pokeTeamMembers.serve() # second last
            if len(t.pokeTeamMembers) == 1:
                special_first_charm = item
            elif t.pokeTeamMembers.is_empty(): # last
                special_second_charm = item
            items.append(item)
        t.pokeTeamMembers = items

        # check that previous front half is reversed, i.e. previous first charmander is now second charmander, and vice versa
        self.assertEqual(first_charm, special_second_charm)
        self.assertEqual(second_charm, special_first_charm)

        # check overall str
        after = str(t)
        self.assertEqual(after, "Jane (1): [LV. 1 Gastly: 6 HP, LV. 1 Eevee: 10 HP, LV. 1 Charmander: 9 HP, LV. 1 Charmander: 9 HP]") 

    def test_special_2(self):
        """Test battle mode 2"""
        RandomGen.set_seed(123456789)
        t = PokeTeam.random_team("Jane", 2, 4, PokeTeam.AI.RANDOM, criterion = Criterion.HP) # initially hp is in descending order
        p = t.retrieve_pokemon() # Bulbasaur retrieved
        p.lose_hp(4) # Bulbasaur now has 9 hp
        t.return_pokemon(p) # Bulbasaur and Charmander have same hp, and according to reversed Pokedex ordering, Bulbasaur is before Charmander
        t.special() # this reverses hp to ascending order and also reverses Pokedex ordering
        after = str(t)
        self.assertEqual(after, "Jane (2): [LV. 1 Gastly: 6 HP, LV. 1 Bulbasaur: 9 HP, LV. 1 Charmander: 9 HP, LV. 1 Eevee: 10 HP]" )

        t.special() # this reverses hp to descending order and pokedex ordering is normal
        after = str(t)
        self.assertEqual(after, "Jane (2): [LV. 1 Eevee: 10 HP, LV. 1 Charmander: 9 HP, LV. 1 Bulbasaur: 9 HP, LV. 1 Gastly: 6 HP]")

        p = t.retrieve_pokemon()
        p.lose_hp(1)
        t.return_pokemon(p)
        t.special() # this reverses hp to ascending order and pokedex is reversed
        after = str(t)
        self.assertEqual(after, "Jane (2): [LV. 1 Gastly: 6 HP, LV. 1 Eevee: 9 HP, LV. 1 Bulbasaur: 9 HP, LV. 1 Charmander: 9 HP]")

class TestRegenerate(BaseTest):
    """Test regeneration for different team states"""

    def test_empty_team(self):
        """Regenerate an empty team which has undergone special"""
        t = PokeTeam("John", [1, 1, 1, 1, 1], 2, PokeTeam.AI.ALWAYS_ATTACK, Criterion.SPD)
        before = str(t) # John (2): [LV. 1 Charmander: 9 HP, LV. 1 Eevee: 10 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Squirtle: 11 HP, LV. 1 Gastly: 6 HP]

        # change the ordering
        t.special() # John (2): [LV. 1 Gastly: 6 HP, LV. 1 Squirtle: 11 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Eevee: 10 HP, LV. 1 Charmander: 9 HP]
        
        while not t.is_empty():
            p = t.retrieve_pokemon()
            p.lose_hp(100)
            t.return_pokemon(p)
        self.assertEqual(str(t), "John (2): []")
        t.regenerate_team()
        after = str(t)
        self.assertEqual(before, after)

    def test_heal_times(self):
        """Test that heal times is reset"""
        t1 = PokeTeam("Jane", [1, 1, 1, 1, 1], 0, PokeTeam.AI.ALWAYS_ATTACK)
        p1 = t1.retrieve_pokemon()
        b = Battle()
        b.heal(t1, p1)
        b.heal(t1, p1)
        b.heal(t1, p1)
        self.assertEqual(t1.heal_times, 3)
        t1.regenerate_team()
        self.assertEqual(t1.heal_times, 0)

    def test_full_team(self):
        """Test that no effect on regenerating full team"""
        t = PokeTeam("John", [1, 1, 1, 1, 1], 1, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        before = str(t)
        t.regenerate_team()
        after = str(t)
        self.assertEqual(before, after)


class TestString(BaseTest):
    """Tests the 3 battle modes"""

    def test_string_bm0(self):
        """Test initial team"""
        t = PokeTeam("Dawn", [1, 1, 1, 1, 1], 0, PokeTeam.AI.RANDOM)
        self.assertEqual(str(t), "Dawn (0): [LV. 1 Charmander: 9 HP, LV. 1 Bulbasaur: 13 HP, LV. 1 Squirtle: 11 HP, LV. 1 Gastly: 6 HP, LV. 1 Eevee: 10 HP]")

    def test_string_bm1(self):
        """Test one fainted pokemon"""
        t = PokeTeam("Jane", [1, 1, 1, 1, 1], 1, PokeTeam.AI.RANDOM)
        p = t.retrieve_pokemon()
        p.lose_hp(9)
        t.return_pokemon(p)
        self.assertEqual(str(t), "Jane (1): [LV. 1 Bulbasaur: 13 HP, LV. 1 Squirtle: 11 HP, LV. 1 Gastly: 6 HP, LV. 1 Eevee: 10 HP]")

    def test_string_bm2(self):
        """Test empty team"""
        t = PokeTeam("John", [1, 1, 1, 1, 1], 2, PokeTeam.AI.ALWAYS_ATTACK, Criterion.HP)
        while not t.is_empty():
            p = t.retrieve_pokemon()
            p.lose_hp(100)
            t.return_pokemon(p)
        self.assertEqual(str(t), "John (2): []")

class TestIsEmpty(BaseTest):
    """Tests conditions when team is empty"""

    def test_all_fainted(self):
        """Test when all pokemon are fainted"""
        t = PokeTeam("Jane", [1, 1, 1, 1, 1], 0, PokeTeam.AI.USER_INPUT)
        # faint all pokemon
        for i in range(len(t.pokeTeamMembers)):
            p = t.retrieve_pokemon()
            p.lose_hp(100)
            t.return_pokemon(p)
        self.assertEqual(str(t), "Jane (0): []")
        self.assertTrue(t.is_empty())

    def test_not_empty(self):
        """Test when at least one pokemon in team"""
        t = PokeTeam("Jane", [0, 0, 0, 0, 1], 2, PokeTeam.AI.RANDOM, Criterion.LV )
        self.assertFalse(t.is_empty())

    def test_retrieve_last_pokemon(self):
        """Test that after retrieving last pokemon the team is empty"""
        t = PokeTeam("Jen", [0, 0, 0, 0, 1], 1, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE)
        p = t.retrieve_pokemon()
        self.assertTrue(t.is_empty())
        
class TestChooseBattleOption(BaseTest):
    """Different options chosen"""

    def test_always_attack(self):
        """Test that always attack"""
        t1 = PokeTeam("Jane", [1, 1, 1, 1, 1], 0, PokeTeam.AI.ALWAYS_ATTACK)
        t2 = PokeTeam("Jen", [1, 1, 1, 1, 1], 1, PokeTeam.AI.ALWAYS_ATTACK)
        b = Battle()
        b.team1 = t1
        b.team2 = t2
        b.team1_poke = t1.retrieve_pokemon()
        b.team2_poke = t2.retrieve_pokemon()
        while (not (b.team1_poke is None or b.team2_poke is None)) and (b.team1.heal_times <= 3 and b.team2.heal_times <=3):
            t1_choice = b.team1.choose_battle_option(b.team1_poke, b.team2_poke) # check that everytime it will be attack
            t2_choice = b.team2.choose_battle_option(b.team2_poke, b.team1_poke)
            self.assertEqual(t1_choice, Action.ATTACK)
            self.assertEqual(t2_choice, Action.ATTACK) 
            b.both_attack() 
            if not (b.team1_poke.is_fainted() or b.team2_poke.is_fainted()):
                # both lose 1 HP if both still alive
                b.team1_poke.lose_hp(1)
                b.team2_poke.lose_hp(1)
            b.handle_level_up()
            b.handle_evolve(b.team1_poke)
            b.handle_evolve(b.team2_poke)
            b.handle_fainted(b.team1, b.team1_poke)
            b.handle_fainted(b.team2, b.team2_poke)

    def test_swap_on_super_effective(self):
        """Test swapping or attacking depending on type_multiplier"""
        # test swap true
        t1 = PokeTeam("John", [1, 1, 0, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK) # John (0): [LV. 1 Charmander: 9 HP, LV. 1 Bulbasaur: 13 HP]
        t2 = PokeTeam("Jane", [0, 1, 1, 0, 0], 1, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE) # Jane (1): [LV. 1 Bulbasaur: 13 HP, LV. 1 Squirtle: 11 HP, LV. 1 Gastly: 6 HP]
        b = Battle()
        b.team1 = t1
        b.team2 = t2
        b.team1_poke = t1.retrieve_pokemon() # Charmander is Fire
        b.team2_poke = t2.retrieve_pokemon() # Bulbasaur is Grass
        t1_choice = b.team1.choose_battle_option(b.team1_poke, b.team2_poke) 
        t2_choice = b.team2.choose_battle_option(b.team2_poke, b.team1_poke) # Fire has 2.0 type effectiveness against Grass
        self.assertEqual(t1_choice, Action.ATTACK)
        self.assertEqual(t2_choice, Action.SWAP) 
        b.swap(b.team2, b.team2_poke) # Bulbasaur returned to end of team, Squirtle retrieved.
        self.assertEqual(type(b.team2_poke), Squirtle)

        # test swap false
        t1 = PokeTeam("John", [0, 1, 1, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK) # John (0): [LV. 1 Bulbasaur: 13 HP, LV. 1 Squirtle: 11 HP]
        t2 = PokeTeam("Jane", [0, 1, 1, 0, 0], 1, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE) # Jane (1): [LV. 1 Bulbasaur: 13 HP, LV. 1 Squirtle: 11 HP]
        b = Battle()
        b.team1 = t1
        b.team2 = t2
        b.team1_poke = t1.retrieve_pokemon() # Bulbasaur is Grass
        b.team2_poke = t2.retrieve_pokemon() # Bulbasaur is Grass
        t1_choice = b.team1.choose_battle_option(b.team1_poke, b.team2_poke) 
        t2_choice = b.team2.choose_battle_option(b.team2_poke, b.team1_poke) # Grass has 1.0 type effectiveness against Grass
        self.assertEqual(t1_choice, Action.ATTACK)
        self.assertEqual(t2_choice, Action.ATTACK) 

    def test_random(self):
        """Test random battle option"""
        # Test ai type is None
        RandomGen.set_seed(12345)
        t1 = PokeTeam("Jane", [1, 1, 1, 1, 1], 0, None)
        p1 = t1.retrieve_pokemon()
        t1_choice = t1.choose_battle_option(t1, p1)
        self.assertEqual(t1_choice, Action.SPECIAL)


        # Test ai type is RANDOM
        RandomGen.set_seed(123)
        t2 = PokeTeam("John", [1, 1, 1, 1, 1], 1, PokeTeam.AI.RANDOM)
        p2 = t2.retrieve_pokemon()
        t2_choice = t2.choose_battle_option(t2, p2)
        self.assertEqual(t2_choice, Action.HEAL)

    def test_user_input(self):
        """Test valid input, invalid string input and invalid range input"""
        # Test ai type is user input with valid input
        t3 = PokeTeam("Jen", [1, 1, 1, 1, 1], 2, PokeTeam.AI.USER_INPUT, Criterion.LV)
        p3 = t3.retrieve_pokemon()
        # t3_choice = t3.choose_battle_option(t3, p3) # Enter 3 which should correspond to HEAL
        self.assertEqual(t3.user_input("3",list(Action)), Action.HEAL)

        # Test ai type is user input with string
        t4 = PokeTeam("Jen", [1, 1, 1, 1, 1], 0, PokeTeam.AI.USER_INPUT)
        p4 = t4.retrieve_pokemon()
        self.assertRaises(ValueError, lambda: t4.user_input("w",list(Action))) # Enter string "w" (not a literal for int() with base 10)

        # Test ai type is user input with invalid range
        t5 = PokeTeam("Jen", [1, 1, 1, 1, 1], 0, PokeTeam.AI.USER_INPUT)
        p5 = t5.retrieve_pokemon()
        self.assertRaises(ValueError, lambda: t5.user_input("0",list(Action))) # Enter 0(not between 1 and 4)
        










