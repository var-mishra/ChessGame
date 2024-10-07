public abstract class ChessPiece 
{
     String color;
    public ChessPiece(String color)
     {
        this.color = color;
    }

    public String getColor() 
    
    {
        return color;
    }

    public abstract boolean isValidMove(String start, String end, ChessBoard board);

    @Override
    public String toString() {
        return color + this.getClass().getSimpleName().charAt(0);
    }
}
