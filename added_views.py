# This is our main file (2 players done)
import arcade
import sys, copy
SPRITE_SNAIL = 0.114

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
SCREEN_TITLE = "Snails Game"

"""
======================================================================

                        All Views 
======================================================================

"""
#  Menu View
class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.screen = arcade.load_texture("images/menu.jpg")

        

    def on_draw(self):
        arcade.start_render()
        
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.screen)
        snail = arcade.Sprite("images/menusnail.png")
        snail.scale = 0.5
        snail.center_x = 300
        snail.center_y = 350
        snail.draw()
        arcade.draw_text("Intelligent Snail", SCREEN_WIDTH/2, SCREEN_HEIGHT - 100,
                         arcade.color.WHITE_SMOKE, font_size=40, anchor_x="center",font_name='comic')
        arcade.draw_text("Press Space To Proceed...!", SCREEN_WIDTH/2,80 ,
                         arcade.color.WHITE_SMOKE, font_size=30, anchor_x="center" ,font_name='comic')
        
        

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:

            instructions_view = InstructionView()
            self.window.show_view(instructions_view)


# Instruction View


class InstructionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Instructions Screen", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = MyGame()
        game_view.setup()
        self.window.show_view(game_view)

"""
======================================================================

                        Extra Views Ended
======================================================================

"""
"""
======================================================================

        Main Game View (All Main Code For Game is Here)
======================================================================

"""

class MyGame(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        """
        Set up the application.
        """

        super().__init__()

        # Create a 2 dimensional array. A two dimensional
        # array is simply a list of lists.
        # Grid is backend ..... 2d array
        self.grid = []
        self.background = None
        self.snail_one = None
        self.snail_two = None
        self.splash_player_list = None
        self.splash_bot_list = None
        self.turn = None
        self.player_score = 0
        self.bot_score = 0
        self.bot_position = [9,9]   # Global to game Current location of bot
        self.player_position = [0,0]

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
        self.splash_player_list = arcade.SpriteList()
        self.splash_bot_list = arcade.SpriteList()


        # Setting up the sprites by calling make_sprites()
        self.snail_one = self.make_sprites("snailone.png",SPRITE_SNAIL)
        self.snail_two = self.make_sprites("snailRed.png",SPRITE_SNAIL,True)
        self.turn = 1
        # print(self.check_possible_actions((9,0)))
        # print(self.islegalMove(1,(1,2),(2,2)))
        # sys.exit()

    
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
    # This creates splashes  
    def create_splashes(self,x,y,name):
        print(x,y)
        splash = arcade.Sprite(f"images/{name}")
        splash.scale = SPRITE_SNAIL
        cen_x = (MARGIN + WIDTH) * (y) + MARGIN + WIDTH // 2
        cen_y = (MARGIN + HEIGHT) * (x) + MARGIN + HEIGHT // 2
        splash.center_x = cen_x
        splash.center_y = cen_y
        print(splash.center_x,splash.center_y)
        return splash
    
    # This function evaluates the board (Backend Grid)
    # Game-loop part (function completed so far)
    def evaluateBoard(self):
        player_score = 0
        bot_score = 0
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == 0:
                    return 0
                elif self.grid[row][col] == 1 or self.grid[row][col] == 10 :
                    player_score += 1
                elif self.grid[row][col] == 2 or self.grid[row][col] == 20 :
                    bot_score += 1
        
        if bot_score == player_score:
            return 50
        elif bot_score > player_score:
            return 200
        elif player_score > bot_score:
            return 100
        
    # Game Loop part (IsleagalMove)
    # Current_pos and new_pos should be passed as a tuple tuple((x,y))
    # This function returns [result,new_row,new_column]
    # if result == True it means it was a legal move else illegal move
    # In case of legal move it will retun True and new row and column nmbr
    def islegalMove(self,turn,current_pos,new_pos):
        actions = self.check_possible_actions(tuple(current_pos))
        # actions contains all possible actions
        # Logic if new_pos is in actions list , so it's good to go ahead
        if list(new_pos) in actions:
           
            # valid move so far
            row,col = new_pos
          
            if turn == 1 : #player turn
                # Check for opponent slime or opponent snail
                if self.grid[row][col] == 2 or self.grid[row][col] == 20:
                    # Invalid move
                    return False,current_pos[0],current_pos[1]   
                elif self.grid[row][col] == 0:
                    return True,row,col
                elif self.grid[row][col] == 10:
                    print(row,col)
                    # Edge Case for moving on its slime
                    location = list(self.spliry_surface((row,col),current_pos,turn))
                    # Updating grid and front end stuff
                    self.grid[current_pos[0]][current_pos[1]] = 10 
                    self.grid[location[0]][location[1]] = 1
                    splash = self.create_splashes(current_pos[0],current_pos[1],"splashBlue.png")
                    self.splash_player_list.append(splash)
                    self.splash_player_list.draw()
                    self.splash_player_list.update()
                    self.snail_one.center_x = (MARGIN + WIDTH) * (location[1]) + MARGIN + WIDTH // 2
                    self.snail_one.center_y = (MARGIN + HEIGHT) * (location[0]) + MARGIN + HEIGHT // 2 
                    self.snail_one.update()
                    return False,current_pos[0],current_pos[1] 
            elif turn == 0: #Bot turn
                if self.grid[row][col] == 1 or self.grid[row][col] == 10:
                    # Invalid move
                    return False,current_pos[0],current_pos[1]   
                elif self.grid[row][col] == 0:
                    return True,row,col
                elif self.grid[row][col] == 20:
                    location = list(self.spliry_surface((row,col),current_pos,turn))
                    # Updating grid and front end stuff
                    self.grid[current_pos[0]][current_pos[1]] = 20 
                    self.grid[location[0]][location[1]] = 2
                    splash = self.create_splashes(current_pos[0],current_pos[1],"splashRed.png")
                    self.splash_bot_list.append(splash)
                    self.splash_bot_list.draw()
                    self.splash_bot_list.update()
                    self.snail_two.center_x = (MARGIN + WIDTH) * (location[1]) + MARGIN + WIDTH // 2
                    self.snail_two.center_y = (MARGIN + HEIGHT) * (location[0]) + MARGIN + HEIGHT // 2 
                    self.snail_two.update()
                    return False,current_pos[0],current_pos[1]
        else:
            # Straight Wrong move Rejected
            print("Far Jump not allowed")
            return False,current_pos[0],current_pos[1]

    

    """
        Slipry Function Tested and it is working great
    """
    # Used By is legal 
    def spliry_surface(self,location,current,turn):
        if turn == 1:
            player = 10
            oppo = 20
        elif turn == 0:
            player = 20
            oppo = 10
        row , col = location
        if row == 0 and col == 0:
            return [row,col]
        elif row == 0 and col == 9:
            return [row,col]
        elif row == 9 and col == 0:
            return [row,col]
        elif row == 9 and col == 9:
            return [row,col]  
        
        # elif (row > 0 and row < 9) and (col > 0 and col < 9):
        else:
            """
            -------------------------------------------
            Horizontal
            """
            # Check for horizontal move
            if col - current[1] > 0 :
                new_col = col
                new_row = row
                # It means horizontal increasing row same
                for x in range(col+1 , 9+1):
                    if self.grid[row][x] == player:
                        new_col = x
                    elif self.grid[row][x] == 0:
                        break 
                # It should return [row, new_col]

            elif col - current[1] < 0 :
                # it means horizontal decreasing row same
                new_col = col
                new_row = row
                for i in reversed(range(col)):
                    if self.grid[row][i] == player:
                        new_col = i
                    elif self.grid[row][i] == 0:
                        break 
            # Vertical movement
            elif col - current[1] == 0:
                # Vertical Movement confirm
                new_row = row
                new_col = col
                # Increasing row direction
                if row - current[0] > 0:
                    for x in range(row+1 , 10):
                        if self.grid[x][col]  == player:
                            new_row = x
                        elif self.grid[x][col]  == 0:
                            break
                # Decreasing row
                elif row - current[0] < 0:
                    for x in reversed(range(row)):
                        if self.grid[x][col]  == player:
                            new_row = x
                        elif self.grid[x][col]  == 0:
                            break
            return [new_row,new_col]
               

    # This function gets row and column and checks for all its possible valid next moves
    # location == tuple(row,column) 
    # This is sub function of islegalMove()
    def check_possible_actions(self,location):
        row , column= location
        possible_actions = []
        if (row > 0 and row < 9) and (column > 0 and column < 9):
            possible_actions.append([row,column-1]) 
            possible_actions.append([row,column+1])
            possible_actions.append([row-1,column])
            possible_actions.append([row+1,column])
        
        elif row == 0:
            if column == 0:
                possible_actions.append([row+1,column])
                possible_actions.append([row,column+1])
            elif column == 9:
                possible_actions.append([row+1,column])
                possible_actions.append([row,column-1])
            elif column > 0 and column < 9:
                possible_actions.append([row,column+1])
                possible_actions.append([row,column-1])
                possible_actions.append([row+1,column])
        elif row == 9:
            if column == 0:
                possible_actions.append([row-1,column])
                possible_actions.append([row,column+1])
            elif column == 9:
                possible_actions.append([row-1,column])
                possible_actions.append([row,column-1])
            elif column > 0 and column < 9:
                possible_actions.append([row,column+1])
                possible_actions.append([row,column-1])
                possible_actions.append([row-1,column])
        elif row < 9 and column == 9:
            possible_actions.append([row,column-1])
            possible_actions.append([row-1,column])
            possible_actions.append([row+1,column])
        elif (row > 0 and row < 9) and column == 0:
            possible_actions.append([row,column+1])
            possible_actions.append([row-1,column])
            possible_actions.append([row+1,column])
          

        return possible_actions
        


    def on_draw(self):
        """ Render the screen."""
        # This command has to happen before we start drawing
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        # Draw Front end grid
        self.initialize_grid()
        # # Draw Splashes and Sprites
            # player drawings
        self.splash_player_list.draw()
        self.snail_one.draw()

            # bot Drawings
        # self.splash_bot_list.draw()
        self.splash_bot_list.draw()
        self.snail_two.draw()
        # self.evaluateBoard()
        
    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        result = self.evaluateBoard()
        if result == 0:
            print("Continue State")
            print(self.grid)
        # Change the x/y screen coordinates to grid coordinates
        column = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))
        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")
        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist

        # Row == row from backend grid and colum form backend grid
        if row < ROW_COUNT and column < COLUMN_COUNT:
            if self.turn == 1:
                # Checking for the legal move
                current_y = self.snail_one.center_x // (MARGIN + WIDTH)
                current_x = self.snail_one.center_y // (MARGIN + HEIGHT)
                
                result,new_x,new_y = self.islegalMove(self.turn,tuple((current_x,current_y)),tuple((row,column)))
                # If move is legal
                if result:
                    self.grid[new_x][new_y] = 1
                    self.grid[current_x][current_y] = 10
                    self.player_position = [new_x,new_y]
                    print("New x y")
                    print(self.player_position)
                    self.player_score += 1
                    self.snail_one.center_x = (MARGIN + WIDTH) * (new_y) + MARGIN + WIDTH // 2
                    self.snail_one.center_y = (MARGIN + HEIGHT) * (new_x) + MARGIN + HEIGHT // 2 
                    self.snail_one.update()
                    splash = self.create_splashes(current_x,current_y,"splashBlue.png")
                    self.splash_player_list.append(splash)
                    self.splash_player_list.draw()
                    self.splash_player_list.update()
                    self.turn = 0 #bot turn given
                    print("Player one moved")

                else:
                    print("No score awarded")
                    self.turn = 0 #bot turn given

            elif self.turn == 0:
                # Checking for the legal move
                current_y = self.snail_two.center_x // (MARGIN + WIDTH)
                current_x = self.snail_two.center_y // (MARGIN + HEIGHT)
                print(current_x,current_y)
                result , new_x,new_y = self.islegalMove(self.turn,tuple((current_x,current_y)),tuple((row,column)))
                if result:
                    print("PLayer 2 result true")
                    print(new_x,new_y)
                    self.grid[new_x][new_y] = 2
                    self.grid[current_x][current_y] = 20
                    self.bot_score += 1
                    self.snail_two.center_x = (MARGIN + WIDTH) * (new_y) + MARGIN + WIDTH // 2
                    self.snail_two.center_y = (MARGIN + HEIGHT) * (new_x) + MARGIN + HEIGHT // 2
                    self.snail_two.update()
                    splash = self.create_splashes(current_x,current_y,"splashRed.png")
                    self.splash_player_list.append(splash)
                    self.splash_player_list.draw()
                    self.splash_player_list.update()
                    self.turn = 1 #player turn given

                else:
                    print("Foul Move Bot, No score awarded")
                    self.turn = 1 #player turn given   
                
            # if self.turn == 1:
            #     # player turn
            #     x = self.snail_one.center_x //(WIDTH+MARGIN) 
            #     y = self.snail_one.center_y //(WIDTH+MARGIN)
            #     splash_one = arcade.Sprite("images/splashBlue.png")
            #     splash_one.scale = SPRITE_SNAIL
            #     splash_one.center_x = self.snail_one.center_x
            #     splash_one.center_y = self.snail_one.center_y
            #     self.splash_player_list.append(splash_one)
            #     self.splash_player_list.draw()
            #     self.snail_one.center_x = (MARGIN + WIDTH) * (column) + MARGIN + WIDTH // 2
            #     self.snail_one.center_y = (MARGIN + HEIGHT) * (row) + MARGIN + HEIGHT // 2
            #     self.turn = 0 #bot turn
            # else:
            #     x = self.snail_two.center_x //(WIDTH+MARGIN) 
            #     y = self.snail_two.center_y //(WIDTH+MARGIN)
            #     splash_one = arcade.Sprite("images/splashRed.png")
            #     splash_one.scale = SPRITE_SNAIL
            #     splash_one.center_x = self.snail_two.center_x
            #     splash_one.center_y = self.snail_two.center_y
            #     self.splash_bot_list.append(splash_one)
            #     self.splash_bot_list.draw()
            #     self.snail_two.center_x = (MARGIN + WIDTH) * (column) + MARGIN + WIDTH // 2
            #     self.snail_two.center_y = (MARGIN + HEIGHT) * (row) + MARGIN + HEIGHT // 2
            #     self.turn = 1 #player turn
                """
                    ===============================================
                """
            # Flip the location between 1 and 0.
            # if self.grid[row][column] == 0:
            #     self.grid[row][column] = 1
            # elif self.grid[row][column] == 2:
            #     self.grid[row][column] = 3
            # elif self.grid[row][column] == 3:
            #      self.grid[row][column] = 2
            # else:
            #     self.grid[row][column] = 0
        else:
            print("Wrong")
    def on_update(self, delta_time):
        self.splash_bot_list.update()
        self.splash_player_list.update()


"""
======================================================================
                    Driver Code Starts Here
======================================================================

"""  
def main():

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Snails Game")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()