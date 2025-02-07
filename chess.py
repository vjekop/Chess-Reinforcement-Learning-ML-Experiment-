import chess
import random
import pickle
from termcolor import colored  

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
                    piece = board.piece_at(move.from_square)

                    
                    if piece and piece.piece_type == chess.PAWN:
                        if chess.square_rank(move.to_square) in [0, 7]:  
                            promotion_piece = input("Promote pawn to (q for Queen, r for Rook, b for Bishop, n for Knight): ").lower()
                            promotion_dict = {'q': chess.QUEEN, 'r': chess.ROOK, 'b': chess.BISHOP, 'n': chess.KNIGHT}
                            if promotion_piece in promotion_dict:
                                move = chess.Move(move.from_square, move.to_square, promotion=promotion_dict[promotion_piece])
                            else:
                                print("Invalid promotion choice, defaulting to Queen.")
                                move = chess.Move(move.from_square, move.to_square, promotion=chess.QUEEN)

                    board.push(move)
                else:
                    print("Invalid move, try again.")
                    continue
            except ValueError:
                print("Invalid move format, try again.")
                continue
        else:  
            ai_move = select_move(board, "black")

            if board.piece_at(ai_move.from_square) and board.piece_at(ai_move.from_square).piece_type == chess.PAWN:
                if chess.square_rank(ai_move.to_square) in [0, 7]:
                    ai_move = chess.Move(ai_move.from_square, ai_move.to_square, promotion=chess.QUEEN) 

            print(f"AI move: {ai_move}")
            board.push(ai_move)

        if board.is_check():
            print("King is in check!")

        if board.is_checkmate():
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
