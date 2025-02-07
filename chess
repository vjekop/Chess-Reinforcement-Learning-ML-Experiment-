import chess
import random
import pickle
from termcolor import colored  

BOARD_SIZE = 8


q_table = {}

def load_q_table():
    try:
        with open("q_table.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        print("No saved Q-table found, starting fresh.")
        return {}

def save_q_table(q_table):
    with open("q_table.pkl", "wb") as file:
        pickle.dump(q_table, file)

def generate_move(board):
    legal_moves = list(board.legal_moves)
    return random.choice(legal_moves) if legal_moves else None

def select_move(board, player):
    board_fen = board.fen()

    if board_fen not in q_table:
        q_table[board_fen] = {move.uci(): 0 for move in board.legal_moves}
    legal_moves = list(board.legal_moves)
    move_values = [q_table[board_fen].get(move.uci(), 0) for move in legal_moves]

    if random.random() < 0.1:
        move = random.choice(legal_moves)
    else:
        max_value = max(move_values)
        best_moves = [legal_moves[i] for i in range(len(legal_moves)) if move_values[i] == max_value]
        move = random.choice(best_moves)

    return move

def promote_pawn(move, board):

    if move.promotion is None and (move.to_square == chess.A8 or move.to_square == chess.H8):
        # Ask the player for the promotion piece
        promotion_piece = input("Promote pawn to (q for queen, r for rook, b for bishop, n for knight): ")
        if promotion_piece == 'q':
            move.promotion = chess.QUEEN
        elif promotion_piece == 'r':
            move.promotion = chess.ROOK
        elif promotion_piece == 'b':
            move.promotion = chess.BISHOP
        elif promotion_piece == 'n':
            move.promotion = chess.KNIGHT
    return move

def is_king_in_check(board):
    return board.is_check()

def is_checkmate(board):
    return board.is_checkmate()
def print_colored_board(board):
    board_str = str(board)
    board_str = board_str.replace("P", colored("P", "blue")).replace("N", colored("N", "blue")).replace("B", colored("B", "blue")).replace("R", colored("R", "blue")).replace("Q", colored("Q", "blue")).replace("K", colored("K", "blue"))
    board_str = board_str.replace("p", colored("p", "red")).replace("n", colored("n", "red")).replace("b", colored("b", "red")).replace("r", colored("r", "red")).replace("q", colored("q", "red")).replace("k", colored("k", "red"))
    print(board_str)

def play_game():
    board = chess.Board()
    while not board.is_game_over():
        print_colored_board(board)
        if board.turn:
            user_move = input("Enter your move (e.g., 'e2e4'): ")
            try:
                move = chess.Move.from_uci(user_move)
                if move in board.legal_moves:
            
                    move = promote_pawn(move, board)
                    board.push(move)
                else:
                    print("Invalid move, try again.")
                    continue
            except ValueError:
                print("Invalid move format, try again.")
                continue
        else:
            ai_move = select_move(board, "black")
            print(f"AI move: {ai_move}")
            board.push(ai_move)

        if is_king_in_check(board):
            print("King is in check!")

        if is_checkmate(board):
            print("Checkmate! The game is over.")
            break

    print_colored_board(board)
    print("Game over!")
    return board.result()

def play_against_trained_agent():
    global q_table
    
    q_table = load_q_table()
    
    print("Starting the game against the AI...")

    result = play_game()
    save_q_table(q_table)
    print("Game result:", result)

if __name__ == "__main__":
    play_against_trained_agent()
