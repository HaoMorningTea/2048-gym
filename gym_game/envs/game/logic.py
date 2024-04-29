import random
from . import constants as c
import sqlite3
import datetime

#gloabl variable to keep track of the score
score = 0
move = 0

#connect to the database
conn = None #to be created in the puzzle function

#set game_time_id by current time
current_time = datetime.datetime.now()

def set_conn(connection):
    global conn
    conn = connection
    
''' def initialize_database():
    # Initialize database and create table
    cursor = conn.cursor()

    cursor.execute(
        CREATE TABLE IF NOT EXISTS game_moves (
            move_id INTEGER PRIMARY KEY,
            board_state TEXT,
            move_type TEXT,
            marginal_score_increase INTEGER,
            game_time_id TIMESTAMP,
            move_number INTEGER
        )
    )

    conn.commit()
    cursor.close()
'''

def new_game(n):
    matrix = []
    for i in range(n):
        matrix.append([0] * n)
    matrix = add_two(matrix)
    matrix = add_two(matrix)
    return matrix

def add_two(mat):
    a = random.randint(0, len(mat)-1)
    b = random.randint(0, len(mat)-1)
    while mat[a][b] != 0:
        a = random.randint(0, len(mat)-1)
        b = random.randint(0, len(mat)-1)
    mat[a][b] = 2
    return mat

def game_state(mat):
    # check for win cell
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 2048:
                return 'win'
    # check for any zero entries
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == 0:
                return 'not over'
    # check for same cells that touch each other
    for i in range(len(mat)-1):
        # intentionally reduced to check the row on the right and below
        # more elegant to use exceptions but most likely this will be their solution
        for j in range(len(mat[0])-1):
            if mat[i][j] == mat[i+1][j] or mat[i][j+1] == mat[i][j]:
                return 'not over'
    for k in range(len(mat)-1):  # to check the left/right entries on the last row
        if mat[len(mat)-1][k] == mat[len(mat)-1][k+1]:
            return 'not over'
    for j in range(len(mat)-1):  # check up/down entries on last column
        if mat[j][len(mat)-1] == mat[j+1][len(mat)-1]:
            return 'not over'
    return 'lose'

def reverse(mat):
    new = []
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0])-j-1])
    return new

def transpose(mat):
    new = []
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new

def cover_up(mat):
    new = []
    for j in range(c.GRID_LEN):
        partial_new = []
        for i in range(c.GRID_LEN):
            partial_new.append(0)
        new.append(partial_new)
    done = False
    for i in range(c.GRID_LEN):
        count = 0
        for j in range(c.GRID_LEN):
            if mat[i][j] != 0:
                new[i][count] = mat[i][j]
                if j != count:
                    done = True
                count += 1
    return new, done

def merge(mat, done):
    global score
    for i in range(c.GRID_LEN):
        for j in range(c.GRID_LEN-1):
            if mat[i][j] == mat[i][j+1] and mat[i][j] != 0:
                mat[i][j] *= 2
                score += mat[i][j]
                mat[i][j+1] = 0
                done = True
    print("Score: ", score)
    return mat, done

def marignal_score_increase(oldscore, score):
    return score - oldscore

def up(game):
    global conn
    global move
    print("up")
    oldscore = score
    # return matrix after shifting up
    game = transpose(game)
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = transpose(game)
    
    # Insert data into the database
#    cursor = conn.cursor()  # Create a cursor
#    cursor.execute('''
#        INSERT INTO game_moves (board_state, move_type, marginal_score_increase, game_time_id, move_number)
#        VALUES (?, ?, ?, ?, ?)
#    ''', (str(game), 'up', marignal_score_increase(oldscore, score), current_time, move))
#    conn.commit()
#    cursor.close()
    move += 1
    return game, done

def down(game):
    global conn
    global move
    print("down")
    oldscore = score
    # return matrix after shifting down
    game = reverse(transpose(game))
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = transpose(reverse(game))
    
    # Insert data into the database
#    cursor = conn.cursor()  # Create a cursor
#    cursor.execute('''
#        INSERT INTO game_moves (board_state, move_type, marginal_score_increase, game_time_id, move_number)
#        VALUES (?, ?, ?, ?, ?)
#    ''', (str(game), 'down', marignal_score_increase(oldscore, score), current_time, move))
#    conn.commit()
#    cursor.close()
    move += 1
    return game, done

def left(game):
    # global score
    global conn
    global move
    print("left")
    oldscore = score
    # return matrix after shifting left
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    
    # Insert data into the database
#    cursor = conn.cursor()  # Create a cursor
#    cursor.execute('''
#        INSERT INTO game_moves (board_state, move_type, marginal_score_increase, game_time_id, move_number)
#        VALUES (?, ?, ?, ?, ?)
#    ''', (str(game), 'left', marignal_score_increase(oldscore, score), current_time, move))
#    conn.commit()
#    cursor.close()
    move += 1
    return game, done

def right(game):
    # global score
    global conn
    global move
    print("right")
    oldscore = score
    # return matrix after shifting right
    game = reverse(game)
    game, done = cover_up(game)
    game, done = merge(game, done)
    game = cover_up(game)[0]
    game = reverse(game)
    
    # Insert data into the database
#    cursor = conn.cursor()  # Create a cursor
#    cursor.execute('''
#        INSERT INTO game_moves (board_state, move_type, marginal_score_increase, game_time_id, move_number)
#        VALUES (?, ?, ?, ?, ?)
#    ''', (str(game), 'right', marignal_score_increase(oldscore, score), current_time, move))
#    conn.commit()
#    cursor.close()
    move += 1
    return game, done