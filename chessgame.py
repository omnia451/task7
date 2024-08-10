import os
import pygame
from pygame.locals import *
import random

class Piece(pygame.sprite.Sprite):
    def __init__(self, filename, cols, rows):
        pygame.sprite.Sprite.__init__(self)
        self.pieces = {
            "white_pawn":   5,
            "white_knight": 3,
            "white_bishop": 2,
            "white_rook":   4,
            "white_king":   0,
            "white_queen":  1,
            "black_pawn":   11,
            "black_knight": 9,
            "black_bishop": 8,
            "black_rook":   10,
            "black_king":   6,
            "black_queen":  7
        }
        self.spritesheet = pygame.image.load(filename).convert_alpha()

        self.cols = cols
        self.rows = rows
        self.cell_count = cols * rows

        self.rect = self.spritesheet.get_rect()
        w = self.cell_width = self.rect.width // self.cols
        h = self.cell_height = self.rect.height // self.rows

        self.cells = list([(i % cols * w, i // cols * h, w, h) for i in range(self.cell_count)])

    def draw(self, surface, piece_name, coords):
        piece_index = self.pieces[piece_name]
        surface.blit(self.spritesheet, coords, self.cells[piece_index])


class Utils:
    def get_mouse_event(self):
        # get coordinates of the mouse
        position = pygame.mouse.get_pos()

        # return left click status and mouse coordinates
        return position

    def left_click_event(self):
        # store mouse buttons
        mouse_btn = pygame.mouse.get_pressed()
        # create flag to check for left click event
        left_click = False

        if mouse_btn[0]:  # and e.button == 1:
            # change left click flag
            left_click = True

        return left_click


class Chess(object):
    def __init__(self, screen, pieces_src, square_coords, square_length):
        # display surface
        self.screen = screen
        # create an object of class to show chess pieces on the board
        self.chess_pieces = Piece(pieces_src, cols=6, rows=2)
        # store coordinates of the chess board squares
        self.board_locations = square_coords
        # length of the side of a chess board square
        self.square_length = square_length
        # dictionary to keeping track of player turn
        self.turn = {"black": 0,
                     "white": 0}

        # list containing possible moves for the selected piece
        self.moves = []
        #
        self.utils = Utils()

        # mapping of piece names to index of list containing piece coordinates on spritesheet
        self.pieces = {
            "white_pawn": 5,
            "white_knight": 3,
            "white_bishop": 2,
            "white_rook": 4,
            "white_king": 0,
            "white_queen": 1,
            "black_pawn": 11,
            "black_knight": 9,
            "black_bishop": 8,
            "black_rook": 10,
            "black_king": 6,
            "black_queen": 7
        }

        # list containing captured pieces
        self.captured = []
        #
        self.winner = ""

        self.reset()

    def reset(self):
        # clear moves lists
        self.moves = []

        # randomize player turn
        x = random.randint(0, 1)
        if (x == 1):
            self.turn["black"] = 1
        elif (x == 0):
            self.turn["white"] = 1

        # two dimensonal dictionary containing details about each board location
        # storage format is [piece_name, currently_selected, x_y_coordinate]
        self.piece_location = {}
        x = 0
        for i in range(97, 105):
            a = 8
            y = 0
            self.piece_location[chr(i)] = {}
            while a > 0:
                # [piece name, currently selected, board coordinates]
                self.piece_location[chr(i)][a] = ["", False, [x, y]]
                a = a - 1
                y = y + 1
            x = x + 1

        # reset the board
        for i in range(97, 105):
            x = 8
            while x > 0:
                if (x == 8):
                    if (chr(i) == 'a' or chr(i) == 'h'):
                        self.piece_location[chr(i)][x][0] = "black_rook"
                    elif (chr(i) == 'b' or chr(i) == 'g'):
                        self.piece_location[chr(i)][x][0] = "black_knight"
                    elif (chr(i) == 'c' or chr(i) == 'f'):
                        self.piece_location[chr(i)][x][0] = "black_bishop"
                    elif (chr(i) == 'd'):
                        self.piece_location[chr(i)][x][0] = "black_queen"
                    elif (chr(i) == 'e'):
                        self.piece_location[chr(i)][x][0] = "black_king"
                elif (x == 7):
                    self.piece_location[chr(i)][x][0] = "black_pawn"
                elif (x == 2):
                    self.piece_location[chr(i)][x][0] = "white_pawn"
                elif (x == 1):
                    if (chr(i) == 'a' or chr(i) == 'h'):
                        self.piece_location[chr(i)][x][0] = "white_rook"
                    elif (chr(i) == 'b' or chr(i) == 'g'):
                        self.piece_location[chr(i)][x][0] = "white_knight"
                    elif (chr(i) == 'c' or chr(i) == 'f'):
                        self.piece_location[chr(i)][x][0] = "white_bishop"
                    elif (chr(i) == 'd'):
                        self.piece_location[chr(i)][x][0] = "white_queen"
                    elif (chr(i) == 'e'):
                        self.piece_location[chr(i)][x][0] = "white_king"
                x = x - 1

    #
    def play_turn(self):
        # white color
        white_color = (255, 255, 255)
        # create fonts for texts
        small_font = pygame.font.SysFont("comicsansms", 20)
        # create text to be shown on the game menu
        if self.turn["black"]:
            turn_text = small_font.render("Turn: Black", True, white_color)
        elif self.turn["white"]:
            turn_text = small_font.render("Turn: White", True, white_color)

        # show welcome text
        self.screen.blit(turn_text,
                         ((self.screen.get_width() - turn_text.get_width()) // 2,
                          10))

        # let player with black piece play
        if (self.turn["black"]):
            self.move_piece("black")
        # let player with white piece play
        elif (self.turn["white"]):
            self.move_piece("white")

    # method to draw pieces on the chess board
    def draw_pieces(self):
        transparent_green = (0, 194, 39, 170)
        transparent_blue = (28, 21, 212, 170)

        # create a transparent surface
        surface = pygame.Surface((self.square_length, self.square_length), pygame.SRCALPHA)
        surface.fill(transparent_green)

        surface1 = pygame.Surface((self.square_length, self.square_length), pygame.SRCALPHA)
        surface1.fill(transparent_blue)

        # loop to change background color of selected piece
        for val in self.piece_location.values():
            for value in val.values():
                # name of the piece in the current location
                piece_name = value[0]
                # x, y coordinates of the current piece
                piece_coord_x, piece_coord_y = value[2]

                # change background color of piece if it is selected
                if value[1] and len(value[0]) > 5:
                    # if the piece selected is a black piece
                    if value[0][:5] == "black":
                        self.screen.blit(surface, self.board_locations[piece_coord_x][piece_coord_y])
                        if len(self.moves) > 0:
                            for move in self.moves:
                                x_coord = move[0]
                                y_coord = move[1]
                                if x_coord >= 0 and y_coord >= 0 and x_coord < 8 and y_coord < 8:
                                    self.screen.blit(surface, self.board_locations[x_coord][y_coord])
                    # if the piece selected is a white piece
                    elif value[0][:5] == "white":
                        self.screen.blit(surface1, self.board_locations[piece_coord_x][piece_coord_y])
                        if len(self.moves) > 0:
                            for move in self.moves:
                                x_coord = move[0]
                                y_coord = move[1]
                                if x_coord >= 0 and y_coord >= 0 and x_coord < 8 and y_coord < 8:
                                    self.screen.blit(surface1, self.board_locations[x_coord][y_coord])

        # draw all chess pieces
        for val in self.piece_location.values():
            for value in val.values():
                # name of the piece in the current location
                piece_name = value[0]
                # x, y coordinates of the current piece
                piece_coord_x, piece_coord_y = value[2]
                # check if there is a piece at the square
                if (len(value[0]) > 1):
                    # draw piece on the board
                    self.chess_pieces.draw(self.screen, piece_name,
                                           self.board_locations[piece_coord_x][piece_coord_y])

    # method to find the possible moves of the selected piece
    def possible_moves(self, piece_name, piece_coord):
        # list to store possible moves of the selected piece
        positions = []
        # find the possible locations to put a piece
        if len(piece_name) > 0:
            # get x, y coordinate
            x_coord, y_coord = piece_coord
            # calculate moves for bishop
            if piece_name[6:] == "bishop":
                positions = self.diagonal_moves(positions, piece_name, piece_coord)

            # calculate moves for pawn
            elif piece_name[6:] == "pawn":
                # convert list index to dictionary key
                columnChar = chr(97 + x_coord)
                rowNo = 8 - y_coord

                # calculate moves for white pawn
                if piece_name == "black_pawn":
                    if y_coord + 1 < 8:
                        # get row in front of black pawn
                        rowNo = rowNo - 1
                        front_piece = self.piece_location[columnChar][rowNo][0]

                        # pawns cannot move when blocked by another another pawn
                        if (front_piece[6:] != "pawn"):
                            positions.append([x_coord, y_coord + 1])
                            # black pawns can move two positions ahead for first move
                            if y_coord < 2:
                                positions.append([x_coord, y_coord + 2])

                        # EM PASSANT
                        # diagonal to the left
                        if x_coord - 1 >= 0 and y_coord + 1 < 8:
                            x = x_coord - 1
                            y = y_coord + 1

                            # convert list index to dictionary key
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if (to_capture[0][:5] == "white"):
                                positions.append([x, y])

                        # diagonal to the right
                        if x_coord + 1 < 8 and y_coord + 1 < 8:
                            x = x_coord + 1
                            y = y_coord + 1

                            # convert list index to dictionary key
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if (to_capture[0][:5] == "white"):
                                positions.append([x, y])

                # calculate moves for white pawn
                elif piece_name == "white_pawn":
                    if y_coord - 1 >= 0:
                        # get row in front of black pawn
                        rowNo = rowNo + 1
                        front_piece = self.piece_location[columnChar][rowNo][0]

                        # pawns cannot move when blocked by another another pawn
                        if (front_piece[6:] != "pawn"):
                            positions.append([x_coord, y_coord - 1])
                            # black pawns can move two positions ahead for first move
                            if y_coord > 5:
                                positions.append([x_coord, y_coord - 2])

                        # EM PASSANT
                        # diagonal to the left
                        if x_coord - 1 >= 0 and y_coord - 1 >= 0:
                            x = x_coord - 1
                            y = y_coord - 1

                            # convert list index to dictionary key
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if (to_capture[0][:5] == "black"):
                                positions.append([x, y])

                        # diagonal to the right
                        if x_coord + 1 < 8 and y_coord - 1 >= 0:
                            x = x_coord + 1
                            y = y_coord - 1

                            # convert list index to dictionary key
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if (to_capture[0][:5] == "black"):
                                positions.append([x, y])


            # calculate moves for rook
            elif piece_name[6:] == "rook":
                # find linear moves
                positions = self.linear_moves(positions, piece_name, piece_coord)

            # calculate moves for knight
            elif piece_name[6:] == "knight":
                # left positions
                if (x_coord - 2) >= 0:
                    if (y_coord - 1) >= 0:
                        positions.append([x_coord - 2, y_coord - 1])
                    if (y_coord + 1) < 8:
                        positions.append([x_coord - 2, y_coord + 1])
                # top positions
                if (y_coord - 2) >= 0:
                    if (x_coord - 1) >= 0:
                        positions.append([x_coord - 1, y_coord - 2])
                    if (x_coord + 1) < 8:
                        positions.append([x_coord + 1, y_coord - 2])
                # right positions
                if (x_coord + 2) < 8:
                    if (y_coord - 1) >= 0:
                        positions.append([x_coord + 2, y_coord - 1])
                    if (y_coord + 1) < 8:
                        positions.append([x_coord + 2, y_coord + 1])
                # bottom positions
                if (y_coord + 2) < 8:
                    if (x_coord - 1) >= 0:
                        positions.append([x_coord - 1, y_coord + 2])
                    if (x_coord + 1) < 8:
                        positions.append([x_coord + 1, y_coord + 2])

            # calculate movs for king
            elif piece_name[6:] == "king":
                if (y_coord - 1) >= 0:
                    # top spot
                    positions.append([x_coord, y_coord - 1])

                if (y_coord + 1) < 8:
                    # bottom spot
                    positions.append([x_coord, y_coord + 1])

                if (x_coord - 1) >= 0:
                    # left spot
                    positions.append([x_coord - 1, y_coord])
                    # top left spot
                    if (y_coord - 1) >= 0:
                        positions.append([x_coord - 1, y_coord - 1])
                    # bottom left spot
                    if (y_coord + 1) < 8:
                        positions.append([x_coord - 1, y_coord + 1])

                if (x_coord + 1) < 8:
                    # right spot
                    positions.append([x_coord + 1, y_coord])
                    # top right spot
                    if (y_coord - 1) >= 0:
                        positions.append([x_coord + 1, y_coord - 1])
                    # bottom right spot
                    if (y_coord + 1) < 8:
                        positions.append([x_coord + 1, y_coord + 1])

            # calculate movs for queen
            elif piece_name[6:] == "queen":
                # find diagonal positions
                positions = self.diagonal_moves(positions, piece_name, piece_coord)

                # find linear moves
                positions = self.linear_moves(positions, piece_name, piece_coord)

            # list of positions to be removed
            to_remove = []

            # remove positions that overlap other pieces of the current player
            for pos in positions:
                x, y = pos

                # convert list index to dictionary key
                columnChar = chr(97 + x)
                rowNo = 8 - y

                # find the pieces to remove
                des_piece_name = self.piece_location[columnChar][rowNo][0]
                if (des_piece_name[:5] == piece_name[:5]):
                    to_remove.append(pos)

            # remove position from positions list
            for i in to_remove:
                positions.remove(i)

        # return list containing possible moves for the selected piece
        return positions

    def move_piece(self, turn):
        # get the coordinates of the square selected on the board
        square = self.get_selected_square()

        # if a square was selected
        if square:
            # get name of piece on the selected square
            piece_name = square[0]
            # color of piece on the selected square
            piece_color = piece_name[:5]
            # board column character
            columnChar = square[1]
            # board row number
            rowNo = square[2]

            # get x, y coordinates
            x, y = self.piece_location[columnChar][rowNo][2]

            # if there's a piece on the selected square
            if (len(piece_name) > 0) and (piece_color == turn):
                # find possible moves for thr piece
                self.moves = self.possible_moves(piece_name, [x, y])

            # checkmate mechanism
            p = self.piece_location[columnChar][rowNo]

            for i in self.moves:
                if i == [x, y]:
                    if (p[0][:5] == turn) or len(p[0]) == 0:
                        self.validate_move([x, y])
                    else:
                        self.capture_piece(turn, [columnChar, rowNo], [x, y])

            # only the player with the turn gets to play
            if (piece_color == turn):
                # change selection flag from all other pieces
                for k in self.piece_location.keys():
                    for key in self.piece_location[k].keys():
                        self.piece_location[k][key][1] = False

                # change selection flag of the selected piece
                self.piece_location[columnChar][rowNo][1] = True

    def get_selected_square(self):
        # get left event
        left_click = self.utils.left_click_event()

        # if there's a mouse event
        if left_click:
            # get mouse event
            mouse_event = self.utils.get_mouse_event()

            for i in range(len(self.board_locations)):
                for j in range(len(self.board_locations)):
                    rect = pygame.Rect(self.board_locations[i][j][0], self.board_locations[i][j][1],
                                       self.square_length, self.square_length)
                    collision = rect.collidepoint(mouse_event[0], mouse_event[1])
                    if collision:
                        selected = [rect.x, rect.y]
                        # find x, y coordinates the selected square
                        for k in range(len(self.board_locations)):
                            #
                            try:
                                l = None
                                l = self.board_locations[k].index(selected)
                                if l != None:
                                    # reset color of all selected pieces
                                    for val in self.piece_location.values():
                                        for value in val.values():
                                            # [piece name, currently selected, board coordinates]
                                            if not value[1]:
                                                value[1] = False

                                    # get column character and row number of the chess piece
                                    columnChar = chr(97 + k)
                                    rowNo = 8 - l
                                    # get the name of the
                                    piece_name = self.piece_location[columnChar][rowNo][0]

                                    return [piece_name, columnChar, rowNo]
                            except:
                                pass
        else:
            return None

    def capture_piece(self, turn, chess_board_coord, piece_coord):
        # get x, y coordinate of the destination piece
        x, y = piece_coord

        # get chess board coordinate
        columnChar, rowNo = chess_board_coord

        p = self.piece_location[columnChar][rowNo]

        if p[0] == "white_king":
            self.winner = "Black"
            print("Black wins")
        elif p[0] == "black_king":
            self.winner = "White"
            print("White wins")

        # add the captured piece to list
        self.captured.append(p)
        # move source piece to its destination
        self.validate_move(piece_coord)

    def validate_move(self, destination):
        desColChar = chr(97 + destination[0])
        desRowNo = 8 - destination[1]

        for k in self.piece_location.keys():
            for key in self.piece_location[k].keys():
                board_piece = self.piece_location[k][key]

                if board_piece[1]:
                    # unselect the source piece
                    self.piece_location[k][key][1] = False
                    # get the name of the source piece
                    piece_name = self.piece_location[k][key][0]
                    # move the source piece to the destination piece
                    self.piece_location[desColChar][desRowNo][0] = piece_name

                    src_name = self.piece_location[k][key][0]
                    # remove source piece from its current position
                    self.piece_location[k][key][0] = ""

                    # change turn
                    if (self.turn["black"]):
                        self.turn["black"] = 0
                        self.turn["white"] = 1
                    elif ("white"):
                        self.turn["black"] = 1
                        self.turn["white"] = 0

                    src_location = k + str(key)
                    des_location = desColChar + str(desRowNo)
                    print("{} moved from {} to {}".format(src_name, src_location, des_location))

    # helper function to find diagonal moves
    def diagonal_moves(self, positions, piece_name, piece_coord):
        # reset x and y coordinate values
        x, y = piece_coord
        # find top left diagonal spots
        while (True):
            x = x - 1
            y = y - 1
            if (x < 0 or y < 0):
                break
            else:
                positions.append([x, y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # reset x and y coordinate values
        x, y = piece_coord
        # find bottom right diagonal spots
        while (True):
            x = x + 1
            y = y + 1
            if (x > 7 or y > 7):
                break
            else:
                positions.append([x, y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # reset x and y coordinate values
        x, y = piece_coord
        # find bottom left diagonal spots
        while (True):
            x = x - 1
            y = y + 1
            if (x < 0 or y > 7):
                break
            else:
                positions.append([x, y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # reset x and y coordinate values
        x, y = piece_coord
        # find top right diagonal spots
        while (True):
            x = x + 1
            y = y - 1
            if (x > 7 or y < 0):
                break
            else:
                positions.append([x, y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        return positions

    # helper function to find horizontal and vertical moves
    def linear_moves(self, positions, piece_name, piece_coord):
        # reset x, y coordniate value
        x, y = piece_coord
        # horizontal moves to the left
        while (x > 0):
            x = x - 1
            positions.append([x, y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # reset x, y coordniate value
        x, y = piece_coord
        # horizontal moves to the right
        while (x < 7):
            x = x + 1
            positions.append([x, y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

                # reset x, y coordniate value
        x, y = piece_coord
        # vertical moves upwards
        while (y > 0):
            y = y - 1
            positions.append([x, y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # reset x, y coordniate value
        x, y = piece_coord
        # vertical moves downwards
        while (y < 7):
            y = y + 1
            positions.append([x, y])

            # convert list index to dictionary key
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # stop finding possible moves if blocked by a piece
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        return positions


class Game:
    def __init__(self):
        # screen dimensions
        screen_width = 640
        screen_height = 750
        # flag to know if game menu has been showed
        self.menu_showed = False
        # flag to set game loop
        self.running = True
        # base folder for program resources
        self.resources = "res"
 
        # initialize game window
        pygame.display.init()
        # initialize font for text
        pygame.font.init()

        # create game window
        self.screen = pygame.display.set_mode([screen_width, screen_height])

        # title of window
        window_title = "Battle Planing With Batman"
        # set window caption
        pygame.display.set_caption(window_title)
        # update display
        pygame.display.flip()
        # set game clock
        self.clock = pygame.time.Clock()


    def start_game(self):
        """Function containing main game loop""" 
        # chess board offset
        self.board_offset_x = 0
        self.board_offset_y = 50
        self.board_dimensions = (self.board_offset_x, self.board_offset_y)
        
        # get location of chess board image
        board_src = os.path.join(self.resources, "chessBoard.png")
        # load the chess board image
        self.board_img = pygame.image.load(board_src).convert()

        # get the width of a chess board square
        square_length = self.board_img.get_rect().width // 8

        # initialize list that stores all places to put chess pieces on the board
        self.board_locations = []

        # calculate coordinates of the each square on the board
        for x in range(0, 8):
            self.board_locations.append([])
            for y in range(0, 8):
                self.board_locations[x].append([self.board_offset_x+(x*square_length), 
                                                self.board_offset_y+(y*square_length)])

        # get location of image containing the chess pieces
        pieces_src = os.path.join(self.resources, "pieces2.png")
        # create class object that handles the gameplay logic
        self.chess = Chess(self.screen, pieces_src, self.board_locations, square_length)

        # game loop
        while self.running:
            self.clock.tick(5)
            # poll events
            for event in pygame.event.get():
                # get keys pressed
                key_pressed = pygame.key.get_pressed()
                # check if the game has been closed by the user
                if event.type == pygame.QUIT or key_pressed[K_ESCAPE]:
                    # set flag to break out of the game loop
                    self.running = False
                elif key_pressed[K_SPACE]:
                    self.chess.reset()
            
            winner = self.chess.winner

            if self.menu_showed == False:
                self.menu()
            elif len(winner) > 0:
                self.declare_winner(winner)
            else:
                self.game()
            
            

            # for testing mechanics of the game
            #self.game()
            #self.declare_winner(winner)

            # update display
            pygame.display.flip()
            # update events
            pygame.event.pump()

        # call method to stop pygame
        pygame.quit()
    

    def menu(self):
        """method to show game menu"""
        # background
        bg_color = (255, 255, 255)
        BG = pygame.image.load('res/BG2.png')
        # set background
        self.screen.blit(BG, (0, 0))
        # black color
        black_color = (0, 0, 0)
        # white color
        white_color = (255, 255, 255)
        # coordinates for "Play" button
        start_btn = pygame.Rect(270, 650, 100, 50)
        # show play button
        pygame.draw.rect(self.screen, white_color, start_btn)

        # white color
        white_color = (255, 255, 255)
        # create fonts for texts
        big_font = pygame.font.SysFont("JUSTICE LEAGUE", 40)
        biggg_font = pygame.font.SysFont("JUSTICE LEAGUE", 60)
        small_font = pygame.font.SysFont("JUSTICE LEAGUE", 20)
        # create text to be shown on the game menu
        welcome_text = big_font.render("Battle Planning with Batman", False, white_color)
        created_by = biggg_font.render("JU$T£¢€*L€AGU€", True, white_color)
        start_btn_label = small_font.render("Play", True, black_color)
        
        # show welcome text
        self.screen.blit(welcome_text, 
                      ((self.screen.get_width() - welcome_text.get_width()) // 2, 
                      50))
        # show credit text
        self.screen.blit(created_by, 
                      ((self.screen.get_width() - created_by.get_width()) // 2, 
                      self.screen.get_height() - created_by.get_height() - 100))
        # show text on the Play button
        self.screen.blit(start_btn_label, 
                      ((start_btn.x + (start_btn.width - start_btn_label.get_width()) // 2, 
                      start_btn.y + (start_btn.height - start_btn_label.get_height()) // 2)))

        # get pressed keys
        key_pressed = pygame.key.get_pressed()
        # 
        util = Utils()

        # check if left mouse button was clicked
        if util.left_click_event():
            # call function to get mouse event
            mouse_coords = util.get_mouse_event()

            # check if "Play" button was clicked
            if start_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                # change button behavior as it is hovered
                pygame.draw.rect(self.screen, white_color, start_btn, 3)
                
                # change menu flag
                self.menu_showed = True
            # check if enter or return key was pressed
            elif key_pressed[K_RETURN]:
                self.menu_showed = True


    def game(self):
        # background color
        color = (0,0,0)
        # set backgound color
        self.screen.fill(color)
        
        # show the chess board
        self.screen.blit(self.board_img, self.board_dimensions)

        # call self.chess. something
        self.chess.play_turn()
        # draw pieces on the chess board
        self.chess.draw_pieces()


    def declare_winner(self, winner):
        # background color
        bg_color = (255, 255, 255)
        # set background color
        self.screen.fill(bg_color)
        # black color
        black_color = (0, 0, 0)
        # coordinates for play again button
        reset_btn = pygame.Rect(250, 300, 140, 50)
        # show reset button
        pygame.draw.rect(self.screen, black_color, reset_btn)

        # white color
        white_color = (255, 255, 255)
        # create fonts for texts
        big_font = pygame.font.SysFont("comicsansms", 50)
        small_font = pygame.font.SysFont("comicsansms", 20)

        # text to show winner
        text = winner + " wins!" 
        winner_text = big_font.render(text, False, black_color)

        # create text to be shown on the reset button
        reset_label = "Play Again"
        reset_btn_label = small_font.render(reset_label, True, white_color)

        # show winner text
        self.screen.blit(winner_text, 
                      ((self.screen.get_width() - winner_text.get_width()) // 2, 
                      150))
        
        # show text on the reset button
        self.screen.blit(reset_btn_label, 
                      ((reset_btn.x + (reset_btn.width - reset_btn_label.get_width()) // 2, 
                      reset_btn.y + (reset_btn.height - reset_btn_label.get_height()) // 2)))

        # get pressed keys
        key_pressed = pygame.key.get_pressed()
        # 
        util = Utils()

        # check if left mouse button was clicked
        if util.left_click_event():
            # call function to get mouse event
            mouse_coords = util.get_mouse_event()

            # check if reset button was clicked
            if reset_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                # change button behavior as it is hovered
                pygame.draw.rect(self.screen, white_color, reset_btn, 3)
                
                # change menu flag
                self.menu_showed = False
            # check if enter or return key was pressed
            elif key_pressed[K_RETURN]:
                self.menu_showed = False
            # reset game
            self.chess.reset()
            # clear winner
            self.chess.winner = ""

if __name__=="__main__":
    game = Game()
    game.start_game()
