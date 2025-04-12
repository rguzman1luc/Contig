import java.util.Random;
import java.util.Scanner;

public class Contig_2 {
    public static String[] squares = new String[]{
            "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16",
            "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32",
            "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "44", "45", "48", "50", "54", "55",
            "60", "64", "66", "72", "75", "80", "90", "96", "100", "108", "120", "125", "144", "150", "180", "216"
    };
    public static String buffer = "";

    public static int player1Score = 0;
    public static int player2Score = 0;
    public static int winningScore = 25;

    public static String player1Initials;
    public static String player2Initials;

    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        //used to determine turn order
        double orderRoll = Math.random();
        //holds t/f value for a game rule
        boolean comebackRule = true;
        //Instructions
        displayBoard();
        instructions();
        buffer = scan.nextLine();
        System.out.print("Play with the Comeback Rule?(Y/N):");
        //Asks the user if they want the comeback rule on or off, and in the case they write "yes" or "no", just gets the first letter
        String response = scan.nextLine().substring(0,1);
        while(!(response.equalsIgnoreCase("Y") || response.equalsIgnoreCase("N"))) {
            System.out.print("(Y/N bot):");
            response = scan.nextLine().substring(0,1);
        }
        //comeback is true by default, so only need to check if they don't want it on
        if (response.equalsIgnoreCase("N")) {
            comebackRule = false;
        }
        //gets names
        getNames();
        //Keeps the game going if both scores are under winningScore or if they're tied
        while((player1Score < winningScore && player2Score < winningScore) || player1Score == player2Score) {
            if (!comebackRule) {
                //When comeback rule is off, checks scores after each turn (the second turn gets checked by the while loop)
                if (orderRoll < .5) {
                    playerTurn(player1Initials);
                    if (player1Score >= winningScore) {
                        break;
                    }
                    playerTurn(player2Initials);
                } else {
                    playerTurn(player2Initials);
                    if (player2Score >= winningScore) {
                        break;
                    }
                    playerTurn(player1Initials);
                }
            //if comeback rule is off, lets both players have their turn
            } else {
                if (orderRoll < .5) {
                    playerTurn(player1Initials);
                    playerTurn(player2Initials);
                } else {
                    playerTurn(player2Initials);
                    playerTurn(player1Initials);
                }
            }
        }
        finishGame();
    }

    public static void instructions(){
        System.out.print("""
                         The game's name is Contig. The goal is to obtain 25 points, first to 25 wins. Every turn, each player will get three random numbers ranging from [1-6].
                         You then use whatever operations you want (to allow) on the numbers. Each number will be used once. If your resulting number is on the board, you may
                         take that square by typing it in on your turn. When a square is taken by a player, that player's name will replace the number on the board. If you
                         can't think of a valid number (or run out of time) you must skip your turn.
                         EXAMPLES OF LEGAL MOVES: (2, 3, 4) 2 * 3 * 4 = 24   (2, 2, 2) 2(2 - 2) = 0   (Expo. allowed)(6, 3, 4) 6^3/4 = 54 (Fact allowed)(3, 4, 4) 4! * (4 - 3) = 24
                         EXAMPLES OF ILLEGAL MOVES: (2, 1, 6) 2 + 1 + 6 = 216   (3, 2, 4) 32/4 = 8
                         SCORING POINTS - When you take a square, you get 1 point for every adjacent tile that has also been taken by any player, including yourself.
                         COMEBACK RULE: With the comeback rule off, if you reach 25 points, or more, you win right then and there. With it on, the game will wait until both
                         players have finished their turns, and if both are at or above 25, the highest score wins. In addition, if both players are at or above 25 points
                         and tied, the game will go in (still letting both players finish their turns) until one player's score is higher than the others.
                         Press enter to continue:""");
    }

    public static void getNames(){
        Scanner scan = new Scanner(System.in);
        String input;

        System.out.print("Player 1, Enter your name (Max 5 characters): ");
        input = scan.nextLine();
        if(input.length() > 5) {
            player1Initials = input.toUpperCase().substring(0, 5);
        }else{
            player1Initials = input.toUpperCase();
        }

        System.out.print("Player 2, Enter your name (Max 5 characters): ");
        input = scan.nextLine();
        if(input.length() > 5) {
            player2Initials = input.toUpperCase().substring(0, 5);
        }else{
            player2Initials = input.toUpperCase();
        }
    }
    //Prints the board layout
    public static void displayBoard(){
        int index = 0;
        System.out.println("\n-------------------------------------------------");
        //amount of rows
        for(int i = 0; i < 8; i++){
            //amount of columns
            for(int j = 0; j < 8; j++) {
                System.out.print("|");
                centerPrint(index);
                index++;
            }
            System.out.println("|");
            System.out.println("-------------------------------------------------");
        }
        //prints the current scores at the bottom, left and right aligned
        System.out.printf("%-17s %13s %17s\n\n", String.format("%s's Score: %d" ,player1Initials, player1Score), " ", String.format("%s's Score: %d" ,player2Initials, player2Score));
    }

    public static void playerTurn(String player) {
        Scanner scan = new Scanner(System.in);
        Random r = new Random();
        int index;

        displayBoard();

        System.out.printf("%s, Press enter when you're ready for your numbers.", player);
        buffer = scan.nextLine();

        //Shows the current player's 3 random dice roll numbers [1-6]
        System.out.printf("\nYour Numbers: %d %d %d\n", r.nextInt(6)+1, r.nextInt(6)+1, r.nextInt(6)+1);

        //won't continue until player enters a valid number or "skip"
        System.out.print("Enter your number choice, or \"skip\" to skip your turn: ");

        //Keeps asking for an input if the input isn't available on the board and isn't "skip"
        String input = scan.nextLine();
        while(!(findNumber(input) || input.equalsIgnoreCase("skip"))){
            System.out.print("Enter your (valid) number choice, or \"skip\" to skip your turn you BOT: ");
            input = scan.nextLine();
        }

        if(findNumber(input)){
            index = findIndex(input);
            squares[index] = player;
            collectPoints(player, index);
        }
    }

    public static void centerPrint(int index){
        int left = (6 - squares[index].length())/2;
        int right = 5 - (left + squares[index].length());
        for(int i = 0; i < left; i++){
            System.out.print(" ");
        }
        System.out.print(squares[index]);
        for(int i = 0; i < right; i++){
            System.out.print(" ");
        }
    }

    public static boolean findNumber(String guess){
        for(int i = 0; i < squares.length; i++){
            if(squares[i].equals(guess) && !(squares[i].equals(player1Initials) || squares[i].equals(player2Initials))){
                return true;
            }
        }
        return false;
    }

    public static int findIndex(String num){
        for(int i = 0; i < squares.length; i++){
            if(squares[i].equals(num)){
                return i;
            }
        }
        return -1;
    }

    public static void collectPoints(String player, int index){
        int sum = 0;

        //checks top left corner
        if(index == 0){
            int [] tLeft = {1, 8, 9};
            for(int i = 0; i < tLeft.length; i++) {
                if (squares[tLeft[i]].equals(player1Initials) || squares[tLeft[i]].equals(player2Initials)) {
                    sum++;
                }
            }
        //checks top right corner
        }else if(index == 7){
            int [] tRight = {6, 14, 15};
            for(int i = 0; i < tRight.length; i++) {
                if (squares[tRight[i]].equals(player1Initials) || squares[tRight[i]].equals(player2Initials)) {
                    sum++;
                }
            }
        //Checks Bottom left corner
        }else if(index == 56){
            int [] bLeft = {48, 49, 57};
            for(int i = 0; i < bLeft.length; i++) {
                if (squares[bLeft[i]].equals(player1Initials) || squares[bLeft[i]].equals(player2Initials)) {
                    sum++;
                }
            }
        //Checks Bottom Right corner
        }else if(index == 63){
            int [] bRight = {54, 55, 62};
            for(int i = 0; i < bRight.length; i++) {
                if (squares[bRight[i]].equals(player1Initials) || squares[bRight[i]].equals(player2Initials)) {
                    sum++;
                }
            }
        //Checks top row cases
        }else if(index == 1 || index == 2 || index == 3 || index == 4 || index == 5 || index == 6){
            int [] tRow = {index - 1, index + 1, index + 7, index + 8, index + 9};
            for(int i = 0; i < tRow.length; i++) {
                if (squares[tRow[i]].equals(player1Initials) || squares[tRow[i]].equals(player2Initials)) {
                    sum++;
                }
            }
        //checks bottom row
        }else if(index == 57 || index == 58 || index == 59 || index == 60 || index == 61 || index == 62) {
            int[] bRow = {index - 1, index + 1, index - 9, index - 8, index - 7};
            for (int i = 0; i < bRow.length; i++) {
                if (squares[bRow[i]].equals(player1Initials) || squares[bRow[i]].equals(player2Initials)) {
                    sum++;
                }
            }
        //checks left edge
        }else if(index == 8 || index == 16 || index == 24 || index == 32 || index == 40 || index == 48){
            int[] lEdge = {index - 8, index - 7, index + 1, index + 8, index + 9};
            for (int i = 0; i < lEdge.length; i++) {
                if (squares[lEdge[i]].equals(player1Initials) || squares[lEdge[i]].equals(player2Initials)) {
                    sum++;
                }
            }
        //Checks Right Edge
        }else if(index == 15 || index == 23 || index == 31 || index == 39 || index == 47 || index == 55){
            int[] rEdge = {index - 9, index - 8, index - 1, index + 7, index + 8};
            for (int i = 0; i < rEdge.length; i++) {
                if (squares[rEdge[i]].equals(player1Initials) || squares[rEdge[i]].equals(player2Initials)) {
                    sum++;
                }
            }
        } else {
            //checks all center squares that aren't the edges
            int[] circle = {index - 9, index - 8, index - 7, index - 1, index + 1, index + 7, index + 8, index + 9};
            for (int i = 0; i < circle.length; i++) {
                if (squares[circle[i]].equals(player1Initials) || squares[circle[i]].equals(player2Initials)) {
                    sum++;
                }
            }
        }
        if(player.equals(player1Initials)){
            player1Score += sum;
        }else{
            player2Score += sum;
        }
    }
    public static void finishGame(){
        if (player1Score > player2Score){
            System.out.printf("%s wins %d to %d", player1Initials, player1Score, player2Score);
        } else {
            System.out.printf("%s wins %d to %d", player2Initials, player2Score, player1Score);
        }
    }
}