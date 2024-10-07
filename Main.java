public class Main
    {
    public static void main(String args[]) 
        {
        ChessBoard board = new ChessBoard();
        board.printBoard();
        board.move("e2", "e4");
        board.printBoard();
        board.move("e7", "e5");
        board.printBoard();
        board.move("g1", "f3");
        board.printBoard();
        board.move("b8", "c6");
        board.printBoard();
    }
}
