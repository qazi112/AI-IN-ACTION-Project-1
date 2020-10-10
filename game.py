import arcade
import os
import random

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 350
SCREEN_HEIGHT = 350
SCREEN_TITLE = "Sprite Bouncing Coins"

MOVEMENT_SPEED = 5


class MyGame(arcade.Window):
    
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.background = None
        self.coin_list = None
        # self.wall_list = None

    def setup(self):

        # Sprite lists
        # self.wall_list = arcade.SpriteList()
        # self.coin_list = arcade.SpriteList()
        self.background = arcade.load_texture("back.jpg")
        self.coin_list = arcade.SpriteList()
        # -- Set up the walls

        # Create horizontal rows of boxes
        # for x in range(32, SCREEN_WIDTH, 64):
        #     # Bottom edge
        #     wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
        #     wall.center_x = x
        #     wall.center_y = 32
        #     self.wall_list.append(wall)

        #     # Top edge
        #     wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
        #     wall.center_x = x
        #     wall.center_y = SCREEN_HEIGHT - 32
        #     self.wall_list.append(wall)

        # # Create vertical columns of boxes
        # for y in range(96, SCREEN_HEIGHT, 64):
        #     # Left
        #     wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
        #     wall.center_x = 32
        #     wall.center_y = y
        #     self.wall_list.append(wall)

        #     # Right
        #     wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
        #     wall.center_x = SCREEN_WIDTH - 32
        #     wall.center_y = y
        #     self.wall_list.append(wall)

        # # Create boxes in the middle
        # for x in range(128, SCREEN_WIDTH, 196):
        #     for y in range(128, SCREEN_HEIGHT, 196):
        #         wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", SPRITE_SCALING)
        #         wall.center_x = x
        #         wall.center_y = y
        #         # wall.angle = 45
        #         self.wall_list.append(wall)

        # Create coins
        # for i in range(10):
        coin = arcade.Sprite("tick.png", 0.4,)
        coin.center_x = 500
        coin.center_y = 500
        print(coin._get_width())
            # while coin.change_x == 0 and coin.change_y == 0:
            #     coin.change_x = random.randrange(-4, 5)
            #     coin.change_y = random.randrange(-4, 5)

        self.coin_list.append(coin)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

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
        
        for x in range(0, SCREEN_WIDTH+1, 70):
            arcade.draw_line(x, 0, x, SCREEN_HEIGHT, arcade.color.WHITE_SMOKE, 3)

        for x in range(0,SCREEN_HEIGHT+1, 70):
            arcade.draw_line(0, x, SCREEN_WIDTH, x, arcade.color.WHITE_SMOKE, 3)
        self.coin_list.draw()
        # Draw all the sprites.
        # self.wall_list.draw()
        # self.coin_list.draw()
        myText = "Arsalan"
        for rows in range(0,SCREEN_WIDTH,70):
            for columns in range(0,SCREEN_HEIGHT,70):
                print(arcade.draw_text(myText,rows,columns,arcade.color.AERO_BLUE,bold=True))
        
    def on_update(self, delta_time):
        """ Movement and game logic """
        pass
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


