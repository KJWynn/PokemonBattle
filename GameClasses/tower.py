from __future__ import annotations
"""
This module implements the battle tower feature in a Pokemon game.
Battle mechanics from the battle.py file are used in this module, as well as ADTs provided in the template
for iterating through teams in the battle tower for battling.
Each function has docstring which specifies details such as complexity of the function.
Unittests (Test cases) for the module will be located under tests\test_tower.py

"""
__author__ = "Scaffold by Jackson Goerner, Code by Lim Yi Xuan, Tee Zhi Hui"

from queue_adt import CircularQueue
from random_gen import RandomGen

from poke_team import PokeTeam
from battle import Battle

class BattleTower(Battle, PokeTeam):
    """
    Class for generating battle tower

    Complexity: All functions, unless stated otherwise, have best/worst case complexity of O(1)
    """

    def __init__(self, battle: Battle|None=None) -> None:
        """ 
        This method is invoked automatically to set a newly created BattleTower object's attributes to their initial state.

        :param: battle (An object of Battle or None) 

        :pre: battle must be the object of the Battle class or None

        :return: None
        """
        try:
            assert isinstance(battle, Battle) or battle is None, "battle must be Battle object or None type"
        except AssertionError as e:
            raise ValueError(e)

        battle = Battle() if battle is None else battle # If battle is none, generate a battle instance, else just let battle be battle
        self.battle_instance = battle
        self.my_team = None
        self.tower_teams = CircularQueue(0)
        self.lives_left = CircularQueue(0)
    
    def set_my_team(self, team: PokeTeam) -> None:
        """ 
        This method set the argument team as my poke team

        :param arg1: team (PokeTeam) - (An object of PokeTeam)

        :pre: team must be the object of PokeTeam

        :return: None
        """
        try:
            assert isinstance(team, PokeTeam), "team must be PokeTeam object"
        except AssertionError as e:
            raise ValueError(e)
        self.my_team = team
    
    def generate_teams(self, n: int) -> None:
        """ 
        This method randomly generate n teams for the tower

        :param arg1: team (PokeTeam) - (An object of PokeTeam)

        :pre: n must greater than 0 and must be an integer

        :return: None
        
        :complexity: Best O(N*M^2), where N is length of CircularQueue, M is sum of team_members
                     Worst O(N*M^2), where N is length of CircularQueue, M is sum of team_members
        """
        try:
            assert n > 0 and isinstance(n,int), " the number of teams must be an integer greater than 0"
        except AssertionError as e:
            raise ValueError(e)

        self.tower_teams = CircularQueue(n)
        self.lives_left = CircularQueue(n)
        
        for i in range (n): # O(N), where N is length of CircularQueue
            team_name = "Team " + str(i)
            battle_mode = RandomGen.randint(0,1)
            team = self.random_team(team_name, battle_mode) # O(N^2), where N is sum of team_numbers
            lives = RandomGen.randint(2,10) # spec sheet specifies team generation before lives so that random generation is not interfered
            self.tower_teams.append(team)
            self.lives_left.append(lives)

    def __iter__(self) -> BattleTowerIterator:
        """ 
        This magic method make the object of BattleTower iterable by returning BattleTowerIterator instance

        :param: None

        :pre: None

        :return: BattleTowerIterator
        """
        return BattleTowerIterator(self)

class BattleTowerIterator(BattleTower):
    """ Class for making battle tower iterable and avoid team with duplications """

    def __init__(self, battle_tower: BattleTower) -> None:
        """ 
        This method is invoked automatically to set a newly created BattleTowerIterator object's attributes to their initial state.

        :param: battle_tower (An object of BattleTower) 

        :pre: battle_tower must be the object of the BattleTower class, and can't be None

        :return: None
        """
        try:
            assert battle_tower is not None and isinstance(battle_tower, BattleTower), "BattleTowerIterator only accepts BattleTower object to be iterated"
        except AssertionError as e:
            raise ValueError(e)
        self.my_team = battle_tower.my_team
        self.tower_teams = battle_tower.tower_teams
        self.battle_tower = battle_tower
        self.battle_result = 1
        self.battle_instance = battle_tower.battle_instance
        self.lives_left = battle_tower.lives_left

    def __next__(self) -> tuple:
        """
        This magic method retrieves next item from the iterator

        :param: None

        :pre: None

        :return: returns the next item from the iterator until it raises StopIteration
        
        :complexity: Best O(R*N), where R is number of rounds until battle ends, N is the length of PokeTeamMembers
                     Worst O(R*N^2), where R is number of rounds until battle ends, N is the length of PokeTeamMembers    
        """ 
        # my team and the queue containing all the opposing teams
        my_team = self.my_team
        num_teams = len(self.tower_teams)

        # while no battle lost and there exists teams to fight in the tower,
        if self.battle_result != 2 and num_teams > 0:
            opponent = self.tower_teams.serve()
            opponent_lives = self.lives_left.serve()
            print(f"Opponent has {opponent_lives} lives")
            self.battle_result = self.battle_instance.battle(my_team, opponent) #? O(R*M^2), where R is number of rounds until battle ends, M is the length of PokeTeamMembers

            # After each battle, regenerate
            my_team.regenerate_team() #? Worst O(N^2 + M^2), where N is sum of team_numbers and M is length of pokeTeamMembers
            opponent.regenerate_team()

            # win/draw: opponent loses live
            if self.battle_result != 2:
                opponent_lives -= 1
                # only append tower_teams that has more than 0 lives
                if opponent_lives != 0:
                    self.tower_teams.append(opponent)
                    self.lives_left.append(opponent_lives)


            # return tuple containing battle result, player team, tower_team, tower_team_lives_left)
            return ((self.battle_result, my_team, opponent, opponent_lives))

        if self.battle_result == 2:
            raise StopIteration ("Sorry, you lost!")          

        if len(self.tower_teams) == 0:
            raise StopIteration("You are victorious!")
        
        
    def avoid_duplicates(self) -> None:
        """ 
        This method remove team that has duplicated pokemon type

        :param: None

        :pre: None

        :return: None

        :complexity: Best O(N*P) where N is the number of trainers remaining in the battle tower and P is the limit on the number of pokemon per team.
                     Worst O(N*P) where N is the number of trainers remaining in the battle tower and P is the limit on the number of pokemon per team.
        """
        i = 0
        ori_length = len(self.tower_teams)
        while i < ori_length:  # O(N)
            # get the current team and its lives
            current_team = self.tower_teams.serve()
            current_team_lives = self.lives_left.serve()
            # get the current team's team numbers to check for duplicates
            current_team_num = current_team.team_numbers
            # reset has_duplicates to False and num to 0 for every team in the queue
            has_duplicates = False
            num = 0
            # check for duplicating pokemon in current team
            while not has_duplicates and num in range(len(current_team_num)): # O(P)
                if current_team_num[num] > 1:
                    has_duplicates = True
                else:
                    num += 1
            if not has_duplicates:
                # only add the team and lives back to queue if there is no duplicates
                self.lives_left.append(current_team_lives)
                self.tower_teams.append(current_team)
            i += 1  # check the next item in Queue

    def sort_by_lives(self):
        # 1054
        raise NotImplementedError()
