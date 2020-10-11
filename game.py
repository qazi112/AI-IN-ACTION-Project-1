import arcade
import os
import random

SPRITE_SCALING = 0.13
COIN_SCALE = 0.13
COIN_START_SCALE = 35 # like x= 35 and y = 35 of starting
# i have decided to keep each block of width = 70 and height = 70
# now if user want 3 * 3 board , we will simply do, 3*70 = 210 size 

# We can go till 10 X 10
# Grid is made using lines, not actual Grid 

SCREEN_WIDTH = 350
SCREEN_HEIGHT = 350
SCREEN_TITLE = "Sprite Bouncing Coins"
GRID_GAP = 70
MOVEMENT_SPEED = 5


class MyGame(arcade.Window):
    
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.background = None
        self.coin_list = None
        self.splash_list = None
        # self.wall_list = None

    def setup(self):

        # Sprite lists
        # self.wall_list = arcade.SpriteList()
        # self.coin_list = arcade.SpriteList()
        self.background = arcade.load_texture("back.jpg")
        self.coin_list = arcade.SpriteList()
        self.splash_list = arcade.SpriteList()
        
        # Here is First snail creaeted at x = 35 , y =35
        coin = arcade.Sprite("snailone.png")
        # Creating a splash
        splash = arcade.Sprite("splash.png")

        """ x = 35 , y = 35 
            and add 70 to loop through
        """
        coin.center_x = COIN_START_SCALE
        coin.center_y = COIN_START_SCALE
        splash.center_x = COIN_START_SCALE
        splash.center_y = COIN_START_SCALE
        splash.scale = 0.131
        coin.scale = 0.13
        print(coin.bottom)
        print(coin.left)
        
        print(coin.width)
        print(coin.height)
        self.coin_list.append(coin)
        self.splash_list.append(splash)

        
        #  First snail done


        # # Generate Sprite in loop in x axis
        # self.coin_list.append(coin)
        # for x in range(35,SCREEN_WIDTH,70):
        #     coin = arcade.Sprite("snailone.png")
        #     coin.scale = 0.13
        #     coin.center_x = x
        #     coin.center_y = 35
        #     self.coin_list.append(coin)
        # # Generate Sprite in loop in y axis
        # for x in range(SCREEN_WIDTH-35 , 0, -70):
        #     coin = arcade.Sprite("snailtwo.png",mirrored=True)
        #     coin.scale = 0.13
        #     coin.center_x = x
        #     coin.center_y = SCREEN_HEIGHT - 35
        #     self.coin_list.append(coin)



        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)
        

        # list for all possible x places for sprite    
        list_for_x = []
        for x in range(COIN_START_SCALE,SCREEN_WIDTH,70):
            list_for_x.append(x)
        print(list_for_x)

        # list for all possible y places for sprite    
        list_for_y = []
        for y in range(COIN_START_SCALE,SCREEN_HEIGHT,70):
            list_for_y.append(y)
        print(list_for_y)      

        # Make random moves
        # coin = arcade.Sprite("snailone.png")
        # coin.center_x = random.choice(list_for_x)
        # coin.center_y = random.choice(list_for_y)

        # coin.scale = 0.13
        # self.coin_list.append(coin)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        # Drawing Lines
        
        for x in range(0, SCREEN_WIDTH+1, GRID_GAP):
            arcade.draw_line(x, 0, x, SCREEN_HEIGHT, arcade.color.WHITE_SMOKE, 3)

        for x in range(0,SCREEN_HEIGHT+1, GRID_GAP):
            arcade.draw_line(0, x, SCREEN_WIDTH, x, arcade.color.WHITE_SMOKE, 3)
        self.splash_list.draw()
        self.coin_list.draw()
        
        # Draw all the sprites.
        # self.wall_list.draw()
        # self.coin_list.draw()
        # myText = "Arsalan"
        # for rows in range(0,SCREEN_WIDTH,GRID_GAP):
        #     for columns in range(0,SCREEN_HEIGHT,GRID_GAP):
        #         arcade.draw_text(myText,rows,columns,arcade.color.AERO_BLUE,bold=True)
        
    def on_update(self, delta_time):
        """ Movement and game logic """
        # self.coin_list[0].left = 0
        # self.coin_list[0].bottom = 0
        # self.coin_list.update()
        # for coin in self.coin_list:

        #     coin.center_x += coin.change_x
        #     walls_hit = arcade.check_for_collision_with_list(coin, self.wall_list)
        #     for wall in walls_hit:
        #         if coin.change_x > 0:
        #             coin.right = wall.left
        #         elif coin.change_x < 0:
        #             coin.left = wall.right
        #     if len(walls_hit) > 0:
        #         coin.change_x *= -1

        #     coin.center_y += coin.change_y
        #     walls_hit = arcade.check_for_collision_with_list(coin, self.wall_list)
        #     for wall in walls_hit:
        #         if coin.change_y > 0:
        #             coin.top = wall.bottom
        #         elif coin.change_y < 0:
        #             coin.bottom = wall.top
        #     if len(walls_hit) > 0:
        #         coin.change_y *= -1


def main():
    """ Main method """

    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()


