import random

squares = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16",
    "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32",
    "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "44", "45", "48", "50", "54", "55",
    "60", "64", "66", "72", "75", "80", "90", "96", "100", "108", "120", "125", "144", "150", "180", "216"
]
buffer = ""
player1_score = 0
player2_score = 0
winning_score = 25
player1_initials = ""
player2_initials = ""


def instructions():
    print("""
    The game's name is Contig. The goal is to obtain 25 points, first to 25 wins. Every turn, each player will get three random numbers ranging from [1-6].
    You then use whatever operations you want (to allow) on the numbers. Each number will be used once. If your resulting number is on the board, you may
    take that square by typing it in on your turn. When a square is taken by a player, that player's name will replace the number on the board.
    If you can't think of a valid number (or run out of time) you must skip your turn.

    SCORING POINTS - When you take a square, you get 1 point for every adjacent tile that has also been taken by any player, including yourself.

    COMEBACK RULE: If on, both players always get a turn before win check. If off, game ends as soon as someone hits 25+.

    Press enter to continue:
    """)
    input()


def get_names():
    global player1_initials, player2_initials
    player1_initials = input("Player 1, Enter your name (Max 5 characters): ").upper()[:5]
    player2_initials = input("Player 2, Enter your name (Max 5 characters): ").upper()[:5]


def display_board():
    print("\n" + "-" * 49)
    for i in range(0, 64, 8):
        for j in range(8):
            index = i + j
            val = squares[index]
            print(f"|{val.center(5)}", end="")
        print("|")
        print("-" * 49)
    print(f"{player1_initials}'s Score: {player1_score}".ljust(24) +
          f"{player2_initials}'s Score: {player2_score}".rjust(24))


def find_number(guess):
    return guess in squares and guess != player1_initials and guess != player2_initials


def find_index(num):
    try:
        return squares.index(num)
    except ValueError:
        return -1


def player_turn(player):
    global squares
    display_board()
    input(f"{player}, press enter when you're ready for your numbers...")
    nums = [random.randint(1, 6) for _ in range(3)]
    print(f"Your numbers: {nums[0]} {nums[1]} {nums[2]}")

    while True:
        guess = input('Enter your number choice, or "skip" to skip your turn: ').strip()
        if guess.lower() == "skip":
            return
        if find_number(guess):
            index = find_index(guess)
            squares[index] = player
            collect_points(player, index)
            return
        else:
            print("Invalid input. Try again.")


def collect_points(player, index):
    global player1_score, player2_score
    score = 0
    adjacent_indices = []

    row, col = divmod(index, 8)
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                adjacent_indices.append(r * 8 + c)

    for i in adjacent_indices:
        if squares[i] == player1_initials or squares[i] == player2_initials:
            score += 1

    if player == player1_initials:
        player1_score += score
    else:
        player2_score += score


def finish_game():
    if player1_score > player2_score:
        print(f"{player1_initials} wins {player1_score} to {player2_score}!")
    else:
        print(f"{player2_initials} wins {player2_score} to {player1_score}!")


def main():
    global player1_score, player2_score
    instructions()

    comeback_rule = input("Play with the Comeback Rule? (Y/N): ").strip().upper().startswith('Y')
    get_names()

    order_roll = random.random()

    while (player1_score < winning_score and player2_score < winning_score) or player1_score == player2_score:
        if not comeback_rule:
            if order_roll < 0.5:
                player_turn(player1_initials)
                if player1_score >= winning_score:
                    break
                player_turn(player2_initials)
            else:
                player_turn(player2_initials)
                if player2_score >= winning_score:
                    break
                player_turn(player1_initials)
        else:
            if order_roll < 0.5:
                player_turn(player1_initials)
                player_turn(player2_initials)
            else:
                player_turn(player2_initials)
                player_turn(player1_initials)

    finish_game()


if __name__ == "__main__":
    main()