public class Rook extends ChessPiece 
{
    public Rook(String color) 
    {
        super(color);
    }
    @Override
    public boolean isValidMove(String start, String end, ChessBoard board)
    {
        char startCol = start.charAt(0);
        char endCol = end.charAt(0);
        int startRow = Integer.parseInt(start.substring(1));
        int endRow = Integer.parseInt(end.substring(1));
        if (startCol == endCol || startRow == endRow) 
        {
            return true;
        }
        return false;
    }
}
