from __future__ import annotations
"""
This module implements the tournament mechanics.
Methods and features required during tournament between various PokeTeams are implemented
following the instructions of the specifications.
Each function has docstring which specifies details such as complexity of the function.
Unittests (Test cases) for the module will be located under tests\test_tournament.py

"""
__author__ = "Scaffold by Jackson Goerner, Code by Khor Jia Wynn"

from poke_team import Criterion, PokeTeam
from battle import Battle
from linked_list import LinkedList
from stack_adt import ArrayStack
from random_gen import *
from bset import BSet


class Tournament:

    def __init__(self, battle: Battle | None = None) -> None:
        """  
        This method is invoked automatically to set a newly created tournament object's attributes to their initial states.

        :param arg1: battle (Battle) - the battle instance, defaults to None

        :pre: None

        :return: none

        :complexity: Best O(1) 
                     Worst O(1) 
        """       

        # generate a new battle instance if no battle instance is passed
        if battle is None:
            self.battle = Battle(verbosity=0)
        else:
            self.battle = battle
        
        # initialise attributes to appropriate values
        self.battle_mode = None
        self.stack1 = None
        self.stack2 = None
        self.count = 0

    def set_battle_mode(self, battle_mode: int) -> None: 
        """
        Set the battle mode for all randomly generated teams. This should be called before start_tournament.

        :param arg1: battle_mode (int) - 0 or 1 or 2

        :pre: battle mode can only be 0 or 1 or 2

        :return: None

        :complexity: Best O(1)
                     Worst O(1)
        """     
        # check for preconditions
        try:
            assert type(battle_mode) == int and 0 <= battle_mode <= 2, "Battle mode should be 0, 1 or 2"
        except Exception as e:
            raise ValueError(e)
        # set the battle mode
        self.battle_mode = battle_mode

    def is_valid_tournament(self, tournament_str: str) -> bool:
        """ 
        Returns true if the tournament_str passed represents a valid tournament.

        :param arg1: tournament_str (str) - string describing the draw

        :pre: None

        :return: bool - True if the string passed is valid

        :complexity: Best O(N), where N is length of the tournament_str
                     Worst O(N), where N is length of the tournament_str
        """
        # preprocess tournament string passed in
        split_str = tournament_str.split(" ")   # O(N), where N is length of tournament string
        stack = ArrayStack(len(split_str))      # create Stack with length equal to the list containing team names and '+'
        
        if split_str[0] == '+': # first two needs to be team names(str)
            return False

        for str in split_str:   # O(N)
            # push the current string in the list into stack if string is not "+"
            if str != "+":
                stack.push(str)

            # "+" means two teams battle with one winner, so pop() removes one player (loser) from stack, leaving another player (winner) in the stack
            else:
                stack.pop() 

            # Stack will be empty when there are more battles than poketeams. 
            if stack.is_empty():
                return False

        # At the end of tournament there should only be one winner, we expect length of stack to be 1
        if len(stack) != 1:
            return False
        return True

    def is_balanced_tournament(self, tournament_str: str) -> bool:
        # 1054 only
        raise NotImplementedError()

    def start_tournament(self, tournament_str: str) -> None:
        """ 
        Generates random teams based on the tournament_str. 

        :param arg1: tournament_str (str) - string describing the draw

        :pre: tournament_str is validated by calling self.is_valid_tournament(tournament_str)

        :return: None

        :complexity: Best O(N), where N is length of the tournament_str
                     Worst O(N), where N is length of the tournament_str
        """        

        # check for precondition (valid tournament string)
        if not self.is_valid_tournament(tournament_str): # O(N)
            raise ValueError("Invalid tournament str")

        # set criterion value as 0 by default
        true_crit = 0
        # get criterion value and criterion if tournament is in battle mode 2
        if self.battle_mode == 2:
            criteria = list(Criterion)
            try:
                print("Please enter criterion to be used to sort PokeTeam")
                crit = int(input("LV: 1/DEF: 2/HP: 3/SPD: 4 "))
                assert isinstance(crit, int) and 1 <= crit <= len(criteria)
            except:
                raise ValueError("Please enter an integer from 1 to 4")
            else:
                true_crit = criteria[crit-1]

        # replaces poketeam names(str) with their poketeam instances(PokeTeam)
        split_str = tournament_str.split(" ")   # O(N)
        # generate PokeTeam object based on PokeTeam names in the tournament string
        for i in range(len(split_str)):         # O(N)
            if split_str[i] != "+":             # O(M), where M is the length of the shorter string, in this case 1
                # generate random team for each PokeTeam name in tournament string
                split_str[i] = PokeTeam.random_team(split_str[i], self.battle_mode, criterion = true_crit) # O(N^2)

        # creates main stack to be operated on
        self.stack1 = ArrayStack(len(split_str)) # O(N)

        # push strings from the list of split tournament string into stack for later operation
        for i in range(len(split_str)-1, -1, -1): # O(N)
            self.stack1.push(split_str[i]) 

        # creates helper stack to store intermediate winners of each battle
        self.stack2 = ArrayStack(len(split_str)) # O(N)

    def advance_tournament(self) -> tuple[PokeTeam, PokeTeam, int] | None:
        """ 

        Simulates one battle of the tournament, following the order of the previously given tournament string (Each + represents a game, 
        and each game is simulated from left to right). If no games are remaining, None is returned.

        :param: None

        :pre: None

        :return: tuple containing the two PokeTeams instances and an battle result(int) or None if no games remain

        :complexity: Best O(R*N), where R is number of rounds until battle ends, N is the length of PokeTeamMembers
                     Worst O(R*N^2), where R is number of rounds until battle ends, N is the length of PokeTeamMembers
        """ 
        winner_found = False    # initialise flag "winner_found" as False

        # returns None if stack is empty and winner is found (no games remain)
        if self.stack2.is_empty() and winner_found: 
            return None

        # operate on stack2 when there are indirect advancements (more than one '+' after both PokeTeam names)
        # battles occur in stack2 self.count times, where self.count is the number of '+' after the first '+'
        # e.g. for + + + , self.count = 2
        # A B + C D + E F + + + G H + + would be: [(A+B) + ((C+D)+(E+F))] + (G+H)
        # "A B +"=(A+B),"C D +"=(C+D), "E F +"=(E+F), "+"=(C+D)+(E+F), "+"=(A+B) + ((C+D)+(E+F)), "G H +"=(G+H), "+"=(A+B + ((C+D)+(E+F))) + (G+H)
        if self.count > 0:
            # retrieve both teams to battle
            second_team = self.stack2.pop() 
            first_team = self.stack2.pop() 

            # if stack2 is empty then current battle would be final battle, winner would be found
            if self.stack2.is_empty():
                winner_found = True

            # both teams battle, then winner would be pushed to stack2
            battle_result = self.battle.battle(first_team, second_team) # O(B)
            if battle_result == 0 or battle_result == 1:
                self.stack2.push(first_team)
            elif battle_result == 2:
                self.stack2.push(second_team)

            # decrement count as one '+' has been considered
            self.count -=1
            # return tuple containing both teams before battle, and their battle result
            return ((first_team, second_team, battle_result))


        # operate on stack1 for direct advancements (one '+' after both PokeTeam names) (stack1 should eventually become empty)
        elif not self.stack1.is_empty():
            
            # retrieve both teams from stack1
            first_team = self.stack1.pop()
            second_team = self.stack1.pop()

            # remove '+' from stack1
            self.stack1.pop()
            
            # check how many pluses come after the teams
            if not self.stack1.is_empty():
                peek_next = self.stack1.peek()
            else:
                peek_next = None
            # count how many "+" comes after the teams
            while peek_next == "+":                 # loops until '+' is not found anymore
                self.count +=1                      # increment count of '+' if found
                self.stack1.pop()                   # remove '+' from stack1
                if not self.stack1.is_empty():      # continue to search if there are more '+'
                    peek_next = self.stack1.peek()  # peek at the next item to check if its '+'
                else:
                    peek_next = None                # stops peeking when at the bottom of stack
              
            # both teams battle in stack1
            battle_result = self.battle.battle(first_team, second_team)

            # push winner of battle into stack2 based on battle result
            if battle_result == 0 or battle_result == 1:
                self.stack2.push(first_team)
            elif battle_result == 2:
                self.stack2.push(second_team)

            # return both teams before battle, and their battle result as tuple
            return ((first_team, second_team, battle_result))



    def linked_list_of_games(self) -> LinkedList[tuple[PokeTeam, PokeTeam]]:
        """ 

        Returns LinkedList containing a tuple of the two PokeTeam instances for each battle that occured in the tournament.

        :param: None

        :pre: None

        :return: LinkedList containing tuples of the two PokeTeams instances

        :complexity: Best O(R*N * M), where R is number of rounds in a battle, N is the length of pokeTeamMembers and M is the number of battles
                     Worst O(R*N^2 * M), where R is number of rounds in a battle, N is the length of pokeTeamMembers and M is the number of battles
        """         
        l = LinkedList()
        while True:
            # keep advancing tournament until no games remain
            res = self.advance_tournament()
            if res is None:
                break
            # add to the front of LinkedList the tuple of two PokeTeam objects battling in the tournament for each advanced tournament
            l.insert(0, (res[0], res[1]))
        return l

    def linked_list_with_metas(self) -> LinkedList[tuple[PokeTeam, PokeTeam, list[str]]]:
        """
        Returns a linked list, containing a tuple for each match of the tournament, in the same order as linked_list_of_games does. Additionally in the tuple
        is a list of strings representing PokeTypes which, for the particular battle listed, are not present in either PokeTeam, but were represented in
        at least one of the PokeTeams beaten by them in the previous matchup.

        :param: None

        :pre: None

        :return: LinkedList containing tuples of the two PokeTeams instances and the list of poketypes(str) which were not present in this pair of PokeTeams,\
                 but was present in at least of the teams beaten by them in the previous matchup.

        :complexity: Best O(R*N * M), where R is number of rounds in a battle, N is the length of pokeTeamMembers and M is the number of battles
                     Worst O(R*N^2 * M), where R is number of rounds in a battle, N is the length of pokeTeamMembers and M is the number of battles
        """
        # initialise local variables
        l = LinkedList()
        latest_meta = BSet()
        all_poketypes = BSet()
        battle_poke = BSet()
        absent_poke = BSet()
        losing_team = None
        winning_team = None

        # set all_poketypes as {1,2,3,4,5}
        # all_poketypes: 11111
        for i in range(1, 6):
            all_poketypes.add(i)

        while True: # O(M)
            # Reset bsets for each advancement
            winner_bset = BSet()
            loser_bset = BSet()
            winner_prev_bset = BSet()
            loser_prev_bset = BSet()

            # obtain result for advancing tournament
            res = self.advance_tournament() # O(R*N^2 * M), where R is number of rounds in a battle, N is the length of pokeTeamMembers and M is the number of battles

            # exit loop when no game remains (no result)
            if res is None:
                break

            # set winning and losing team based on the battle result between two teams
            if res[2] == 1 or res[2] == 0:
            # winning team is team 1 for result draw and team 1 wins
                losing_team = res[1]
                winning_team = res[0]
            elif res[2] == 2:
            # winning team is team2 for result team 2 wins
                losing_team = res[0]
                winning_team = res[1]

            # if the winning team has not won against any team, update won_against to the current losing team
            if winning_team.won_against is None:
                winning_team.won_against = losing_team
                updated = True
            else: # if winner of this round won the previous round, don't update self.won_against yet.
                updated = False

            
            # only enter if both winning and losing team has won_against other teams,
            # so that we can get the pokemon types that are in the meta based on the teams that they had won against before.
            # meta is pokemon types that are absent in either current match teams, but are present in some of the teams that they have won against.
            if winning_team.won_against is not None and losing_team.won_against is not None:
                # create BSet for both teams then find absent poke in this pair
                for i in range(1, 6):
                    if winning_team.team_numbers[i - 1] != 0:
                        winner_bset.add(i)
                    if losing_team.team_numbers[i - 1] != 0:
                        loser_bset.add(i)
                # get pokemons that has battled for winning and losing teams into battle_poke
                battle_poke = winner_bset.union(loser_bset)
                # get absent pokemon using difference on all_poketypes with battle_poke
                absent_poke = all_poketypes.difference(battle_poke)

                # update latest_meta as the pokemon types that current match teams has won against
                winner_prev_win = winning_team.won_against
                loser_prev_win = losing_team.won_against
                for i in range(1, 6):
                    if winner_prev_win.team_numbers[i - 1] != 0:
                        winner_prev_bset.add(i)
                    if loser_prev_win.team_numbers[i - 1] != 0:
                        loser_prev_bset.add(i)
                # latest meta is the pokemon types that either current match teams has won against
                latest_meta = winner_prev_bset.union(loser_prev_bset)

                # obtain the list of strings representing poketypes that are in absent_poke and latest_meta
                lst_of_types = []
                poke_type = ""
                for i in range(1, 6):
                    # check if absent_poke is present in meta
                    if (i in absent_poke) and (i in latest_meta):
                        if i == 1:
                            poke_type = "FIRE"
                        elif i == 2:
                            poke_type = "GRASS"
                        elif i == 3:
                            poke_type = "WATER"
                        elif i == 4:
                            poke_type = "GHOST"
                        elif i == 5:
                            poke_type = "NORMAL"
                        # append the string representing PokeType
                        lst_of_types.append(poke_type)

                # add the tuple for the match with list of types to the start of LinkedList
                l.insert(0, (res[0], res[1], lst_of_types))

                # At this point, now that meta has been updated, we can safely update the winner's .won_against
                if not updated:
                    winning_team.won_against = losing_team
            else:
                # add the tuple of result for the match to the start of LinkedList
                l.insert(0, (res[0], res[1], []))

        # return the LinkedList containing tuple for each match of tournament with list of types that are meta.
        return l

    def flip_tournament(self, tournament_list: LinkedList[tuple[PokeTeam, PokeTeam]], team1: PokeTeam,
                        team2: PokeTeam) -> None:
        # 1054
        raise NotImplementedError()
