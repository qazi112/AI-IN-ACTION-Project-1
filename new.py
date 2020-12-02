# This is our main file
import arcade
SPRITE_SNAIL = 0.114
SPRITE_SCALING_COIN = .25
COIN_COUNT = 50
# Set how many rows and columns we will have
ROW_COUNT = 10
COLUMN_COUNT = 10

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 60
HEIGHT = 60

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 3

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "Array Backed Grid Example"


class InstructionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Instructions Screen", WIDTH/2, HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", WIDTH/2, HEIGHT/2-75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = MyGame()
        self.window.show_view(game_view)

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Set up the application.
        """

        super().__init__(width, height, title)

        # Create a 2 dimensional array. A two dimensional
        # array is simply a list of lists.
        # Grid is backend ..... 2d array
        self.grid = []
        self.background = None
        self.snail_one = None
        self.snail_two = None
        self.one_splash = None
        self.two_splash = None
        self.turn = None
    # Generate BackEnd Grid
    def initialize_board(self,rows,cols):
        grid = []
        for row in range(rows):
            grid.append([])
            for column in range(cols):
                grid[row].append(0)  # Append a cell
        grid[0][0] = 1  # player == 1
        grid[rows-1][cols-1] = 2 # bot == 2
        return grid


    # Pass sprite name , its scaling and specify if oponent or Player Making sprites
    def make_sprites(self,name,sprite_scaling,oponent = False):
        if oponent:
            sprite = arcade.Sprite(f"images/{name}",mirrored= True)
            sprite.scale = sprite_scaling
            sprite.center_x = (MARGIN + WIDTH) * (COLUMN_COUNT-1) + MARGIN + WIDTH // 2
            sprite.center_y = (MARGIN + HEIGHT) * (ROW_COUNT-1) + MARGIN + HEIGHT // 2
            sprite.mirrored = True
        else:
            sprite = arcade.Sprite(f"images/{name}")
            sprite.scale = sprite_scaling
            sprite.center_x = MARGIN + WIDTH // 2
            sprite.center_y = MARGIN + HEIGHT // 2
        return sprite

    # This Sets up all things.... arcade function
    def setup(self):
        # Get Backend grid ready
        self.grid = self.initialize_board(ROW_COUNT,COLUMN_COUNT)
        # arcade.set_background_color(arcade.color.BLACK)
        
        # Background ready
        self.background = arcade.load_texture("images/back.jpg")
        
        # self.snail_one = arcade.Sprite("images/snailone.png")
        # self.snail_one.scale = 0.114
        # self.snail_one.center_x = MARGIN + WIDTH // 2
        # self.snail_one.center_y = MARGIN + HEIGHT // 2
        # self.snail_two = arcade.Sprite("images/snailone.png")
   

        # Setting up the sprites by calling make_sprites()
        self.snail_one = self.make_sprites("snailone.png",SPRITE_SNAIL)
        self.snail_two = self.make_sprites("snailRed.png",SPRITE_SNAIL,True)
        self.one_splash = self.make_sprites("splashBlue.png",SPRITE_SNAIL)
        self.two_splash = self.make_sprites("splashRed.png",SPRITE_SNAIL,True)
        self.turn = 1


    
    # This Function is to make Front end Grid
    def initialize_grid(self):
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
                # Figure out what color to draw the box
                # if self.grid[row][column] == 1:
                #     color = arcade.color.GREEN
                # elif self.grid[row][column] == 2:
                #     color = arcade.color.RED
                # else:
                #     color = arcade.color.EBONY
                color = arcade.color.SMOKE
                color = list(color)
                color.append(120)
                color = tuple(color)
                # Do the math to figure out where the box is
                x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                y = (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2

                # Draw the box
                arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)
    
    

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        # Draw Front end grid
        self.initialize_grid()
        # # Draw Splashes and Sprites
            # player drawings
        self.one_splash.draw()
        self.snail_one.draw()
            # bot Drawings
        self.two_splash.draw()
        self.snail_two.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        

        # Change the x/y screen coordinates to grid coordinates
        column = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))
        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")
        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
        if row < ROW_COUNT and column < COLUMN_COUNT:
            
            if self.turn == 1:
                # player turn
                self.one_splash.center_x = (MARGIN + WIDTH) * (column) + MARGIN + WIDTH // 2
                self.one_splash.center_y = (MARGIN + HEIGHT) * (row) + MARGIN + HEIGHT // 2 
                self.snail_one.center_x = (MARGIN + WIDTH) * (column) + MARGIN + WIDTH // 2
                self.snail_one.center_y = (MARGIN + HEIGHT) * (row) + MARGIN + HEIGHT // 2
                self.turn = 0 #bot turn
            else:
                self.two_splash.center_x = (MARGIN + WIDTH) * (column) + MARGIN + WIDTH // 2
                self.two_splash.center_y = (MARGIN + HEIGHT) * (row) + MARGIN + HEIGHT // 2 
                self.snail_two.center_x = (MARGIN + WIDTH) * (column) + MARGIN + WIDTH // 2
                self.snail_two.center_y = (MARGIN + HEIGHT) * (row) + MARGIN + HEIGHT // 2
                self.turn = 1 #player turn
            # Flip the location between 1 and 0.
            # if self.grid[row][column] == 0:
            #     self.grid[row][column] = 1
            # elif self.grid[row][column] == 2:
            #     self.grid[row][column] = 3
            # elif self.grid[row][column] == 3:
            #      self.grid[row][column] = 2
            # else:
            #     self.grid[row][column] = 0


def main():

    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()