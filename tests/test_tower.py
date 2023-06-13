"""
This file includes test cases added for testing methods in the tower.py module alongside the provided tests in the original template.
Methods to be tested (BattleTower): __init__, set_my_team, generate_teams
Methods to be tested (BattleTowerIterator): __init__, __next__, avoid_duplicates

"""
__author__ = "Scaffold by Jackson Goerner, Code by Lim Yi Xuan"

from random_gen import RandomGen
from poke_team import Criterion, PokeTeam
from battle import Battle
from tower import BattleTower, BattleTowerIterator
from tests.base_test import BaseTest

class TestTower(BaseTest):
    """Test cases for tower that is provided by default in template"""
    def test_creation(self):
        """Test case for testing initialisation of BattleTower object"""
        RandomGen.set_seed(51234)
        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(PokeTeam.random_team("N", 2, team_size=6, criterion=Criterion.HP))
        bt.generate_teams(4)
        # Teams have 7, 10, 10, 3 lives.
        RandomGen.set_seed(1029873918273)
        results = [
            (1, 6),
            (1, 9),
            (2, 10)
        ]
        it = iter(bt)
        for (expected_res, expected_lives), (res, me, tower, lives) in zip(results, it):
            self.assertEqual(expected_res, res, (expected_res, expected_lives))
            self.assertEqual(expected_lives, lives)

    def test_duplicates(self):
        RandomGen.set_seed(29183712400123)
    
        bt = BattleTower(Battle(verbosity=0))
        bt.set_my_team(PokeTeam.random_team("Jackson", 0, team_size=6))
        bt.generate_teams(10)

        # Team numbers before:
        # [0, 4, 1, 0, 0], 6
        # [1, 0, 2, 0, 0], 5
        # [1, 1, 0, 1, 0], 8
        # [1, 2, 1, 1, 0], 10
        # [0, 0, 2, 1, 1], 8
        # [1, 1, 3, 0, 0], 4
        # [0, 2, 0, 1, 0], 5
        # [1, 0, 0, 4, 0], 3
        # [1, 1, 1, 0, 2], 7
        # [0, 1, 1, 1, 0], 9
        it = iter(bt)
        it.avoid_duplicates()
        # Team numbers after:
        # [1, 1, 0, 1, 0], 8
        # [0, 1, 1, 1, 0], 9

        l = []
        for res, me, tower, lives in bt:
            tower.regenerate_team()
            l.append((res, lives))
        
        self.assertEqual(l, [
            (1, 7),
            (1, 8),
            (2, 7)
        ])
        
    # def test_sort_lives(self):
    #     # 1054 only
    #     RandomGen.set_seed(9821309123)
    
    #     bt = BattleTower(Battle(verbosity=0))
    #     bt.set_my_team(PokeTeam.random_team("Jackson", 1, team_size=6))
    #     bt.generate_teams(10)

    #     it = iter(bt)
    #     # [1, 1, 3, 0, 0] 3 Name: Team 0
    #     # [2, 1, 0, 1, 0] 2 Name: Team 1
    #     # [2, 0, 0, 1, 1] 4 Name: Team 2
    #     # [3, 0, 1, 0, 1] 2 Name: Team 3
    #     # [0, 0, 2, 1, 2] 4 Name: Team 4
    #     # [0, 1, 0, 2, 0] 3 Name: Team 5
    #     # [3, 0, 2, 0, 0] 8 Name: Team 6
    #     # [0, 0, 2, 1, 0] 4 Name: Team 7
    #     # [0, 2, 1, 1, 0] 3 Name: Team 8
    #     # [1, 0, 1, 3, 1] 4 Name: Team 9
    #     RandomGen.set_seed(123)
    #     res, me, other_1, lives = next(it)
    #     it.sort_by_lives()
    #     # [1, 1, 3, 0, 0] 2 Name: Team 0
    #     # [2, 1, 0, 1, 0] 2 Name: Team 1
    #     # [3, 0, 1, 0, 1] 2 Name: Team 3
    #     # [0, 1, 0, 2, 0] 3 Name: Team 5
    #     # [0, 2, 1, 1, 0] 3 Name: Team 8
    #     # [2, 0, 0, 1, 1] 4 Name: Team 2
    #     # [0, 0, 2, 1, 2] 4 Name: Team 4
    #     # [0, 0, 2, 1, 0] 4 Name: Team 7
    #     # [1, 0, 1, 3, 1] 4 Name: Team 9
    #     # [3, 0, 2, 0, 0] 8 Name: Team 6
    #     res, me, other_2, lives = next(it)

    #     self.assertEqual(str(other_1), str(other_2))

class TestTowerInit(BaseTest):
    """3 test cases for initialisation of BattleTower object in different scenarios (succesful/fail)"""
    def test_init_successful(self):
        """Test case for successful initialisation of BattleTower object when battle object is passed in as argument."""
        b = Battle()                                                # b is an battle object
        bt = BattleTower(b)                                         # pass b as argument for BattleTower object bt's initialisation
        self.assertEqual(bt.battle_instance, b)                     # battle instance is equal to the battle object passed

    def test_init_none(self):
        """
        Test case for succesful initialisation when None is passed in as argument,
        the __init__ method will generate a new battle instance when None is passed as argument.
        """
        b = None                                                    # b is None type object
        bt = BattleTower(b)                                         # pass b as argument for BattleTower object bt's initialisation
        self.assertNotEqual(bt.battle_instance, None)               # another instance of battle is generated for battle_instance when b is None    
        self.assertIsInstance(bt.battle_instance, Battle)           # the new battle_instance is Battle object
    
    def test_init_fail(self):
        """Test case for failed initialisation when non-battle object is passed as argument."""
        b = PokeTeam("Ash",[1,2,2,1,0],0,PokeTeam.AI.ALWAYS_ATTACK) # b is Pokemon object
        self.assertRaises(ValueError,lambda: BattleTower(b))        # ValueError raised when object of not Battle class or None is passed as argument
        


class TestTowerSetMyTeam(BaseTest):
    """3 test cases for set_my_team under different scenarios (successful/fail)"""
    def test_set_my_team_successful(self):
        """Test case for successful team set when PokeTeam object is passed as argument"""
        bt = BattleTower(Battle())                                      # bt is a BattleTower object
        team = PokeTeam("Ash",[1,2,2,1,0],0,PokeTeam.AI.ALWAYS_ATTACK)  # team is PokeTeam object
        bt.set_my_team(team)                                            # invoke set_my_team method with team as argument
        self.assertEqual(team, bt.my_team)                              # my_team attribute is succesfully set to team passed in
    
    def test_set_my_team_fail(self):
        """Test case for failed set of team when argument passed in is not PokeTeam object"""
        bt = BattleTower(Battle())                                      # bt is a BattleTower object
        team = Battle()                                                 # team is Battle object
        self.assertRaises(ValueError,lambda: bt.set_my_team(team))      # ValueError raised for object of wrong class passed in

    def test_set_my_team_none(self):
        """Test case for failed set of team when argument passed in is None"""
        bt = BattleTower(Battle())                                      # bt is a BattleTower object
        self.assertRaises(ValueError,lambda: bt.set_my_team(None))      # ValueError raised for None type passed as argument
        

class TestTowerGenerateTeams(BaseTest):
    """3 test cases for generate_teams in different scenarios (succesful/fail)"""
    def test_gen_one_team_successful(self):
        """Test case for succesfully generating one team"""
        RandomGen.set_seed(0)
        bt = BattleTower(Battle())                              # bt is BattleTower object
        self.assertEqual(len(bt.tower_teams), 0)                # bt initially has 0 team
        self.assertEqual(len(bt.lives_left), 0)                 # bt initailly has no records of lives for teams
        bt.generate_teams(1)                                    # invoke generate_teams with 1 as argument
        self.assertEqual(len(bt.tower_teams),1)                 # bt now has 1 team only
        self.assertEqual(len(bt.lives_left),1)                  # bt now has 1 record of lives for teams
        # Teams generated for BattleTower (team_numbers, lives)
        # [0, 2, 0, 0, 2], 3    Name: Team 0
        team = bt.tower_teams.serve()
        team_lives = bt.lives_left.serve()
        self.assertEqual(team.team_numbers, [0,2,0,0,2])
        self.assertEqual(team_lives, 3)

    def test_gen_teams_successful(self):
        """Test case for succesfully generating multiple teams"""
        RandomGen.set_seed(0)
        bt = BattleTower(Battle())                              # bt is BattleTower object
        self.assertEqual(len(bt.tower_teams), 0)                # bt initially has 0 team
        self.assertEqual(len(bt.lives_left), 0)                 # bt initailly has no records of lives for teams
        bt.generate_teams(5)                                    # invoke generate_teams with 5 as argument
        self.assertEqual(len(bt.tower_teams),5)                 # bt now has 5 teams
        self.assertEqual(len(bt.lives_left),5)                  # bt now has 5 record of lives for teams
        # Teams generated for BattleTower (team_numbers, lives)
        # [0, 2, 0, 0, 2], 3    Name: Team 0
        # [1, 1, 0, 1, 0], 7    Name: Team 1
        # [0, 2, 0, 2, 0], 10   Name: Team 2
        # [0, 3, 0, 0, 1], 9    Name: Team 3
        # [0, 1, 3, 0, 0], 6    Name: Team 4
        l = []
        for _ in range(len(bt.tower_teams)):
            team = bt.tower_teams.serve()
            lives = bt.lives_left.serve()
            l.append((team.team_numbers,lives))
        expected_teams = [
            ([0, 2, 0, 0, 2], 3),
            ([1, 1, 0, 1, 0], 7),
            ([0, 2, 0, 2, 0], 10),
            ([0, 3, 0, 0, 1], 9),
            ([0, 1, 3, 0, 0], 6)]
        self.assertEqual(l, expected_teams)

    def test_gen_team_fail(self):
        """Test case for failed generation of teams when argument passed in is not integer greater than 0"""
        bt = BattleTower(Battle())                                      # bt is BattleTower object
        self.assertEqual(len(bt.tower_teams), 0)                        # bt initially has 0 team
        self.assertEqual(len(bt.lives_left), 0)                         # bt initailly has no records of lives for teams
        self.assertRaises(ValueError, lambda: bt.generate_teams(1.25))  # ValueError raised when argument is not integer
        self.assertRaises(ValueError, lambda: bt.generate_teams(0))     # ValueError raised when argument is not integer greater than 0
        self.assertRaises(ValueError, lambda: bt.generate_teams(-2))    # ValueError raised when argument is not integer greater than 0
        self.assertEqual(len(bt.tower_teams), 0)                        # bt initially has 0 team
        self.assertEqual(len(bt.lives_left), 0)                         # bt initailly has no records of lives for teams
        

class TestTowerIteratorInit(BaseTest):
    """3 test cases for __init__ method in BattleTowerIterator in different scenarios (succesful/fail/None)"""
    def test_init_successful(self):
        """Test case calling __iter__ on BattleTower object which indirectly calls __init__ for BattleTowerIterator successfully"""
        RandomGen.set_seed(0)
        bt = BattleTower(Battle())                                      # bt is a BattleTower object
        team = PokeTeam("Ash",[1,1,2,0,1],0,PokeTeam.AI.ALWAYS_ATTACK)  # team is a PokeTeam object
        bt.set_my_team(team)                                            # set_my_team with team as argument
        bt.generate_teams(5)                                            # generate 5 random teams for tower_teams in BattleTower
        # Teams generated for BattleTower (team_numbers, lives)
        # [0, 2, 0, 0, 2], 3    Name: Team 0
        # [1, 1, 0, 1, 0], 7    Name: Team 1
        # [0, 2, 0, 2, 0], 10   Name: Team 2
        # [0, 3, 0, 0, 1], 9    Name: Team 3
        # [0, 1, 3, 0, 0], 6    Name: Team 4
        it = iter(bt)                                                   # get the iterator object for BattleTower object (BattleTowerIterator)
        self.assertEqual(it.battle_tower, bt)                           # BattleTowerIterator iterates through the same BattleTower object passed
        self.assertEqual(it.my_team,team)                               # BattleTowerIterator has the same team for my_team as the BattleTower object
        self.assertEqual(it.tower_teams, bt.tower_teams)                # BattleTowerIterator will iterate through the tower_teams generated by the BattleTower object
        self.assertEqual(it.battle_instance, bt.battle_instance)        # BattleTowerIterator uses the same battle instance passed into BattleTower object for battling
        self.assertEqual(it.lives_left, bt.lives_left)                  # BattleTowerIterator will iterate through the lives_left of the teams generated by the BattleTower object
        
    def test_init_fail(self):
        """Test case of failed initialisation of BattleTowerIterator when wrong argument is passed as argument"""
        self.assertRaises(ValueError, lambda: BattleTowerIterator(Battle()))    # ValueError raised when argument of non BattleTower object is passed as argument for initialisation of BattleTowerIterator

    def test_init_none(self):
        """Test case of failed initialisation of BattleTowerIterator when wrong argument is passed as argument"""
        self.assertRaises(ValueError, lambda: BattleTowerIterator(None))        # BattleTowerIterator raises ValueError when argument is not BattleTower object

class TestTowerIteratorNext(BaseTest):
    """3 test cases for __next__ method in BattleTowerIterator under different scenarios"""
    def test_next_single_team(self):
        """Test case for calling next for BattleTower with 1 team only, and my_team always win"""
        RandomGen.set_seed(112003456)
        bt = BattleTower(Battle())                                      # bt is a BattleTower object
        team = PokeTeam("Ash",[1,1,2,0,1],0,PokeTeam.AI.ALWAYS_ATTACK)  # team is a PokeTeam object
        bt.set_my_team(team)                                            # set_my_team with team as argument
        bt.generate_teams(1)                                            # generate 1 team for BattleTower
        # Team generated for BattleTower (team_number, lives)
        # [0, 2, 1, 0, 1], 3    Name: Team 0
        it = iter(bt)
        res, me, tower, lives = next(it)                        # call next() directly for BattleTowerIterator
        self.assertEqual((res,lives), (1,2))                    # the result of battle and lives of tower_team should be (1,2)
        res, me, tower, lives = next(it)                        # call next() directly for BattleTowerIterator
        self.assertEqual((res,lives), (1,1))                    # the result of battle and lives of tower_team should be (1,1)
        res, me, tower, lives = next(it)                        # call next() directly for BattleTowerIterator
        self.assertEqual((res,lives), (1,0))                    # the result of battle and lives of tower_team should be (1,0)
        self.assertEqual(len(bt.tower_teams), 0)                # team with 0 lives is removed from the tower_team
        self.assertRaises(StopIteration, lambda: next(it))      # StopIteration raised after tower_team has no lives left

    def test_next_multiple_teams(self):
        """Test case for iterating through BattleTower with 5 teams, and my_team always wins"""
        RandomGen.set_seed(0)
        bt = BattleTower(Battle())                                      # bt is a BattleTower object
        team = PokeTeam("Ash",[1,1,2,0,1],0,PokeTeam.AI.ALWAYS_ATTACK)  # team is a PokeTeam object
        bt.set_my_team(team)                                            # set_my_team with team as argument
        bt.generate_teams(5)                                            # generate 5 random teams for tower_teams in BattleTower
        # Teams generated for BattleTower (team_numbers, lives)
        # [0, 2, 0, 0, 2], 3    Name: Team 0
        # [1, 1, 0, 1, 0], 7    Name: Team 1
        # [0, 2, 0, 2, 0], 10   Name: Team 2
        # [0, 3, 0, 0, 1], 9    Name: Team 3
        # [0, 1, 3, 0, 0], 6    Name: Team 4

        # the expected results for team 0-4, each column represents each team
        expected_res = [(1, 2),(1, 6),(1, 9),(1, 8),(1, 5),
                        (1, 1),(1, 5),(1, 8),(1, 7),(1, 4),
                        (1, 0),(1, 4),(1, 7),(1, 6),(1, 3),
                               (1, 3),(1, 6),(1, 5),(1, 2),
                               (1, 2),(1, 5),(1, 4),(1, 1),
                               (1, 1),(1, 4),(1, 3),(1, 0),
                               (1, 0),(1, 3),(1, 2),
                                      (1, 2),(1, 1),
                                      (1, 1),(1, 0),
                                      (1, 0)]
        l = []
        for res, me, tower, lives in bt:    # iterate through BattleTower. The for loop is calling next() for BattleTowerIterator every loop
            l.append((res,lives))           # append the obtained results and lives for each iterator for comparison later
        self.assertEqual(expected_res, l)   # expect iteration to stop until all teams has no lives left


    def test_next_lose(self):
        """Test case for iterating through BattleTower with 5 teams, and my_team loses"""
        RandomGen.set_seed(5668)
        bt = BattleTower(Battle())                                      # bt is a BattleTower object
        team = PokeTeam("Ash",[1,1,2,0,1],0,PokeTeam.AI.ALWAYS_ATTACK)  # team is a PokeTeam object
        bt.set_my_team(team)                                            # set_my_team with team as argument
        bt.generate_teams(5)                                            # generate 5 random teams for tower_teams in BattleTower
        # Teams generated for BattleTower
        # [1, 0, 0, 2, 0], 7    Name: Team 0
        # [0, 0, 3, 1, 1], 9    Name: Team 1
        # [1, 3, 0, 1, 1], 5    Name: Team 2
        # [1, 0, 2, 1, 2], 5    Name: Team 3
        # [1, 0, 1, 1, 2], 8    Name: Team 4
        expected_res = [(1, 6),(1, 8),(1, 4),(1, 4),(1, 7),
                        (1, 5),(1, 7),(1, 3),(1, 3),(1, 6),
                        (1, 4),(1, 6),(1, 2),(1, 2),(2, 6)]
        l = []
        for res, me, tower, lives in bt:    # iterate through BattleTower. The for loop is calling next() for BattleTowerIterator every loop
            l.append((res,lives))           # append the obtained results and lives for each iterator for comparison later
        self.assertEqual(expected_res, l)   # expect the iteration to stop when result is 2 (my_team loses)
        
        
class TestTowerIteratorAvoidDuplicates(BaseTest):
    """3 test cases for avoid_duplicates in BattleTowerIterator under different scenarios"""
    def test_all_duplicates(self):
        """Test case for removing multiple teams with duplicates"""
        RandomGen.set_seed(5668)
        bt = BattleTower(Battle())                                      # bt is a BattleTower object
        bt.generate_teams(5)                                            # generate 5 random teams for tower_teams in BattleTower
        it = iter(bt)
        # Teams generated for BattleTower (Before avoid_duplicates)
        # [1, 0, 0, 2, 0], 7    Name: Team 0
        # [0, 0, 3, 1, 1], 9    Name: Team 1
        # [1, 3, 0, 1, 1], 5    Name: Team 2
        # [1, 0, 2, 1, 2], 5    Name: Team 3
        # [1, 0, 1, 1, 2], 8    Name: Team 4
        l = []
        # for loop to get all items in the tower_teams and lives_left queue
        for _ in range(len(bt.tower_teams)):
            team = bt.tower_teams.serve()           # get the head of queue for tower_teams
            lives = bt.lives_left.serve()           # get the head of queue for lives_left
            l.append((team.team_numbers,lives))     # get the team numbers of team and lives then put it into a list for comparison later
            bt.tower_teams.append(team)             # put the team back to the end of queue for tower_teams
            bt.lives_left.append(lives)             # put the lives back to the end of queue for lives_left
        expected_teams = [
            ([1, 0, 0, 2, 0], 7),
            ([0, 0, 3, 1, 1], 9),
            ([1, 3, 0, 1, 1], 5),
            ([1, 0, 2, 1, 2], 5),
            ([1, 0, 1, 1, 2], 8)]
        self.assertEqual(l, expected_teams)         # compare the teams, lives and the expected teams result
        it.avoid_duplicates()                       # call avoid_duplicates

        # Teams in BattleTower (after avoid_duplicates)
        # No teams left
        self.assertEqual(len(bt.tower_teams), 0)    # tower_teams now has length 0 since all teams are removed
        self.assertEqual(len(bt.lives_left), 0)     # lives_left now has length 0 since all teams and its corresponding lives are removed

    def test_some_duplicates(self):
        """Test case for removing team with duplicate for tower_team consisting of one team only"""
        RandomGen.set_seed(1136)
        bt = BattleTower(Battle())                                      # bt is a BattleTower object
        bt.generate_teams(4)                                            # generate 4 random teams for tower_teams in BattleTower
        it = iter(bt)
        # Teams generated for BattleTower (Before avoid_duplicates)
        # [1, 0, 1, 1, 0], 9    Name: Team 0
        # [0, 2, 1, 2, 0], 9    Name: Team 1
        # [4, 1, 0, 0, 1], 5    Name: Team 2
        # [1, 0, 0, 2, 0], 6    Name: Team 3
        l = []
        # for loop to get all items in the tower_teams and lives_left queue
        for _ in range(len(bt.tower_teams)):
            team = bt.tower_teams.serve()           # get the head of queue for tower_teams
            lives = bt.lives_left.serve()           # get the head of queue for lives_left
            l.append((team.team_numbers,lives))     # get the team numbers of team and lives then put it into a list for comparison later
            bt.tower_teams.append(team)             # put the team back to the end of queue for tower_teams
            bt.lives_left.append(lives)             # put the lives back to the end of queue for lives_left
        expected_teams =[ 
            ([1, 0, 1, 1, 0], 9), 
            ([0, 2, 1, 2, 0], 9),
            ([4, 1, 0, 0, 1], 5),
            ([1, 0, 0, 2, 0], 6)]
        self.assertEqual(l, expected_teams)         # compare the teams, lives and the expected teams result
        it.avoid_duplicates()                       # call avoid_duplicates

        # Teams in BattleTower (after avoid_duplicates)
        # [1, 0, 1, 1, 0], 9    Name: Team 0
        self.assertEqual(len(bt.tower_teams), 1)                                    # expect only one team left in tower_teams
        self.assertEqual(len(bt.lives_left), 1)                                     # expect only one record of lives left in lives_left
        actual_res = (bt.tower_teams.serve().team_numbers,bt.lives_left.serve())    # get the team numbers of the team left in tower_teams and its lives in lives_left
        self.assertEqual(actual_res, ([1, 0, 1, 1, 0], 9))                          # compare the actual outcome with the expected results
        
    def test_no_duplicates(self):
        """Test case for removing no teams when there is no duplicated teams"""
        RandomGen.set_seed(1136)
        bt = BattleTower(Battle())                                      # bt is a BattleTower object
        bt.generate_teams(4)                                            # generate 4 random teams for tower_teams in BattleTower
        it = iter(bt)
        # Teams generated for BattleTower (Before avoid_duplicates)
        # [1, 1, 1, 0, 0], 9    Name: Team 0
        # [1, 1, 1, 0, 0], 9    Name: Team 1
        # [1, 1, 1, 0, 0], 5    Name: Team 2
        # [1, 1, 1, 0, 0], 6    Name: Team 3
        l = []
        # for loop to get all items in the tower_teams and lives_left queue
        for i in range(len(bt.tower_teams)):
            bt.tower_teams.serve()                  # get the head of queue for tower_teams
            lives = bt.lives_left.serve()           # get the head of queue for lives_left
            # create poke team to be duplicated for the whole tower team that has no duplicating pokemon
            team = PokeTeam("Team" + str(i), [1,1,1,0,0], 0, PokeTeam.AI.ALWAYS_ATTACK) 
            l.append(([1, 1, 1, 0, 0],lives))       # get the team numbers of team and lives then put it into a list for comparison later
            bt.tower_teams.append(team)             # add the team to the end of queue for tower_teams
            bt.lives_left.append(lives)             # put the lives back to the end of queue for lives_left

        expected_teams =[ 
            ([1, 1, 1, 0, 0], 9),
            ([1, 1, 1, 0, 0], 9),
            ([1, 1, 1, 0, 0], 5),
            ([1, 1, 1, 0, 0], 6)]
        self.assertEqual(l, expected_teams)         # compare the teams, lives and the expected teams result
        it.avoid_duplicates()                       # call avoid_duplicates

        # Teams in BattleTower (after avoid_duplicates)
        # [1, 1, 1, 0, 0], 9    Name: Team 0
        # [1, 1, 1, 0, 0], 9    Name: Team 1
        # [1, 1, 1, 0, 0], 5    Name: Team 2
        # [1, 1, 1, 0, 0], 6    Name: Team 3
        self.assertEqual(len(bt.tower_teams), 4)                                        # expect no teams removed in tower_teams (length remains at 4)
        self.assertEqual(len(bt.lives_left), 4)                                         # expect no record of lives removed in lives_left (length remains at 4)
        for i in range(len(bt.tower_teams)):
            actual_res = (bt.tower_teams.serve().team_numbers, bt.lives_left.serve())   # get the actual team and its lives in tuple form
            self.assertEqual(expected_teams[i], actual_res)                             # compare all teams and its lives to the expected teams

        
        