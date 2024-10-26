import random

def guessing_game():
    # Generate a random number between 1 and 100
    random_number = random.randint(1, 100)
    attempts = 0

    print("Welcome to the Guessing Game!")
    print("I'm thinking of a number between 1 and 100. Can you guess it?")

    while True:
        # Prompt the user to input their guess
        guess = input("Enter your guess: ")

        # Ensuring the input is a valid integer
        if not guess.isdigit():
            print("Please enter a valid number.")
            continue

        guess = int(guess)
        attempts += 1

        # Comparing the guess to the random number
        if guess < random_number:
            print("Too low! Try again.")
        elif guess > random_number:
            print("Too high! Try again.")
        else:
            # If the guess is correct, exit the loop
            print(f"Congratulations! You guessed the correct number: {random_number}")
            print(f"It took you {attempts} attempts.")
            break

guessing_game()
