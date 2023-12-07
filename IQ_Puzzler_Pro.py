import itertools

Shape_1 = [
    [1, 0],
    [1, 0],
    [1, 1]
]

Shape_2 = [
    [1, 1, 1],
    [0, 1, 0]
]

Shape_3 = [
    [1, 1],
    [1, 0],
    [1, 0],
    [1, 0]
]

Shape_4 = [
    [1, 0],
    [1, 1],
    [0, 1],
    [0, 1]
]

Shape_5 = [
    [0, 1, 0],
    [1, 1, 0], 
    [0, 1, 1]
]

Shape_6 = [
    [1, 0, 0], 
    [1, 1, 0], 
    [0, 1, 1]
]

Shape_7 = [
    [1, 0], 
    [1, 1],
    [1, 1]
]

Shape_8 = [
    [1, 1, 1], 
    [1, 0, 0], 
    [1, 0, 0]
]

Shape_9 = [
    [1, 1], 
    [0, 1]
]

Shape_10 = [
    [1, 0],
    [1, 1], 
    [0, 1]
]

Shape_11 = [
    [1, 0],
    [1, 1], 
    [1, 0],
    [1, 0]
]

Shape_12 = [
    [1, 1],
    [1, 0], 
    [1, 1]
]

# Function to create the board
def create_board(width, height):
    return [[0 for _ in range(width)] for _ in range(height)]

# Function to print the board with different characters for each piece
def print_board(board):
    for row in board:
        print(" ".join(str(cell) for cell in row))
    print()

# Function to check if a piece can be placed
def can_place_piece(board, piece, x, y):
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if piece[i][j] == 1:
                if x + i >= len(board) or y + j >= len(board[0]) or board[x + i][y + j] == 1:
                    return False
    return True

# Function to place a piece on the board with a unique identifier
def place_piece(board, piece, x, y, piece_id):
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if piece[i][j] == 1:
                board[x + i][y + j] = piece_id

# Modified remove_piece function to clear the piece_id
def remove_piece(board, piece, x, y, piece_id):
    for i in range(len(piece)):
        for j in range(len(piece[i])):
            if piece[i][j] == 1:
                board[x + i][y + j] = 0

# Recursive backtracking algorithm to find all solutions
def solve_puzzle(board, pieces, current_piece=0, solutions=None):
    if solutions is None:
        solutions = []

    if current_piece == len(pieces):
        solutions.append([row[:] for row in board])  # Append a copy of the solution
        return solutions

    for x in range(len(board)):
        for y in range(len(board[0])):
            if can_place_piece(board, pieces[current_piece], x, y):
                place_piece(board, pieces[current_piece], x, y, current_piece + 1)  # Use current_piece + 1 as the identifier
                solutions = solve_puzzle(board, pieces, current_piece + 1, solutions)
                remove_piece(board, pieces[current_piece], x, y, current_piece + 1)

    return solutions

def is_solvable(partial_board, remaining_pieces):
    # Attempt to solve the partial board using only the remaining pieces
    return solve_puzzle(partial_board, remaining_pieces)

# Main function to find and print all solutions
def main():
    board = create_board(11, 5)
    pieces = [Shape_1, Shape_2, Shape_3, Shape_4, Shape_5, Shape_6, Shape_7, Shape_8, Shape_9, Shape_10, Shape_11, Shape_12]
    num_pieces_to_remove = 7  # Set the number of pieces you want to remove

    full_solutions = solve_puzzle(board, pieces)
    solvable_partial_boards = set()

    for solution in full_solutions:
        piece_indices = list(range(len(pieces)))
        for pieces_to_remove in itertools.combinations(piece_indices, num_pieces_to_remove):
            partial_board = [row[:] for row in solution]  # Create a copy of the full solution
            remaining_pieces = [pieces[i] for i in piece_indices if i not in pieces_to_remove]

            for idx in pieces_to_remove:
                remove_piece(partial_board, pieces[idx], 0, 0, idx + 1)  # Removing the piece

            if is_solvable(partial_board, remaining_pieces):
                # Convert the board to a tuple of tuples for hashability and add to the set
                partial_board_tuple = tuple(tuple(row) for row in partial_board)
                solvable_partial_boards.add(partial_board_tuple)

    print(f"Generated {len(solvable_partial_boards)} solvable partial board states with {num_pieces_to_remove} pieces removed.")

    # Optional: Print some or all solvable partial board states
    for partial_board in list(solvable_partial_boards)[:10]:  # Print the first 10 as an example
        print_board(list(partial_board))
        print()

if __name__ == "__main__":
    main()