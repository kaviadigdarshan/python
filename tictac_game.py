import sys

players = []
symbols = ["X", "O"]
global player_to_start; player_to_start = None

def reset_board():
    board_initial_state = ["+", "|", " 1 ", " 2 ", " 3 ", " 4 ", " 5 ", " 6 ", " 7 ", " 8 ", " 9 "]
    return board_initial_state

def assign_symbols_and_get_starting_player(players):
    global player_to_start
    player1_name = players[0]["name"]
    player1_symbol = str(input(f"{player1_name}: Enter your symbol of choice (X / O): "))
    player1_symbol = player1_symbol.upper()
    if player1_symbol not in symbols:
        print("Wrong choice! Try again!")
        assign_symbols_and_get_starting_player(players)
    else:
        players[0]["symbol"] = player1_symbol
        players[1]["symbol"] = [i for i in symbols if i not in [player1_symbol]][0]
        player_to_start = [d["name"] for d in players if d["symbol"] == "X"][0]
        print(f"{player_to_start} will start the game!")

def print_board(board_state):
    lines = []
    h_sep = board_state[0]
    v_sep = board_state[1]
    lines.append(h_sep*13)
    lines.append(v_sep + board_state[2] + v_sep + board_state[3] + v_sep + board_state[4] + v_sep)
    lines.append(h_sep*13)
    lines.append(v_sep + board_state[5] + v_sep + board_state[6] + v_sep + board_state[7] + v_sep)
    lines.append(h_sep*13)
    lines.append(v_sep + board_state[8] + v_sep + board_state[9] + v_sep + board_state[10] + v_sep)
    lines.append(h_sep*13)
    print("\n".join(lines))

def is_number_valid(player_num, board_state):
    is_valid = False
    for i in board_state[2:]:
        if i.strip() not in symbols:
          if int(i) == player_num:
            is_valid = True
    return is_valid

def get_next_player(curr_player):
    return [d["name"] for d in players if d["name"] != curr_player][0]

def found_three_occurences(symbol_positions):
    winning_positions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for pos in winning_positions:
        common_pos = tuple(sorted(set(symbol_positions).intersection(set(pos))))
        if pos == common_pos:
            return True
    return False

def check_if_game_over(curr_player, board_state): 
    player_symbol = [d["symbol"] for d in players if d["name"] == curr_player][0]
    symbol_positions = [i for i, symbol in enumerate(board_state[2:]) if player_symbol in symbol]
    if found_three_occurences(symbol_positions):
        return True, curr_player
    else:
        remaining_positions = [pos for pos in board_state[2:] if pos.strip().isdigit()]
        if len(remaining_positions) == 0:
            return True, None
        else:
            return False, curr_player
        

def play_game(curr_player, board_state):
    try:
        player_num = int(input(f"\n{curr_player}, Enter a number on the board: "))
    except ValueError:
        print(f"\n{curr_player}: Incorrect Input! Enter the number which is present on the board. Try again.")
        print_board(board_state)
        play_game(curr_player, board_state)
    if player_num > 9 or player_num < 0:
        print(f"\n{curr_player}: Incorrect Input! Enter the number which is present on the board. Try again.")
        print_board(board_state)
        play_game(curr_player, board_state)
    if not is_number_valid(player_num, board_state):
        print(f"\n{curr_player}: Incorrect Input! Enter the number which is present on the board. Try again.")
        print_board(board_state)
        play_game(curr_player, board_state)
    board_state[player_num + 1] = [" " + d["symbol"] + " " for d in players if d["name"] == curr_player][0]
    print_board(board_state)
    is_game_over, winner = check_if_game_over(curr_player, board_state)
    if not is_game_over and winner:
        next_player = get_next_player(curr_player)
        play_game(next_player, board_state)
    else:
        if winner and is_game_over:
            print(f"\n{winner} have won the game!")
        elif not winner and is_game_over:
            print(f"Whew! That was a tough one. Both of you were great but none of you are winner.")
        replay_choice = str(input("Want to play again? (Y/N): "))
        if replay_choice in ('Y', 'y'):
            retain_choice = str(input("Want to retain the same players? (Y/N): "))
            if retain_choice in ('Y', 'y'):
                initiate(players[0]['name'], players[1]['name'])
            else:
                initiate()
        sys.exit(1)

def initiate(player1_name=None, player2_name=None):
    if not player1_name:
        player1_name = str(input("Enter Player 1 name: "))
        players.append({"name": player1_name})
    if not player2_name:
        player2_name = str(input("Enter Player 2 name: "))
        players.append({"name": player2_name})
    board_state = reset_board()
    print_board(board_state)
    assign_symbols_and_get_starting_player(players)
    play_game(player_to_start, board_state)

if __name__ == '__main__':
    initiate()
    
