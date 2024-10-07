import java.util.*;
public class ChessBoard
    {
     Map<String, ChessPiece> board;
     String currentPlayer;
    public ChessBoard() 
        {
        board = new HashMap<>();
        currentPlayer = "W"; 
        initializeBoard();
    }

    public void initializeBoard() 
        {
        board.put("a1", new Rook("W"));
        board.put("d1", new Queen("W"));
        board.put("e1", new King("W"));
        board.put("h1", new Rook("W"));
        for (char c = 'a'; c <= 'h'; c++) 
        {
            board.put(c + "2", new Pawn("W"));
        }
        board.put("a8", new Rook("B"));
        board.put("d8", new Queen("B"));
        board.put("e8", new King("B"));
        board.put("h8", new Rook("B"));
        for (char c = 'a'; c <= 'h'; c++) {
            board.put(c + "7", new Pawn("B"));
        }
        for (int row = 3; row <= 6; row++)
            {
            for (char col = 'a'; col <= 'h'; col++)
            {
                board.put(col + String.valueOf(row), null);
            }
        }
    }

    public void printBoard() {
        for (int row = 8; row >= 1; row--) {
            for (char col = 'a'; col <= 'h'; col++) 
            {
                ChessPiece piece = board.get(col + String.valueOf(row));
                if (piece == null) 
                {
                    System.out.print("-- ");
                } else
                {
                    System.out.print(piece + " ");
                }
            }
            System.out.println();
        }
        System.out.println();
    }

    public boolean move(String start, String end)
        {
        if (!isValidPosition(start) || !isValidPosition(end))
        {
            System.out.println("Invalid Move");
            return false;
        }

        ChessPiece piece = board.get(start);

        if (piece == null || !piece.getColor().equals(currentPlayer))
        {
            System.out.println("Invalid Move");
            return false;
        }
        if (!piece.isValidMove(start, end, this)) 
        {
            System.out.println("Invalid Move");
            return false;
        }

        movePiece(start, end);
        switchPlayer();
        return true;
    }

    public boolean isValidPosition(String position)
    {
        return position.length() == 2 && position.charAt(0) >= 'a' && position.charAt(0) <= 'h' && position.charAt(1) >= '1' && position.charAt(1) <= '8';
    }
    public void movePiece(String start, String end)
    {
        board.put(end, board.get(start));
        board.put(start, null);
    }
    public ChessPiece getPiece(String position) 
    {
        return board.get(position);
    }

    public boolean isEmpty(String position) 
    {
        return board.get(position) == null;
    }
    public void switchPlayer()
     {
        currentPlayer = currentPlayer.equals("W") ? "B" : "W";
    }
}
