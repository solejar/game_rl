import numpy as np
from graphics import *

win = GraphWin("Connect 4 Board", 400,400)

def draw_initial_board():

    for row in range(1,7):
        for col in range(1,8):
            c = Circle(Point(col*50,row*50),15)
            c.draw(win)

def draw_new_piece(new_row,new_col, player_index):
    if player_index==0:
        color='blue'
    else:
        color='red'

    piece_x = (new_col+1)*50
    piece_y = (6-new_row)*50
    new_circle = Circle(Point(piece_x,piece_y),15)
    new_circle.setFill(color)
    new_circle.draw(win)

#technically functional, at least for random selection
def select_action(action_space, curr_state, policy, draw=False):

    #return the indices of non-full columns
    valid_cols = np.nonzero(action_space<6)[0]
    if policy=='random':
        return np.random.choice(valid_cols)
    elif policy=='human':

        while 1<2:
            message = 'Choose a column from ' + ', '.join('{0}'.format(n+1) for n in valid_cols.tolist())
            if draw:
                textObj = Text(Point(200,350),message)
                textObj.draw(win)
                selected_col = int(win.getKey())
                textObj.undraw()

            else:

                selected_col = int(input(message+'\n'))

            if np.isin(selected_col-1,valid_cols):
                return selected_col-1
            else:
                message = 'Your selection needs to be from the following: ' + ', '.join('{0}'.format(n+1) for n in valid_cols.tolist())
                if draw:
                    textObj = Text(Point(200,350),message)
                    textObj.draw(win)
                    win.getKey()
                    textObj.undraw()
                else:
                    print(message)

#offset directions for the 4 axes of game completion
#which are up-down, left-right, forward diag, backward diag
offsets = np.full((4,2,2),0)
offsets[0][0] = [-1,0] #left-right
offsets[0][1] = [1,0]
offsets[1][0] = [0,-1] #up-down
offsets[1][1] = [0,1]
offsets[2][0] = [-1,1] #back diag
offsets[2][1] = [1,-1]
offsets[3][0] = [-1,-1] #forward diag
offsets[3][1] = [1,1]

#checks a new game board for victory
def victory_check(game_board,new_row,new_col):

    #check along the four axes of completion for a 4-in-a-row
    for victory_dim in range(1,5): #not a typo, i=0 reserved for gamestate representation
        game_state = game_board[victory_dim] #array of how close to completion along the axis

        curr_offset_1 = offsets[victory_dim-1][0] #[x,y] loc offset for given axis
        curr_offset_2 = offsets[victory_dim-1][1]

        curr_offsets = [curr_offset_1,curr_offset_2] #put them in array to avoid repeated code blocks

        #at the very least incrementing by 1 for new disc
        total = 1

        for direction in range(0,2): #if in bounds, add total of 'left' and 'right' along axis

            offset_row = curr_offsets[direction][0] + new_row
            offset_col = curr_offsets[direction][1] + new_col

            #print('direction: ', direction, ' , new_row: ' ,new_row,' , offset_row: ',offset_row, ' curr offsets for x: ', curr_offsets[direction][0])
            in_row_bound = (offset_row>=0 and offset_row<6)
            in_col_bound = (offset_col>=0 and offset_col<7)

            #greater than 0 check is because enemy discs are -1
            if in_row_bound and in_col_bound and game_state[offset_row][offset_col]>0:
                total += game_state[offset_row][offset_col]

        if total>=4:
            return True

        game_state[new_row][new_col] = total

        #update the current running totals for next time
        for direction in range(0,2):

            offset_row = curr_offsets[direction][0] + new_row
            offset_col = curr_offsets[direction][1] + new_col

            in_row_bound = (offset_row>=0 and offset_row<6)
            in_col_bound = (offset_col>=0 and offset_col<7)

            #greater than 0 check ensures that we only
            while in_row_bound and in_col_bound and game_state[offset_row][offset_col]>0:
                game_state[offset_row][offset_col] = total
                offset_row += curr_offsets[direction][0]
                offset_col += curr_offsets[direction][1]

                in_row_bound = (offset_row>=0 and offset_row<7)
                in_col_bound = (offset_col>=0 and offset_col<6)


    #if no win condition yet found, return false
    return False


def play_game(policy1='random',policy2='random', draw=False):

    if draw:
        draw_initial_board()



    #the action space is represented by a 1x7 array
    #values represent how many discs are currently in the column
    action_space = np.full((1,7),0)[0]

    #initialize the empty game board.
    #first x-dim represents the disc positions as -1, or 1  (0 is empty)
    #next four represent up-down, left-right, forward-diagonal, and backward-diagonal
    #these are used to check for game completion in a non-redundant way
    game_board = np.full((5,6,7),0.0)

    #put player policies in array so we can alternate between them every iter of game loop
    player_policies = [policy1,policy2]

    #choose first player randomly
    if np.random.rand()<0.5:
        curr_player=0
    else:
        curr_player=1

    #play game forever (until game completion)
    while 1<2:

        #decide where current player will drop disc
        action_col = select_action(action_space,game_board,player_policies[curr_player],draw)

        #figure out current unoccupied row in that column
        action_row = action_space[action_col]

        #increment the action space and add the disc to the game board
        action_space[action_col] += 1
        game_board[0][action_row][action_col] = 1

        if draw:
            draw_new_piece(action_row, action_col, curr_player)

        #check if that move ended the game
        game_over = victory_check(game_board,action_row,action_col)

        if game_over:
            message = 'Player {0} is the winner!'.format(str(curr_player+1))

            if draw:
                textObj = Text(Point(200,350),message)
                textObj.draw(win)
                win.getMouse()
                win.close()

            else:
                print(message)
            break

        elif np.sum(action_space) == 42: #this occurs if all 42 discs are filled $ no one has won
            message = 'Game ends in a draw'

            if draw:
                win.getMouse()
                win.close()

            else:
                print(message)

            break

        #alternate the players & 'flip' polarity of game board
        curr_player = 1 - curr_player
        game_board = -1*game_board


if __name__ =='__main__':

    play_game(policy1='random',policy2='human',draw=True)
