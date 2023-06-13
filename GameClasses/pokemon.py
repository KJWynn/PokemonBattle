"""
This module implements Pokemon classes that inherits PokemonBase class.
Methods, attributes and features that are specific to each Pokemon objects are implemented in this module,
which allow initialisation of different types of Pokemon objects.
Each function has docstring which gives us description of the function.
Unittests (Test cases) for the module will be located under tests\test_shared_methods.py

"""
__author__ = "Scaffold by Jackson Goerner, Code by Khor Jia Wynn"

from pokemon_base import PokeType, PokemonBase

class Charizard(PokemonBase):
    """
    Complexity: All functions, unless stated otherwise, have best/worst case complexity of O(1)
    """
    def __init__(self, current_status=None, current_hp_difference=0, instance = 0 ) -> None:
        """
        This method invoked automatically to set a newly created object's attributes to their initial state.

        :param arg1: current_status (String) - the current status of Charizard (default = None)
        :param arg2: current_hp_difference (int) - (default = 0)
        :param arg3: instance (int) - the number of Charizard (default = 0)

        :pre: None

        :return: None
        
        """
        self.level = 3
        self.poke_type = PokeType.FIRE
        self.hp = 12 + 1 * self.level
        self.current_hp = self.hp - current_hp_difference
        self.attack_stat = 10 + 2 * self.level
        self.speed_stat = 9 + 1 * self.level
        self.current_speed_stat = self.speed_stat
        self.defence = 4
        self.status = current_status
        self.poke_name = "Charizard"
        self.status_inflicted = "burn"
        self.pokedex = 2
        self.instance = instance
        self.isParalysed = False

    def defend(self, effective_damage: int) -> None:
        """
        This method will determine and update how much hp the pokemon has lost

        :param: effective_damage (int) - the damage caused by the opponent

        :pre: None

        :return: None
        """
        if effective_damage > self.get_defence():
            self.lose_hp(effective_damage * 2)
        else:
            self.lose_hp(effective_damage)


    def level_up(self) -> None:
        """
        This method will level up the pokemon, update the attributes (hp, speed stat, attack_stat) of the pokemon object accordingly 

        :param:  None

        :pre: None

        :return: None
        """
        self.level += 1
        if self.get_hp() == self.hp:
            self.hp += 1
            self.current_hp += 1
        else:
            previous_max = self.hp
            self.hp += 1
            self.current_hp = self.hp - (previous_max - self.current_hp)
        self.attack_stat += 2
        if self.current_speed_stat == self.speed_stat:
            self.speed_stat += 1
            self.current_speed_stat += 1
        else:
            if self.isParalysed:
                self.isParalysed = False # To get the updated current speed of the level-up pokemon
            self.speed_stat += 1

    def get_evolved_version(self) -> None:
        """
        This method will raise exception as the Charizard couldn't evolve anymore

        :param: None

        :pre: None

        :return: None
        """
        raise Exception(self.poke_name + " cannot evolve!")


class Charmander(PokemonBase):
    """
    Complexity: All functions, unless stated otherwise, have best/worst case complexity of O(1)
    """
    def __init__(self, instance = 0) -> None:
        """
        This method invoked automatically to set a newly created object's attributes to their initial state.

        :param: instance (int) - the number of Charmander (default = 0)

        :pre: None

        :return: None
        """
        self.level = 1
        self.poke_type = PokeType.FIRE
        self.hp = 8 + 1 * self.level
        self.current_hp = self.hp
        self.attack_stat = 6 + 1 * self.level
        self.speed_stat = 7 + 1 * self.level
        self.current_speed_stat = self.speed_stat
        self.defence = 4
        self.status = "free"
        self.poke_name = "Charmander"
        self.status_inflicted = "burn"
        self.evolve_level = 3
        self.pokedex = 1
        self.instance = instance
        self.isParalysed = False

    def defend(self, effective_damage: int) -> None:
        """
        This method will determine and update how much hp the pokemon has lost

        :param: effective_damage (int) - the damage caused by the opponent
        
        :pre: None
        
        :return: None
        """
        if effective_damage > self.get_defence():
            self.lose_hp(effective_damage)
        else:
            self.lose_hp(effective_damage // 2)

    def level_up(self) -> None:
        """
        This method will level up the pokemon, update the respective attributes of the pokemon object accordingly 

        :param:  None

        :pre: None

        :return: None
        """
        self.level += 1
        if self.get_hp() == self.hp:
            self.hp += 1
            self.current_hp += 1
        else:
            previous_max = self.hp
            self.hp += 1
            self.current_hp = self.hp - (previous_max - self.current_hp)
        self.attack_stat += 1
        if self.current_speed_stat == self.speed_stat:
            self.speed_stat += 1
            self.current_speed_stat += 1
        else:
            if self.isParalysed:
                self.isParalysed = False # To get the updated current speed of the level-up pokemon
            self.speed_stat += 1

    def get_evolved_version(self) -> Charizard:
        """
        This method will get the object of evolved pokemon

        :param:  None
        
        :pre: None
        
        :return: Charizard (Pokemon) - the object of Charizard
        """
        current_hp_difference = self.hp - self.current_hp
        return Charizard(self.status, current_hp_difference, self.instance)


class Venusaur(PokemonBase):
    """
    Complexity: All functions, unless stated otherwise, have best/worst case complexity of O(1)
    """
    def __init__(self, current_status=None, current_hp_difference=0, instance = 0) -> None:
        """
        This method invoked automatically to set a newly created object's attributes to their initial state.

        :param arg1: current_status (String) - the current status of Venusaur (default = None)
        :param arg2: current_hp_difference (int) - (default = 0)
        :param arg3: instance (int) - the number of Charizard (default = 0)
        
        :pre: None
        
        :return: None
        """
        self.level = 2
        self.poke_type = PokeType.GRASS
        self.hp = 20 + self.level // 2
        self.current_hp = self.hp - current_hp_difference
        self.attack_stat = 5
        self.speed_stat = 3 + self.level // 2
        self.current_speed_stat = self.speed_stat
        self.defence = 10
        self.status = current_status
        self.poke_name = "Venusaur"
        self.status_inflicted = "poison"
        self.pokedex = 4
        self.instance = instance
        self.isParalysed = False

    def defend(self, effective_damage: int) -> None:
        """
        This method will determine and update how much hp the pokemon has lost

        :param: arg1 effective_damage (int) - the damage caused by the opponent
        
        :pre: None
        
        :return: None
        """
        if effective_damage > (self.get_defence()+5):
            self.lose_hp(effective_damage)
        else:
            self.lose_hp(effective_damage // 2)

    def level_up(self) -> None:
        """
        This method will level up the pokemon, update the respective attributes of the pokemon object accordingly 

        :param:  None
        
        :pre: None
        
        :return: None
        """
        self.level += 1
        if self.get_hp() == self.hp:
            self.hp = 20 + (self.get_level()//2)
            self.current_hp = self.hp
        else:
            previous_max = self.hp
            self.hp = 20 + self.get_level()//2
            self.current_hp = self.hp - (previous_max - self.current_hp)
        if self.current_speed_stat == self.speed_stat:
            self.speed_stat = 3 + (self.get_level()//2)
            self.current_speed_stat = 3 + (self.get_level()//2)
        else:
            if self.isParalysed:
                self.isParalysed = False # To get the updated current speed of the level-up pokemon
            self.speed_stat = 3 + (self.get_level()//2)

    def get_evolved_version(self) -> None:
        """
        This method will raise exception as the Venusaur couldn't evolve anymore

        :param:  None
        
        :pre: None
        
        :return: None
        """
        raise Exception(self.poke_name + " cannot evolve!")


class Bulbasaur(PokemonBase):
    """
    Complexity: All functions, unless stated otherwise, have best/worst case complexity of O(1)
    """
    def __init__(self, instance = 0) -> None:
        """
        This method invoked automatically to set a newly created object's attributes to their initial state.

        :param: arg1 instance (int) - the number of Bulbasaur (default = 0)
        
        :pre: None
        
        :return: None
        """
        self.level = 1
        self.poke_type = PokeType.GRASS
        self.hp = 12 + 1*self.level
        self.current_hp = self.hp
        self.attack_stat = 5
        self.speed_stat = 7 + self.level//2
        self.current_speed_stat = self.speed_stat
        self.defence = 5
        self.status = "free"
        self.poke_name = "Bulbasaur"
        self.status_inflicted = "poison"
        self.evolve_level = 2
        self.pokedex = 3
        self.instance = instance
        self.isParalysed = False

    def defend(self, effective_damage: int) -> None:
        """
        This method will determine and update how much hp the pokemon has lost

        :param: arg1 effective_damage (int) - the damage caused by the opponent
        
        :pre: None
        
        :return: None
        """
        if effective_damage > (self.get_defence()+5):
            self.lose_hp(effective_damage)
        else:
            self.lose_hp(effective_damage // 2)

    def level_up(self) -> None:
        """
        This method will level up the pokemon, update the respective attributes of the pokemon object accordingly 

        :param:  None
        
        :pre: None
        
        :return: None
        """
        self.level += 1
        if self.get_hp() == self.hp:
            self.hp += 1
            self.current_hp += 1
        else:
            previous_max = self.hp
            self.hp += 1
            self.current_hp = self.hp - (previous_max - self.current_hp)

        if self.current_speed_stat == self.speed_stat:
            self.speed_stat = 7 + (self.get_level()//2)
            self.current_speed_stat = 7 + (self.get_level()//2)
        else:
            if self.isParalysed:
                self.isParalysed = False # To get the updated current speed of the level-up pokemon
            self.speed_stat = 7 + (self.get_level()//2)

    def get_evolved_version(self) -> Venusaur:
        """
        This method will get the object of evolved pokemon

        :param:  None
        
        :pre: None
        
        :return: Venusaur (Pokemon) - the object of Venusaur
        """
        current_hp_difference = self.hp - self.current_hp
        return Venusaur(self.status, current_hp_difference, self.instance)


class Blastoise(PokemonBase):
    """
    Complexity: All functions, unless stated otherwise, have best/worst case complexity of O(1)
    """
    def __init__(self, current_status=None, current_hp_difference=0, instance = 0) -> None:
        """
        This method invoked automatically to set a newly created object's attributes to their initial state.

        :param arg1: current_status (String) - the current status of Blastoise (default = None)
        :param arg2: current_hp_difference (int) - (default = 0)
        :param arg3: instance (int) - the number of Blastoise (default = 0)
        
        :pre: None
        
        :return: None
        """
        self.level = 3
        self.poke_type = PokeType.WATER
        self.hp = 15 + 2 * self.level
        self.current_hp = self.hp - current_hp_difference
        self.attack_stat = 8 + self.level // 2
        self.speed_stat = 10
        self.current_speed_stat = self.speed_stat
        self.defence = 8 + 1 * self.level
        self.status = current_status
        self.poke_name = "Blastoise"
        self.status_inflicted = "paralysis"
        self.pokedex = 6
        self.instance = instance
        self.isParalysed = False

    def defend(self, effective_damage: int) -> None:
        """
        This method will determine and update how much hp the pokemon has lost

        :param: arg1 effective_damage (int) - the damage caused by the opponent
        
        :pre: None
        
        :return: None
        """
        if effective_damage > (2 * self.get_defence()):
            self.lose_hp(effective_damage)
        else:
            self.lose_hp(effective_damage // 2)

    def level_up(self) -> None:
        """
        This method will level up the pokemon, update the respective attributes of the pokemon object accordingly 

        :param:  None
        
        :pre: None
        
        :return: None
        """
        self.level += 1
        if self.get_hp() == self.hp:
            self.hp += 2
            self.current_hp += 2
        else:
            previous_max = self.hp
            self.hp += 2
            self.current_hp = self.hp - (previous_max - self.current_hp)
        self.attack_stat = 8 + (self.get_level()//2)
        self.defence += 1

    def get_evolved_version(self) -> None:
        """
        This method will raise exception as the Blastoise couldn't evolve anymore

        :param:  None
        
        :pre: None
        
        :return: None
        """
        raise Exception(self.poke_name + " cannot evolve!")

class Squirtle(PokemonBase):
    """
    Complexity: All functions, unless stated otherwise, have best/worst case complexity of O(1)
    """
    def __init__(self, instance = 0) -> None:
        """
        This method invoked automatically to set a newly created object's attributes to their initial state.

        :param: instance (int) - the number of Squirtle (default = 0)
        
        :pre: None
        
        :return: None
        """
        self.level = 1
        self.poke_type = PokeType.WATER
        self.hp = 9 + 2 * self.level
        self.current_hp = self.hp
        self.attack_stat = 4 + self.level // 2
        self.speed_stat = 7
        self.current_speed_stat = self.speed_stat
        self.defence = 6 + self.level
        self.status = "free"
        self.poke_name = "Squirtle"
        self.status_inflicted = "paralysis"
        self.evolve_level = 3
        self.pokedex = 5
        self.instance = instance
        self.isParalysed = False

    def defend(self, effective_damage: int) -> None:
        """
        This method will determine and update how much hp the pokemon has lost

        
        :param: effective_damage (int) - the damage caused by the opponent
        
        :pre: None
        
        :return: None
        """
        if effective_damage > (2 * self.get_defence()):
            self.lose_hp(effective_damage)
        else:
            self.lose_hp(effective_damage // 2)

    def level_up(self) -> None:
        """
        This method will level up the pokemon, update the respective attributes of the pokemon object accordingly 

        
        :param: None
        
        :pre: None
        
        :return: None
        """
        self.level += 1
        if self.get_hp() == self.hp:
            self.hp += 2
            self.current_hp += 2
        else:
            previous_max = self.hp
            self.hp += 2
            self.current_hp = self.hp - (previous_max - self.current_hp)
        self.attack_stat = 4 + (self.get_level()//2)
        self.defence += 1

    def get_evolved_version(self) -> Blastoise:
        """
        This method will get the object of evolved pokemon

        
        :param:  None
        
        :pre: None
        
        :return: Blastoise (Pokemon) - the object of Blastoise
        """
        current_hp_difference = self.hp - self.current_hp
        return Blastoise(self.status, current_hp_difference, self.instance)


class Gengar(PokemonBase):
    """
    Complexity: All functions, unless stated otherwise, have best/worst case complexity of O(1)
    """
    def __init__(self, current_status=None, current_hp_difference=0, instance = 0) -> None:
        """
        This method invoked automatically to set a newly created object's attributes to their initial state.

        :param arg1: current_status (String) - the current status of Gengar (default = None)
        :param arg2: current_hp_difference (int) - (default = 0)
        :param arg3: instance (int) - the number of Gengar (default = 0)

        :pre: None

        :return: None
        """
        self.level = 3
        self.poke_type = PokeType.GHOST
        self.hp = 12 + self.level//2
        self.current_hp = self.hp - current_hp_difference
        self.attack_stat = 18
        self.speed_stat = 12
        self.current_speed_stat = self.speed_stat
        self.defence = 3
        self.status = current_status
        self.poke_name = "Gengar"
        self.status_inflicted = "sleep"
        self.pokedex = 9
        self.instance = instance
        self.isParalysed = False

    def defend(self, effective_damage: int) -> None:
        """
        This method will update how much hp the pokemon has lost

        :param:  arg1 effective_damage (int) - the damage caused by the opponent

        :pre: None

        :return: None
        """
        self.lose_hp(effective_damage)

    def level_up(self) -> None:
        """
        This method will level up the pokemon, update the respective attributes of the pokemon object accordingly 

        :param:  None

        :pre: None

        :return: None
        """
        self.level += 1
        if self.get_hp() == self.hp:
            self.hp = 12 + self.get_level()//2
            self.current_hp = self.hp
        else:
            previous_max = self.hp
            self.hp = 12 + self.get_level()//2
            self.current_hp = self.hp - (previous_max - self.current_hp)

    def get_evolved_version(self) -> None:
        """
        This method will raise exception as the Gengar couldn't evolve anymore

        :param:  None

        :pre: None

        :return: None
        """
        raise Exception(self.poke_name + " cannot evolve!")


class Haunter(PokemonBase):
    """
    Complexity: All functions, unless stated otherwise, have best/worst case complexity of O(1)
    """
    def __init__(self, current_status=None, current_hp_difference=0, instance = 0) -> None:
        """
        This method invoked automatically to set a newly created object's attributes to their initial state.

        :param arg1: current_status (String) - the current status of Haunter (default = None)
        :param arg2: current_hp_difference (int) - (default = 0)
        :param arg3: instance (int) - the number of Haunter (default = 0)

        :pre: None
        
        :return: None
        """
        self.level = 1
        self.poke_type = PokeType.GHOST
        self.hp = 9 + self.level//2
        self.current_hp = self.hp - current_hp_difference
        self.attack_stat = 8
        self.speed_stat = 6
        self.current_speed_stat = self.speed_stat
        self.defence = 6
        self.status = current_status
        self.poke_name = "Haunter"
        self.status_inflicted = "sleep"
        self.evolve_level = 3
        self.pokedex = 8
        self.instance = instance
        self.isParalysed = False

    def defend(self, effective_damage: int) -> None:
        """
        This method will update how much hp the pokemon has lost

        :param: arg1 effective_damage (int) - the damage caused by the opponent

        :pre: None

        :return: None
        """
        self.lose_hp(effective_damage)

    def level_up(self) -> None:
        """
        This method will level up the pokemon, update the respective attributes of the pokemon object accordingly 

        :param:  None

        :pre: None

        :return: None
        """
        self.level += 1
        if self.get_hp() == self.hp:
            self.hp = 9 + self.get_level()//2
            self.current_hp = self.hp
        else:
            previous_max = self.hp
            self.hp = 9 + self.get_level()//2
            self.current_hp = self.hp - (previous_max - self.current_hp)
        self.defence += 1

    def get_evolved_version(self) -> Gengar:
        """
        This method will get the object of evolved pokemon

        :param:  None

        :pre: None

        :return: Gengar (Pokemon) - the object of Gengar
        """
        current_hp_difference = self.hp - self.current_hp
        return Gengar(self.status, current_hp_difference, self.instance)


class Gastly(PokemonBase):
    """
    Complexity: All functions, unless stated otherwise, have best/worst case complexity of O(1)
    """
    def __init__(self, instance = 0) -> None:
        """
        This method invoked automatically to set a newly created object's attributes to their initial state.

        :param: arg1 instance (int) - the number of Gastly (default = 0)

        :pre: None

        :return: None
        """
        self.level = 1
        self.poke_type = PokeType.GHOST
        self.hp = 6 + self.level//2
        self.current_hp = self.hp
        self.attack_stat = 4
        self.speed_stat = 2
        self.current_speed_stat = self.speed_stat
        self.defence = 8
        self.status = "free"
        self.poke_name = "Gastly"
        self.status_inflicted = "sleep"
        self.evolve_level = 1
        self.pokedex = 7
        self.instance = instance
        self.isParalysed = False

    def defend(self, effective_damage: int) -> None:
        """
        This method will update how much hp the pokemon has lost

        :param: effective_damage (int) - the damage caused by the opponent

        :pre: None

        :return: None
        """
        self.lose_hp(effective_damage)

    def level_up(self) -> None:
        """
        This method will level up the pokemon, update the respective attributes of the pokemon object accordingly 

        :param:  None

        :pre: None

        :return: None
        """
        self.level += 1
        if self.get_hp() == self.hp:
            self.hp = 6 + self.get_level()//2
            self.current_hp = self.hp
        else:
            previous_max = self.hp
            self.hp = 6 + self.get_level()//2
            self.current_hp = self.hp - (previous_max - self.current_hp)

    def get_evolved_version(self) -> Haunter:
        """
        This method will get the object of evolved pokemon

        :param:  None

        :pre: None

        :return: Haunter (Pokemon) - the object of Haunter
        """
        current_hp_difference = self.hp - self.current_hp
        return Haunter(self.status, current_hp_difference, self.instance)


class Eevee(PokemonBase):
    """
    Complexity: All functions, unless stated otherwise, have best/worst case complexity of O(1)
    """
    def __init__(self, instance = 0) -> None:
        """
        This method invoked automatically to set a newly created object's attributes to their initial state.

        :param: instance (int) - the number of Eevee (default = 0)

        :pre: None

        :return: None
        """
        self.level = 1
        self.poke_type = PokeType.NORMAL
        self.hp = 10
        self.current_hp = self.hp
        self.attack_stat = 6 + self.level
        self.speed_stat = 7 + self.level
        self.current_speed_stat = self.speed_stat
        self.defence = 4 + self.level
        self.status = "free"
        self.poke_name = "Eevee"
        self.status_inflicted = "confuse"
        self.pokedex = 10
        self.instance = instance
        self.isParalysed = False

    def defend(self, effective_damage: int) -> None:
        """
        This method will determine and update how much hp the pokemon has lost

        :param: effective_damage (int) - the damage caused by the opponent
        
        :pre: None

        :return: None
        """
        if effective_damage >= self.get_defence():
            self.lose_hp(effective_damage)
        else:
            self.lose_hp(0)

    def level_up(self) -> None:
        """
        This method will level up the pokemon, update the respective attributes of the pokemon object accordingly 

        :param: None
        
        :pre: None
        
        :return: None
        """
        self.level += 1
        self.attack_stat += 1
        if self.current_speed_stat == self.speed_stat:
            self.speed_stat += 1
            self.current_speed_stat += 1
        else:
            if self.isParalysed:
                self.isParalysed = False # To get the updated current speed of the level-up pokemon
            self.speed_stat += 1
        self.defence += 1

    def get_evolved_version(self) -> None:
        """
        This method will raise exception as the Eevee couldn't evolve anymore

        :param:  None
        
        :pre: None
        
        :return: None
        """
        raise Exception(self.poke_name + " cannot evolve!")