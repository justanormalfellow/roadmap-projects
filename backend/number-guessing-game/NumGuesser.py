import argparse
import random


def intro():
    print("Welcome to Random Number Guesser V 1.2.3!")
    print("Where you try to guess a number between 1 and 100.")


def difficulty_set(difficulty):
    if difficulty == "easy":
        return 10
    elif difficulty == "medium":
        return 3
    elif difficulty == "hard":
        return 1


def gameLoop(difficulty):
    intro()

    chances = difficulty_set(difficulty)
    number = random.randint(1, 100)
    attempts = 0

    if chances != 10:
        while chances > 0:
            print("Guess a number between 1 and 100.")
            guess = int(input("> "))
            attempts += 1

            if guess != number:
                chances -= 1
                if guess > number:
                    print("Lower!")
                else:
                    print("Higher!")
            else:
                print(f"Correct! The number was {number}")
                print(f"You guessed it in {attempts} attempts.")
                return

    else:
        while True:
            print("Guess a number between 1 and 100.")
            guess = int(input("> "))
            attempts += 1

            if guess != number:
                if guess > number:
                    print("Lower!")
                else:
                    print("Higher!")
            else:
                print(f"Correct! The number was {number}")
                print(f"You guessed it in {attempts} attempts.")
                return

    print(f"Tough luck!\nThe number was {number}")


def main():
    parser = argparse.ArgumentParser(
        description="CLI Number Guessing Game"
    )

    parser.add_argument(
        "-d",
        "--difficulty",
        choices=["easy", "medium", "hard"],
        required=True,
        help="Choose the difficulty level."
    )

    args = parser.parse_args()

    gameLoop(args.difficulty)


if __name__ == "__main__":
    main()
