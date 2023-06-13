from __future__ import annotations
"""
This module implements the classes and functions required for generating a PokeTeam object to hold Pokemon objects.
The PokeTeam is implemented using the provided ADT modules, and does not use inbuilt lists unless specified in the specification
and Ed forum announcements.
Functions specified in the specifications are implemented as well as additional functions and classes for ease of maintainence.
Each function has docstring which specifies the details such as complexity of the function.
Unittests (Test cases) for the module will be located under tests\test_poke_team.py

"""
__author__ = "Scaffold by Jackson Goerner, Code by Khor Jia Wynn, Tee Zhi Hui, Lim Yi Xuan."

from stack_adt import ArrayStack

from random_gen import RandomGen
from queue_adt import CircularQueue


from enum import Enum, auto
from pokemon_base import PokemonBase
from pokemon import *
from sorted_list import ListItem
from array_sorted_list import ArraySortedList


class Action(Enum):
    """Enum class containing actions to be chosen by pokemon trainer when battling"""
    ATTACK = auto()
    SWAP = auto()
    HEAL = auto()
    SPECIAL = auto()


class Criterion(Enum):
    """Enum class containing criterion to sort by in battle mode 2"""
    SPD = auto()
    HP = auto()
    LV = auto()
    DEF = auto()


class BM2SortedList(ArraySortedList):
    """
    Class inheriting ArraySortedList methods, but with additional methods and attribute that allows the items to be sorted in descending or ascending order.
    Swap method added for bubble sort(used in sort_by_pokedex).
    Can be sorted by increasing or decreasing criterion depending on the order argument during initialization.
    """

    def __init__(self, max_capacity: int, order: int) -> None:
        """ 
        BM2SortedList object initialiser which inherits ArraySortedList functionality and can be sorted based on specified order(ascending/descending).
        This method is invoked to create an BM2SortedList object and initialise its state.

        :param arg1: max_capacity (int) - Integer representing the maximum capacity for the ArraySortedList to be generated
        :param arg2: order (int) - Integer to represent whether to sort by ascending (order = 0) or descending order (order = 1)

        :pre: 
        - max_capacity must be integer greater than 0
        - order must be integer 0 or 1

        :return: None

        :complexity: Best O(N), where N is the max_capacity representing the length of the referential array in BM2SortedList.
                     Worst O(N), where N is the max_capacity representing the length of the referential array in BM2SortedList.
        """
        # check the preconditions
        try:
            assert isinstance(max_capacity, int), "Max capacity must be an integer"
            assert isinstance(order, int) and (order == 0 or order == 1), "Order must be integer 0 or 1"
        except AssertionError as e:
            raise ValueError(e)

        # first initialise the sorted list with capacity
        ArraySortedList.__init__(self, max_capacity)
        self.order = order

    def __setitem__(self, index: int, item: ListItem) -> None:
        """ 
        Magic method. Insert the item at a given position, if possible while following the order. Shift the following elements to the right.
        Order determines ascending or descending criterion, 1 is descending order, 0 is ascending order.

        :param: index(int) - the index to insert the item

        :pre: 
        - index is an integer greater or equal to 0
        - item is a ListItem object

        :return: None

        :complexity: Best O(N), where N is length of the array in the BM2SortedList object
                     Worst O(N), where N is length of the array in the BM2SortedList object
        """
        # check the preconditions
        try:
            assert index is not None and isinstance(index, int) and index >= 0 , "Index must be an integer greater or equal to 0"
            assert item is not None and isinstance(item, ListItem), "item must be an ListItem object"
        except AssertionError as e:
            raise ValueError(e)

        can_place = False
        # ascending order
        ascending = self.order == 0 and (self.is_empty() or \
                    (index == 0 and item.key <= self[index].key) or \
                    (index == len(self) and self[index - 1].key <= item.key) or \
                    (index > 0 and self[index - 1].key <= item.key <= self[index].key))
        # descending order
        descending = self.order == 1 and (self.is_empty() or \
                    (index == 0 and item.key >= self[index].key) or \
                    (index == len(self) and self[index - 1].key >= item.key) or \
                    (index > 0 and self[index].key <= item.key <= self[index - 1].key))

        if ascending or descending:
            # resize the array if the array is full
            if self.is_full():
                self._resize()

            # shuffle ListItems after the current index to the right to accomodate space for the new item
            self._shuffle_right(index)
            # set item at index position where space has been allocated
            self.array[index] = item
        else:
            # the list isn't empty and the item's position is wrong with respect to its neighbours
            raise IndexError('Element should be inserted in sorted order')

    def _index_to_add(self, item: ListItem) -> int:
        """
        Find the position where the new item should be placed using binary search.

        :param arg1: item (ListItem) - ListItem object to be inserted into the BM2SortedList object array

        :pre: None

        :return: integer representing the index where the new item should be added into

        :complexity:Best O(1), when the index to add is directly at the centre.
                    Worst O(log N), where N is the length of the array in BM2SortedList object, when index to add is not within the searching list.
        """
        # check for preconditions
        try:
            assert item is not None and isinstance(item,ListItem), "item must be ListItem object."
        except AssertionError as e:
            raise ValueError(e)
        low = 0
        high = len(self) - 1

        while low <= high:
            mid = (low + high) // 2         # get the middle index of the search list
            if self[mid].key < item.key:    # enter when item larger than middle
                if self.order == 0:         # when order is in ascending order
                    low = mid + 1           # make the search list search from middle to end of current search list
                elif self.order == 1:       # when order is in descending order
                    high = mid - 1          # make the search list serach from start to middle of current search list
            elif self[mid].key > item.key:  # enter when item smaller than middle
                if self.order == 0:         # when order is in ascending order
                    high = mid - 1          # search from start to middle of current search list
                elif self.order == 1:       # when order is in descending order
                    low = mid + 1           # search from middle to end of current search list
            else:
                return mid                  # return the middle index when item is equal to middle

        return low                          # return the low index indicating the index to insert the item into

    def swap(self, index1: int, index2: int) -> None:
        """
        Swaps the ListItems of index1 and index2 in BM2SortedList's array. Used in sort_by_pokedex method.

        :param arg1: index1 (int) - Integer representing index of the item to be swapped
        :param arg2: index2 (int) - Integer representing index of another item to be swapped

        :pre: index1 and index2 must be integers greater or equal to 0

        :return: None

        :complexity:Best O(N), where N is the length of the array in BM2SortedList object.
                    Worst O(N), where N is the length of the array in BM2SortedList object.
        """
        # check for preconditions
        try:
            assert index1 is not None and isinstance(index1, int) and len(self) > index1 >= 0
            assert index2 is not None and isinstance(index2, int) and len(self) > index2 >= 0
        except AssertionError:
            raise ValueError("index1 and index2 must be integer greater or equal to 0.")

        # additional swap method for sort_by_pokedex
        temp = self.array[index1]
        self.array[index1] = self.array[index2]
        self.array[index2] = temp

    def delete_at_index(self, index: int) -> ListItem:
        """
        Delete the ListItem  at the specified index in the BM2SortedList array.
        Similar to ArraySortedList method but when index >= len(self), instead of raising index error return None.

        :param arg1: index (int) - Integer representing index of item to be deleted

        :pre: index must be an integer greater or equal to 0

        :return: item (ListItem) - The ListItem deleted from the BM2Sorted list

        :complexity:Best O(N), where N is the length of the array in BM2SortedList object.
                    Worst O(N), where N is the length of the array in BM2SortedList object.
        """
        try:
            assert index is not None and isinstance(index, int) and index >= 0
        except AssertionError:
            raise ValueError("Index must be an integer greater or equal to 0")
        if index >= len(self):
            return None
        item = self.array[index]
        self.length -= 1
        self._shuffle_left(index)
        return item


class BattleMode0():
    """
    Class of generating Queue object and peforming operations on the poke teams with battle mode 0

    :complexity: All functions, unless stated otherwise, have best/worst case complexity of O(1)
    """
    def __init__(self, poke_team_list) -> None:
        """
        This method invoked automatically to set a newly created object's attributes to their initial state.

        :param: poke_team_list (list) - the list of the poke team

        :pre: None

        :return: None

        :complexity: Best O(N), where N is length of pokeTeamMembers
                     WorstO(N), where N is length of pokeTeamMembers
        """
        self.poke_team_list = poke_team_list
        self.pokeTeamMembers = self.generate_queue_ADT_battle_0()

    def generate_queue_ADT_battle_0(self) -> CircularQueue:
        """
        This method generate a queue for the pokemon team in battle mode 0

        :param: None

        :pre: None

        :return: pokeTeamMembers (CircularQueue obj) - the queue which stores the pokemon

        :complexity: Best O(N), where N is length of pokeTeamMembers
                     WorstO(N), where N is length of pokeTeamMembers
        """
        array_poke_team = self.poke_team_list
        len_poke_team = len(self.poke_team_list)

        self.pokeTeamMembers = CircularQueue(len_poke_team)

        for i in range(len_poke_team):
            self.pokeTeamMembers.append(array_poke_team[i])

        return self.pokeTeamMembers

    def return_pokemon(self, poke: PokemonBase) -> None:
        """
        This method put poke to the front of the queue only if the poke isn't fainted

        :param: poke (PokemonBase) - a PokemonBase object

        :pre: ensure that the argument poke is an object of PokemonBase

        :return: None

        :complexity: Best O(N), where N is length of pokeTeamMembers
                     WorstO(N), where N is length of pokeTeamMembers
        """
        try:
            assert (isinstance(poke,PokemonBase)), "poke should be an object of PokemonBase"
        except AssertionError as e:
            raise ValueError(e)

        if not poke.is_fainted(): 
            temp_queue = CircularQueue(len(self.pokeTeamMembers))

            # add all the pokemon in the queue to temporary queue
            for _ in range(len(self.pokeTeamMembers)):
                item = self.pokeTeamMembers.serve()
                temp_queue.append(item)

            # ensure the queue is clear now
            self.pokeTeamMembers.clear()

            # put the poke to the front of the queue
            self.pokeTeamMembers.append(ListItem(poke, poke.pokedex))  # remember that we want list items

            # add back the pokemon which we store in the temp queue to the queue 
            for _ in range(len(temp_queue)):
                item = temp_queue.serve()
                self.pokeTeamMembers.append(item)


    def retrieve_pokemon(self) -> PokemonBase | None:
        """ 
        This method retrieves the first pokemon in the team or None if the team is empty

        :param: None

        :pre: None

        :return: First pokemon in the team (PokemonBase) or None

        """ 
        len_poke_team = len(self.pokeTeamMembers)

        if len_poke_team == 0:
            print("No pokemon")
            return None

        first_pokemon = self.pokeTeamMembers.serve()

        # the object is a list item 
        return first_pokemon.value

    def special(self) -> None:
        """ 
        This method swaps the position of the first and last pokemon on the team

        :param: None

        :pre: None

        :return: None

        :complexity: Best O(N), where N is length of pokeTeamMembers
                     WorstO(N), where N is length of pokeTeamMembers
        """ 
        if len(self.pokeTeamMembers) == 1:
            print("Special not available")
            temp = CircularQueue(len(self.pokeTeamMembers))
            item = self.pokeTeamMembers.serve()
            self.pokeTeamMembers.append(item)
            temp.append(item)

            
        # This is to store all elements except first and last   
        temp_queue = CircularQueue(len(self.pokeTeamMembers)-2)

        # This is new queue
        new_queue = CircularQueue(len(self.pokeTeamMembers))

        # Get first item
        first_item = self.pokeTeamMembers.serve()

        # Add all elements except last element
        for i in range(len(self.pokeTeamMembers)-1):
            temp_queue.append(self.pokeTeamMembers.serve())

        # Get last element
        try:
            last_item = self.pokeTeamMembers.serve()
        except Exception: # when only one pokemon left, this method should do nothing, so pokeTeamMembers should remain unchanged.
            self.pokeTeamMembers = temp
        else:
            # Add last element
            new_queue.append(last_item)

            # Add all elements in temp_queue to new_queue
            for i in range(len(temp_queue)):
                new_queue.append(temp_queue.serve())    
            # Add first element     
            new_queue.append(first_item)
                        
            self.pokeTeamMembers = new_queue

class BattleMode1():
    """
    Class of generating CircularQueue object and peforming operations on the poke teams with battle mode 0
    Complexity: All functions, unless stated otherwise, have best/worst case complexity of O(1)
    """
    def __init__(self, poke_team_list) -> None:
        """
        This method invoked automatically to set a newly created object's attributes to their initial state.

        :param: poke_team_list (list) - the list of the poke team

        :pre: None

        :return: None

        :complexity: Best O(N), where N is length of pokeTeamMembers
                     WorstO(N), where N is length of pokeTeamMembers
        """
        self.poke_team_list = poke_team_list
        self.pokeTeamMembers = self.generate_queue_ADT_battle_1()

    def generate_queue_ADT_battle_1(self) -> CircularQueue:
        """
         This method generate a queue for the pokemon team in battle mode 1

        :param: None

        :pre: None

        :return: pokeTeamMembers (CircularQueue obj) - the queue which stores the pokemon

        :complexity: Best O(N), where N is length of pokeTeamMembers
                     WorstO(N), where N is length of pokeTeamMembers
        """
        array_poke_team = self.poke_team_list
        len_poke_team = len(self.poke_team_list)

        self.pokeTeamMembers = CircularQueue(len_poke_team)

        for i in range(len_poke_team):
            self.pokeTeamMembers.append(array_poke_team[i])

        return self.pokeTeamMembers

    def return_pokemon(self, poke: PokemonBase) -> None:
        """
        This method put poke to the end of the queue only if the poke isn't fainted

        :param: poke (PokemonBase) - a PokemonBase object

        :pre: ensure that the argument poke is an object of PokemonBase

        :return: None

        :complexity: Best O(N), where N is len(pokeTeamMembers)
                     Worst O(N), where N is len(pokeTeamMembers)
        """
        try:
            assert (isinstance(poke,PokemonBase)), "poke should be an object of PokemonBase"
        except AssertionError as e:
            raise ValueError(e)

        # add the pokemon to the end of the queue if it is not fainted
        if not poke.is_fainted():
            self.pokeTeamMembers.append(ListItem(poke, poke.pokedex))


    def retrieve_pokemon(self) -> PokemonBase | None:
        """
        This method retrieves the first pokemon in the team or None if the team is empty

        :param: None

        :pre: None

        :return: First pokemon in the team (PokemonBase) or None

        """ 
        len_poke_team = len(self.pokeTeamMembers)

        if len_poke_team == 0:
            return None

        # get the pokemon at the start of the queue
        first_pokemon = self.pokeTeamMembers.serve()

        # the object is a list item
        return first_pokemon.value

    def special(self) -> None:
        """ 
        Swap the first halve and second halve of the team (second half includes the middle pokemon for odd team num
        and reverse the order of the front half.

        if the num of pokemon is 5, mid_idx = 2
        if the num of pokemon is 6, mid_idx = 3

        :param: None

        :pre: None

        :return: None
    
        :complexity: Best O(N), where N is length of pokeTeamMembers
                     WorstO(N), where N is length of pokeTeamMembers
            
        """

        num_of_pokemon = len(self.pokeTeamMembers)
        mid_idx = num_of_pokemon // 2

        # store the first halve of the team in temp_stack
        temp_stack = ArrayStack(mid_idx)
        for _ in range(mid_idx):
            item = self.pokeTeamMembers.serve()
            temp_stack.push(item)

        # add the front team which in the stack back to the queue
        for _ in range(mid_idx):
            item = temp_stack.pop()
            self.pokeTeamMembers.append(item)

        temp_stack.clear()

class BattleMode2():
    """Class which defines how to generate and how to perform operations on poke teams with battle mode 2"""
    def __init__(self, team_numbers, criterion):
        """ 

        This method invoked to set a newly created Poke Team object's attributes to their initial state.

        :param arg1: team_numbers (list[int]) - List representing the number of specific pokemons to generate
        :param arg2: criterion (Criterion) - Criterion to sort the members in Poke Team (default = None)

        :pre: None

        :return: None

        :complexity: Best O(N^2), where N is sum of team_numbers
                     Worst O(N^2), where N is sum of team_numbers
        """

        self.criterion = criterion
        self.pokeTeamMembers = self.bm_2_team(team_numbers)  # this is sorted by criterion only

    def get_criterion(self, pokemon: PokemonBase) -> int:
        """ 
        This method retrieves the attribute value of the pokemon based on the criterion specified on PokeTeam creation

        :param arg1: pokemon (PokemonBase) 

        :pre: None

        :return: speed or hp or level or defence stat(int) of the pokemon

        :complexity: Best O(1)
                     Worst O(1)
        """
        if self.criterion == Criterion.SPD:
            return pokemon.get_current_speed()
        elif self.criterion == Criterion.HP:
            return pokemon.get_hp()
        elif self.criterion == Criterion.LV:
            return pokemon.get_level()
        elif self.criterion == Criterion.DEF:
            return pokemon.get_defence()

    def bm_2_team(self, team_numbers) -> BM2SortedList[ListItem(PokemonBase, int)]:
        """ 

        This method returns a BM2SortedList instance containing ListItems of the pokemon with their criterion values based on team_numbers

        :param arg1: team_numbers (list[int])  - List representing the number of specific pokemons to generate

        :pre: None

        :return: pokeTeamMembers (BM2SortedList[ListItem(PokemonBase, int)])
        
        :complexity: Best O(N^2), where N is sum of team_numbers
                     Worst O(N^2), where N is sum of team_numbers
        """        

        pokeTeamMembers = BM2SortedList(sum(team_numbers), 1)
        for i in range(5): # always 5
            for j in range(len(team_numbers)): # always 5
                if i == j:
                    for k in range(team_numbers[j]): # this executes sum(team_numbers) times
                        if i == 0:
                            pokeTeamMembers.add(ListItem(Charmander(k), self.get_criterion(Charmander()))) # add is O(len(pokeTeamMembers))
                        elif i == 1:
                            pokeTeamMembers.add(ListItem(Bulbasaur(k), self.get_criterion(Bulbasaur())))
                        elif i == 2:
                            pokeTeamMembers.add(ListItem(Squirtle(k), self.get_criterion(Squirtle())))
                        elif i == 3:
                            pokeTeamMembers.add(ListItem(Gastly(k), self.get_criterion(Gastly())))
                        elif i == 4:
                            pokeTeamMembers.add(ListItem(Eevee(k), self.get_criterion(Eevee())))
        return pokeTeamMembers

    def return_pokemon(self, poke: PokemonBase) -> None:
        """ 
        This method returns the poke back to the team if it has not fainted

        :param arg1: poke (PokemonBase) - The pokemon to be returned to the team

        :pre: ensure that the argument poke is an object of PokemonBase

        :return: None

        :complexity: Best O(N), where N is length of pokeTeamMembers
                     WorstO(N), where N is length of pokeTeamMembers
        """ 
        try:
            assert (isinstance(poke,PokemonBase)), "poke should be an object of PokemonBase"
        except AssertionError as e:
            raise ValueError(e)

        criterion_value = self.get_criterion(poke)
        if not poke.is_fainted(): 
            self.pokeTeamMembers.add(ListItem(poke, criterion_value)) # O(len(pokeTeamMembers))

    def retrieve_pokemon(self) -> PokemonBase | None:
        """ 
        This method retrieves the first pokemon in the team or None if the team is empty

        :param: None

        :pre: None

        :return: First pokemon in the team (PokemonBase) or None

        :complexity: Best O(N), where N is length of pokeTeamMembers
                     Worst O(N), where N is length of pokeTeamMembers
        """ 
        list_item = self.pokeTeamMembers.delete_at_index(0) # O(len(pokeTeamMembers))
        if list_item is not None:
            return list_item.value
        return None

    def special(self):
        """
        Reverses the sorting of the criterion and also the pokedex from increasing to decreasing and vice versa

        :param: None

        :pre: None

        :return: None

        :complexity: Best case: O(N^2), where N is length of pokeTeamMembers
                     Worst case: O(N^2), where N is length of pokeTeamMembers        
        
        """
 
        new_order = 1-self.pokeTeamMembers.order
        queue = CircularQueue(len(self.pokeTeamMembers)) # O(len(self.pokeTeamMembers))

        for i in range(len(self.pokeTeamMembers)): # O(len(self.pokeTeamMembers))
            queue.append(self.pokeTeamMembers[i])

        self.pokeTeamMembers = BM2SortedList(len(queue), new_order) # O(len(self.pokeTeamMembers))

        for i in range(len(queue)): # O(len(self.pokeTeamMembers))
            self.pokeTeamMembers.add(queue.serve()) # O(len(self.pokeTeamMembers))

        # reverse pokedex sorting
        self.pokeTeamMembers = PokeTeam.sort_by_pokedex(self.pokeTeamMembers, new_order)



class PokeTeam(BattleMode0, BattleMode1, BattleMode2):
    """Class for generating poke teams and performing operations on poke team"""
    class AI(Enum):
        ALWAYS_ATTACK = auto()
        SWAP_ON_SUPER_EFFECTIVE = auto()
        RANDOM = auto()
        USER_INPUT = auto()

    MAX_TEAM_SIZE = 6   # class variable for maximum team size

    def __init__(self, team_name: str, team_numbers: list[int], battle_mode: int, ai_type: PokeTeam.AI, criterion=None,
                 criterion_value=None) -> None:
        """ 
        This method invoked to set a newly created PokeTeam object's attributes to their initial state,
        generate PokeTeam based on the team_numbers passed in as argument.

        :param arg1: team_name (string)        - Name for the Poke Team in string
        :param arg2: team_numbers (list[int])  - List representing the number of specific pokemons to generate
        :param arg3: battle_mode (int)         - Integer representing battle mode for the team
        :param arg4: ai_type (PokeTeam.AI)     - AI Mode to be used by the Poke Team during battle
        :param arg5: criterion (Criterion)     - Criterion to sort the members in Poke Team (default = None)
        :param arg6: criterion_value (int)     - Number to select closest pokemon to criterion value (default = None)

        :pre:
        - team_name must be string
        - team_numbers must be list of integer with sum of numbers not exceeding 6
        - battle_mode must be integer between 0 to 2
        - ai_type should be member of enum class AI if specified, or none by default
        - criterion should be member of enum class Criterion, or none by default
        - criterion value should be integer larger than 0 if specified, and none by default
        - criterion should be member of enum class Criterion and not none when battle_mode is 2
        
        :return:None

        :complexity: Best O(N), where N is sum of team_numbers
                     Worst O(N^2), where N is sum of team_numbers
        """
        try:
            assert team_name is not None and isinstance(team_name, str), "Team name should be string"
            assert team_numbers is not None and len(team_numbers) == 5 and all([isinstance(num,int) and num >= 0 for num in team_numbers]) and sum(team_numbers) <= PokeTeam.MAX_TEAM_SIZE, "Team numbers should be list with integers not exceeding 6"
            assert battle_mode is not None and isinstance(battle_mode,int) and 0 <= battle_mode <= 2, "Battle mode should be integer 0,1 or 2"
            assert (ai_type is None or isinstance(ai_type,PokeTeam.AI)), "AI Mode should be AI enum member (ALWAYS_ATTACK/SWAP_ON_SUPER_EFFECTIVE/RANDOM/USER_INPUT)"
            # assert (criterion is None or isinstance(criterion,Criterion)), "Criterion should be criterion enum member (SPD/HP/LV/DEF)"
            assert criterion_value is None or (isinstance(criterion_value, int) and criterion_value > 0), "Criterion value must be integer larger than zero"
            if battle_mode == 2:
                assert criterion is not None and isinstance(criterion,Criterion), "Criterion must be specified for battle mode 2"
                assert (criterion is None or isinstance(criterion,Criterion)), "Criterion should be criterion enum member (SPD/HP/LV/DEF)"
        except AssertionError as e:
            raise ValueError(e)

        self.team_name = team_name
        self.team_numbers = team_numbers
        self.battle_mode = battle_mode
        self.ai_type = ai_type
        self.criterion = criterion
        self.criterion_value = criterion_value
        self.heal_times = 0
        self.won_against = None
        self.pokeTeamMembers = self.generate_team()

    def generate_team(self) -> CircularQueue | BM2SortedList:
        """
        Generate a team based on the team_number and battle mode.

        :param: None

        :pre: None

        :return: CircularQueue (Battle mode 0 or 1) or BM2SortedList (Battle mode 2)

        :complexity: Best O(N), where N is sum of team_numbers
                     Worst O(N^2), where N is sum of team_numbers
        """
        team_numbers = self.team_numbers
        if self.battle_mode == 0:
            # generate team for battle_mode 0 (CircularQueue)
            self.poke_team_list = self.bm_0_or_1_team(team_numbers) # generate ArraySortedList containing pokemons as ListItem according to team_numbers
            self.bm = BattleMode0(self.poke_team_list)              # generate CircularQueue based on the ArraySortedList

        elif self.battle_mode == 1:
            # generate team for battle_mode 1 (CircularQueue)
            self.poke_team_list = self.bm_0_or_1_team(team_numbers) # generate ArraySortedList containing pokemons as ListItem according to team_numbers
            self.bm = BattleMode1(self.poke_team_list)              # generate Stack based on the ArraySortedList

        elif self.battle_mode == 2:
            # generate team for battle_mode 2 (BM2SortedList)
            # the criterion is used as the key for each pokemon to get sorted in the ArraySortedList
            self.bm = BattleMode2(team_numbers,self.criterion)                          # BattleMode2.pokeTeamMembers is sorted based on criterion
            self.bm.pokeTeamMembers = self.sort_by_pokedex(self.bm.pokeTeamMembers, 1)  # Now it is sorted by pokedex to break ties in criterion

        return self.bm.pokeTeamMembers      # return the pokeTeamMembers as the team generated based on battle mode

    @classmethod
    def random_team(cls, team_name: str, battle_mode: int, team_size=None, ai_mode=None, **kwargs) -> PokeTeam:
        """
        Generate a team based on the team_number generated randomly for a random team.

        :param arg1: team_name (string)        - Name for the Poke Team in string
        :param arg2: team_numbers (list[int])  - List representing the number of specific pokemons to generate
        :param arg3: battle_mode (int)         - Integer representing battle mode for the team
        :param arg4: ai_type (PokeTeam.AI)     - AI Mode to be used by the Poke Team during battle

        :pre: None

        :return: PokeTeam object initialised using arguments passed in

        :complexity: Best O(N^2), where N is sum of team_numbers
                     Worst O(N^2), where N is sum of team_numbers
        """
        team_numbers = cls.generate_random_team(team_size)
        return PokeTeam(team_name, team_numbers, battle_mode, ai_mode, **kwargs)

    @classmethod
    def generate_random_team(cls, team_size:int|None = None) -> list[int]:
        """
        Generate list of integers as team_numbers for random team generation based on the team_size.

        :param arg1: team_size (int) - Integer representing the number of pokemon to generate in the team.

        :pre: team_size is a positive integer greater or equal to 0

        :return: team_numbers (list[int]) - list of integers representing number of different type of pokemon in a team

        :complexity: Best O(N), where N is the maximum team size for PokeTeam object
                     Worst O(N), where N is the maximum team size for PokeTeam object
        """
        team_numbers = list()
        if team_size is None:
            # Generate team size between half of poke limit and poke limit
            team_size = RandomGen.randint(PokeTeam.MAX_TEAM_SIZE//2, PokeTeam.MAX_TEAM_SIZE)

        try:
            assert isinstance(team_size, int) and team_size >= 0
        except AssertionError:
            raise ValueError("Team size must be integer greater or equal than 0")

        # Sorted list for team number generation
        sorted_list_team_num = ArraySortedList(PokeTeam.MAX_TEAM_SIZE)

        # Add 0 and team size to sorted list
        sorted_list_team_num.add(ListItem(0, 0))
        sorted_list_team_num.add(ListItem(team_size, team_size))

        # Generate and add 4 random numbers from 0 to team size
        for _ in range(4):
            random_number = RandomGen.randint(0, team_size)
            sorted_list_team_num.add(ListItem(random_number, random_number))

        team_numbers = []
        # 1-0, 2-1, 3-2, 4-3, 5-4, where 5 is len-1
        first = 0
        second = 1
        for i in range(len(sorted_list_team_num) - 1):
            team_numbers.append(sorted_list_team_num[second].value - sorted_list_team_num[first].value)
            first += 1
            second += 1
        return team_numbers

    @classmethod
    def sort_by_pokedex(self, lst: BM2SortedList, order: int) -> BM2SortedList:
        """
        Sorts the BM2SortedList based on its ListItem's key in specified order, where order 1 is ascending, order 0 is descending.
        This method is called when breaking ties for criterion values of pokemon in the BM2SortedList.
        This method uses Bubble sort for sorting.

        :param arg1: lst (BM2SortedList) - BM2SortedList object to get sorted
        :param arg2: order (int) - Integer representing ascending or descending order to get sorted.

        :pre: 
        - lst must be BM2SortedList object where BM2SortedList has swap method defined.
        - order must be integer 0 or 1

        :return: lst - Sorted BM2SortedList which is the Bm2SortedList passed in as argument   

        :complexity: Best O(N), where N is the length of the BM2SortedList
                     Worst O(N^2), where N is the length of the BM2SortedList
        """
        try:
            assert lst is not None and isinstance(lst, BM2SortedList), "lst must be BM2SortedList object"
            assert order is not None and isinstance(order, int) and (order == 0 or order == 1), "Order must be integer 0 (ascending) or 1 (descending) only"
        except AssertionError as e:
            raise ValueError(e)

        if order == 1: # ascending pokedex
            # traverse through all ListItems in BM2SortedList
            for mark in range(len(lst) - 1, 0, -1):
                swapped = False

                # last "mark" elements are already in correct place
                for i in range(mark):
                    # if have same key(criterion), then check pokedex value to sort based on pokedex order
                    if (lst[i].key == lst[i + 1].key) and (lst[i].value.pokedex > lst[i + 1].value.pokedex):
                        lst.swap(i, i + 1)
                        swapped = True

                # if no swapping occur by inner loop, lst is sorted. Break the loop.
                if not swapped:
                    break
            return lst
            
        elif order == 0: # descending pokedex
            # traverse through all ListItems in BM2SortedList
            for mark in range(len(lst) - 1, 0, -1):
                swapped = False
                # last "mark" elements are already in correct place
                for i in range(mark):
                    # if have same key(criterion), then check pokedex value to sort based on pokedex order
                    if (lst[i].key == lst[i + 1].key) and (lst[i].value.pokedex < lst[i + 1].value.pokedex):
                        lst.swap(i, i + 1)
                        swapped = True
                # if no swapping occur by inner loop, lst is sorted. Break the loop.
                if not swapped:
                    break
            return lst            

    def bm_0_or_1_team(self, team_numbers: list[int]) -> ArraySortedList:
        """
        Creates an ArraySortedList for the PokeTeam object based on team_numbers passed in.
        The ArraySortedList will contain ListItem of Pokemon object and its pokedex order as key.

        :param: team_numbers (list[int])  - List representing the number of specific pokemons to generate

        :pre: None

        :return: pokeTeamMembers (ArraySortedList) - ArraySortedList with ListItems of pokemon and its order in pokedex

        :complexity: Best O(N), where N is smallest possible number for specific pokemon.
                     Worst O(N*M) where N is maximum team size for PokeTeam object, M is length of pokeTeamMembers
        """
        pokeTeamMembers = ArraySortedList(sum(team_numbers))
        for i in range(5):
            for j in range(len(team_numbers)):  # This executes constant times, since team_numbers is always 5
                if i == j:
                    for k in range(team_numbers[j]):    # Worst case: This case executes PokeTeam.MAX_TEAM_SIZE times
                        # add Pokemon object and their pokedex order as ListItem into the ArraySortedList
                        if i == 0:
                            pokeTeamMembers.add(ListItem(Charmander(k), Charmander().pokedex))  # add is O(len(pokeTeamMembers))
                        elif i == 1:
                            pokeTeamMembers.add(ListItem(Bulbasaur(k), Bulbasaur().pokedex))
                        elif i == 2:
                            pokeTeamMembers.add(ListItem(Squirtle(k), Squirtle().pokedex))
                        elif i == 3:
                            pokeTeamMembers.add(ListItem(Gastly(k), Gastly().pokedex))
                        elif i == 4:
                            pokeTeamMembers.add(ListItem(Eevee(k), Eevee().pokedex))

        return pokeTeamMembers

    def retrieve_pokemon(self) -> PokemonBase | None:
        """
        Retrieve the first pokemon in PokeTeam based on the battle mode of PokeTeam.

        :param: None

        :pre: None

        :return: Pokemon object which inherits PokemonBase class.
        
        :complexity: Best O(1), when battle mode is 0 or 1
                     Worst O(N), where N is the length of ArraySortedList for PokeTeam in battle mode 2
        """
        if isinstance(self.bm, BattleMode0):
            poke = BattleMode0.retrieve_pokemon(self)
            return poke
        elif isinstance(self.bm, BattleMode1):
            poke = BattleMode1.retrieve_pokemon(self)
            return poke
        elif isinstance(self.bm, BattleMode2):
            poke = BattleMode2.retrieve_pokemon(self)
        return poke

    def return_pokemon(self, poke: PokemonBase) -> None:
        """
        Reset status of pokemon and return it to its team based on battle mode of PokeTeam.

        :param arg1: poke (PokemonBase) - Pokemon object to get returned back to its team

        :pre: None

        :return: None

        :complexity: Best O(N), where N is the length of pokeTeamMembers
                     Worst O(N^2), where N is the length of pokeTeamMembers
        """
        if poke is not None: 
            poke.status = "free"
        poke.paralysis()
        if isinstance(self.bm, BattleMode0):
            BattleMode0.return_pokemon(self, poke)
        elif isinstance(self.bm, BattleMode1):
            BattleMode1.return_pokemon(self, poke)
        elif isinstance(self.bm, BattleMode2):
            BattleMode2.return_pokemon(self, poke)
            order = self.pokeTeamMembers.order
            self.pokeTeamMembers = self.sort_by_pokedex(self.pokeTeamMembers, order)

    def special(self) -> None:
        """  
        Calls special function for team based on their battle mode.

        :param: None

        :pre: None

        :return: None

        :complexity: Best O(N), where N is length of pokeTeamMembers
                     Worst O(N^2), where N is length of pokeTeamMembers
        """
        if isinstance(self.bm, BattleMode0):
            BattleMode0.special(self)
        elif isinstance(self.bm, BattleMode1):
            BattleMode1.special(self)
        elif isinstance(self.bm, BattleMode2):
            BattleMode2.special(self)

    def regenerate_team(self) -> None:
        """
        Regenerate team based on its team_numbers and reset its heal_times to 0.

        :param: None

        :pre: None

        :return: None

        :complexity: Best O(N), where N is the length of the pokeTeamMembers (Battle mode 0 or 1)
                      Worst O(N^2), where N is the length of the pokeTeamMembers (Battle mode 2)
        """
        battle_mode = self.battle_mode
        if battle_mode == 0 or battle_mode == 1:
            # generate CircularQueue based on team_numbers for battle mode 0 and 1
            pokeTeamList = self.bm_0_or_1_team(self.team_numbers)
            bm = BattleMode0(pokeTeamList)
            self.pokeTeamMembers = bm.pokeTeamMembers

        elif battle_mode == 2:
            # generate ArraySortedList based on team_numbers for battle mode 2
            self.pokeTeamMembers = self.bm_2_team(self.team_numbers)
            # Sort in decresing pokemon order to break ties for criterion value
            self.pokeTeamMembers = self.sort_by_pokedex(self.pokeTeamMembers, 1)

        # reset heal_times to 0
        self.heal_times = 0

    def __str__(self) -> str:
        """
        Return string representation for PokeTeam object.

        :param: None

        :pre: None

        :return: String representation of PokeTeam

        :complexity: Best O(N), where N is length of pokeTeamMembers
                     Worst O(N), where N is length of pokeTeamMembers
        """
        queue_items = []
        result = f"{self.team_name} ({self.battle_mode}): ["

        if self.battle_mode == 0 or self.battle_mode == 1:
            # need to serve and append back the ListItems to queue after getting the string for battle mode 0 and 1
            original_length = self.pokeTeamMembers.length
            for i in range(original_length):
                item = self.pokeTeamMembers.serve()
                result += str(item.value)
                if i < original_length - 1:
                    result += ", "
                self.pokeTeamMembers.append(item)

            for i in range(len(queue_items)):
                self.pokeTeamMembers.append(queue_items[i])
            
        elif self.battle_mode == 2:
            # iterate through the whole ArraySortedList to get the string representation for each pokemon in the team
            result += ", ".join([str(self.pokeTeamMembers[i].value) for i in range(len(self.pokeTeamMembers))])

        return result + "]"

    @classmethod
    def leaderboard_team(cls):
        raise NotImplementedError()

    def is_empty(self) -> bool:
        """ 
        This method returns truth value of whether the PokeTeam array is empty

        :param: None

        :pre: None

        :return: True when PokeTeam array is not empty, False otherwise.  

        :complexity: Best O(1)
                     Worst O(1)
        """
        return len(self.pokeTeamMembers) == 0

    def choose_battle_option(self, my_pokemon: PokemonBase, their_pokemon: PokemonBase) -> Action:
        """ 
        This method returns Action chosen during battle by attacking pokemon based on its team's AI type/mode

        :param arg1: my_pokemon    - Attacking Pokemon object to choose battle option
        :param arg2: their_pokemon - Defending Pokemon object
        :pre: None
        :return: Action enum class member        
        :complexity: Best O(N), where N is the length of actions list
                     Worst O(N), where N is the length of actions list
        """
        # make actions into list
        actions = list(Action)

        if self.ai_type == self.AI.ALWAYS_ATTACK:
        # always attack
            return actions[0]

        elif self.ai_type == self.AI.SWAP_ON_SUPER_EFFECTIVE:
        # swap if opposing pokemon attack are super effective (>= 1.5)
            if 1.5 <= their_pokemon.type_multiplier(my_pokemon) <= 2:
                return actions[1]
            else:
            # else attack
                return actions[0]

        elif self.ai_type is None or self.ai_type == self.AI.RANDOM or self.ai_type == self.AI.USER_INPUT: 
            if self.heal_times >= 3:
                # remove heal option if already reached maximum heal times
                actions.remove(Action.HEAL)
            if self.ai_type == self.AI.RANDOM or self.ai_type is None:
                # return a random action in the actions list
                return actions[RandomGen.randint(0, len(actions) - 1)]

            if self.ai_type == self.AI.USER_INPUT:
                # prompt user for user input
                return self.user_input(input(f"Enter AI Mode that you want in integer {actions}: "), actions)

    def user_input(self, input: str, actions: list) -> Action:
        """
        This method returns Action based on the input by user from the actions list.

        :param arg1: input      - String of user input 
        :param arg2: actions - List consisting of Action enum members

        :pre: 
        - User input can be parsed as integer
        - User input is in range 1 to length of actions list

        :return: Action enum class member       

        :complexity: Best O(1), since accessing items in list has constant time
                     Worst O(1), since accessing items in list has constant time
        """
        user_input = int()
        try:
            # test if user input is integer
            print(f"Enter AI Mode that you want in integer {actions}: ")
            user_input = int(input)
            # test if user input is valid enum member
            assert 1 <= user_input <= len(actions), f"Please enter an integer from 1 to {len(actions)}"
        except ValueError:
            raise ValueError(f"Please enter an integer from 1 to {len(actions)}")
        except AssertionError as e:
            raise ValueError(e)

        # return selected Action based on enum value
        return actions[user_input-1]

