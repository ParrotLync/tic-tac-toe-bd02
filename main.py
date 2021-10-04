import random
from os import system
from math import inf as infinity


def get_empty_board():
    return [
        ['', '', ''],
        ['', '', ''],
        ['', '', '']
    ]


board = get_empty_board()

computer = 'X'
human = 'O'


def print_board():
    print("-----------")
    print("A {}".format(board[0]))
    print("B {}".format(board[1]))
    print("C {}".format(board[2]))
    print("-----------")


def get_formatted_state(state, opponent):

    for i in range(0, 3):
        for j in range(0, 3):
            if state[i][j] == opponent:
                state[i][j] = ''
    return state


def check_win(state):
    win_states = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]

    if [computer, computer, computer] in win_states:
        return computer
    elif [human, human, human] in win_states:
        return human

    return False


def is_empty(row, column):
    return board[row][column] == ''


def handle_player_move(player, row, column):
    board[row][column] = player


def get_valid_row(row_input):
    if row_input == 'A':
        return 0
    elif row_input == 'B':
        return 1
    elif row_input == 'C':
        return 2

    return None


def get_valid_column(col_input):
    if 0 < col_input < 4:
        return col_input - 1

    return None


def human_move():
    valid = False
    while not valid:
        move = input("\n(@) Please enter your new move (example: A3): ")

        row_valid = True
        i = get_valid_row(move[0].upper())
        if i is None:
            row_valid = False
            print("(!) Invalid row defined! (A, B, C)")

        column_valid = True
        j = get_valid_column(int(move[1]))
        if j is None:
            column_valid = False
            print("(!) Invalid column defined! (1, 2, 3)")

        if row_valid and column_valid:
            if is_empty(i, j):
                valid = True
                handle_player_move(human, i, j)
            else:
                print("(!) That position is not empty!")


def has_empty_positions(state):
    for i in range(0, 3):
        for j in range(0, 3):
            if state[i][j] == '':
                return True

    return False


def get_empty_positions(state):
    positions = []
    for x, row in enumerate(state):
        for y, col in enumerate(row):
            if col == '':
                positions.append([x, y])
    return positions


def get_current_score(state):
    score = 0
    if check_win(state) == computer:
        score += 1
    elif check_win(state) == human:
        score -= 1

    return score


def minimax(state, depth, player):
    if player == computer:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or check_win(state) is not False:
        score = get_current_score(state)
        return [-1, -1, score]

    for position in get_empty_positions(state):
        x, y = position[0], position[1]
        state[x][y] = player

        if player == computer:
            next_player = human
        else:
            next_player = computer

        score = minimax(state, depth - 1, next_player)
        score[0], score[1] = x, y

        if player == computer:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score

    return best


def get_state_copy(state):
    new_state = []
    for i in range(0, 3):
        row = []
        for j in range(0, 3):
            row.append(state[i][j])
        new_state.append(row)
    return new_state


def computer_move():
    depth = len(get_empty_positions(board))

    if depth == 9:
        x = random.choice([0, 1, 2])
        y = random.choice([0, 1, 2])
    else:
        state = get_state_copy(board)
        move = minimax(state, depth, computer)
        x, y = move[0], move[1]

    handle_player_move(computer, x, y)


def get_random_player():
    return random.choice([human, computer])


def main_loop():
    system('cls')

    game_end = False
    turn = get_random_player()
    if turn == human:
        print("\n(@) You are playing as O and starting the game. Good luck!")
    else:
        print("\n(@) Computer is playing as X and starting the game. Good luck!")

    while not game_end:
        print_board()
        if turn == human:
            human_move()

        if turn == computer:
            print("\n(#) Computer is thinking...")
            computer_move()

        win = check_win(board)
        if win is not False:
            print_board()
            game_end = True
            if win == human:
                print("\n(@) You have won! Congratulations!")
            else:
                print("\n(@) Computer has won! You lose...")

        if not has_empty_positions(board):
            game_end = True
            print("\n(@) Out of moves. It's a tie!")

        if turn == human:
            turn = computer
        else:
            turn = human

    input("\n(@) Game has ended. Press ENTER to exit the game.")


if __name__ == '__main__':
    main_loop()
