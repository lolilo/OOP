import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
from random import randint


"""
You have just arrived in the Bay Area and you're super excited to try all the foods that 
Bay Area has to offer. Navigate the map to collect all the delicious foods and bring it 
to starving Hackbright students. 

If you do not collect enough food for Hackbright, they will send you back out.
"""


#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 8
GAME_HEIGHT = 8

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class BB(GameElement):
    IMAGE = "Chest"
    def interact(self, player):
            player.inventory.append(self)
            GAME_BOARD.draw_msg("You just acquired food! You have %d items!"%(len(player.inventory)))

class HB(GameElement):
    IMAGE = "Rock"


class Cart(GameElement):
    IMAGE = "Heart"


class Character(GameElement):
    IMAGE = "Girl"

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    def next_pos(self, direction):

        # Check if player is trying to move off the board. 
        next_location = (0, 0)

        if direction == "up":
            next_location = (self.x, self.y - 1)
        elif direction == "down":
            next_location = (self.x, self.y + 1)
        elif direction == "left":
            next_location = (self.x - 1, self.y)
        elif direction == "right":
            next_location = (self.x + 1, self.y)

        next_x = next_location[0]
        next_y = next_location[1] 

        # boundary_boolean returns True if it's not safe to move ahead
        out_of_bounds = (next_x < 0 or next_y < 0) or (next_x > GAME_WIDTH - 1 or next_y > GAME_HEIGHT - 1)
        # on_water returns True if player is about to move onto water
        on_water = next_x != 3 and next_y == 3

    # cash
    # list =[a,b,c]
    # for i in list:
    #     if type(i) == type(cash)

        bridge_toll = True
        if next_x == 3 and next_y == 3:
            print self.inventory
            print cash
            if cash in self.inventory:
                GAME_BOARD.draw_msg("You crossed the Golden Gate Bridge!")
            else: 
                GAME_BOARD.draw_msg("You need to pay bridge toll in order to cross the Golden Gate Bridge.")
                bridge_toll = False

        food_quota = True
        if next_x == 7 and next_y == 7:
            if len(self.inventory) < 5:
                GAME_BOARD.draw_msg("This is not enough food. Hackbright students need more!")
                food_quota = False
            else:
                GAME_BOARD.draw_msg("You have made all the Hackbright students' tummies very happy!")
        # if boundary_boolean:
        #     print "It's going to break! Don't move!"

        if not out_of_bounds and not on_water and bridge_toll and food_quota:

            if direction == "up":
                return (self.x, self.y - 1)
            elif direction == "down":
                return (self.x, self.y + 1)
            elif direction == "left":
                return (self.x - 1, self.y)
            elif direction == "right":
                return (self.x + 1, self.y)
        
        return (self.x, self.y)

class Money(GameElement):
    def interact(self, player):
            player.inventory.append(self)
            GAME_BOARD.draw_msg("You just acquired money! You have %d items!"%(len(player.inventory)))
    IMAGE = "BlueGem"
    SOLID = False

   
####   End class definitions    ####

def initialize():
    """Put game initialization code here"""

    rock_positions = [
    (2, 1),
    (1, 2),
    (3, 2)
    ]

    rocks = []

    # for pos in rock_positions:
    #     rock = Rock()
    #     GAME_BOARD.register(rock)
    #     GAME_BOARD.set_el(pos[0], pos[1], rock)
    #     rocks.append(rock)

    # rocks[-1].SOLID = False

    bluebottle = BB()
    GAME_BOARD.register(bluebottle)
    # print randint(0, GAME_WIDTH)
    # print randint(0, GAME_HEIGHT)
    GAME_BOARD.set_el(randint(0, GAME_WIDTH - 1), randint(0, 2), bluebottle)
    GAME_BOARD.set_el(randint(0, GAME_WIDTH - 1), randint(0, 2), bluebottle)
    GAME_BOARD.set_el(randint(0, GAME_WIDTH - 1), randint(0, 2), bluebottle)
    GAME_BOARD.set_el(randint(0, GAME_WIDTH - 1), randint(0, 2), bluebottle)
    GAME_BOARD.set_el(randint(0, GAME_WIDTH - 1), randint(4, GAME_HEIGHT - 1), bluebottle)

    hackbright = HB()
    GAME_BOARD.register(hackbright)
    GAME_BOARD.set_el(7, 7, hackbright)

    cart = Cart()
    GAME_BOARD.register(cart)
    GAME_BOARD.set_el(randint)

    # for rock in rocks: 
    #     print rock

    # In the initialize function
    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)
    print 'this is player', PLAYER

    welcome_message = "Collect all the food you see and deliver to starving Hackbright students!"

    GAME_BOARD.draw_msg(welcome_message)

    global cash
    cash = Money()
    GAME_BOARD.register(cash)
    GAME_BOARD.set_el(randint(0, GAME_WIDTH - 1), randint(0, 2), cash)
    print 'this is cash', cash
    print type(cash)


def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"

    elif KEYBOARD[key.DOWN]:
        direction = "down"

    elif KEYBOARD[key.RIGHT]:
        direction = "right"

    elif KEYBOARD[key.LEFT]:
        direction = 'left'


# bridge is at (3,3). Can only cross bridge if cash is in inventory
# must prevent player from walking on water. 

    if direction: 
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1] 

        existing_el = GAME_BOARD.get_el(next_x, next_y)
        if existing_el:
            existing_el.interact(PLAYER)

        if (existing_el is None or not existing_el.SOLID):
            GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
            GAME_BOARD.set_el(next_x, next_y, PLAYER)

    # elif KEYBOARD[key.SPACE]:
    #     GAME_BOARD.erase_msg()




# def keyboard_handler():
#     if KEYBOARD[key.UP]:
#         GAME_BOARD.draw_msg("You pressed up")
#         next_y = PLAYER.y - 1
#         GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
#         GAME_BOARD.set_el(PLAYER.x, next_y, PLAYER)

#     elif KEYBOARD[key.DOWN]:
#         GAME_BOARD.draw_msg("You pressed down")
#         next_y = PLAYER.y + 1
#         GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
#         GAME_BOARD.set_el(PLAYER.x, next_y, PLAYER)

#     elif KEYBOARD[key.RIGHT]:
#         GAME_BOARD.draw_msg("You pressed right")
#         next_x = PLAYER.x + 1
#         GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
#         GAME_BOARD.set_el(next_x, PLAYER.y, PLAYER)

#     elif KEYBOARD[key.LEFT]:
#         GAME_BOARD.draw_msg("You pressed left")
#         next_x = PLAYER.x - 1
#         GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
#         GAME_BOARD.set_el(next_x, PLAYER.y, PLAYER)

#     elif KEYBOARD[key.SPACE]:
#         GAME_BOARD.erase_msg()


    # GAME_BOARD.erase_msg()

    # rock1 = Rock()
    # GAME_BOARD.register(rock1)
    # # The set_el function takes in three elements, 
    # # the x position, the y position, and the element you're placing at that position. 
    # GAME_BOARD.set_el(1, 1, rock1)

    # # Initialize and register rock2
    # rock2 = Rock()
    # GAME_BOARD.register(rock2)
    # GAME_BOARD.set_el(2, 2, rock2)

    # print "The rock is at", (rock1.x, rock1.y)
    # print "The second rock is at", (rock2.x, rock2.y)
    # print "Rock 1 image", rock1.IMAGE
    # print "Rock 2 image", rock2.IMAGE




# >>> class Pet():
# ...     def __init__(self, name):
# ...             self.name = name
# ... 
# >>> p = Pet("Fido")
# >>> p2 = Pet("Fido")
# >>> p == p2
# False
# >>> print p
# <__main__.Pet instance at 0x7f8a6d32f2d8>
# >>> print p2
# <__main__.Pet instance at 0x7f8a6d32f320>
# >>> p.name
# 'Fido'
# >>> p.name == p2.name
# True
# >>> class Pen();
#   File "<stdin>", line 1
#     class Pen();
#                ^
# SyntaxError: invalid syntax
# >>> class Pen():
# ...     def __repr__(self):
# ...             return "Hi"
# ... 
# >>> pen = Pen()
# >>> print pen
# Hi

