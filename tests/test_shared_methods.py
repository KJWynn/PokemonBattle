"""
    This file contains test cases for the shared methods in task 1 and task 2 using unittest. Shared methods to be tested:
    is_fainted, get_speed, get_current_speed, get_attack_damage, get_defence, get_hp, lose_hp, attack,
    get_poke_name, get_level, heal, __str__, should_evolve, can_evolve, type_multiplier, get_status_inflicted, paralysis.

"""
__author__ = "Scaffold by Jackson Goerner, Code by Lim Yi Xuan"

from random_gen import RandomGen
from pokemon import Blastoise, Bulbasaur, Charizard, Charmander, Gastly, Gengar, Haunter, Squirtle, Eevee, Venusaur
from tests.base_test import BaseTest


class TestIsFainted(BaseTest):
    """ 3 Tests for is_fainted function, where hp < 0, hp == 0, hp > 0"""
    def test_is_fainted_lt_0(self):
        """Test case for pokemon fainting when hp less than 0"""
        # e is fainted when hp is less than 0
        e = Eevee()
        e.lose_hp(e.get_hp()+100)           # make e lose its original hp + 100 to ensure hp will be less than 0
        self.assertLess(e.get_hp(), 0)      # hp must be less than 0
        self.assertTrue(e.is_fainted())     # e is fainted when hp less than 0

    def test_is_fainted_eq_0(self):
        """Test case for pokemon fainting when hp is 0"""
        # e is fainted when hp is 0
        e = Eevee()
        e.lose_hp(e.get_hp())               # make e lose its original hp
        self.assertEqual(e.get_hp(), 0)     # e now has 0 hp
        self.assertTrue(e.is_fainted())     # e is fainted when hp is 0
    
    def test_not_fainted(self):
        """Test case for pokemon fainting when hp greater than 0"""
        # e is not fainted when hp greater than 0
        e = Eevee()
        self.assertGreater(e.get_hp(), 0)   # e has not lose any hp, hp is greater than 0
        self.assertFalse(e.is_fainted())    # e is not fainted when hp greater 0
        

class TestGetSpeed(BaseTest):
    """3 Tests for get_speed functions, for 3 different pokemons"""        
    def test_get_speed_eevee(self):
        """Test case for getting speed of Eevee before and after levelling up"""
        # Base speed of eevee is 8, speed increase to 9 after levelling up
        e = Eevee()
        self.assertEqual(e.get_speed(),8)   # e base speed is 8
        e.level_up()                        # e levels up
        self.assertEqual(e.get_speed(),9)   # e speed increase to 9 after levelling up

    def test_get_speed_bulbasaur(self):
        """Test case for getting speed of Bulbasaur before and after levelling up"""
        # Base speed of bulbasaur is 7
        b = Bulbasaur()
        self.assertEqual(b.get_speed(), 7)  # Base speed of bulbasaur is 7
        b.level_up()                        # b levels up
        self.assertEqual(b.get_speed(),8)   # Speed becomes 8 after levelling up

    def test_get_speed_evolve_gastly(self):
        """Test case for getting speed of Gastly before and after evolving"""
        # Base speed of gastly is 2, speed becomes 6 after evolving to haunter
        g = Gastly()
        self.assertEqual(g.get_speed(), 2)  # Base speed of gastly is 2
        h = g.get_evolved_version()         
        self.assertIsInstance(h, Haunter)   # Gastly evolves to haunter
        self.assertEqual(h.get_speed(), 6)  # Haunter has base speed 6
    

class TestGetCurrentSpeed(BaseTest):
    """3 tests for get_current_speed for 3 different pokemon"""
    def test_get_current_speed_paralysed_gastly(self):
        """Test case for getting current speed for paralysed Gastly"""
        g = Gastly()
        self.assertEqual(g.get_current_speed(),2)   # Base speed for gastly is 2
        g.status = 'paralysis'
        g.paralysis()                               # Gastly get paralysed
        self.assertEqual(g.get_current_speed(),1)   # Current speed for gastly is halved speed = 1

    def test_get_current_speed_paralysed_charmander(self):
        """Test case for getting current speed for paralysed Charmander during and after paralysis effect cleared"""
        c = Charmander()
        self.assertEqual(c.get_current_speed(),8)   # Base speed for charmander is 8
        c.status = 'paralysis'
        c.paralysis()                               # Charmander is paralysed
        self.assertEqual(c.get_current_speed(),4)   # Paralysed charmander has halved speed = 4
        c.status = "free"
        c.paralysis()                               # Paralysis effect wears off for charmander
        self.assertEqual(c.get_current_speed(),8)   # Speed returns to 8 after paralyse effect wears off

    def test_get_current_speed_paralysed_eevee(self):
        """Test case for getting current speed for Eevee before and after paralysis"""
        e = Eevee()
        self.assertEqual(e.get_speed(),8)           # Base speed for eevee is 7
        e.status = 'paralysis'
        e.paralysis()                               # Eevee gets paralysed
        self.assertEqual(e.get_current_speed(),4)   # Paralysed eevee has halved speed = 3

class TestGetAttackDamage(BaseTest):
    """3 Tests for get_attack_damage, for 3 different pokemons"""        
    def test_get_attack_dmg_eevee(self):
        """Test case for getting attack damage by Eevee before and after levelling up"""
        # Base attack for eevee is 7, increase to 8 after levelling up
        e = Eevee()
        self.assertEqual(e.get_attack_damage(),7)   # Base attack for eevee is 7
        e.level_up()                                # e levels up
        self.assertEqual(e.get_attack_damage(),8)   # Attack damage increase to 8 after levelling up

    def test_get_attack_dmg_squirtle(self):
        """Test case for getting attack damage by Squirtle before and after levelling up"""
        # Base attack for squirtle is 4, increase to 5 after levelling up
        s = Squirtle()
        self.assertEqual(s.get_attack_damage(),4)   # Base attack for squirtle is 4
        s.level_up()                                # s levels up
        self.assertEqual(s.get_attack_damage(),5)   # Attack damage increase to 5 after levelling up

    def test_get_attack_dmg_evolve_charmander(self):
        """Test case for getting attack damage by Charmander before and after evolving"""
        # Base attack for charmander is 7, increase to 16 after evolving to charizard
        c = Charmander()
        self.assertEqual(c.get_attack_damage(),7)   # Base attack for charmander is 7
        c = c.get_evolved_version() 
        self.assertIsInstance(c,Charizard)          # Charmander evolved to charizard
        self.assertEqual(c.get_attack_damage(),16)  # Attack damage increase to 16 after evolving to charizard


class TestGetDefence(BaseTest):
    """3 Tests for get_defence function, for 3 different pokemons"""
    def test_get_defence_charizard(self):
        """Test case for getting defence for Charizard"""
        # Base defense for charizard is 4
        c = Charizard()
        self.assertEqual(c.get_defence(), 4)

    def test_get_defence_eevee(self):
        """Test case for getting defence for Eevee after levelling up"""
        # Base defense for eevee is 5, increase to 6 after levelling up
        e = Eevee()
        self.assertEqual(e.get_defence(),5) # Base defense for eevee is 5
        e.level_up()
        self.assertEqual(e.get_defence(),6) # defence increase to 6 after levelling up

    def test_get_defense_evolve_bulbasaur(self):
        """Test case for getting defence for Bulbasaur after evolve"""
        # Base defense for bulbasaur is 5, defense becomes 10 after evolving to venusaur
        b = Bulbasaur()
        self.assertEqual(b.get_defence(),5) # Base defense for bulbasaur is 5
        v = b.get_evolved_version()
        self.assertEqual(v.get_defence(),10) # Defense becomes 10 after evolving to venusaur


class TestGetHp(BaseTest):
    """3 Tests for get_hp function, for 3 different pokemons"""
    def test_get_hp_eevee(self):
        """Test case for getting current hp of Eevee after before and after losing hp"""
        # Base hp for eevee is 10, becomes 8 after losing 2 hp
        e = Eevee()
        self.assertEqual(e.get_hp(),10) # Base hp for eevee is 10
        e.lose_hp(2)                    # e lose 2 hp
        self.assertEqual(e.get_hp(),8)  # Hp becomes 8 after losing 2 hp

    def test_get_hp_gastly(self):
        """Test case for getting current hp of Gastly before and after losing hp, then levelling up"""
        # Base hp for gastly is 6, becomes 4 after losing 2 hp, hp becomes 5 after level up
        g = Gastly()
        self.assertEqual(g.get_hp(), 6) # g has base hp of 6
        g.lose_hp(2)                    # g loses 2 hp
        self.assertEqual(g.get_hp(), 4) # Hp becomes 4 after losing 2 hp
        g.level_up()                    # g levels up
        self.assertEqual(g.get_hp(),5)  # Hp becomes 5 to remain same difference after levelling up

    def test_get_hp_evolve_bulbasaur(self):
        """Test case for getting current hp of Bulbasaur before and after evolving"""
        # Base hp for bulbasaur is 12, hp becomes 14 after evolving to venusaur
        b = Bulbasaur()
        self.assertEqual(b.get_hp(),13)  # Base hp for bulbasaur is 12
        v = b.get_evolved_version()      # Bulbasaur evolves to venusaur
        self.assertEqual(v.get_hp(),21)  # hp becomes 14 after evolving to venusaur


class TestLoseHp(BaseTest):
    """3 Tests for lose_hp function, for invalid lose hp, lose hp = negative value, lose hp = positive value"""
    def test_lose_hp_invalid(self):
        """Test case for passing invalid argument to lose_hp (non positive integer)"""
        e = Eevee()
        self.assertEqual(e.get_hp(),10)                                 # e has base hp of 10
        self.assertRaises(TypeError, lambda: e.lose_hp('invalid hp'))   # raise TypeError when input is invalid type

    def test_lose_hp_positive(self):
        """Test case for passing valid argument to lose_hp for Eevee"""
        e = Eevee()
        self.assertEqual(e.get_hp(),10)                                 # e has base hp of 10
        e.lose_hp(2)                                                    # e loses 2 hp
        self.assertEqual(e.get_hp(),8)                                  # e has 8 hp after losing 2 hp

    def test_lose_hp_negative(self):
        """Test case for passing invalid argument to lose_hp (negative)"""
        e = Eevee()
        self.assertEqual(e.get_hp(),10)                                 # e has base hp of 10
        self.assertRaises(ValueError, lambda: e.lose_hp(-2))            # raise ValueError when hp to be lost is negative


class TestAttack(BaseTest):
    """3 test case for 3 different sets of attack against different pokemon"""
    def test_attack_confusion_sleep(self):
        """Test case for attacks with confuse and sleep status between Eevee and Gastly"""
        RandomGen.set_seed(0)
        e = Eevee()
        g = Gastly()

        e.attack(g)                             # e attack g
        self.assertEqual(g.status,'confuse')  # e attacks g and make g confused
        self.assertEqual(g.get_hp(), 6)         # Normal type (e) has type multiplier 0 for ghost type(g), g remains at initial hp 6
        g.attack(e)                             # g attack e
        self.assertEqual(g.get_hp(), -2)        # g is confused and attacks itself (loses 8 hp)
        self.assertEqual(g.status, 'sleep')     # g inflicted sleep on itself
        g.attack(e)                             # g attack e again
        self.assertEqual(e.get_hp(),10)         # g fails to attack when asleep, e remains at full hp 10

    def test_attack_burn_poison(self):
        """Test case for attacks with burn and poison status between Charmander and Bulbasaur"""
        RandomGen.set_seed(0)
        c = Charmander()
        b = Bulbasaur()
    
        c.attack(b)
        self.assertEqual(b.status,'burn')       # c inflict burn status to b
        # fire type has type multiplier 2 against grass, effective damage dealt is 7*2 = 14 after defence calculation
        self.assertEqual(b.get_hp(), -1)        # b now has -1 hp after attacked by c
        b.attack(c)                             # b attacks c
        self.assertEqual(b.status,'burn')       # b remains in burn status
        # grass type has type multiplier 1 against grass, but because b is in burn status, effective damage is halved
        # c loses 0 hp from b (5*0.5)//2)//2 = 0
        self.assertEqual(c.get_hp(), 9)         # c remains in full hp after b attack
        self.assertEqual(c.status, 'poison')    # b inflict poison status on c
        self.assertEqual(b.get_hp(),-2)         # b loses 1 hp from burn effect

    def test_attack_posion_paralyse(self):
        """Test case for attacks with poison and paralyse status between Squirtle and Bulbasaur"""
        RandomGen.set_seed(0)
        s = Squirtle()  # water, initial hp 11
        b = Bulbasaur() # grass, initial hp 13
    
        b.attack(s)                                 # b attack s
        # b has type multiplier 2 against s
        # s has initial hp 11, after battle, hp = 11 - (2*5)//2 = 6
        self.assertEqual(s.get_hp(),6)              # s loses 5 hp to become 6 hp
        self.assertEqual(s.status,'poison')         # b inflict poison status on s
        s.attack(b)                                 # s attack b
        self.assertEqual(s.status,'poison')         # s remains poisoned
        # s has type multiplier 0.5 against b
        # b has initial hp 13, after battle, hp = 13 - (0.5*4)//2 = 12
        self.assertEqual(b.get_hp(), 12)            # b loses 1 hp to become 12 hp
        self.assertEqual(b.status, 'paralysis')     # b is paralysed by s
        b.paralysis()                               # b is paralysed
        self.assertEqual(b.get_current_speed(), 3)  # current speed of b speed halves due to paralysis
        self.assertEqual(s.get_hp(),3)              # after successful attack, s lose 3 hp due to poison effect
        
        
class TestGetPokeName(BaseTest):
    """3 Test for get_poke_name for 3 different pokemon"""
    def test_get_poke_name_charmander(self):
        """Test case for getting pokemon name for Charmander before and after evolve"""
        c = Charmander()
        self.assertIsInstance(c,Charmander)                 # c is Charmander object
        self.assertEqual("Charmander", c.get_poke_name())   # c has name Charmander
        # Charmander evolves to charizard
        c = c.get_evolved_version()                         # c evolves to Charizard
        self.assertIsInstance(c,Charizard)                  # c is Charizard object
        self.assertEqual("Charizard", c.get_poke_name())    # c has name Charizard

    def test_get_poke_name_eevee(self):
        """Test case for getting pokemon name for Eevee"""
        e = Eevee()
        self.assertIsInstance(e,Eevee)                      # e is Eevee object
        self.assertEqual("Eevee", e.get_poke_name())        # e has name Eevee

    def test_get_poke_name_evolve(self):
        """Test case for getting pokemon name for Gastly before and after evolve"""
        g = Gastly()
        self.assertIsInstance(g,Gastly)                     # g is Gastly object
        self.assertEqual("Gastly", g.get_poke_name())       # g has name Gastly
        h = g.get_evolved_version()                         # g evolves to h
        self.assertIsInstance(h,Haunter)                    # h is Haunter object
        self.assertEqual("Haunter", h.get_poke_name())      # h has name Haunter
        g = h.get_evolved_version()                         # h evolves to g
        self.assertIsInstance(g,Gengar)                     # g is Gengar object
        self.assertEqual("Gengar", g.get_poke_name())       # g has name Gengar


class TestGetLevel(BaseTest):
    """3 test cases of get_level for 3 different types of pokemon"""
    def test_get_level_squirtle(self):
        """Test case for getting level of Squirtle before and after levelling up"""
        s = Squirtle()
        self.assertEqual(s.get_level(),1)       # s has base level 1
        s.level_up()                            # s levels up
        self.assertEqual(s.get_level(),2)       # s now has level 2

    def test_get_level_gengar(self):
        """Test case for getting level of Gengar before and after levelling up"""
        g = Gengar()
        self.assertEqual(g.get_level(),3)       # g has base level 3
        g.level_up()                            # g levels up
        self.assertEqual(g.get_level(),4)       # g now has level 4

    def test_get_level_evolve_bulbasaur(self):
        """Test case for getting level of Bulbasaur before and after levelling up and evolving"""
        b = Bulbasaur()
        self.assertEqual(b.get_level(),1)       # b has base level 1
        b.level_up()                            # b levels up
        self.assertEqual(b.get_level(),2)       # b now has level 2
        v = b.get_evolved_version()             # b evolves to v
        self.assertIsInstance(v,Venusaur)       # v is Venusaur object
        self.assertEqual(v.get_level(),2)       # v has base level 2

class TestHeal(BaseTest):
    """3 different test cases for heal function for 3 different cases of pokemon"""
    def test_heal_level_squirtle(self):
        """Test case for healing Squirtle after levelling up and losing hp"""
        s = Squirtle()
        self.assertEqual(s.get_hp(),11)         # s has base hp of 11
        s.level_up()                            # s levels up
        self.assertEqual(s.get_hp(),13)         # s has hp of 13 now
        s.lose_hp(5)                            # s loses 5 hp
        self.assertEqual(s.get_hp(),8)          # s now has 8 hp
        s.heal()                                # heal s
        self.assertEqual(s.get_hp(),13)         # s restores hp to 13

    def test_heal_paralysed_eevee(self):
        """Test case for clearing status effect for paralysed Eevee after healing"""
        e = Eevee()
        self.assertEqual(e.get_hp(),10)             # e has base hp of 10
        e.status = "paralysis"
        e.paralysis()                               # e gets paralysed
        e.lose_hp(2)                                # e loses 2 hp
        self.assertEqual(e.get_hp(),8)              # e now has 8 hp
        self.assertEqual(e.get_current_speed(),4)   # current speed of e is halved due to paralysis
        e.heal()                                    # heal e
        self.assertEqual(e.get_hp(),10)             # e restores hp to 10
        self.assertEqual(e.status, "free")            # removes paralysis effect
        self.assertEqual(e.get_current_speed(),8)   # current speed restored after removing paralysis effect

    def test_heal_burning_evolve_bulbasaur(self):
        """Test case for clearing status effect for burning evolved Bulbasaur after healing"""
        b = Bulbasaur()
        self.assertEqual(b.get_hp(),13)         # b has base hp of 13
        b.lose_hp(3)                            # b loses 3 hp
        b.status = "burn"                       # b is burning
        self.assertEqual(b.get_hp(),10)         # b now has 10 hp
        v = b.get_evolved_version()             # b evolves to v
        self.assertIsInstance(v,Venusaur)       # v is Venusaur object
        self.assertEqual(v.get_hp(), 18)        # v has 18 hp (same hp difference as before evolving, 21-3 = 18)
        self.assertEqual(v.status,"burn")       # v is burning
        v.heal()                                # heal v
        self.assertEqual(v.get_hp(),21)         # v restores hp to 21, the max hp of evolved version
        self.assertEqual(v.status, "free")        # v is not burning anymore

class TestString(BaseTest):
    """3 test cases of __str__ for 3 different pokemon"""
    def test_str_base_charmander(self):
        """Test case for string representation of Charmander"""
        c = Charmander()
        self.assertEqual(c.get_level(), 1)  # c has base level 1
        self.assertEqual(c.get_hp(), 9)    # c has 9 hp 
        self.assertEqual(str(c), "LV. 1 Charmander: 9 HP")

    def test_str_eevee(self):
        """Test case for string representation of Eevee after losing hp"""
        e = Eevee()
        self.assertEqual(e.get_level(),1)       # e has base level 1
        # e level up 3 times
        e.level_up()
        e.level_up()
        e.level_up()
        self.assertEqual(e.get_level(), 4)      # e now is in level 4
        self.assertEqual(e.get_hp(),10)         # e has 10 hp
        e.lose_hp(2)                            # e loses 2 hp
        self.assertEqual(e.get_hp(),8)          # e now has 8 hp
        self.assertEqual(str(e), "LV. 4 Eevee: 8 HP")

    def test_str_gengar(self):
        """Test case for string representation of Gengar after levelling up"""
        g = Gengar()
        self.assertEqual(g.get_level(), 3)  # g has base level 3
        # g level up 2 times
        g.level_up()
        g.level_up()
        self.assertEqual(g.get_level(), 5)  # g is now level 5
        self.assertEqual(g.get_hp(), 14)    # g has 14 hp 
        g.lose_hp(5)                        # g loses 5 hp
        self.assertEqual(g.get_hp(),9)      # g now has 9 hp left
        self.assertEqual(str(g), "LV. 5 Gengar: 9 HP")


class TestCanEvolve(BaseTest):
    """3 test cases of can_evolve for 3 different pokemons """
    def test_can_evolve_eevee(self):
        """Test case to check if Eevee can evolve"""
        e = Eevee()
        self.assertFalse(e.can_evolve())    # can_evolve returns False because eevee cant evolve

    def test_can_evolve_squirtle(self):
        """Test case to check if Squirtle can evolve after evolving to Blastoise"""
        s = Squirtle()
        self.assertTrue(s.can_evolve())     # can_evolve returns True because squirtle can evolve
        b = s.get_evolved_version()         # s evolves to b
        self.assertIsInstance(b,Blastoise)  # b is Blastoise object
        self.assertFalse(b.can_evolve())    # can_evolves returns False because blastoise cant evolve

    def test_can_evolve_gastly(self):
        """Test case to check if Gastly can evolve after evolving to Haunter"""
        g = Gastly()
        self.assertTrue(g.can_evolve())     # can_evolve returns True because Gastly can evolve
        h = g.get_evolved_version()         # g evolves to h
        self.assertIsInstance(h,Haunter)    # h is Haunter object
        self.assertTrue(h.can_evolve())     # can_evolve returns True because Haunter can evolve
        g = h.get_evolved_version()         # h evolves to g
        self.assertIsInstance(g,Gengar)     # g is now Gengar object
        self.assertFalse(g.can_evolve())    # can_evolve returns False because Gengar cant evolve further


class TestShouldEvolve(BaseTest):
    """3 test cases of should_evolve for 3 different pokemons, True when reach evolving level """
    def test_should_evolve_eevee(self):
        """Test case to check if Eevee should evolve"""
        e = Eevee()
        self.assertFalse(e.should_evolve()) # should_evolve returns False since eevee cant evolve

    def test_should_evolve_squirtle(self):
        """Test case to check if Squirtle should evolve after reaching evolving level"""
        s = Squirtle()
        self.assertTrue(s.can_evolve())     # can_evolve returns True because squirtle can evolve
        self.assertFalse(s.should_evolve()) # should_evolve returns False because level havent reach evolve level
        # s level up 3 times
        s.level_up()
        s.level_up()
        s.level_up()
        self.assertEqual(s.get_level(),4)   # s is now level 4
        self.assertTrue(s.should_evolve())  # should_evolve returns True because level reached evolve level
        b = s.get_evolved_version()         # s evolves to b
        self.assertIsInstance(b,Blastoise)  # b is Blastoise object
        self.assertFalse(b.can_evolve())    # can_evolves returns False because blastoise cant evolve
        self.assertFalse(b.should_evolve()) # should_evolve retruns False because cant evolve

    def test_should_evolve_charmander(self):
        """Test case to check if Charmander can evolve after reaching evolving level"""
        c = Charmander()
        self.assertTrue(c.can_evolve())   # can_evolve return True as charizard can evolve
        self.assertFalse(c.should_evolve())   # should_evolve return False as evolve level not reached
        # level up 2 times
        c.level_up()
        c.level_up()
        self.assertEqual(c.get_level(),3)   # c is now level 3
        self.assertTrue(c.should_evolve())  # c should evolve because reached evolve level


class TestTypeMultiplier(BaseTest):
    """3 test cases for testing type multiplier for all types of pokemon in range 0-1, 1-2, 2"""
    def test_type_multiplier_0_to_1(self):
        """Test cases for all combinations of types that has type multiplier 0 to less than 1"""
        ghost = Gengar()
        normal = Eevee()
        fire = Charizard()
        grass = Bulbasaur()
        water = Squirtle()
        self.assertEqual(0, ghost.type_multiplier(normal))  # ghost has type multiplier 0 against normal
        self.assertEqual(0, normal.type_multiplier(ghost))  # normal has type multiplier 0 against ghost
        self.assertEqual(0.5, fire.type_multiplier(water))  # fire has type multiplier 0.5 against water
        self.assertEqual(0.5, grass.type_multiplier(fire))  # grass has type multiplier 0.5 against fire
        self.assertEqual(0.5, water.type_multiplier(grass)) # water has type multiplier 0.5 against grass
        
    def test_type_multiplier_1_to_2(self):
        """Test cases for all combinations of types that has type multiplier 1 to less than 2"""
        ghost = Gengar()
        normal = Eevee()
        fire = Charizard()
        grass = Bulbasaur()
        water = Squirtle()
        self.assertEqual(1, fire.type_multiplier(fire))         # fire has type multiplier 1 against fire
        self.assertEqual(1, fire.type_multiplier(ghost))        # fire has type multiplier 1 against ghost
        self.assertEqual(1, fire.type_multiplier(normal))       # fire has type multiplier 1 against normal
        self.assertEqual(1, grass.type_multiplier(grass))       # grass has type multiplier 1 against grass
        self.assertEqual(1, grass.type_multiplier(ghost))       # grass has type multiplier 1 against ghost
        self.assertEqual(1, grass.type_multiplier(normal))      # grass has type multiplier 1 against normal
        self.assertEqual(1, water.type_multiplier(water))       # water has type multiplier 1 against water
        self.assertEqual(1, water.type_multiplier(ghost))       # water has type multiplier 1 against ghost
        self.assertEqual(1, water.type_multiplier(normal))      # water has type multiplier 1 against normal
        self.assertEqual(1.25, ghost.type_multiplier(fire))     # ghost has type multiplier 1.25 against fire
        self.assertEqual(1.25, normal.type_multiplier(fire))    # normal has type multiplier 1.25 against fire
        self.assertEqual(1.25, ghost.type_multiplier(grass))    # ghost has type multiplier 1.25 against grass
        self.assertEqual(1.25, normal.type_multiplier(grass))   # normal has type multiplier 1.25 against grass
        self.assertEqual(1.25, ghost.type_multiplier(water))    # ghost has type multiplier 1.25 against water
        self.assertEqual(1.25, normal.type_multiplier(water))   # normal has type multiplier 1.25 against water

    def test_type_multiplier_2(self):
        """Test cases for all combinations of types that has type multiplier 2"""
        fire = Charizard()
        grass = Bulbasaur()
        water = Squirtle()
        ghost = Gengar()
        self.assertEqual(2, fire.type_multiplier(grass))     # fire has type multiplier 2 against grass
        self.assertEqual(2, grass.type_multiplier(water))    # grass has type multiplier 2 against water
        self.assertEqual(2, water.type_multiplier(fire))     # water has type multiplier 2 against fire
        self.assertEqual(2, ghost.type_multiplier(ghost))    # ghost has type multiplier 2 against ghost


class TestGetStatusInflicted(BaseTest):
    """"3 different test case of get_status_inflicted for pairs of different pokemons"""
    def test_get_status_inflicted_burn_poison(self):
        """Test case to get status inflicted by Charizard and Bulbasaur"""
        RandomGen.set_seed(0)
        fire = Charizard()
        grass = Bulbasaur()
        fire.attack(grass)                                        # fire type attacks grass
        self.assertEqual(fire.get_status_inflicted(),'burn')      # fire type can inflict burn status
        self.assertEqual(grass.status, 'burn')                    # fire inflict burn status on grass
        grass.attack(fire)                                        # grass type attack fire
        self.assertEqual(grass.get_status_inflicted(), 'poison')  # grass type can inflict poison status
        self.assertEqual(fire.status, 'poison')                   # grass inflict poison status on fire

    def test_get_status_inflicted_paralysis_sleep(self):
        """Test case to get status inflicted by Squirtle and Gengar"""
        RandomGen.set_seed(0)
        water = Squirtle()
        ghost = Gengar()
        water.attack(ghost)                                         # water type attacks ghost
        self.assertEqual(water.get_status_inflicted(),'paralysis')  # water type can inflict paralysis status
        self.assertEqual(ghost.status,'paralysis')                  # water inflicted paralysis on ghost
        ghost.attack(water)                                         # ghost type attacks water
        self.assertEqual(ghost.get_status_inflicted(),'sleep')      # ghost type can inflict sleep status
        self.assertEqual(water.status,'sleep')                      # ghost inflicted sleep status on water

    def test_get_status_inflicted_sleep_confusion(self):
        """Test case to get status inflicted by Eevee and Gengar"""
        RandomGen.set_seed(0)
        ghost = Gengar()
        normal = Eevee()
        ghost.attack(normal)                                         # ghost type attacks water
        self.assertEqual(ghost.get_status_inflicted(),'sleep')      # ghost type can inflict sleep status
        self.assertEqual(normal.status,'sleep')                      # ghost inflicted sleep status on water

class TestParalysis(BaseTest):
    """3 test case for 3 different cases of entering paralysis function"""
    def test_paralysis_true(self):
        """Test case for entering paralysis function when Pokemon has paralysis status"""
        RandomGen.set_seed(0)
        water = Squirtle()
        ghost = Gengar()
        self.assertEqual(ghost.get_current_speed(),12)              # ghost initial speed is 12
        water.attack(ghost)                                         # water type attacks ghost
        self.assertEqual(water.get_status_inflicted(),'paralysis')  # water type can inflict paralysis status
        self.assertEqual(ghost.status,'paralysis')                  # water inflicted paralysis on ghost
        ghost.paralysis()                                           # enter paralysis function to remove/add paralysis effect
        self.assertEqual(ghost.get_current_speed(),6)               # current speed of ghost is halved to be 6
        self.assertTrue(ghost.isParalysed)                          # ghost is paralysed

    def test_paralysis_overwrite(self):
        """Test case for entering paralysis function when Pokemon paralysis status is overwritten by other status"""
        RandomGen.set_seed(0)
        water = Squirtle()
        ghost = Gengar()
        fire = Charizard()
        self.assertEqual(ghost.get_current_speed(),12)              # ghost initial speed is 12
        water.attack(ghost)                                         # water type attacks ghost
        self.assertEqual(water.get_status_inflicted(),'paralysis')  # water type can inflict paralysis status
        self.assertEqual(ghost.status,'paralysis')                  # water inflicted paralysis on ghost
        ghost.paralysis()                                           # enter paralysis function to remove/add paralysis effect
        self.assertEqual(ghost.get_current_speed(),6)               # current speed of ghost is halved to be 6
        self.assertTrue(ghost.isParalysed)                          # ghost is paralysed

        fire.attack(ghost)                                          # fire attacks ghost
        self.assertEqual(ghost.status,'burn')                       # fire inflict burn status on ghost
        ghost.paralysis()                                           # enter paralysis function to remove/add paralysis effect
        self.assertFalse(ghost.isParalysed)                         # ghost is not paralysed
        self.assertEqual(ghost.get_current_speed(),12)              # restore to original speed after removed paralysis effect

    def test_paralysis_false(self):
        """Test case for entering paralysis function when Pokemon has no paralysis status"""
        ghost = Gengar()
        fire = Charizard()
        self.assertEqual(ghost.get_current_speed(),12)              # ghost has speed of 12
        fire.attack(ghost)                                          # fire attack ghost
        self.assertEqual(ghost.status,'burn')                       # ghost get status burn
        ghost.paralysis()                                           # enter paralysis function to remove/add paralysis effect
        self.assertFalse(ghost.isParalysed)                         # ghost is not paralysed even after entering paralysis function
        self.assertEqual(ghost.get_current_speed(),12)              # speed remains constant when not paralysed
        
        
