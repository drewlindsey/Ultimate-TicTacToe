import pygame
import random as rand

# class TicTacToe
# represents an individual tic tac toe board
class TicTacToe:

    # all combinations of victories
    wins = [
                 [ [x,x] for x in [0,1,2]],
                 [ [2-x, x] for x in [0,1,2]],
                 [ [0,x] for x in [0,1,2] ],
                 [ [1,x] for x in [0,1,2] ],
                 [ [2,x] for x in [0,1,2] ],
                 [ [x,0] for x in [0,1,2] ],
                 [ [x,1] for x in [0,1,2] ],
                 [ [x,2] for x in [0,1,2] ]
            ]
    
    def __init__(self, board_num):
        self.values = [None]*9 # stores the player who owns that spot of the index
        self.winner = None # the winner of this board
        self.board_num = board_num # this board number in the grand scheme of things

    # returns all remaining moves in this board
    def get_possible_moves(self):
        return [i for i,e in enumerate (self.values) if e is None]

    def get_values(self):
        return self.values

    def get_winner(self):
        return self.winner

    def get_width(self):
        return self.winner

    # checks the validity of the given move
    # returns true if mov_loc is None in self.values
    # returns false if a player has already played in the spot ( self.values[mov_loc] is not None )
    def check_move(self, mov_loc):
        if mov_loc < 9 and mov_loc >= 0:
            return self.values[mov_loc] is None
        return False

    def is_won(self):
        return self.winner is not None

    def set_winner(self, winner):
        self.winner = winner

    def get_winner(self):
        return self.winner

    # checks each combination of a players winning spaces with all combinations of wins
    # sets the board winner to player
    # returns True if the board is won
    #         False otherwise
    def check_win(self, player):
        for loc1 in player.get_taken_at(self.board_num):
            for loc2 in player.get_taken_at(self.board_num):
                for loc3 in player.get_taken_at(self.board_num):
                    if [loc1, loc2, loc3] in self.wins:
                        self.set_winner(player)
                        return True
        return False

    # adds the spot to the player's taken list
    # sets this board's value at this spot to the player (claiming ownership)
    def make_move(self, spot, player):
        player.add_taken(self.board_num, spot)
        #print("TEST: " + str(self.board_num) + " " + str(spot))
        self.values[spot] = player

    def add_player(self, player):
        self.players.append(player)

    #returns the player if it finds it by name
    #        otherwise returns None
    def get_player(self, name):
        for player in self.players:
            if player.get_name() == name:
                return player
        return None

    def get_players(self):
        return self.players

# class Player
# represents a player and all the things this player owns (game positions, game boards, colors, name)
# holds whether or not the player is AI
class Player:
    def __init__(self, name, color, is_ai):
        self.name = name #name of this specific player
        self.taken = {x : [] for x in range(9)} # dictionary of values taken in each board
        self.main_taken = [] # values of each board taken
        self.color = color
        self.is_ai = is_ai        

    def get_name(self):
        return self.name

    def get_main_taken(self):
        return self.main_taken

    def get_taken_at(self, big_spot):
        return self.taken[big_spot]

    def add_main_taken(self, big_spot):
        self.main_taken.append(big_spot)

    def add_taken(self, big_array_value, small_array_value):        
        self.taken.get(big_array_value).append([small_array_value%3, small_array_value//3])

    def is_random_ai(self):
        return self.is_ai

    def get_color(self):
        return self.color

# class UltimateTTT
# represents the game as a whole
# handles all drawing of the board and sub-boards
class UltimateTTT:

    # all winning combinations
    wins = [
                 [ [x,x] for x in [0,1,2]],
                 [ [2-x, x] for x in [0,1,2]],
                 [ [0,x] for x in [0,1,2] ],
                 [ [1,x] for x in [0,1,2] ],
                 [ [2,x] for x in [0,1,2] ],
                 [ [x,0] for x in [0,1,2] ],
                 [ [x,1] for x in [0,1,2] ],
                 [ [x,2] for x in [0,1,2] ]
            ]

    def __init__(self):
        self.boards = [] # initialize a list of boards
        for i in range(9): # populate the list with 9 boards
            a = TicTacToe(i)
            self.boards.append(a)
        self.screen = pygame.display.set_mode((900,900)) # create the pygame display
        self.players = [] # initialize the list of players (has to be 2 for the game to work)
        pygame.init() # init the pygame module

    # return all boards that are not won and have possible moves remaining
    def get_possible_moves(self):
        moves = []
        for index, board in enumerate(self.boards):
            if board.is_won():
                continue
            if len(board.get_possible_moves()) > 0:
                moves.append(index)
        return moves
        #return [i for i,e in enumerate (self.boards) if (not e.is_won()) or len(e.get_possible_moves()) > 0]

    # draws each sub board and each line for the main board
    def draw(self, curr_board, color_bg=(0,0,0), color_line=(255,255,255), color_line_2=(255,0,255)):
        self.screen.fill(color_bg)
        for i in range(9):
            if curr_board == i:
                self.draw_sub_board((120,0,120), i, True)
            else:
                self.draw_sub_board((120,0,120), i)
        pygame.draw.line(self.screen, color_line, (300,900), (300,0))
        pygame.draw.line(self.screen, color_line, (600,900), (600,0))
        pygame.draw.line(self.screen, color_line, (900,300), (0, 300))
        pygame.draw.line(self.screen, color_line, (900, 600), (0,600))
        #pygame.draw.line(self.screen, color_line_2, (900, 900), (0, 900), 5)

    #updates the pygame display
    def update(self):
        pygame.display.update()

    # calculates the top left corner of this current board
    # if this board is won, color it the color of the winner
    # if this board is not won, color each cell claimed by each player and highlight the current board
    # draw the lines for this individual board
    def draw_sub_board(self, color_line, board_number, is_current=False):
        start_x = (board_number % 3) * 300
        start_y = (board_number // 3) * 300

        sub_board = self.get_board(board_number)
        if sub_board.is_won():
            s = pygame.Surface((300,300))
            #s.set_alpha(100)
            s.fill(sub_board.get_winner().get_color())
            
            self.screen.blit(s, (start_x, start_y))
            
        else:
            if is_current:
                s = pygame.Surface((300,300))
                s.set_alpha(100)
                s.fill((255,215,0))
                self.screen.blit(s, (start_x, start_y))
            for i in range(9):
                if sub_board.get_values()[i] is not None:
                    player = self.get_player(sub_board.get_values()[i].get_name())
                    s = pygame.Surface((100,100))
                    s.fill(player.get_color())
                    start_x_1 = start_x + i%3*100
                    start_y_1 = start_y + i//3*100
                    self.screen.blit(s, (start_x_1, start_y_1))
    
        
        pygame.draw.line(self.screen, color_line, (start_x + 300, start_y + 300//3), (start_x, start_y + 300//3))
        pygame.draw.line(self.screen, color_line, (start_x + 300, start_y + 2*300//3), (start_x, start_y + 2*300//3))
        pygame.draw.line(self.screen, color_line, (start_x + 300//3, start_y + 300), (start_x + 300//3, start_y))
        pygame.draw.line(self.screen, color_line, (start_x + 2*300//3, start_y + 300), (start_x + 2*300//3, start_y))

    # draw the TIE screen
    def draw_tie(self):
        self.screen.fill((0,0,0))
        font = pygame.font.Font(pygame.font.get_default_font(), 60)
        text_surface = font.render("It's a tie!", True, (0,255,120))
        self.screen.blit(text_surface, (250, 250))
        pygame.display.update()
        pygame.time.wait(5000)

    # draw the victory screen ** CAUTION MAY CAUSE SEIZURES **
    def draw_win(self, player):
        color1 = (255,0,0)
        color2 = (0,255,0)

        font = pygame.font.Font(pygame.font.get_default_font(), 60)
        text_surface = font.render(player.get_name() + " HAS WON!", True, (0,0,255))
        
        for i in range(10):
            color1, color2 = color2, color1
            self.screen.fill(color1)
            self.screen.blit(text_surface, ( 250, 250))
            pygame.time.delay(300)
            pygame.display.update()
            
    # check each combination of victories with each players taken boards
    def check_win(self, player):
        for loc1 in player.get_main_taken():
            for loc2 in player.get_main_taken():
                for loc3 in player.get_main_taken():
                    if [loc1, loc2, loc3] in self.wins:
                        return True
        return False

    def get_board(self, board_num):
        return self.boards[board_num]

    def is_board_won(self, board_num):
        return self.boards[board_num].is_won()

    def make_move(self, spot, player):
        player.add_taken(spot)
        self.values[spot] = player

    def add_player(self, player):
        self.players.append(player)

    def get_player(self, name):
        for player in self.players:
            if player.get_name() == name:
                return player
        return None

    def get_players(self):
        return self.players
# Game Logic
# initialize each player and add to the game
# while playing game:
#   if no more moves are available,
#       call a tie and stop looping
#   else
#       draw the game board
#       if the curr_player is ai
#           select a random, available move
#           if this move results in an open position for next move (see rules in readme.txt)
#               set curr_board to -1
#           else
#               set curr_board to move
#           if this move won the small board
#               add this board to player's main_taken list
#       if the curr_player is not ai
#           while we do not have a valid mousebuttondown event
#               loc = location of the mouse event
#               if this event is valid (location is in the correct board and selecting a sub-board location that is not taken)
#                   make the move
#                   check the move for win, if yes
#                       add this board to player's main_board
#                   if this move results in open position for next board
#                       set curr_board to -1
#                   otherwise,
#                       set curr_board to move
#               
def main():
    player1 = Player("Player 2", (0,255,0), True) # set the boolean value to False to play as a human
    player2 = Player("Player 1", (0, 0, 255), False) # set the boolean value to False to play as a human
    game = UltimateTTT()
    game.add_player(player2)
    game.add_player(player1)

    curr_board = -1
    curr_player = game.get_players()[0]
    curr_player_id = 0

    game.draw(curr_board)
    game.update()
    loop = True
    while loop:
        prev_player = curr_player
        if len(game.get_possible_moves()) == 0:
            game.draw_tie()
            loop = False
        else:
            game.draw(curr_board)
            game.update()
            if curr_player.is_random_ai():
                boards_avail = game.get_possible_moves()
                if curr_board == -1:
                    curr_board = rand.choice(boards_avail)
                #board_moves = game.get_board(curr_board).get_possible_moves()
                try:    
                    move = rand.choice(game.get_board(curr_board).get_possible_moves())
                    game.get_board(curr_board).make_move(move, curr_player)
                except Exception as e:
                    print(e)
                if game.get_board(curr_board).check_win(curr_player):
                    curr_player.add_main_taken([curr_board%3, curr_board//3])
                if move not in game.get_possible_moves():
                    curr_board = -1
                else:
                    curr_board = move
                pygame.time.delay(10)
                pygame.event.pump()
            else:
                wait = True
                while wait:
                    mouse_pos = pygame.mouse.get_pos()
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:                            
                            mov_loc = [int(mouse_pos[1]/300), int(mouse_pos[0]/300)]
                            board_num = mov_loc[0] * 3 + mov_loc[1]
                            small_mov_loc = [int(mouse_pos[1]/100), int(mouse_pos[0]/100)]
                            small_board_loc = [small_mov_loc[0]%3, small_mov_loc[1]%3]
                            small_arr_val = small_board_loc[0]*3 + small_board_loc[1]
                            if not game.is_board_won(board_num) and (board_num == curr_board or curr_board == -1):
                                if game.get_board(board_num).check_move(small_arr_val):
                                    #print(small_arr_val)
                                    print(game.get_possible_moves())
                                    game.get_board(board_num).make_move(small_arr_val, curr_player)                                    
                                    wait = False
                                     #or game.get_board(board_num).check_win(curr_player):
                                    if game.get_board(board_num).check_win(curr_player):
                                        curr_player.add_main_taken([board_num%3, board_num//3])
                                    if small_arr_val not in game.get_possible_moves():
                                        curr_board = -1
                                    else:
                                        curr_board = small_arr_val
                        if event.type == pygame.QUIT: # handles the red X
                            wait = False
                            pygame.quit()
                            loop = False

        curr_player = game.get_players()[1-curr_player_id] # change players
        curr_player_id = 1-curr_player_id           # change ID

        # if the entire game is won
        #   enter game win sequence
        if game.check_win(prev_player):
            print("GAME WON")
            print(curr_player.get_main_taken())
            print(prev_player.get_main_taken())
            game.draw(curr_board)
            game.update()
            pygame.time.wait(2000)
            game.draw_win(prev_player)
            loop = False
        
    print("GAME OVER")
    pygame.quit()
                                
main()
