#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Very simple tetris implementation
#
# Control keys:
#       Down - Drop stone faster
# Left/Right - Move stone
#         Up - Rotate Stone clockwise
#     Escape - Quit game
#          P - Pause game
#     Return - Instant drop
#
# Have fun!

# NOTE: If you're looking for the old python2 version, see
#       <https://gist.github.com/silvasur/565419/45a3ded61b993d1dd195a8a8688e7dc196b08de8>

# Copyright (c) 2010 "Laria Carolin Chabowski"<me@laria.me>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Original code: https://gist.github.com/silvasur/565419

#TESTING GLOBAL VARS FROM ARGS
Test = False
Strat = 0
Outfile = None
append = None

from random import randrange as rand
import pygame, sys

# The configuration
cell_size = 18
cols =      10
rows =      22
maxfps =    30

colors = [
(0,   0,   0  ),
(255, 85,  85),
(100, 200, 115),
(120, 108, 245),
(255, 140, 50 ),
(50,  120, 52 ),
(146, 202, 73 ),
(150, 161, 218 ),
(35,  35,  35) # Helper color for background grid
]

# Define the shapes of the single parts
tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

### When the piece is flush, check if we can move it side to side to fill in gaps

# Placement weights (can be adjusted later)

weights = {
    "flush" :               0,      # Stone placement is flush with the surface beneath (good)
    "full_line" :           30,    # Stone placement completes a line (very good)
    "fully_enclosed" :      -50,    # Stone placement fully encloses at least one open square (very bad)
    "multiple_enclosed" :   -10,     # Stone placement encloses multiple open squares, weight per square enclosed (very bad)
    "height" :              1,      # Closeness to the bottom of the board (good)
    "second_block":         0,       # Weight of the next stone
    "height_spectrum":      0.1,         # Value full lines more the higher we are on the board
    "enclosed_spectrum":    0.1,        # Value enclosed squares less the higher we are on the board
}

# Whether or not to require the space key be pressed between moves
manual = False

# User input or computer bot
user_input = True

# Whether or not to print info
debug = False

def rotate_clockwise(shape):
    return [
        [ shape[y][x] for y in range(len(shape)) ]
        for x in range(len(shape[0]) - 1, -1, -1)
    ]

def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[ cy + off_y ][ cx + off_x ]:
                    return True
            except IndexError:
                return True
    return False

def remove_row(board, row):
    del board[row]
    return [[0 for i in range(cols)]] + board

def join_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy+off_y-1 ][cx+off_x] += val
    return mat1

def new_board():
    board = [
        [ 0 for x in range(cols) ]
        for y in range(rows)
    ]
    board += [[ 1 for x in range(cols)]]
    return board

class TetrisApp(object):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(250,25)
        self.width = cell_size*(cols+6)
        self.height = cell_size*rows
        self.rlim = cell_size*cols
        self.bground_grid = [[ 8 if x%2==y%2 else 0 for x in range(cols)] for y in range(rows)]

        self.default_font =  pygame.font.Font(
            pygame.font.get_default_font(), 12)

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION) # We do not need
                                                     # mouse movement
                                                     # events, so we
                                                     # block them.
        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
        self.init_game()

    def new_stone(self):
        self.stone = self.next_stone[:]
        self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
        self.stone_x = int(cols / 2 - len(self.stone[0])/2)
        self.stone_y = 0

        if check_collision(self.board,
                           self.stone,
                           (self.stone_x, self.stone_y)):
            self.gameover = True

    def init_game(self):
        self.board = new_board()
        self.new_stone()
        self.level = 1
        self.score = 0
        self.lines = 0
        pygame.time.set_timer(pygame.USEREVENT+1, 1000)

    def disp_msg(self, msg, topleft):
        x,y = topleft
        for line in msg.splitlines():
            self.screen.blit(
                self.default_font.render(
                    line,
                    False,
                    (255,255,255),
                    (0,0,0)),
                (x,y))
            y+=14

    def center_msg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image =  self.default_font.render(line, False,
                (255,255,255), (0,0,0))

            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2

            self.screen.blit(msg_image, (
              self.width // 2-msgim_center_x,
              self.height // 2-msgim_center_y+i*22))

    def draw_matrix(self, matrix, offset):
        off_x, off_y  = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen,
                        colors[val],
                        pygame.Rect(
                            (off_x+x) *
                              cell_size,
                            (off_y+y) *
                              cell_size,
                            cell_size,
                            cell_size),0)

    def add_cl_lines(self, n):
        linescores = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += linescores[n] * self.level
        if self.lines >= self.level*6:
            self.level += 1
            newdelay = 1000-50*(self.level-1)
            newdelay = 100 if newdelay < 100 else newdelay
            pygame.time.set_timer(pygame.USEREVENT+1, newdelay)

    def move(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > cols - len(self.stone[0]):
                new_x = cols - len(self.stone[0])
            if not check_collision(self.board,
                                   self.stone,
                                   (new_x, self.stone_y)):
                self.stone_x = new_x

    def quit(self):
        self.center_msg("Exiting...")
        pygame.display.update()
        sys.exit()

    def drop(self, manual):
        if not self.gameover and not self.paused:
            self.score += 1 if manual else 0
            self.stone_y += 1
            if check_collision(self.board,
                               self.stone,
                               (self.stone_x, self.stone_y)):
                self.board = join_matrixes(
                  self.board,
                  self.stone,
                  (self.stone_x, self.stone_y))
                self.new_stone()
                cleared_rows = 0
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.board = remove_row(
                              self.board, i)
                            cleared_rows += 1
                            break
                    else:
                        break
                self.add_cl_lines(cleared_rows)
                return True
        return False

    def insta_drop(self):
        if not self.gameover and not self.paused:
            while(not self.drop(True)):
                pass

    def rotate_stone(self):
        if not self.gameover and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board,
                                   new_stone,
                                   (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def toggle_pause(self):
        self.paused = not self.paused

    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False
            self.printed = False

    def determineMove(self):
        # Things to use:
        #   - self.move(val) - move the piece left or right
        #   - rotate_clockwise(stone) - rotate the stone clockwise
        #   - self.insta_drop() - drop the stone immediately
        #   - self.next_stone - get the next stone available
        #   - check_collision(self.board, stone, offset) - check if a stone position is valid

        # A choice will be made by evaluationg check_collision with different stone orientations
        # and offsets (stone positions). Once a decision is made, you'll call rotate_clockwise
        # and self.move until the stone is in the desired column and orientation, then call
        # self.insta_drop and return

        # col, rotations = self.getRandomMove(self.stone) # Random bot
        col, rotations = self.greedyChoiceMove() # Greedy bot
        
        for _ in range(rotations):
            self.stone = rotate_clockwise(self.stone)
        self.move(col - self.stone_x)
        self.insta_drop()
    
    def getRandomMove(self, current_stone):
        ### Return a random column and orientation
        return rand(0,cols - len(current_stone[0])), rand(0,4)

    def evalGreedyOption(self, st, coords, next_st = None, next_coords = None):
        x, y = coords
        count = 0
        total = 0
        val = 0
        full_lines = 0
        num_enclosed = 0
        if(debug): print("Coords:",coords,"Stone:",st,"Next Stone:",next_st,"Next Coords:",next_coords)

        # We do not want placements that make us lose
        if(y <= 0):
            return -99999999

        # Iterate thru the stone's individual squares
        for dy in range(len(st)):
            for dx in range(len(st[0])):
                # No square here so skip
                if st[dy][dx] == 0:
                    continue

                total += 1
                # Check if the piece is flush
                if y + dy + 1 >= rows: # Square is touching the bottom of the board
                    count += 1
                else:
                    if self.board[y + dy + 1][x + dx]: # Square is touching a square below
                        count += 1
                    elif dy + 1 < len(st) and st[dy + 1][dx] > 0: # Square is touching another square from the same piece below
                        count += 1
                    else: #if dy == len(st) - 1: # Not flush, count enclosed squares
                        i = 1
                        while y + dy + i < rows and not self.board[y + dy + i][x + dx]:
                            num_enclosed += 1
                            i += 1
            full = 1
            for c in range(cols):
                con = 0
                for n in range(len(st[0])):
                    if x + n == c and st[dy][n] > 0:
                        con = 1
                        break
                if con == 1:
                    continue
                if self.board[dy][c] == 0:
                    full = 0
                    break
            if full == 1:
                full_lines += 1

        mult = 1
        if weights["enclosed_spectrum"] > 0: mult = 1 / ((rows - y) * weights["enclosed_spectrum"])
        val += weights["full_line"] * full_lines + full_lines * (rows - y) * weights["height_spectrum"]
        if total == count:
            val += weights["flush"]
        else:
            val += weights["fully_enclosed"] * mult 
        val += y * weights["height"]
        val += num_enclosed * weights["multiple_enclosed"] * mult
        if(debug and num_enclosed > 0): print("Num enclosed:",num_enclosed)

        if(next_st == None):
            return val 
        
        x,y = next_coords
        count = 0
        total = 0
        full_lines = 0
        num_enclosed = 0
        if(y <= 0):
            return -99999999
        
        for dy in range(len(next_st)):
            for dx in range(len(next_st[0])):
                # No square here so skip
                if next_st[dy][dx] == 0:
                    continue

                total += 1
                # Check if the piece is flush
                if y + dy + 1 >= rows: # Square is touching the bottom of the board
                    count += 1
                else:
                    if self.board[y + dy + 1][x + dx] or (y + dy + 1, x + dx) in [(coords[0] + int(i % len(st[0])),coords[1] + int((i - (i % len(st[0]))) / len(st[0]))) if st[int((i - (i % len(st[0]))) / len(st[0]))][i % len(st[0])] > 0 else None for i in range(len(st) * len(st[0]))]: # Square is touching a square below
                        count += 1
                    elif dy + 1 < len(next_st) and next_st[dy + 1][dx] > 0: # Square is touching another square from the same piece below
                        count += 1
                    else: #if dy == len(st) - 1: # Not flush, count enclosed squares
                        i = 1
                        while y + dy + i < rows and not self.board[y + dy + i][x + dx] and (y + dy + i, x + dx) not in [(coords[0] + int(i % len(st[0])),coords[1] + int((i - (i % len(st[0]))) / len(st[0]))) if st[int((i - (i % len(st[0]))) / len(st[0]))][i % len(st[0])] > 0 else None for i in range(len(st) * len(st[0]))]:
                            num_enclosed += 1
                            i += 1
            full = 1
            for c in range(cols):
                con = 0
                for n in range(len(next_st[0])):
                    if x + n == c and next_st[dy][n] > 0:
                        con = 1
                        break
                for n in range(len(st[0])):
                    if coords[0] + n == c and dy < len(st) and st[dy][n] > 0:
                        con = 1
                        break 
                if con == 1:
                    continue
                if self.board[dy][c] == 0:
                    full = 0
                    break
            if full == 1:
                full_lines += 1

        mult = 1
        if weights["enclosed_spectrum"] > 0: mult = 1 / ((rows - y) * weights["enclosed_spectrum"])
        val += weights["full_line"] * full_lines * weights["second_block"] + full_lines * (rows - y) * weights["height_spectrum"] * weights["second_block"]
        if total == count:
            val += weights["flush"] * weights["second_block"]
        else:
            val += weights["fully_enclosed"] * weights["second_block"] * mult
        val += y * weights["height"] * weights["second_block"]
        val += num_enclosed * weights["multiple_enclosed"] * weights["second_block"] * mult

        return val
    
    def check_overlap(self, st1, st2, c1, c2):
        return False

    def greedyChoiceMove(self):
        ### Use the weights defined above to evaluate the best move, 
        ### looking at the board, the current stone, and the next stone.
        if(debug): print("================================")
        curr_st = self.stone
        next_st = self.next_stone
        options = {}
        for r1 in range(4):
            for c1 in range(cols): # look at every column
                if check_collision(self.board, curr_st, (c1,0)):
                    continue
                y1 = 0
                while(1):
                    if check_collision(self.board, curr_st, (c1,y1)):
                        y1 -= 1
                        break
                    y1 += 1
                
                if weights["second_block"] != 0:
                    for r2 in range(4):
                        for c2 in range(cols):
                            if check_collision(self.board, next_st, (c2,0)):
                                continue
                            y2 = 0
                            while(1):
                                if check_collision(self.board, next_st, (c2,y2)):
                                    y2 -= 1
                                    break
                                y2 += 1
                            num = self.evalGreedyOption(curr_st, (c1,y1), next_st, (c2,y2))
                            if (c1,r1) not in options.keys(): options[(c1,r1)] = num 
                            else: options[(c1,r1)] = max(num, options[(c1,r1)])
                        next_st = rotate_clockwise(next_st) 
                else:
                    num = self.evalGreedyOption(curr_st, (c1,y1), None, None)
                    options[(c1,r1)] = num 
            curr_st = rotate_clockwise(curr_st) 
        best = -999999
        bestAction = (0,0)
        for key in options:
            if(options[key] > best):
                best = options[key]
                bestAction = key
        if(debug): print("Picked:",bestAction,"for",self.stone)
        return bestAction

    def run(self):
        key_actions = {
            'ESCAPE':   self.quit,
            'LEFT':     lambda:self.move(-1),
            'RIGHT':    lambda:self.move(+1),
            'DOWN':     lambda:self.drop(True),
            'UP':       self.rotate_stone,
            'p':        self.toggle_pause,
            'SPACE':    self.start_game,
            'RETURN':   self.insta_drop
        }

        self.gameover = False
        self.printed = False
        self.paused = False

        dont_burn_my_cpu = pygame.time.Clock()
        while 1:
            self.screen.fill((0,0,0))
            if self.gameover:
                if Test:
                    self.outputcsvtest(Strat, Outfile, append, self.score, self.level, self.lines)
                self.center_msg("""Game Over!\nYour score: %d
Press space to continue""" % self.score)
                
            else:
                if self.paused:
                    self.center_msg("Paused")
                else:
                    pygame.draw.line(self.screen,
                        (255,255,255),
                        (self.rlim+1, 0),
                        (self.rlim+1, self.height-1))
                    self.disp_msg("Next:", (
                        self.rlim+cell_size,
                        2))
                    self.disp_msg("Score: %d\n\nLevel: %d\
\nLines: %d" % (self.score, self.level, self.lines),
                        (self.rlim+cell_size, cell_size*5))
                    self.draw_matrix(self.bground_grid, (0,0))
                    self.draw_matrix(self.board, (0,0))
                    self.draw_matrix(self.stone,
                        (self.stone_x, self.stone_y))
                    self.draw_matrix(self.next_stone,
                        (cols+1,2))
            pygame.display.update()

            if self.gameover and Strat == 1:
                self.outputWeights(self.score, weights)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == eval("pygame.K_" + "SPACE"):
                        file = open("log.txt",'a')
                        file.write("Score: %d\n" % self.score)
                        file.close()
                        self.start_game()
                elif user_input and event.type == pygame.USEREVENT+1:
                    self.drop(False)
                elif user_input and event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_"
                        +key):
                            key_actions[key]()
            
            # Ask the AI for a move
            self.determineMove()
            
            # print("===================")

            while(manual):
                br = 0
                dont_burn_my_cpu.tick(maxfps)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == eval("pygame.K_" + "SPACE"):
                            br = 1
                            break
                if br == 1:
                    break

            dont_burn_my_cpu.tick(maxfps)
    def outputcsvtest(self, strategy, outfilename, appending, score, level, lines):
        if not self.printed:
            if strategy == 0:
                strstrat = "Greedy"
            else:
                strstrat = "Learning"
            if appending:
                f = open(outfilename, 'a')
            else:
                f = open(outfilename, 'w')
                f.write("Strategy,Score,Level,Lines\n")
            nextEntry = "%s,%s,%s,%s\n"
            nextEntry = nextEntry % (strstrat,str(score), str(level), str(lines))
            f.write(nextEntry)
            self.printed = True
            f.close()
            if(appending):
                self.start_game
    def outputWeights(self, score, weights):
        f = open("learningData.txt", 'a')
        nextEntry = str(score) + ","
        for a in weights.values:
            nextEntry + str(a) + ","
        nextEntry = nextEntry[:-1]
        f.write(nextEntry)

    


if __name__ == '__main__':
    print("Testing args: <strategy select> <outfile name> <append?>")
    print("strategy select: 0 - greedy, 1 - other")
    print("outfile name: name of desired output file")
    print("append outfile? 0 - no, 1 - yes")
    if len(sys.argv) == 4:
        Strat = int(sys.argv[1])
        Outfile = sys.argv[2]
        append = int(sys.argv[3])
        if append == 1:
            append = True
        else:
            append = False
        Test = True
        App = TetrisApp()
        App.run()
        print("Testing with args:" + Strat + " " + Outfile + " " + append)
    else:
        print("Is not Testing")
        App = TetrisApp()
        App.run()
