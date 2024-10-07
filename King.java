public class King extends ChessPiece 
{
    public King(String color) 
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
        int colDiff = Math.abs(endCol - startCol);
        int rowDiff = Math.abs(endRow - startRow);
        return colDiff <= 1 && rowDiff <= 1;
    }
}
