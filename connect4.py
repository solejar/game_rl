import numpy as np

def select_action(action_space, curr_state, policy):

    for col in range(0,7):
        if action_space[col]==0
        if policy=='random':


offsets = np.full((4,2,2),0)
offsets[0][0] = [-1,0]
offsets[0][1] = [1,0]
offsets[1][0] = [0,-1]
offsets[1][1] = [0,1]
offsets[2][0] = [-1,1]
offsets[2][1] = [1,-1]
offsets[3][0] = [-1,-1]
offsets[3][1] = [1,1]

def victory_check(game_board,new_x,new_y):

    for victory_dim in range(1,5):
        game_state = game_board[victory_dim]

        curr_offset_1 = offsets[victory_dim-1][0]
        curr_offset_2 = offsets[victory_dim-1][1]

        curr_offsets = [curr_offset_1,curr_offset_2]

        total = 1

        for direction in range(0,2):

            offset_x = curr_offsets[direction][0] + new_x
            offset_y = curr_offsets[direction][1] + new_y
            if (offset_x>=0 and offset_x<7) and (offset_y>=0 and offset_y<7):
                total += game_state[offset_x][offset_y]

        if total>=4:
            return True

        game_state[new_x][new_y] = total

        #update the current running totals for next time
        for direction in range(0,2):

            offset_x = curr_offsets[direction][0] + new_x
            offset_y = curr_offsets[direction][1] + new_y

            in_x_bound = (offset_x>=0 and offset_x<7)
            in_y_bound = (offset_y>=0 and offset_y<6)

            while game_state[offset_x][offset_y]>0 and in_left_bound and in_right_bound:
                game_state[offset_x][offset_y] = total
                offset_x += curr_offsets[direction][0]
                offset_y += curr_offsets[direction][1]

                in_x_bound = (offset_x>=0 and offset_x<7)
                in_y_bound = (offset_y>=0 and offset_y<6)






def play_game(policy1='random',policy2='random'):

    #the action space is represented by a 1x7 array with initial values representing
    #how many discs can be added before column is full
    action_space = np.full((1,7),0)

    #initialize the empty game board.
    #first x-dim represents
    game_board = np.full((5,6,7),0.0)

    game_over = False

    player_policies = [policy1,policy2]

    if np.random().rand()<0.5:
        curr_player=1
    else:
        curr_player=0

    while 1<2:

        action_col = select_action(action_space,game_board,policy)

        action_row = action_space[action_col]
        action_space[action_col] += 1
        game_board[0][action_row][action_col] = 1

        game_over = victory_check(game_board,action[0],action[1])

        if(game_over):
            print('Player ',curr_player+1, ' is the winner!')
            break

        curr_player = 1 - curr_player
        game_board = -1*game_board




if __name__ == __main__:

    play_game()
