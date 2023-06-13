"""
This file includes test cases added for testing methods in the battle class alongside the provided tests in the original template.
"""
from random_gen import RandomGen
from battle import Battle
from poke_team import Action, Criterion, PokeTeam
from pokemon import Charizard, Charmander, Eevee, Gastly, Squirtle, Venusaur
from tests.base_test import BaseTest

__author__ = "Scaffold by Jackson Goerner, Code by Tee Zhi Hui"

class TestBattle(BaseTest):
    """Class containing test cases for methods provided by template"""
    def test_basic_battle(self):
        """" Test case for basic battle provided by template """
        RandomGen.set_seed(1337)
        team1 = PokeTeam("Ash", [1, 1, 1, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        team2 = PokeTeam("Gary", [0, 0, 0, 0, 3], 0, PokeTeam.AI.ALWAYS_ATTACK)
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)
        self.assertEqual(res, 1)
        self.assertTrue(team2.is_empty())
        remaining = []
        while not team1.is_empty():
            remaining.append(team1.retrieve_pokemon())
        self.assertEqual(len(remaining), 2)
        self.assertEqual(remaining[0].get_hp(), 1)
        self.assertIsInstance(remaining[0], Venusaur)
        self.assertEqual(remaining[1].get_hp(), 11)
        self.assertIsInstance(remaining[1], Squirtle)

    def test_complicated_battle(self):
        """" Test case for complicated battle provided by template """
        RandomGen.set_seed(192837465)
        team1 = PokeTeam("Brock", [1, 1, 1, 1, 1], 2, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE, criterion=Criterion.HP)
        team2 = PokeTeam("Misty", [0, 0, 0, 3, 3], 2, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE, criterion=Criterion.SPD)
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)
        self.assertEqual(res, 1)
        remaining = []
        while not team1.is_empty():
            remaining.append(team1.retrieve_pokemon())
        self.assertEqual(len(remaining), 2)
        self.assertEqual(remaining[0].get_hp(), 11)
        self.assertIsInstance(remaining[0], Charizard)
        self.assertEqual(remaining[1].get_hp(), 6)
        self.assertIsInstance(remaining[1], Gastly)

class TestBattleInit(BaseTest):
    """ Test cases for initialisation of Battle object """
    def test_result (self):
        """Test the result of Battle object right after initialisation"""
        b = Battle()                                        # b is an battle object
        self.assertEqual(b.result, None)                    # result of the battle is None

    def test_team (self):
        """Test the  Battle object of team1 and team2 right after initialisation"""
        b = Battle()                                        # b is an battle object
        self.assertEqual(b.team1, None)                     # team1 is None when the b object is initialised 
        self.assertEqual(b.team2, None)                     # team2 is None when the b object is initialised

    def test_team_poke (self):
        """Test the pokemons chosen by team1 and team2 of Battle object right after initialisation"""
        b = Battle()                                        # b is an battle object
        self.assertEqual(b.team1_poke, None)                # team1.poke is None when the b object is initialised               
        self.assertEqual(b.team2_poke, None)                # team2.poke is None when the b object is initialised  

    def test_choice(self):
        """Test the choices of team1 and team2 of Battle object right after initialisation"""
        b = Battle()                                        # b is an battle object
        self.assertEqual(b.choice1, None)                   # choice1 from team1 is None when the b object is initialised                
        self.assertEqual(b.choice2, None)                   # choice2 from team2 is None when the b object is initialised    

class TestBattleBattle(BaseTest):
    """
    3 test cases for Battle object with different result 
    result :0 -> draw
    result :1 -> team 1 won, team 2 lost
    result :2 -> team 2 won, team 1 lost
    """

    def test_battle_team1_win (self):
        """Test case for team1 won the battle"""
        RandomGen.set_seed(0)
        team1 = PokeTeam("Hush", [1, 2, 1, 1, 1], 1, PokeTeam.AI.RANDOM)
        team2 = PokeTeam("Mady", [0, 3, 0, 3, 0], 1, PokeTeam.AI.RANDOM)
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)                                # team 1 battle with team 2 
        self.assertEqual(res, 1)
        self.assertTrue(team2.is_empty())                           # team2 should be empty as it lost 

    def test_battle_team2_win (self):
        """Test case for team2 won the battle, as team2 has twice heal_times of team1 """
        RandomGen.set_seed(0)
        team1 = PokeTeam("Trash", [2, 1, 1, 1, 0], 1, PokeTeam.AI.RANDOM, criterion=Criterion.LV)
        team2 = PokeTeam("Gold", [2, 1, 1, 1, 1], 2, PokeTeam.AI.ALWAYS_ATTACK, criterion=Criterion.DEF)
        team2.heal_times = 6                                        # set heal_times of team2 to 6 
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)                                # team 1 battle with team 2 
        self.assertEqual(res, 2)
        self.assertEqual(team1.heal_times, 3)                       # team1 reach the max heal_times which is 3

    def test_battle_draw (self):
        """ Test case for draw result, when both team have no pokemon in the team """
        RandomGen.set_seed(0)
        team1 = PokeTeam("Ben", [0, 0, 0 ,0 ,0], 1, PokeTeam.AI.ALWAYS_ATTACK, criterion=Criterion.DEF)
        team2 = PokeTeam("Bald", [0, 0, 0 ,0 ,0], 2, PokeTeam.AI.SWAP_ON_SUPER_EFFECTIVE, criterion=Criterion.LV)
        b = Battle(verbosity=0)
        res = b.battle(team1, team2)                                # team 1 battle with team 2 
        self.assertEqual(res, 0)
        
