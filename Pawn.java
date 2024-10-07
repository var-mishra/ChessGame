public class Pawn extends ChessPiece {
    public Pawn(String color) {
        super(color);
    }

    @Override
    public boolean isValidMove(String start, String end, ChessBoard board) 
    {
        char startCol = start.charAt(0);
        char endCol = end.charAt(0);
        int startRow = Integer.parseInt(start.substring(1));
        int endRow = Integer.parseInt(end.substring(1));
        int direction = getColor().equals("W") ? 1 : -1; 

        if (startCol == endCol)
        {
            if (endRow == startRow + direction && board.isEmpty(end)) 
            {
                return true;
            }
            if ((startRow == 2 && getColor().equals("W")) || (startRow == 7 && getColor().equals("B"))) 
            {
                return endRow == startRow + 2 * direction && board.isEmpty(end);
            }
        } 
        else if(Math.abs(startCol - endCol) == 1 && endRow == startRow + direction) 
        {
            return !board.isEmpty(end) && !board.getPiece(end).getColor().equals(getColor());
        }
        return false;
    }
}
