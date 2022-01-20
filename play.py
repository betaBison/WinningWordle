"""Wordle AI advisor

"""

__authors__ = "D. Knowles"
__date__ = "19 Jan 2022"

import os
import random

import numpy as np


def main():

    # display some intro text
    intro()

    # pick a random five letter word
    solution, all_words = random_solution()

    victory = False
    turn_count = 0
    while not victory and turn_count < 6:

        guess = advise_guess(all_words)

        victory, metrics = evaluate_guess(guess, solution)

        all_words = prune_words(all_words, guess, metrics)

        turn_count += 1

    end_game(victory, turn_count)



def intro():
    """Display some intro text.

    """

    print("\n\
                        _ _                 _____ \n \
                       | | |          /\   |_   _|\n \
 __      _____  _ __ __| | | ___     /  \    | |  \n \
 \ \ /\ / / _ \| '__/ _` | |/ _ \   / /\ \   | |  \n \
  \ V  V / (_) | | | (_| | |  __/  / ____ \ _| |_ \n \
   \_/\_/ \___/|_|  \__,_|_|\___| /_/    \_\_____|\n"
    )
    print("Welcome to the Wordle AI Advisor.")
    input("Press Enter to begin the game.")

def random_solution():
    """Pick a random five letter word from dictionary list.

    Returns
    -------
    solution : string
        random five letter word.
    all_words : list of strings
        list of all possible five letter words

    """

    # read in dictionary
    root_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(root_dir,"fiveletterwords.txt")
    file = open(file_path, "r")
    all_words = file.read().split("\n")

    # remove empty strings if present
    while "" in all_words : all_words.remove("")

    # chose random word
    solution = random.choice(all_words)

    return solution, all_words

def advise_guess(all_words):
    """Give advice but letter the user enter a word.

    Parameters
    ----------
    all_words : list of strings
        list of all possible five letter words

    Returns
    -------
    guess : string
        Current guess for the word.

    """

    advice = ""
    if len(all_words) == 0:
        print("\nI'm out of options! You're on your own!")

    else:

        # create probabilities of each letter in each spot based on
        # the remaining words available
        spot_probabilities = np.zeros((26,5))
        for word in all_words:
            for spot, letter in enumerate(word):
                spot_probabilities[ord(letter) - 97, spot] += 1
        spot_probabilities /= np.sum(spot_probabilities, axis = 0).reshape(1,-1)

        # score each word based on letter spot probabilities
        candidate_scores = {}
        for word in all_words:
            score = 1.0
            for spot, letter in enumerate(word):
                score *= spot_probabilities[ord(letter) - 97, spot]
            candidate_scores[word] = score

        # find best candidate, i.e. the key with the largest value associated with it
        best_candidate = max(candidate_scores, key=candidate_scores.get)

        print("\nI'd advise guessing **" + best_candidate + "**")
        random_odds = round((1./len(all_words))*100.,2)
        print("Random odds are currently " + str(random_odds) + "%")

        # get user guess
        guess = input("Enter 's' to show all possibilities \n" \
                    + "or input your guess then press Enter.\n")
        while len(guess) != 5:
            if guess == "s":
                for key, value in sorted(candidate_scores.items(), key=lambda item: item[1]):
                    print(key + " : " + str(value))

            else:
                print("ERROR: Input must be five letters.\n")

            guess = input("Input your guess then press Enter.\n")


    return guess

def evaluate_guess(guess, solution):
    """Check victory.

    Parameters
    ----------
    guess : string
        Current guess for the word.
    solution : string
        five letter word which is the wordle solution.

    Returns
    -------
    victory : bool
        True if victory was achieved
    metrics : string
        Five letter string where 'o' means letter is in correct spot,
        '-' if letter in word, but not correct spot, and 'x' if the
        letter is not in the word.

    """

    victory = guess == solution

    metrics = ""
    printed_metrics = ""
    for spot, letter in enumerate(guess):
        if letter in solution and letter == solution[spot]:
            metrics += "o"
            printed_metrics += "\u2713"
        elif letter in solution:
            metrics += "-"
            printed_metrics += "-"
        else:
            metrics += "x"
            printed_metrics += "x"

    print(printed_metrics)

    return victory, metrics

def prune_words(all_words, guess, metrics):
    """Prune impossible words.

    Parameters
    ----------
    all_words : list of strings
        list of all possible five letter words
    guess : string
        Current guess for the word.
    metrics : string
        Five letter string where 'o' means letter is in correct spot,
        '-' if letter in word, but not correct spot, and 'x' if the
        letter is not in the word.

    Returns
    -------
    all_words : list of strings
        pruned list of all remaining possible five letter words

    """

    for spot, metric in enumerate(metrics):
        if metric == "o":
            new_words = []
            for word in all_words:
                if word[spot] == guess[spot]:
                    new_words.append(word)
        elif metric == "-":
            new_words = []
            for word in all_words:
                if guess[spot] in word and word[spot] != guess[spot]:
                    new_words.append(word)
        elif metric == "x":
            new_words = []
            for word in all_words:
                if guess[spot] not in word:
                    new_words.append(word)
        all_words = new_words

    return all_words

def end_game(victory, turn_count):
    """Print goodbye text.

    Parameters
    ----------
    victory : bool
        Whether victory was achieved
    turn_count : int
        Number of turns used.

    """
    if victory:
        print("Congrats! You guessed correctly in " + str(turn_count) \
            + " turns!")
    if not victory:
        print("You're out of turns. Better luck next time!")

    print("\nThanks for playing with the Wordle AI! Goodbye.")

if __name__ == "__main__":

    main()
