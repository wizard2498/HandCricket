import random
import sys
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="To create a personalised game.")
    parser.add_argument(
        "-n", "--name", metavar="name", required=True,
        help="The name of the player who wants to play the game."
    )
    args = parser.parse_args()


class points:
    def __init__(self, name, point):
        self.point = point
        self.name = name

    def add_point(self, run):
        self.point += run

    def get_point(self):
        print(f"{self.name}, your point is {self.point}.")

    def total_run(self):
        # Return the runs needed (current points + 1)
        return self.point + 1


py = points("Python", 0)
player = points(args.name, 0)


def game():
    global BatPLayer, playerBat
    BatPLayer = False
    playerBat = False

    # First‑innings random seeds (they'll be re‑generated each ball)
    tossNum = random.randint(1, 6)

    print("Welcome to Hand Cricket.")
    toss = int(input(f"Toss... Choose odd or even.\n1 for odd\n2 for even.\n{args.name} choice = "))

    # Validate toss choice
    if toss < 1 or toss > 2:
        print(f"{args.name}, you should select from the given numbers only.")
        return  # quit this round

    # Ask for toss number
    choice_str = "odd" if toss == 1 else "even"
    comp_choice_str = "even" if toss == 1 else "odd"
    print(f"{args.name}, you chose {choice_str}.\nPython chose {comp_choice_str}.")
    AskTossNum = input(f"\n{args.name}, give your toss number (1–6): ")
    try:
        AskTossNum = int(AskTossNum)
        tossNum = (tossNum + AskTossNum) % 2
    except ValueError:
        print("You should give a number only.")
        return

    # Determine toss winner
    if tossNum == 0:
        print("Python wins the toss and chooses to bat first.")
        BatPLayer = True
    else:
        print(f"{args.name}, you won the toss.")
        BatBowl = int(input("Choose:\n1 for bat\n2 for bowl\nYour choice = "))
        if BatBowl == 1:
            print("You chose to bat first.")
            playerBat = True
        elif BatBowl == 2:
            print("You chose to bowl first.")
            BatPLayer = True
        else:
            print("You should choose from the given numbers only.")
            return

    # ── First Innings ────────────────────────────────────────────────────────────
    if BatPLayer:
        print("\n--- First Innings: Python batting ---")
        while True:
            RandomNum = random.randint(0, 10)
            try:
                askNum = int(input(f"{args.name}, give your bowl (0–10): "))
            except ValueError:
                print("You should enter a number between 0 and 10 only.")
                continue

            if askNum < 0 or askNum > 10:
                print("You should give numbers between 0 and 10 only.")
                continue

            if RandomNum != askNum:
                print(f"You bowled {askNum}, Python scored {RandomNum}.")
                py.add_point(RandomNum)
                py.get_point()
            else:
                # Python is out
                runs_needed = py.total_run()
                print(f"\nYou bowled {askNum} and Python scored {RandomNum}. Python is out.")
                print(f"Batting turn... Runs to make = {runs_needed}")
                break

        # Second half of first‑innings: player batting the chase
        while True:
            RandomNum = random.randint(0, 10)
            try:
                askNum = int(input(f"\n{args.name}, give your bat (0–10): "))
            except ValueError:
                print("You should enter a number between 0 and 10 only.")
                continue

            if askNum < 0 or askNum > 10:
                print("You should give numbers between 0 and 10 only.")
                continue

            if RandomNum != askNum:
                print(f"You batted {askNum}, Python bowled {RandomNum}.")
                player.add_point(askNum)
                player.get_point()
                # Continue until out or reach target
                if player.point >= runs_needed:
                    print(f"\n{args.name}, You won! 🎉")
                    break
            else:
                print(f"\nYou batted {askNum} and Python bowled {RandomNum}. You are out.")
                if player.point + 1 > py.point + 0:
                    print(f"{args.name}, You won! 🎉")
                else:
                    print(f"{args.name}, You lost the match.")
                break

    # ── First Innings: Player batted first ───────────────────────────────────────
    elif playerBat:
        print("\n--- First Innings: You batting ---")
        while True:
            RandomNum = random.randint(0, 10)
            try:
                askNum = int(input(f"{args.name}, give your bat (0–10): "))
            except ValueError:
                print("You should enter a number between 0 and 10 only.")
                continue

            if askNum < 0 or askNum > 10:
                print("You should give numbers between 0 and 10 only.")
                continue

            if RandomNum != askNum:
                print(f"You batted {askNum}, Python bowled {RandomNum}.")
                player.add_point(askNum)
                player.get_point()
            else:
                runs_needed = player.total_run()
                print(f"\nYou batted {askNum} and Python bowled {RandomNum}. You are out.")
                print(f"Batting turn... Runs to make = {runs_needed}")
                break

        # Second half: Python batting the chase
        while True:
            RandomNum = random.randint(0, 10)
            try:
                askNum = int(input(f"\n{args.name}, give your bowl (0–10): "))
            except ValueError:
                print("You should enter a number between 0 and 10 only.")
                continue

            if askNum < 0 or askNum > 10:
                print("You should give numbers between 0 and 10 only.")
                continue

            if RandomNum != askNum:
                print(f"You bowled {askNum}, Python scored {RandomNum}.")
                py.add_point(RandomNum)
                py.get_point()
                if py.point >= runs_needed:
                    print("\nPython won! 🎉")
                    break
            else:
                print(f"\nYou bowled {askNum} and Python scored {RandomNum}. Python is out.")
                print(f"{args.name}, You won! 🎉")
                break

    # ── Play Again ────────────────────────────────────────────────────────────────
    def PlayAgain():
        try:
            again = int(input(f"\n{args.name}, do you want to play again?\n1 for yes\n2 for no\n"))
            if again == 1:
                print("\nOK... Restarting.\n")
                # reset scores
                py.point = 0
                player.point = 0
                game()
            elif again == 2:
                print(f"\n{args.name}, Thanks for playing. Bye!")
                sys.exit()
            else:
                print("Choose 1 or 2 only.")
                PlayAgain()
        except ValueError:
            print("Choose 1 or 2 only.")
            PlayAgain()

    PlayAgain()


if __name__ == "__main__":
    game()
