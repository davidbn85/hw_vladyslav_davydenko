import random


def guess_number():
    secret_number = random.randint(1, 100)
    max_attempts = 5

    print("Welcome to the Guess the Number game!")
    print("I have chosen a number between 1 and 100.")
    print(f"You have {max_attempts} attempts to guess it.")

    for attempt in range(1, max_attempts + 1):

        guess = int(input(f"\nAttempt {attempt}: Enter your guess: "))

        if guess == secret_number:
            print("Congratulations! You guessed the right number.")
            return

        elif guess > secret_number:
            print("Too high.")

        else:
            print("Too low.")

    print(f"\nSorry, you've run out of attempts.")
    print(f"The correct number was {secret_number}.")

guess_number()