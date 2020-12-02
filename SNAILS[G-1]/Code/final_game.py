# This is our main file (Final code is here)
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
# USED AS LOCAL TO MINIMAX (HEURISTIC)
BOT_POS = [9,9]
PLAYER_POS = [0,0]
bot_places = []
player_places = []
RESULT = 0
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
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Instructions Screen", SCREEN_WIDTH/2, SCREEN_HEIGHT-100,
                         arcade.color.WHITE_SMOKE, font_size=50, anchor_x="center")

        arcade.draw_text("Click to advance", SCREEN_WIDTH/2, SCREEN_HEIGHT-180,
                         arcade.color.RED, font_size=10, anchor_x="center")
        arcade.draw_text("First turn is of Human", SCREEN_WIDTH/2, SCREEN_HEIGHT- 240,
                         arcade.color.WHITE_SMOKE, font_size=16, anchor_x="center")
        arcade.draw_text("In Case of 7 Blocked Turns by both ", SCREEN_WIDTH/2, SCREEN_HEIGHT-300,
                         arcade.color.WHITE_SMOKE, font_size=15, anchor_x="center")
        arcade.draw_text("Human and Computer,Game Result", SCREEN_WIDTH/2, SCREEN_HEIGHT-360,
                         arcade.color.WHITE_SMOKE, font_size=15, anchor_x="center")
        arcade.draw_text("Will be decided on current Grid Position", SCREEN_WIDTH/2, SCREEN_HEIGHT-400,
                         arcade.color.WHITE_SMOKE, font_size=15, anchor_x="center")
        arcade.draw_text("20 -> Bot Slime , 10 -> Human Slime", SCREEN_WIDTH/2, SCREEN_HEIGHT-450,
                         arcade.color.WHITE_SMOKE, font_size=15, anchor_x="center")
        arcade.draw_text("Movement : UP DOWN LEFT RIGHT", SCREEN_WIDTH/2, SCREEN_HEIGHT-480,
                         arcade.color.WHITE_SMOKE, font_size=15, anchor_x="center")                                 
        snail = arcade.Sprite("images/snailone.png")
        snail.scale = 0.15
        snail.center_x = 250
        snail.center_y = 100
        snail.draw()
        snail = arcade.Sprite("images/snailtwo.png")
        snail.scale = 0.15
        snail.center_x = 350
        snail.center_y = 100
        snail.draw()
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = MyGame()
        game_view.setup()
        self.window.show_view(game_view)
    
class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self,result):
        """ This is run once when we switch to this view """
        super().__init__()
        self.result = result
        self.texture = arcade.load_texture("images/back.jpg")

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        message = self.result
        if self.result == 50:
            message = "Draw"
        elif self.result == 100:
            message = "Human Wins"
        elif self.result == 200:
            message = "AI Agent Wins"

        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)
        arcade.draw_text("Game Over... !!!", SCREEN_WIDTH/2, SCREEN_HEIGHT - 100,
                         arcade.color.WHITE_SMOKE, font_size=60, anchor_x="center")

        arcade.draw_text(f"{message}, {self.result}", SCREEN_WIDTH/2, SCREEN_HEIGHT - 200,
                         arcade.color.WHITE_SMOKE, font_size=50, anchor_x="center")
        arcade.draw_text(f"Click To Quit", SCREEN_WIDTH/2, SCREEN_HEIGHT - 300,
                         arcade.color.WHITE_SMOKE, font_size=30, anchor_x="center")
        snail = arcade.Sprite("images/menusnail.png")
        snail.scale = 0.4
        snail.center_x = 300
        snail.center_y = 200
        snail.draw()
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        arcade.close_window()
        

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
        self.BOT_POS = [9,9]
        self.PLAYER_POS = [0,0]
        self.slimed_list = []
        self.slimed_list_play = []
        # For Stuckness logic
        self.NUMBER_OF_TURNS = 0
        self.BOT_TURNS = 0

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
        
        # Background ready
        self.background = arcade.load_texture("images/back.jpg")
        self.splash_player_list = arcade.SpriteList()
        self.splash_bot_list = arcade.SpriteList()


        # Setting up the sprites by calling make_sprites()
        self.snail_one = self.make_sprites("snailone.png",SPRITE_SNAIL)
        self.snail_two = self.make_sprites("snailRed.png",SPRITE_SNAIL,True)
        self.turn = 1

            
    
    # This Function is to make Front end Grid
    def initialize_grid(self):
        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):
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
    def evaluateBoard(self,board):
        player_score = 0
        bot_score = 0
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == 0:
                    return 0
                elif board[row][col] == 1 or board[row][col] == 10 :
                    player_score += 1
                elif board[row][col] == 2 or board[row][col] == 20 :
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
                    elif self.grid[row][x] == 0 or self.grid[row][x] == oppo:
                        break 
                # It should return [row, new_col]

            elif col - current[1] < 0 :
                # it means horizontal decreasing row same
                new_col = col
                new_row = row
                for i in reversed(range(col)):
                    if self.grid[row][i] == player:
                        new_col = i
                    elif self.grid[row][i] == 0 or self.grid[row][i] == oppo:
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
                        elif self.grid[x][col]  == 0 or self.grid[row][x] == oppo:
                            break
                # Decreasing row
                elif row - current[0] < 0:
                    for x in reversed(range(row)):
                        if self.grid[x][col]  == player:
                            new_row = x
                        elif self.grid[x][col]  == 0 or self.grid[row][x] == oppo:
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

    # ===================================================================================
    #                       Functions for AI AGENT
    # ===================================================================================
    def allowed_actions(self,location,board,turn):
        # It also uses possible_actions function
        # Returns List of possible moves for AI Agent
        if turn == 1:
            pos = copy.deepcopy(location)
            slime = 10
        else:
            pos = copy.deepcopy(location)
            slime = 20
        actions = self.check_possible_actions(list(pos))
        # print(actions)
        allowed = []
        slimed = []        
        for acts in actions:
            if board[acts[0]][acts[1]] == 0: 
                allowed.append(acts)
            elif board[acts[0]][acts[1]] == slime:
                slimed.append(acts)
        return allowed,slimed
    
    # So far completed
    def findBestMove(self):
        copied_board = copy.deepcopy(self.grid)
        best_value = -9999
        best_move = copy.deepcopy(self.bot_position)
        # Allowed action return all allowed actions bot slime plus empty
        zero_blocks,slimed = self.allowed_actions(self.bot_position,copied_board,0)
        self.BOT_POS = copy.deepcopy(self.bot_position)
        self.BOT_POS[0] = self.bot_position[0]
        self.BOT_POS[1] = self.bot_position[1]
        print(zero_blocks)
        print(slimed)
        # Logic check for all allowed actions
        if len(zero_blocks) == 0 and len(slimed) == 0:
            print("Blocked Bot No More Moves Left")
            return list(self.bot_position),False
        if len(zero_blocks) == 0 and len(slimed) != 0:
            # Can Move on slime only
            print("In slimed")  
            for slimed_move in slimed:
                result = self.ai_slip_checking(copied_board,slimed_move,self.bot_position,0)
                print("After Slimed")
                print(result)
                value = self.check_situation(copied_board,result)
                if value > best_value:
                    best_value = value
                    best_move[0] = slimed_move[0]
                    best_move[1] = slimed_move[1]
            return list(best_move),True

        if len(zero_blocks) != 0:
            
            for move in zero_blocks:
                copied_board[move[0]][move[1]] = 2
                prev_mov = copy.deepcopy(move)
                copied_board[self.bot_position[0]][self.bot_position[1]] = 20
                self.BOT_POS[0] = move[0]
                self.BOT_POS[1] = move[1]
                
                # This BOT_POS will be used by MINIMAX and its subs
                value = self.minimax(copied_board,0,8,False)
                
                # Undo the move and restore the place

                copied_board[prev_mov[0]][prev_mov[1]] = 0
                copied_board[self.bot_position[0]][self.bot_position[1]] = 2
                self.BOT_POS = copy.deepcopy(self.bot_position)
                if value >= best_value :
                    best_value = value
                    best_move[0] = move[0]
                    best_move[1] = move[1]

       
        
        return list(best_move),False
            
    def heuristic(self,board):
        wining_chances = 0
        # Looking for visited by bot
        for x in range(len(board)):
            for y in range(len(board[x])):
                if board[x][y] == 20 :
                    wining_chances += 1
        
        if self.BOT_POS[0] in range(3,7) and self.BOT_POS[1] in range(3,7):
            wining_chances +=10 
        

        chance = 200
        current = self.current_position(board,True)
        
        xx = abs(current[0] - self.BOT_POS[0])
        yy = abs(current[1] - self.BOT_POS[1])
        import math
        result = int(math.sqrt((xx*xx)+ (yy*xx)))
     
        if result == 0:
            result = 1
            
        chance = int(chance / result)
        
        wining_chances += chance
        
        # Thz currentPos on simulation board
        
        x,y = list(self.BOT_POS)
        chance = self.check_situation(board,self.BOT_POS)
        player = self.check_situation(board,self.PLAYER_POS)
        print(f"h{chance},{player}")
        
        return wining_chances+chance

    def minimax(self,board,depth,max_depth,is_max):
        # print(depth)
        result = self.evaluateBoard(board)
        if result == 100 or result == 200 or result == 50 or depth == 7:
           
            # print(result+self.heuristic(board))
            return result + self.heuristic(board)
        if is_max:
            # Bot turn(0)
            best = -10000
            zero_moves , slimed_moves = self.allowed_actions(self.BOT_POS,board,0)
            
            if len(zero_moves) == 0 and len(slimed_moves) == 0:
                print("Blocked Bot No More Moves Left")
                
            elif len(zero_moves) == 0 and len(slimed_moves) != 0:
                # Slimed Moves
                for move in slimed_moves:
                    result = self.ai_slip_checking(board,move,self.BOT_POS,0)
                    self.slimed_list.append(self.BOT_POS)
                    board[self.BOT_POS[0]][self.BOT_POS[1]] = 20
                    board[result[0]][result[1]] = 2
                    self.BOT_POS[0] = result[0]
                    self.BOT_POS[1] = result[1]
                    best = max(best,self.minimax(board,depth+1,8,False))
                    board[result[0]][result[1]] = 20
                    pos = list(self.slimed_list.pop())
                    self.BOT_POS = copy.deepcopy(pos)
                    board[pos[0]][pos[1]] = 2
                
            elif len(zero_moves) != 0:
                # Zeros left
                for move in zero_moves:
                    board[move[0]][move[1]] = 2
                    board[self.BOT_POS[0]][self.BOT_POS[1]] = 20
                    bot_places.append(self.BOT_POS)
                    self.BOT_POS = copy.deepcopy(move)
                    best = max(best,self.minimax(board,depth+1,8,False))
                    # Undo the move
                    board[move[0]][move[1]] = 0
                    pos = list(bot_places.pop())
                    self.BOT_POS = copy.deepcopy(pos)
                    board[pos[0]][pos[1]] = 2
            return best

        else:
            best = 1000
            # Player turn(1) simulation
            zero_move, slimed = self.allowed_actions(self.PLAYER_POS,board,1)
            
            if len(zero_move) == 0 and len(slimed) == 0:
                print("Blocked Human No More Moves Left")
                
            elif len(zero_move) == 0 and len(slimed) != 0:
                # Slimed Moves
                for move in slimed:
                    result = self.ai_slip_checking(board,move,self.PLAYER_POS,1)
                    self.slimed_list_play.append(self.PLAYER_POS)
                    board[self.PLAYER_POS[0]][self.PLAYER_POS[1]] = 10
                    board[result[0]][result[1]] = 1
                    self.PLAYER_POS[0] = result[0]
                    self.PLAYER_POS[1] = result[1]
                    best = min(best,self.minimax(board,depth+1,7,True))
                    board[result[0]][result[1]] = 10
                    pos = list(self.slimed_list_play.pop())
                    self.PLAYER_POS = copy.deepcopy(pos)
                    board[pos[0]][pos[1]] = 2
                
            elif len(zero_move) != 0:
                # Zeros left 
                for move in zero_move:
                    board[move[0]][move[1]] = 1
                    board[self.PLAYER_POS[0]][self.PLAYER_POS[1]] = 10
                    player_places.append(self.PLAYER_POS)
                    self.PLAYER_POS = copy.deepcopy(move)
                    # print(board)
                    best = min(best,self.minimax(board,depth+1,8,True))
                    # Undo the move
                    board[move[0]][move[1]] = 0
                    pos = list(player_places.pop())
                    self.PLAYER_POS = copy.deepcopy(pos)
                    board[pos[0]][pos[1]] = 1
            return best




    
    def bot_playing(self):
        self.BOT_POS = copy.deepcopy(self.bot_position)
        print(self.bot_position)
        move,is_slimed = list(self.findBestMove())
        self.BOT_TURNS += 1
        if move == self.bot_position:
            # print("Blocked, No score awarded")
            self.turn = 1
        elif is_slimed == False:
            
            self.bot_score += 1
            self.BOT_TURNS = 0
            self.grid[move[0]][move[1]] = 2
            self.grid[self.bot_position[0]][self.bot_position[1]] = 20
            pre_x = self.bot_position[0]
            pre_y = self.bot_position[1]
            self.bot_position = copy.deepcopy(move)
            self.snail_two.center_x = (MARGIN + WIDTH) * (move[1]) + MARGIN + WIDTH // 2
            self.snail_two.center_y = (MARGIN + HEIGHT) * (move[0]) + MARGIN + HEIGHT // 2
            self.snail_two.update()
            splash = self.create_splashes(pre_x,pre_y,"splashRed.png")
            self.splash_player_list.append(splash)
            self.splash_player_list.draw()
            self.splash_player_list.update()
            self.turn = 1

        elif is_slimed:
            print(f"Selected Move {move} ")
            row,col = self.spliry_surface(move,self.bot_position,0)
            self.grid[row][col] = 2
            self.grid[self.bot_position[0]][self.bot_position[1]] = 20
            pre_x = self.bot_position[0]
            pre_y = self.bot_position[1]
            self.bot_position[0] = row
            self.bot_position[1] = col
            splash = self.create_splashes(pre_x,pre_y,"splashRed.png")
            self.splash_bot_list.append(splash)
            self.splash_bot_list.draw()
            self.splash_bot_list.update()
            self.snail_two.center_x = (MARGIN + WIDTH) * (col) + MARGIN + WIDTH // 2
            self.snail_two.center_y = (MARGIN + HEIGHT) * (row) + MARGIN + HEIGHT // 2 
            self.snail_two.update()
            self.turn = 1
    def ai_slip_checking(self,board,location,current,turn):
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
                    if board[row][x] == player:
                        new_col = x
                    elif board[row][x] == 0:
                        break 
                # It should return [row, new_col]

            elif col - current[1] < 0 :
                # it means horizontal decreasing row same
                new_col = col
                new_row = row
                for i in reversed(range(col)):
                    if board[row][i] == player:
                        new_col = i
                    elif board[row][i] == 0:
                        break 
            # Vertical movement
            elif col - current[1] == 0:
                # Vertical Movement confirm
                new_row = row
                new_col = col
                # Increasing row direction
                if row - current[0] > 0:
                    for x in range(row+1 , 10):
                        if board[x][col]  == player:
                            new_row = x
                        elif board[x][col]  == 0:
                            break
                # Decreasing row
                elif row - current[0] < 0:
                    for x in reversed(range(row)):
                        if board[x][col]  == player:
                            new_row = x
                        elif board[x][col]  == 0:
                            break
            return [new_row,new_col]

    # This function will be used by may be heuristic
    def check_situation(self,board,postion):
        x,y = postion
        chances = 0
        # If Row is zero
        if x == 0:
            if y == 0:
                if True:
                # if board[x][y+1] == 0 or board[x+1][y] == 0:
                    for row in range(x+1,6):
                        for col in range(y+1,6):
                            if board[row][col] == 0:
                                chances += 1
            elif y == 9:
                if True:
                # if board[x][y-1] == 0 or board[x+1][y] == 0:
                    for row in range(x+1,6):
                        for col in reversed(range(5,y)):
                            if board[row][col] == 0:
                                chances += 1
            # Check in surrounding mini board number of empty boxes
            else:
                if True :
                # if board[x][y+1] == 0 or board[x+1][y] == 0 or board[x][y-1] == 0 :
                    for row in range(x,5):
                        for col in range(y,y+3):
                            if col > 9 :
                                break
                            if board[row][col] == 0:
                                chances += 1
                    for row in range(x,5):
                        for col in range(y,y-3,-1):
                            if col < 0  :
                                break
                            if board[row][col] == 0:
                                chances += 1
        # if row is 9
        elif x == 9:
            if y == 0:
                if True:
                # if board[x][y+1] == 0 or board[x-1][y] == 0:
                    for row in range(x,x-5,-1):
                        for col in range(y,5):
                            if board[row][col] == 0:
                                chances += 1
            elif y == 9:
                if 1==1:
                # if board[x][y-1] == 0 or board[x-1][y] == 0:
                    for row in range(x,x-5,-1):
                        for col in range(y,y-5,-1):
                            if board[row][col] == 0:
                                chances += 1
            # Check in surrounding mini board number of empty boxes
            else:
                if True :
                # if board[x][y+1] == 0 or board[x-1][y] == 0 or board[x][y-1] == 0 :
                    for row in range(x,x-4,-1):
                        for col in range(y,y+3):
                            if col > 9 :
                                break
                            if board[row][col] == 0:
                                chances += 1
                    for row in range(x,x-4,-1):
                        for col in range(y,y-3,-1):
                            if col < 0  :
                                break
                            if board[row][col] == 0:
                                chances += 1
        
        elif y == 0 and (x > 0 or x < 9):
            if True:
            # if board[x][y+1] == 0 or board[x+1][y] == 0 or board[x-1][y] == 0:
                for row in range(x,x-4,-1):
                    for col in range(y,5):
                        if row < 0 :
                            break
                        if board[row][col] == 0:
                            chances += 1
                for row in range(x,x+4):
                    for col in range(y,5):
                        if row > 9 :
                            break
                        if board[row][col] == 0:
                            chances += 1

        elif  y == 9 and (x > 0 or x < 9):
            if board[x][y-1] == 0 or board[x+1][y] == 0 or board[x-1][y] == 0:
                # print("Hello")
                for row in range(x,x-4,-1):
                    for col in reversed(range(5,y)):
                        if row < 0 :
                            break
                        if board[row][col] == 0:
                            chances += 1
                for row in range(x,x+4):
                    for col in reversed(range(5,y)):
                        if row > 9 :
                            break
                        if board[row][col] == 0:
                            chances += 1
        # in between
        else:
            # print("Else")
            if True:
            # if board[x][y+1] == 0 or board[x][y-1] == 0 or board[x+1][y] == 0 or board[x-1][y+1] == 0:
                for row in range(x,x+4):
                    for col in range(y,y+4):
                        if row > 9 or col > 9 :
                            break
                        if board[row][col] == 0:
                            chances += 1
                for row in range(x,x+4):
                    for col in range(y,y-4,-1):
                        if row > 9 or col < 0 :
                            break
                        if board[row][col] == 0:
                            chances += 1

                for row in range(x,x-4,-1):
                    for col in range(y,y+4):
                        if row < 0 or col > 9 :
                            break
                        if board[row][col] == 0:
                            chances += 1
                for row in range(x,x-4,-1):
                    for col in range(y,y-4,-1):
                        if row < 0 or col < 0 :
                            break
                        if board[row][col] == 0:
                            chances += 1    
        return chances        
    # ===================================================================================
    #                       Functions for AI AGENT (SECTION ENDED)
    # ===================================================================================
    def current_position(self,board,is_human):
        if is_human:
            for x in range(len(board)):
                for y in range(len(board[x])):
                    if board[x][y] == 1:
                        return [x,y]
        else:
            for x in range(len(board)):
                for y in range(len(board[x])):
                    if board[x][y] == 2:
                        return [x,y]
        
    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        result = self.evaluateBoard(self.grid)
        print(self.NUMBER_OF_TURNS)
        print(self.BOT_TURNS)
        if result == 0:
            print("Continue State")
            print(self.grid)
            
            
        elif result == 100 or result == 200 or result == 50 :
            print(f"RESULT = {result}")
            gameover = GameOverView(result)
            self.window.show_view(gameover)
        # Stucked Criteria
        if (self.NUMBER_OF_TURNS >= 7 and self.BOT_TURNS >= 7) :
            human = 0
            bot = 0
            for x in range(len(self.grid)):
                for y in range(len(self.grid[x])):
                    if self.grid[x][y] == 10 or self.grid[x][y] == 1:
                        human +=1
                    elif self.grid[x][y] == 20 or self.grid[x][y] == 2:
                        bot += 1
            if human > bot:
                result = 100
            elif human < bot :
                result = 200
            elif human == bot:
                result = 50
            gameover = GameOverView(result)
            self.window.show_view(gameover)

        # Change the x/y screen coordinates to grid coordinates
        column = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))
        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")
        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist

        # row == row from backend grid and colum form backend grid
        if row < ROW_COUNT and column < COLUMN_COUNT:
            if self.turn == 1:
                # Checking for the legal move
                current_y = self.snail_one.center_x // (MARGIN + WIDTH)
                current_x = self.snail_one.center_y // (MARGIN + HEIGHT)
                
                result,new_x,new_y = self.islegalMove(1,tuple((current_x,current_y)),tuple((row,column)))
                # If move is legal
                if result:
                    self.grid[new_x][new_y] = 1
                    self.grid[current_x][current_y] = 10
                    self.player_position = [new_x,new_y]
                    self.PLAYER_POS = copy.deepcopy(self.player_position)

                    self.player_score += 1
                    self.NUMBER_OF_TURNS = 0
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
                self.NUMBER_OF_TURNS += 1
                print("Bot Turn")
                self.bot_playing()
            # elif self.turn == 0:
            #     # Checking for the legal move
            #     current_y = self.snail_two.center_x // (MARGIN + WIDTH)
            #     current_x = self.snail_two.center_y // (MARGIN + HEIGHT)
            #     print(current_x,current_y)
            #     result , new_x,new_y = self.islegalMove(self.turn,tuple((current_x,current_y)),tuple((row,column)))
            #     if result:
            #         print("PLayer 2 result true")
            #         print(new_x,new_y)
            #         self.grid[new_x][new_y] = 2
            #         self.grid[current_x][current_y] = 20
            #         self.bot_score += 1
            #         self.snail_two.center_x = (MARGIN + WIDTH) * (new_y) + MARGIN + WIDTH // 2
            #         self.snail_two.center_y = (MARGIN + HEIGHT) * (new_x) + MARGIN + HEIGHT // 2
            #         self.snail_two.update()
            #         splash = self.create_splashes(current_x,current_y,"splashRed.png")
            #         self.splash_player_list.append(splash)
            #         self.splash_player_list.draw()
            #         self.splash_player_list.update()
            #         self.turn = 1 #player turn given

            #     else:
            #         print("Foul Move Bot, No score awarded")
            #         self.turn = 1 #player turn given   
                
            
                """
                    ===============================================
                """
        
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