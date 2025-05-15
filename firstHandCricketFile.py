import random
import sys
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="To create a personalised game.")
    parser.add_argument(
        "-n","--name",metavar="name",required=True,help="The name of the player who want to play the game."
    )
    args = parser.parse_args()



class points:
    def __init__(self,name,point):
        self.point = point
        point = 0
        self.name = name
    def add_point(self,run):
        self.point += run
    def get_point(self):
        print(f"{self.name} your point is {self.point}.")
    def total_run(self):
        print(self.point + 1)

py = points("Python",0)
player = points(args.name,0)

def game():
    global BatPLayer,playerBat
    BatPLayer = False
    playerBat = False
    # Getting random number from 1 to 6
    tossNum = random.randint(1,6)
    RandomNum = random.randint(0,10)

    print("Welcome to Hand Cricket.")
    toss = input(f"Toss.....Choose odd or even.\n1 for odd\n2 for even.\n{args.name} choice = ")
    toss = int(toss)

    #j Geting player choice in odd or even
    if toss < 1 or toss > 2:
        print(f"{args.name}, you should select from the given numbers only.")
    elif toss == 1:
        print(f"{args.name}, you choosed odd.\nPython choosed even")
        AskTossNum = input(f"\n{args.name} give your number. ")
        try:
            AskTossNum = int(AskTossNum)
            tossNum = tossNum + AskTossNum
            tossNum = tossNum%2
        except:
            print("you should give a number only.")

        if tossNum == 0:
            print(f"Python wins it choosed to bat.")
            BatPLayer = True
        else:
            BatBowl = input(f"Python lost. {args.name}, you won.\nChoose.....\n1 for bat\n2 for bowl.")
            BatBowl = int(BatBowl)
            if BatBowl > 2 or BatBowl<1:
                print("you should choose from the given numbers only.")
            elif BatBowl == 1:
                print("You choosed to bat.")
            else:
                print("You choosed to bowl.")
    else:
        print(f"{args.name}, you choosed even.\nPython choosed odd")
        AskTossNum = input(f"\n{args.name} give your number. ")
        try:
            AskTossNum = int(AskTossNum)
            tossNum = tossNum + AskTossNum
            tossNum = tossNum%2
        except:
            print("you should give a number only.")

        if tossNum == 0:
            print(f"Python wins it choosed to bat.")
            BatPLayer = True
        else:
            BatBowl = input(f"Python lost. {args.name}, you won.\nChoose.....\n1 for bat\n2 for bowl.")
            BatBowl = int(BatBowl)
            if BatBowl > 2 or BatBowl<1:
                print("you should choose from the given numbers only.")
            elif BatBowl == 1:
                print("You choosed to bat.")
                playerBat = True
            else:
                print("You choosed to bowl.")
                BatPLayer = True
                playerBat = False


    if BatPLayer == True:
        print("Game starts.........")
        while True:
            try:
                askNum = input(f"{args.name} give your number.")
                askNum = int(askNum)
                if askNum > 10 or askNum < 0:
                    print("You should give numbers between 0 to 10 only.")
                elif RandomNum != askNum:
                    print(f"\n{args.name} choosed {askNum}\nPython choosed {RandomNum}")
                    py.add_point(RandomNum)
                    pyMade = py.get_point
                    py.get_point()
                else:
                    print(f"\n{args.name} choosed {askNum} and Python choosed {RandomNum}\nPython is out.\nBatting turn......\nRuns to make = {py.total_run()}")
                    while True:
                        try:
                            askNum = input(f"\n{args.name} give your number.")
                            askNum = int(askNum)
                            if askNum > 10 or askNum < 0:
                                print("You should give numbers between 0 to 10 only.")
                            elif RandomNum != askNum:
                                print(f"\n{args.name} choosed {askNum}\nPython choosed {RandomNum}")
                                player.add_point(askNum)
                                runMade = player.get_point
                                player.get_point()
                            elif runMade == pyMade or runMade > pyMade:
                                print(f"{args.name}, You won!🎉")
                            else:
                                print(f"{args.name}, You losed the match.")
                                break
                        except:
                            print(f"You should enter number between 1 and 10 only.")
                            break
            except:
                print("You should enter between numbers 1 to 10 only.")   
                break



    if playerBat == True:
        print("Game starts.........")
        while True:
            try:
                askNum = input(f"{args.name} give your number.")
                askNum = int(askNum)
                if askNum > 10 or askNum < 0:
                    print("You should give numbers between 0 to 10 only.")
                elif RandomNum != askNum:
                    print(f"\n{args.name} choosed {askNum}\nPython choosed {RandomNum}")
                    player.add_point(askNum)
                    youMade = player.get_point
                    player.get_point()
                else:
                    print(f"\n{args.name} choosed {askNum} and Python choosed {RandomNum}\n{args.name} is out.\nBatting turn......\nRuns to make = {player.total_run()}")
                    while True:
                        try:
                            askNum = input(f"\n{args.name} give your number.")
                            askNum = int(askNum)
                            if askNum > 10 or askNum < 0:
                                print("You should give numbers between 0 to 10 only.")
                            elif RandomNum != askNum:
                                print(f"\n{args.name} choosed {askNum}\nPython choosed {RandomNum}")
                                py.add_point(RandomNum)
                                runMade = py.get_point
                                py.get_point()
                            elif runMade == pyMade or runMade > pyMade:
                                print(f"\n\nPython, won!🎉")
                            else:
                                print(f"\n\n{args.name}, You won!🎉")
                                break
                        except:
                            print(f"You should enter number between 1 and 10 only.")
                            break
            except:
                print("You should enter between numbers 1 to 10 only.")   
                break 


    def PlayAgain():
        try:
            again = input(f"{args.name} do you want to play again.\n1 for yes \n2 for No Thanks.")
            again = int(again)
            if again > 2 or again < 1:
                print(f"{args.name}, You should enter from 1 and 2 only.")
                PlayAgain()
            elif again == 1:
                print(f"\n\nOk....")
                game()
            elif again == 2:
                print(f"\n\n{args.name}, Thanks for playing.\nBye....")
                sys.exit()
        except:
            print(f"{args.name}, You should select from 1 and 2 only.")
game()