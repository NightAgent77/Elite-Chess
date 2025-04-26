import chess

class ChessGame:
    def __init__(self):
        self.board = chess.Board()

    def move_piece(self, move):
        """Attempt to make a move on the board.
        Args:
            move (str): A move in UCI format (e.g., 'e2e4').
        Returns:
            bool: True if the move was successful, False otherwise.
        """
        try:
            chess_move = chess.Move.from_uci(move)
            if chess_move in self.board.legal_moves:
                self.board.push(chess_move)
                return True
            else:
                return False
        except ValueError:
            return False

    def get_legal_moves(self):
        """Get all legal moves for the current position.
        Returns:
            list: A list of moves in UCI format.
        """
        return [move.uci() for move in self.board.legal_moves]

    def is_game_over(self):
        """Check if the game is over.
        Returns:
            bool: True if the game is over, False otherwise.
        """
        return self.board.is_game_over()

    def get_winner(self):
        """Get the winner of the game if it is over.
        Returns:
            str: 'white', 'black', or 'draw' depending on the result.
        """
        if self.board.is_checkmate():
            return 'white' if self.board.turn == chess.BLACK else 'black'
        elif self.board.is_stalemate() or self.board.is_insufficient_material():
            return 'draw'
        return None
