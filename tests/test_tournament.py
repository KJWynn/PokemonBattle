"""
This file includes test cases added for testing methods in the tournament.py module alongside the provided tests in the original template.
Methods to be tested: __init__, set_battle_mode, is_valid_tournament, start_tournament, advance_tournament, inked_list_with_metas.

"""
__author__ = "Scaffold by Jackson Goerner, Code by Khor Jia Wynn"

from poke_team import PokeTeam
from random_gen import RandomGen
from stack_adt import ArrayStack
from tournament import Tournament
from battle import Battle
from tests.base_test import BaseTest

class TestTournament(BaseTest):
    """Class containing tests for methods in tournament provided by template"""
    def test_creation(self):
        """Test case for failed creation of tournament for invalid tournament string passed and start tournament"""
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(1)
        self.assertRaises(ValueError, lambda: t.start_tournament("Roark Gardenia + Maylene Crasher_Wake + + + Fantina Byron + Candice Volkner + + +"))
        t.start_tournament("Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +")

    def test_random(self):
        """Test case for methods in a random tournament"""
        RandomGen.set_seed(123456)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +")

        team1, team2, res = t.advance_tournament() # Roark vs Gardenia
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Roark"))
        self.assertTrue(str(team2).startswith("Gardenia"))

        team1, team2, res = t.advance_tournament() # Maylene vs Crasher_Wake
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Maylene"))
        self.assertTrue(str(team2).startswith("Crasher_Wake"))

        team1, team2, res = t.advance_tournament() # Fantina vs Byron
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Fantina"))
        self.assertTrue(str(team2).startswith("Byron"))

        team1, team2, res = t.advance_tournament() # Maylene vs Fantina
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("Maylene"))
        self.assertTrue(str(team2).startswith("Fantina"))

        team1, team2, res = t.advance_tournament() # Roark vs Fantina
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Roark"))
        self.assertTrue(str(team2).startswith("Fantina"))

        team1, team2, res = t.advance_tournament() # Candice vs Volkner
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("Candice"))
        self.assertTrue(str(team2).startswith("Volkner"))

        team1, team2, res = t.advance_tournament() # Roark vs Candice
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("Roark"))
        self.assertTrue(str(team2).startswith("Candice"))

    def test_metas(self):
        """Test case for getting metas after tournament"""
        RandomGen.set_seed(123456)
        t = Tournament(Battle(verbosity=0))
        t.set_battle_mode(0)
        t.start_tournament("Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +")
        l = t.linked_list_with_metas()
        # Roark = [0, 2, 1, 1, 1]
        # Garderia = [0, 0, 2, 0, 1]
        # Maylene = [6, 0, 0, 0, 0]
        # Crasher_Wake = [0, 2, 0, 1, 0]
        # Fantina = [0, 0, 1, 1, 1]
        # Byron = [0, 2, 0, 0, 1]
        # Candice = [2, 2, 1, 0, 0]
        # Volkner = [0, 5, 0, 0, 0]
        expected = [
            [],
            [],
            ['FIRE'], # Roark Fantina do not have Fire types, but Maylene does (lost to Fantina)
            ['GRASS'], # Maylene Fantina do not have Grass types, but Byron/Crasher_Wake does (lost to Fantina/Maylene)
            [],
            [],
            [],
        ]
        for x in range(len(l)):
            team1, team2, types = l[x]
            self.assertEqual(expected[x], types)

    # def test_balance(self):
    #     # 1054
    #     t = Tournament()
    #     self.assertFalse(t.is_balanced_tournament("Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +"))

class TestInit(BaseTest):
    """Test init"""

    def test_no_battle(self):
        """Test that if no battle instance given, one is created"""
        t = Tournament()
        self.assertNotEqual(t.battle, None)

    def test_battle_given(self):
        """Test that battle instance is correctly assigned"""
        b = Battle(verbosity=0)
        t = Tournament(b)
        self.assertEqual(t.battle, b)

    def test_attributes(self):
        """Test that initial attributes are correct"""
        t = Tournament()
        self.assertEqual(t.battle_mode, None)
        self.assertEqual(t.count, 0)
        self.assertEqual(t.stack1, None)
        self.assertEqual(t.stack2, None)

class TestSetBattleMode(BaseTest):
    """Test setting battle modes"""

    def test_invalid_battle_mode(self):
        """Test invalid battle mode given"""
        t = Tournament()
        self.assertRaises(ValueError, lambda: t.set_battle_mode("w"))

    def test_valid_battle_mode(self):
        """Test valid battle mode"""
        t = Tournament()
        t.set_battle_mode(0)
        self.assertEqual(t.battle_mode, 0)

    def test_all_teams(self):
        """Test that all teams share same battle mode"""
        t = Tournament()
        t.set_battle_mode(1)
        t.start_tournament("Roark Gardenia + Maylene Crasher_Wake + Fantina Byron + + + Candice Volkner + +")
        teams = []
        while not t.stack1.is_empty():
            item = t.stack1.pop()
            if type(item) == PokeTeam:
                teams.append(item)
        for team in teams:
            self.assertEqual(team.battle_mode, 1)


class TestIsValidTournament(BaseTest):
    """Test different tournament_str"""
    def test_too_many_plus(self):
        """Test too many battles"""
        t = Tournament()
        str1 = "+ Roark Gardenia + Maylene Crasher_Wake + + + Fantina Byron + Candice Volkner + + +"
        self.assertFalse(t.is_valid_tournament(str1)) # false more + than needed

    def test_too_few_plus(self):
        """Test too few battles"""
        t = Tournament()
        str2 = "Monfils + Berrettini + Shapovalov Nadal + + Kale Polite + Sinner Tsitsipas + Auger-Aliassime Medvedev + + +"
        self.assertFalse(t.is_valid_tournament(str2))

    def test_just_right(self):
        """Test valid"""
        t = Tournament()
        str3 = "Monfils Berrettini + Shapovalov Nadal + John Jane + + + Kale Polite + Sinner Tsitsipas + Auger-Aliassime Medvedev + + + +"
        self.assertTrue(t.is_valid_tournament(str3))


class TestAdvanceTournament(BaseTest):
    """Test different stages of tournaments"""
    def test_tournament_end(self):
        """Test end of tournament"""
        t = Tournament()
        t.set_battle_mode(0)
        t.start_tournament("Roark Gardenia +")
        res1 = t.advance_tournament() # should yield a winner
        res2 = t.advance_tournament() # no games remain so returns None
        self.assertEqual(res2, None)
        res3 = t.advance_tournament()
        self.assertEqual(res3, None)

    def test_simple_tournament(self):
        """Test simple tournament"""
        t = Tournament()
        team1 = PokeTeam("A", [0, 0, 0, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        team2 = PokeTeam("B", [1, 0, 0, 0, 0], 1, PokeTeam.AI.ALWAYS_ATTACK) # Fire
        team3 = PokeTeam("C", [0, 0, 1, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK) # Water
        team4 = PokeTeam("D", [0, 0, 0, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)
        t.stack1 = ArrayStack(10)
        t.stack1.push("+")
        t.stack1.push("+")
        t.stack1.push(team4)
        t.stack1.push(team3)
        t.stack1.push("+")
        t.stack1.push(team2)
        t.stack1.push(team1) 
        # [team1, team2, +, team3, team4, +, +]
        t.stack2 = ArrayStack(len(t.stack1))
        res1 = t.advance_tournament()
        self.assertEqual(res1, (team1, team2, 2))
        res2 = t.advance_tournament()
        self.assertEqual(res2, (team3, team4, 1))
        res3 = t.advance_tournament()
        self.assertEqual(res3, (team2, team3, 2)) # Water should easily beat fire

    def test_complicated_tournament(self):
        """Test long tournament"""
        RandomGen.set_seed(0)
        t = Tournament()
        t.set_battle_mode(1)
        t.start_tournament("A B + C D + + E F + + G H + I J + K L + M N + + + + +")

        team1, team2, res = t.advance_tournament() 
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("A"))
        self.assertTrue(str(team2).startswith("B"))
        
        team1, team2, res = t.advance_tournament() 
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("C"))
        self.assertTrue(str(team2).startswith("D"))

        team1, team2, res = t.advance_tournament() 
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("B"))
        self.assertTrue(str(team2).startswith("C"))

        team1, team2, res = t.advance_tournament() 
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("E"))
        self.assertTrue(str(team2).startswith("F"))

        team1, team2, res = t.advance_tournament() 
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("B"))
        self.assertTrue(str(team2).startswith("E"))
 
        team1, team2, res = t.advance_tournament() 
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("G"))
        self.assertTrue(str(team2).startswith("H"))

        team1, team2, res = t.advance_tournament() 
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("I"))
        self.assertTrue(str(team2).startswith("J"))

        team1, team2, res = t.advance_tournament() 
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("K"))
        self.assertTrue(str(team2).startswith("L"))

        team1, team2, res = t.advance_tournament() 
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("M"))
        self.assertTrue(str(team2).startswith("N"))

        team1, team2, res = t.advance_tournament() 
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("L"))
        self.assertTrue(str(team2).startswith("N"))

        team1, team2, res = t.advance_tournament() 
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("I"))
        self.assertTrue(str(team2).startswith("N"))

        team1, team2, res = t.advance_tournament() 
        self.assertEqual(res, 2)
        self.assertTrue(str(team1).startswith("G"))
        self.assertTrue(str(team2).startswith("N"))

        team1, team2, res = t.advance_tournament() 
        self.assertEqual(res, 1)
        self.assertTrue(str(team1).startswith("B"))
        self.assertTrue(str(team2).startswith("N"))


class TestLinkedListWithMetas(BaseTest):
    """Test getting metas after tournament"""
    def test_no_meta(self):
        """Test no metas"""
        t = Tournament()
        t.stack1 = ArrayStack(7)
        t.stack2 = ArrayStack(7)
        team1 = PokeTeam("Team1", [1, 1, 1, 1, 1], 0, PokeTeam.AI.ALWAYS_ATTACK)      
        team2 = PokeTeam("Team2", [1, 1, 1, 1, 1], 0, PokeTeam.AI.ALWAYS_ATTACK)  
        team3 = PokeTeam("Team3", [1, 1, 1, 1, 1], 0, PokeTeam.AI.ALWAYS_ATTACK)  
        team4 = PokeTeam("Team4", [1, 1, 1, 1, 1], 0, PokeTeam.AI.ALWAYS_ATTACK)  
        # No absent poketypes so no meta
        t.stack1.push("+")
        t.stack1.push("+")
        t.stack1.push(team4)
        t.stack1.push(team3)    
        t.stack1.push("+")
        t.stack1.push(team2)
        t.stack1.push(team1)     

        l = t.linked_list_with_metas()

        expected = [[] for i in range(len(l))]
        for x in range(len(l)):
            team1, team2, types = l[x]
            self.assertEqual(expected[x], types) 

    def test_simple_meta(self):
        """Test short tournament with simple meta"""
        t = Tournament()
        t.stack1 = ArrayStack(7)
        t.stack2 = ArrayStack(7)
        team1 = PokeTeam("Team1", [0, 0, 1, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)      
        team2 = PokeTeam("Team2", [0, 1, 0, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)  
        team3 = PokeTeam("Team3", [1, 0, 0, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK)  
        team4 = PokeTeam("Team4", [0, 1, 0, 0, 0], 0, PokeTeam.AI.ALWAYS_ATTACK) 
        t.stack1.push("+")
        t.stack1.push("+")
        t.stack1.push(team4)
        t.stack1.push(team3)    
        t.stack1.push("+")
        t.stack1.push(team2)
        t.stack1.push(team1)  

        l = t.linked_list_with_metas()

        expected = [["WATER"], # Team2, Team3, 2, Water, Ghost, Normal absent, check Team1 or Team4, yes, Water present in Team1
        [], #Team3, Team4, 1
        [], #Team1, Team2, 2
        ]
        for x in range(len(l)):
            team1, team2, types = l[x]
            self.assertEqual(expected[x], types)  

    def test_complicated_metas(self):
        """Test long tournament with complicated meta"""
        RandomGen.set_seed(0)
        t = Tournament()
        t.set_battle_mode(0)
        t.start_tournament("A B + C D + + E F + + G H + I J + K L + M N + + + + +")
        l = t.linked_list_with_metas()

        # A[0, 0, 1, 1, 1]
        # B[0, 1, 1, 0, 1]
        # C[2, 1, 2, 0, 0]
        # D[0, 2, 0, 2, 0]
        # E[1, 0, 1, 0, 1]
        # F[0, 0, 1, 0, 3]
        # G[1, 0, 2, 1, 1]
        # H[0, 0, 1, 0, 2]
        # I[0, 3, 0, 1, 0]
        # J[1, 1, 0, 1, 2]
        # K[1, 2, 0, 2, 1]
        # L[2, 1, 1, 1, 1]
        # M[1, 1, 1, 1, 0]
        # N[0, 2, 1, 0, 0]
        expected = [
            ["NORMAL"], 
            [], 
            ["WATER"], 
            [], 
            [], 
            [], 
            [], 
            [], 
            [], 
            [], 
            ["GHOST"],
            [], 
            [], 
        ]
        for x in range(len(l)):
            team1, team2, types = l[x]
            self.assertEqual(expected[x], types)       

 