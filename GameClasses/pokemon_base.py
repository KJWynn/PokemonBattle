from __future__ import annotations
"""
Pokemon ADT. Defines a generic abstract structure of pokemon with the standard methods.

This module acts as the abstract class for Pokemon objects.
Methods and features that are shared by all Pokemon objects are implemented in this function,
which allow initialisation of Pokemon.
Each function has docstring which specifies details such as complexity of the function.
Unittests (Test cases) for the module will be located under tests\test_shared_methods.py

"""
__author__ = "Scaffold by Jackson Goerner, Code by Khor Jia Wynn, Tee Zhi Hui"

from abc import ABC, abstractmethod
from random_gen import RandomGen
from enum import Enum, auto

class PokeType(Enum):
    """Enum class containing Pokemon types"""
    FIRE = auto()
    GRASS = auto()
    WATER = auto()
    GHOST = auto()
    NORMAL = auto()

class PokemonBase(ABC):
    """
    :complexity: All functions, unless stated otherwise, have best/worst case complexity of O(1)
    """

    def __init__(self, hp: int, poke_type: PokeType) -> None:
        """ 
        This method invoked automatically to set a newly created object's attributes to their initial state.

        :param arg1: hp (integer) - the hit points of the pokemon
        :param arg2: poke_type (An object of Poketype)

        :pre1: hp must be integer greater than zero
        :pre2: poke_type must be enum member (FIRE/GRASS/WATER/GHOST/NORMAL)

        :return: None
        
        :complexity: Best: O(n), the number of members in the Enum class
                     Worst: O(n), the number of members in the Enum class
        """
        try: 
            assert hp > 0 and isinstance(hp, int), 'hp must be integer greater than zero'
            assert poke_type in PokeType, "Invalid poke type"
        except AssertionError as e:
            raise ValueError(e)

        self.level = int()
        self.poke_type = poke_type
        self.hp = hp
        self.current_hp = self.hp
        self.attack_stat = int()
        self.speed_stat = int()
        self.current_speed_stat = int()
        self.defence = int()
        self.status = "free"
        self.poke_name = ""
        self.status_inflicted = ""
        self.evolve_level = int()
        self.pokedex = int()
        self.isParalysed = False

    def is_fainted(self) -> bool:
        """ 
        If the pokemon has hp is less than or equal to 0, then the pokemon has fainted

        :param: None

        :pre: None

        :return: boolean - True, if hp less than or equal to 0
        
        :complexity:
        Best: O(1), This function always access the current hp of the pokemon and do comparison. It is a constant time.
        Worst: O(1), This function always access the current hp of the pokemon and do comparison. It is a constant time.
        """
        return self.get_hp() <= 0

    @abstractmethod
    def level_up(self) -> None:
        """ The Pokemon will level up if the opponent has fainted """
        pass

    def get_speed(self) -> int:
        """ 
        Get the speed points of the Pokemon

        :param: None

        :pre: None

        :return: speed_stat (integer) - the speed stat of the pokemon 
        
        :complexity:
        Best: O(1), This function always access the speed stat of the pokemon. It is a constant time.
        Worst: O(1), This function always access the speed stat of the pokemon. It is a constant time.
        """
        return self.speed_stat

    def get_current_speed(self) -> int:
        """ 
        Get the current speed of the Pokemon 

        :param: None

        :pre: None

        :return: current_speed_stat (integer) - the latest speed stat of the pokemon 
        
        :complexity:
        Best: O(1), This function always access the current speed stat of the pokemon. It is a constant time.
        Worst: O(1), This function always access the current speed stat of the pokemon. It is a constant time.
        """
        return self.current_speed_stat

    def get_attack_damage(self) -> int:
        """ 
        Get the attack points of the Pokemon

        :param: None

        :pre: None

        :return:
        attack_stat (integer) - the attack points of the pokemon 
        
        :complexity:
        Best: O(1), This function always access the attack points of the pokemon. It is a constant time.
        Worst: O(1), This function always access the attack points of the pokemon. It is a constant time.
        """
        return self.attack_stat

    def get_defence(self) -> int:
        """ 
        Get the defence points of the Pokemon

        :param: None

        :pre: None

        :return:
        defence (integer) - the defence points of the pokemon 
        
        :complexity:
        Best: O(1), This function always access the defence points of the pokemon. It is a constant time.
        Worst: O(1), This function always access the defence points of the pokemon. It is a constant time.
        """
        return self.defence

    def get_hp(self) -> int:
        """ 
        Get the current hit points of the Pokemon

        :param: None

        :pre: None

        :return:
        current_hp (integer) - the current hit points of the Pokemon 
        
        :complexity:
        Best: O(1), This function always access the current hit points of the Pokemon. It is a constant time.
        Worst: O(1), This function always access the current hit points of the Pokemon. It is a constant time.
        """
        return self.current_hp

    def lose_hp(self, lost_hp: int) -> None:
        """ 
        Get the amount of Hit Points of the Pokemon has lost

        :param arg1: lost_hp (integer) - the amount of hit points of the Pokemon will lose

        :pre1: lost_hp must be greater or equal to 0
        :pre2: the value of lost_hp must be an integer

        :return:
        current_hp (integer) - the current hit points of the Pokemon 
        
        :complexity:
        Best: O(1),  Comparing number and operation require constant time. It is a constant time.
        Worst: O(1),  It is a constant time.
        """
        try:
            assert lost_hp >= 0 
            self.current_hp -= lost_hp
        except TypeError:
            raise TypeError("Invalid lost hp, argument must be integer")
        except AssertionError:
            raise ValueError("Lost hp must be greateer or equal to 0")

    @abstractmethod
    def defend(self, damage: int) -> None:
        pass

    def attack(self, other: PokemonBase):
        """ 
        Attack the pokemon of the opponent on the field by its status

        :param:nother (PokemonBase) - the object of PokemonBase

        :pre: None

        :return: None
        
        :complexity:
        Best: O(comp), where comp is the complexity of status comparison.
        Worst: O(comp), where comp is the complexity of status comparison.
        """
        attack_multiplier = 1
        # Step 1: Status effects on attack damage / redirecting attacks
        if self.status == "sleep": 
            print(self.poke_name, 'is asleep!')
            pass
        elif self.status == "confuse": 
            if RandomGen.random_chance(0.5): 
                print(self.poke_name, 'is confused and attacked itself!')
                other = self
        elif self.status == "burn": 
            print(f"Because {self.get_poke_name()} is burning, it only deals half damage!")
            attack_multiplier = 0.5

        # Step 2: Do the attack
        print(f"{self.get_poke_name()} has base attack of {self.get_attack_damage()} and type effectiveness of {self.type_multiplier(other)} against {other.get_poke_name()}")
        effective_damage = int(self.get_attack_damage()* attack_multiplier * self.type_multiplier(other))
        print(self.poke_name, "has effective damage output of", str(effective_damage))
        other.defend(effective_damage) 

        # Step 3: Losing hp to status effects
        if self.status == "poison": 
            self.lose_hp(3)
            print(self.poke_name + 'lost 3 hp to poison damage!')
        elif self.status == "burn":
            self.lose_hp(1)
            print(self.poke_name + 'lost 1 hp to fire damage!')

        # Step 4: Possibly applying status effects
        if RandomGen.random_chance(0.2):
            status = self.get_status_inflicted()
            if status == "paralysis" and other.isParalysed == True:
                print(f"{other.get_poke_name()} is already paralysed so cannot be paralysed again!")
            else:
                other.status = status
                print(f"{self.get_poke_name()} inflicted {self.get_status_inflicted()} on {other.get_poke_name()}!")

    def get_poke_name(self) -> str:
        """ 
        Get the name of the pokemon

        :param: None

        :pre: None

        :return:
        poke_name (string) - the name of the pokemon 
        
        :complexity:
        Best: O(1), This function always access the name of the pokemon. It is a constant time.
        Worst: O(1), This function always access the name of the pokemon. It is a constant time.
        """
        return self.poke_name

    def get_level(self) -> int:
        """ 
        Get the level of the pokemon

        :param: None

        :pre: None

        :return:
        level (int) - the level of the pokemon 
        
        :complexity:
        Best: O(1), This function always access the level of the pokemon. It is a constant time.
        Worst: O(1), This function always access the level of the pokemon. It is a constant time.
        """
        return self.level

    def heal(self) -> None:
        """ 
        Heal the pokemon

        :param: None

        :pre: None

        :return: None
        
        :complexity:
        Best: O(1), All operations that this function do is O(1). It is a constant time.
        Worst: O(1), All operations that this function do is O(1). It is a constant time.
        """
        self.current_hp = self.hp
        self.status = "free"
        self.current_speed_stat = self.get_speed()


    def should_evolve(self) -> bool:
        """ 
        Check if the pokemon type can be evolved AND if the pokemon achieves the level that it can be evolved - 
        if the current level of the pokemon is greater or equal to its evolve level, return True

        :param: None

        :pre: None

        :return:
        boolean - True, if the pokemon can evolve and the current level of the pokemon is greater or equal to its evolve level
        
        :complexity:
        Best: O(1), All operations that this function do is O(1). It is a constant time.
        Worst: O(1), All operations that this function do is O(1). It is a constant time.
        """
        if self.can_evolve():
            return self.get_level() >= self.evolve_level
        return False

    def can_evolve(self) -> bool:
        """ 
        Check if the type of the pokemon can be evolved, if yes, return True

        :param: None

        :pre: None

        :return:
        boolean - True, if the pokemon can be evolved
        
        :complexity:
        Best: O(comp), where comp is the complexity of name comparison.
        Worst: O(comp), where comp is the complexity of name comparison.
        """
        name = self.get_poke_name()
        return name == "Charmander" or name == "Squirtle" or name == "Bulbasaur" or name == "Gastly" or name == "Haunter"

    @abstractmethod
    def get_evolved_version(self) -> PokemonBase:
        pass

    def type_multiplier(self, other : PokemonBase) -> float:
        """ 
        Get the multipliers for attack

        :param: other (PokemonBase) - the object of PokemonBase

        :pre: None

        :return:
        (float) - the multiplier of the attack pokemon and defence pokemon
        
        :complexity:
        Best : O(1), since the list of types has constant size
        Worst: O(1), since the list of types has constant size
        """
        types = [PokeType.FIRE, PokeType.GRASS, PokeType.WATER, PokeType.GHOST, PokeType.NORMAL]
        matcher = [[1, 2, 0.5, 1, 1],
                  [0.5, 1, 2, 1, 1],
                  [2, 0.5, 1, 1, 1],
                  [1.25, 1.25, 1.25, 2, 0],
                  [1.25, 1.25, 1.25, 0, 1]]
        self_index = 0
        other_index = 0

        for i in range(len(types)):
            if self.poke_type == types[i]:
                self_index = i
            if other.poke_type == types[i]:
                other_index = i
        return matcher[self_index][other_index]

    def get_status_inflicted(self) -> None:
        """ 
        Get the inflicted status of the pokemon

        :param: None

        :pre: None

        :return: None
        
        :complexity:
        Best: O(1), This function always access the status_inflicted of the pokemon. It is a constant time.
        Worst: O(1), This function always access the status_inflicted of the pokemon. It is a constant time.
        """
        return self.status_inflicted

    def paralysis(self):
        """ 
        This function must be called before attack. If the pokemon is paralysed, its speed will be halved

        :param: None

        :pre: None

        :return: None
        
        :complexity:
        Best: O(comp), where comp is the complexity of status comparison
        Worst: O(comp), where comp is the complexity of status comparison
        """
        # Need to evaluate speed affected by Paralysis before attacking. Assumption: Speed only halves once, not every turn
        if self.status == "paralysis" and not self.isParalysed:
            print(f"{self.get_poke_name()} is paralysed and its speed is halved from {self.get_speed()} to {self.get_speed()//2}")
            self.current_speed_stat = self.get_speed() // 2
            self.isParalysed = True # This ensures that next turn won't halve speed again

        # case when paralysis is overwritten with another status(either inflicted or None if healed/taken off field)
        if self.status != "paralysis" and self.isParalysed: 
            self.current_speed_stat = self.get_speed() # ensures that speed debuff is removed
            self.isParalysed = False # ensures that poke can be paralysed next time around

    def __str__(self) -> str:
        """
        return the string representation of each pokemon instance

        :param: None

        :pre: None

        :return:
        (str) - the string representation of each pokemon instance
        
        :complexity:
        Best: O(1), All operations that this function do is O(1). It is a constant time.
        Worst: O(1), All operations that this function do is O(1). It is a constant time.

        """
        return f"LV. {self.level} {self.get_poke_name()}: {self.get_hp()} HP"
