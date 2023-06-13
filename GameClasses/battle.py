"""
This module implements battling mechanics between PokeTeams using functions that are
specified in the specifications, as well as additional functions added for ease of readability.
Each function has docstring which specifies complexity of the function.
Unittests (Test cases) for the module will be located under tests\test_battle.py

"""
__author__ = "Scaffold by Jackson Goerner, Code by Lim Yi Xuan, Tee Zhi Hui, Khor Jia Wynn"

from pokemon_base import PokemonBase
from poke_team import Action, PokeTeam
from print_screen import print_game_screen

class Battle:
    """Battle logics and battle mechanics are implemented in this class for each battle object"""
    def __init__(self, verbosity=0) -> None:
        """  
        This method is invoked automatically to set a newly created battle object's attributes to their initial states.

        :param: verbosity (int) - optional switch to enable more printing/logging, defaults to 0

        :pre: None

        :return: None

        :complexity: Best O(1), this function only assign values to variables
                     Worst O(1), this function only assign values to variables
        """
        self.result = None
        self.team1 = None
        self.team2 = None
        self.team1_poke = None
        self.team2_poke = None
        self.choice1 = None
        self.choice2 = None

    def print_screen(self) -> None:
        """ 
        Display the current game screen and status of the pokemon as well as their team.

        :param: None

        :pre: None

        :return: None 

        :complexity: Best O(N*M), where N is length of lines(height) for pokemon sprite, M is length of characters in line (width)for sprite
                     Worst O(N*M), where N is length of lines(height) for pokemon sprite, M is length of characters in line (width)for sprite
        """
        # get the remaining number of pokemon in the teams
        remaining_team1_poke = len(self.team1.pokeTeamMembers) + 1
        remaining_team2_poke = len(self.team2.pokeTeamMembers) + 1
        # print the game screen
        print_game_screen(  self.team1_poke.poke_name, self.team2_poke.poke_name, self.team1_poke.get_hp(), self.team1_poke.hp,\
                            self.team2_poke.get_hp(), self.team2_poke.hp, self.team1_poke.get_level(), self.team2_poke.get_level(),\
                            self.team1_poke.status, self.team2_poke.status, remaining_team1_poke, remaining_team2_poke)
        # display the current state of both teams
        print(self.team1)
        print(self.team2)

    def swap(self, team: PokeTeam, poke: PokemonBase) -> None:
        """  
        Swap returns current pokemon to its team, then another pokemon is retrieved from the team (could be same pokemon).

        :param arg1: team (PokeTeam) - the PokeTeam instance to return the pokemon to and to retrieve pokemon from
        :param arg2: poke (PokemonBase) - the Pokemon instance to get swapped out (return to its field)

        :pre: None

        :return: None
        
        :complexity: Best O(N), where N is the length of pokeTeamMembers
                     Worst O(N^2), where N is the length of pokeTeamMembers
        """
        print(f"{team.team_name} swapped out {poke} and got ", end = "")
        # return current pokemon back to its team
        team.return_pokemon(poke)
        # retrieve a pokemon from the team again
        poke = team.retrieve_pokemon()
        # display the pokemon retrieved
        print(poke)
        # set pokemon retrieved as team1_poke or team2_poke depending on its team
        if team == self.team1:
            self.team1_poke = poke
        elif team == self.team2:
            self.team2_poke = poke

    def special(self, team: PokeTeam, poke: PokemonBase) -> None:
        """  
        Returns current pokemon, do a special action on the team (depending on battle mode), then retrieve a new pokemon from the team.
        
        :param arg1: team (PokeTeam) - the PokeTeam instance to return the pokemon to and to retrieve pokemon from
        :param arg2: poke (PokemonBase) - the Pokemon instance to get swapped out (return to its field)
        
        :pre: None
        
        :return: None
        :complexity: Best O(N) where N is length of pokeTeamMembers
                     Worst O(N^2), where N is length of pokeTeamMembers
        """
        print(f"{team.team_name} used special with {poke} and got ", end = "")
        # returns current pokemon to its team
        team.return_pokemon(poke)
        # perform special action on team
        team.special()
        # retrieve a pokemon from the team
        poke = team.retrieve_pokemon()
        # display pokemon retrieved
        print(poke)
        # set pokemon retrieved as team1_poke or team2_poke depending on its team
        if team == self.team1:
            self.team1_poke = poke
        elif team == self.team2:
            self.team2_poke = poke

    def heal(self, team: PokeTeam, pokemon: PokemonBase) -> None:
        """ 
        Heals current pokemon and increment the number of times healed for the team.
        
        :param arg1: team (PokeTeam) - the PokeTeam instance to increment heal times
        :param arg2: poke (PokemonBase) - the Pokemon instance to get healed
        
        :pre: None
        
        :return: None

        :complexity: Best O(1), comparison between two integers
                     Worst O(1), heal has only O(1) complexity
        """
        # increment times healed by team
        team.heal_times += 1
        # only heal pokemon if heal times less than three
        if team.heal_times <= 3:
            # heal the pokemon
            pokemon.heal()
            print(f"{team.team_name} healed {pokemon}")

    def attack(self, attacking_poke: PokemonBase, defending_poke: PokemonBase) -> None:
        """ 
        Attacking pokemon attacks the defending pokemon.
        
        :param arg1: attacking_poke (PokemonBase) - the Pokemon instance to attack
        :param arg2: defending_poke (PokemonBase) - the Pokemon instance to defend against another pokemon's attack
        
        :pre: None
        
        :return: None
        
        :complexity: Best O(comp), where comp is the complexity of status comparison
                     Worst O(comp), where comp is the complexity of status comparison
        """
        # call paralysis() to check if the speed stat is halved when there is paralysis effect on either pokemon
        attacking_poke.paralysis()
        defending_poke.paralysis()
        print(f"{attacking_poke} attacks {defending_poke}.")
        # attacking pokemon attacks defending pokemon
        attacking_poke.attack(defending_poke)
        print(f"Result: {attacking_poke} {defending_poke}")

    def both_attack(self) -> None:
        """ 
        Method invoked when pokemon of different teams both choose to attack each other.
        Compares the speed status of both pokemon, then attack based on result of comparison.
        
        :param: None
        
        :pre: None
        
        :return: None
        
        :complexity: Best O(comp), where comp is the complexity of status comparison
                     Worst O(comp), where comp is the complexity of status comparison
        """
        # call paralysis() to check if the speed stat is halved when there is paralysis effect on either pokemon
        self.team1_poke.paralysis()
        self.team2_poke.paralysis()
        # get current speed of both pokemon for comparison later
        poke1_current_spd = self.team1_poke.get_current_speed()
        poke2_current_spd = self.team2_poke.get_current_speed()
        print(f"{self.team1_poke} has {poke1_current_spd} speed, and {self.team2.team_name}, {self.team2_poke} has {poke2_current_spd} speed")

        if poke1_current_spd == poke2_current_spd:
            # both pokemon attack each other regardless of fainting status if speed stat is the same
            # team1 would attack first
            self.attack(self.team1_poke, self.team2_poke)
            self.attack(self.team2_poke, self.team1_poke)

        elif poke1_current_spd > poke2_current_spd:
            # faster pokemon attacks slower pokemon, then slower pokemon attacks back if not fainted
            self.attack(self.team1_poke, self.team2_poke)
            if not self.team2_poke.is_fainted():
                self.attack(self.team2_poke, self.team1_poke)

        elif poke1_current_spd < poke2_current_spd:
            # faster pokemon attacks slower pokemon, then slower pokemon attacks back if not fainted
            self.attack(self.team2_poke, self.team1_poke)
            if not self.team1_poke.is_fainted():
                self.attack(self.team1_poke, self.team2_poke)

    def handle_level_up(self) -> None:
        """ 
        Levels up pokemon when another pokemon from different team has fainted but itself is not fainted.
        
        :param: None
        
        :pre: None
        
        :return: None
        
        :complexity: Best O(1), This function always access the current hp of the pokemon and do comparison, then assign value to variable.
                     Worst O(1), This function always access the current hp of the pokemon and do comparison, then assign value to variable.
        """
        poke = None
        # get the pokemon eligible to be leveled up
        # pokemon is eligible to level up if it has not fainted but another pokemon fainted
        if not self.team1_poke.is_fainted() and self.team2_poke.is_fainted():
            poke = self.team1_poke
        elif not self.team2_poke.is_fainted() and self.team1_poke.is_fainted():
            poke = self.team2_poke

        # level up if there is eligible pokemon to level up
        if poke is not None:
            print(f"{poke} levels up to ", end = "")
            # level up the pokemon
            poke.level_up()
            print(poke,"!")

    def handle_evolve(self, poke: PokemonBase) -> None:
        """ 
        Evolve pokemon if it has not fainted, can evolve and reached evolve level.
        
        :param: poke (PokemonBase) - The pokemon to check if it is able to evolve or not
        
        :pre: None
        
        :return: None
        
        :complexity: Best O(comp), where comp is the complexity of name comparison
                     Worst O(comp), where comp is the complexity of name comparison           
        """
        # pokemon can be evolved if it has not fainted, can evolve, and reached evolve level
        if not poke.is_fainted() and poke.can_evolve() and poke.should_evolve():
            print(f"{poke} evolved to ", end = "")
            # get the evolved version of current pokemon
            evolved_poke = poke.get_evolved_version()
            print(evolved_poke)
            # set the current pokemon as the evolved pokemon
            if poke == self.team1_poke:
                self.team1_poke = evolved_poke
            elif poke == self.team2_poke:
                self.team2_poke = evolved_poke

    def handle_fainted(self, team: PokeTeam, poke: PokemonBase) -> None:
        """ 
        Return fainted pokemon to its team, then retrieve a new pokemon.
        
        :param arg1: team (PokeTeam) - The team to return the pokemon to
        :param arg2: poke (PokemonBase) - The pokemon to return to its team if fainted
        
        :pre: None
        
        :return: None
        
        :complexity: Best O(N), where N is the length of pokeTeamMembers
                     Worst O(N), where N is the length of pokeTeamMembers         
        """
        # only enter if pokemon is fainted
        if poke.is_fainted():
            print(poke.get_poke_name() + " is fainted!")
            # return fainted pokemon back to its team
            team.return_pokemon(poke)       
            # retrieve pokemon from the team      
            poke = team.retrieve_pokemon()
            # set current pokemon as the retrieved pokemon
            if team == self.team1:
                self.team1_poke = poke
            elif team == self.team2:
                self.team2_poke = poke

    def battle(self, team1: PokeTeam, team2: PokeTeam) -> int:
        """ 
        Performs the battle between team1 and team2. battle should return 0 1 or 2. 0 representing a draw, and 1 or 2 representing player 1 or player 2 winning respectively.
        Battle starts with both teams retrieving and choosing battle option, then the actions are handled in order of swap, special, heal, attacks.
        The rounds continue until either team is empty, or either team healed more than 3 times.
        
        :param arg1: team1 (PokeTeam) - Team 1 to battle
        :param arg2: team2 (PokeTeam) - Team 2 to battle
        
        :pre: None
        
        :return: result (int) - Integer representing result of battle, 0 is draw, 1 is team 1 win, 2 is team 2 wins.
        
        :complexity: Best O(R*N), where R is number of rounds until battle ends, N is the length of PokeTeamMembers
                     Worst O(R*N^2), where R is number of rounds until battle ends, N is the length of PokeTeamMembers    
        """       

        # set both teams as the current battling team
        self.team1 = team1
        self.team2 = team2

        # both teams retrieve pokemon
        self.team1_poke = self.team1.retrieve_pokemon()
        self.team2_poke = self.team2.retrieve_pokemon()

        # battle while either team not empty, heal_time of each team not exceed 3 (loop for R times, where R is number of rounds)
        while (not (self.team1_poke is None or self.team2_poke is None)):

            # display game screen for each round of fight until lose
            self.print_screen()

            # each team choose their battle choice
            self.choice1 = self.team1.choose_battle_option(self.team1_poke, self.team2_poke)
            self.choice2 = self.team2.choose_battle_option(self.team2_poke, self.team1_poke)
            print(f"{self.team1.team_name} chooses {self.choice1} and {self.team2.team_name} chooses {self.choice2}")

            # handle swaps if chosen
            if self.choice1 == Action.SWAP: 
                self.swap(self.team1, self.team1_poke)
            if self.choice2 == Action.SWAP:
                self.swap(self.team2, self.team2_poke)

            # handle special if chosen
            if self.choice1 == Action.SPECIAL:
                self.special(self.team1, self.team1_poke)
            if self.choice2 == Action.SPECIAL:
                self.special(self.team2, self.team2_poke)

            # handle heal if chosen
            if self.choice1 == Action.HEAL:
                self.heal(self.team1, self.team1_poke)
                if self.team1.heal_times > 3:
                    break
            if self.choice2 == Action.HEAL:
                self.heal(self.team2, self.team2_poke)
                if self.team2.heal_times > 3:
                    break

            # handle attack if chosen
            if self.choice1 == Action.ATTACK and self.choice2 == Action.ATTACK:
                self.both_attack()
            elif self.choice1 == Action.ATTACK:
                self.attack(self.team1_poke, self.team2_poke)
            elif self.choice2 == Action.ATTACK:
                self.attack(self.team2_poke, self.team1_poke)

            # both pokemon lose 1 HP if both not fainted
            if not (self.team1_poke.is_fainted() or self.team2_poke.is_fainted()):
                # both lose 1 HP if both still alive
                self.team1_poke.lose_hp(1)
                self.team2_poke.lose_hp(1)
                print("Both are still alive so lose 1 hp each")

            # handle level up
            self.handle_level_up()

            # handle evolve
            self.handle_evolve(self.team1_poke)
            self.handle_evolve(self.team2_poke)

            # handle fainted
            self.handle_fainted(self.team1, self.team1_poke)
            self.handle_fainted(self.team2, self.team2_poke)

        # after battle ends must return alive pokemon on the field to its team
        if self.team1_poke is not None and not self.team1_poke.is_fainted():
            self.team1.return_pokemon(self.team1_poke)
        elif self.team2_poke is not None and not self.team2_poke.is_fainted():
            self.team2.return_pokemon(self.team2_poke)

        print("--------------------Result--------------------")
        # check result
        if self.team1.is_empty() and self.team2.is_empty():
            # draw if both teams empty
            self.result = 0
            print("BOTH TEAMS DRAWED!")
        elif self.team1.is_empty() or self.team1.heal_times > 3:
            # team 1 loses if its empty, or if heal times exceeded 3
            self.result = 2
            print("TEAM 2 WINS!")
        elif self.team2.is_empty() or self.team2.heal_times > 3:
            # team 2 loses if its empty, or if heal times exceeded 3
            self.result = 1
            print("TEAM 1 WINS!")
        return self.result

