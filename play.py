"""Wordle AI advisor

"""

__authors__ = "D. Knowles"
__date__ = "19 Jan 2022"

import os
import random

import numpy as np
from tqdm import tqdm

class WordleAI():

    def __init__(self):
        pass

    def play(self):
        """Basic console UI for playing Wordle.

        """

        # display some intro text
        self.intro()

        # choose how to get the solution word
        input_type = self.choose_input()

        self.all_words = self.get_all_words()

        if input_type == "r":
            # pick a random five letter word
            self.solution = self.random_solution()
            self.ask_to_show()
        elif input_type == "i":
            # input a solution yourself
            self.solution = self.input_solution()
            self.ask_to_show()
        elif input_type == "u":
            self.solution = ""

        victory = False
        turn_count = 0
        while not victory and turn_count < 6:

            if len(self.all_words) < 1000:
                best_candidate, candidate_scores = self.prune_advisor()
            else:
                best_candidate, candidate_scores = self.spot_advisor()

            guess = self.advise_and_guess(best_candidate, candidate_scores)

            if self.solution != "":
                victory, metrics = self.evaluate_guess(guess, self.solution, True)
            else:
                victory, metrics = self.input_evaluation()

            self.all_words = self.prune_words(self.all_words, guess, metrics)

            turn_count += 1

        self.end_game(victory, turn_count)


    def intro(self):
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
        # input("Press Enter to begin the game.")

    def choose_input(self):
        """Choose solution input type.

        Returns
        -------
        input_type : string
            options are either "r" for random word choice, "i" to input
            a specific word choice, "u" for unknown.

        """

        print("\nChoose an option for the solution word.")
        print("'r' : random word choice")
        print("'i' : input a solution word yourself")
        print("'u' : unknown (Choose this option to input")
        print("      online results (green, yellow, grey)")
        print("      to get help with wordle online)")
        input_type = input("Input letter option and then press Enter.\n")
        input_type = input_type.lower()

        while not(input_type == "r" or input_type == "i" or input_type == "u"):
            print("\nERROR, must chose valid option of 'r', 'i', or 'u'")
            input_type = input("Enter letter option and then press Enter.\n")
            input_type = input_type.lower()

        return input_type

    def get_all_words(self):
        """Read file that houses fie letter word dictionary

        Returns
        -------
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

        return all_words

    def random_solution(self):
        """Pick a random five letter word from dictionary list.

        Returns
        -------
        solution : string
            random five letter word.

        """

        # chose random word
        solution = random.choice(self.all_words)

        return solution

    def input_solution(self):
        """Input a five-letter word yourself.

        Returns
        -------
        solution : string
            chosen five letter word.

        """

        solution = input("\nInput a five letter word then press Enter.\n")
        while len(solution) != 5:
            print("\nERROR: input must be five letters.")
            solution = input("Input a five letter word then press Enter.")

        return solution

    def ask_to_show(self):
        """Shows solution if requested.

        """
        user_input = input("\nInput 'y' to show result" \
                         + " or just press Enter to continue\n")
        if user_input == "y":
            print("Solution word is : " + self.solution)

    def spot_advisor(self):
        """Give advice but letter the user enter a word.

        Returns
        -------
        best_candidate : string
            Advised word.
        candidate_scores : dict
            Dictionary of word (string) : score (float)

        """

        advice = ""
        if len(self.all_words) == 0:
            print("\nI'm out of options! You're on your own!")

        else:

            # create probabilities of each letter in each spot based on
            # the remaining words available
            spot_probabilities = np.zeros((26,5))
            for word in self.all_words:
                for spot, letter in enumerate(word):
                    spot_probabilities[ord(letter) - 97, spot] += 1
            spot_probabilities /= np.sum(spot_probabilities, axis = 0).reshape(1,-1)

            # score each word based on letter spot probabilities
            candidate_scores = {}
            for word in self.all_words:
                score = 1.0
                for spot, letter in enumerate(word):
                    score *= spot_probabilities[ord(letter) - 97, spot]
                candidate_scores[word] = score

            total_scores = float(sum(list(candidate_scores.values())))

            candidate_scores = {k : v/total_scores for k,v in candidate_scores.items()}

            candidate_list = [k for k, v in sorted(candidate_scores.items(), key=lambda x: x[1])]

            best_index = 0
            best_candidate = ""
            while best_candidate == "" or len(set(best_candidate)) != 5:
                best_index -= 1
                if abs(best_index) > len(candidate_list):
                    best_candidate = candidate_list[-1]
                    break
                best_candidate = candidate_list[best_index]

        return best_candidate, candidate_scores

    def prune_advisor(self):
        """Give advice based on maximum prune.

        Returns
        -------
        best_candidate : string
            Advised word.
        candidate_scores : dict
            Dictionary of word (string) : score (float)

        """

        advice = ""
        if len(self.all_words) == 0:
            print("\nI'm out of options! You're on your own!")
        else:
            self.branches_dict = {}
            candidate_scores = {}

            for guess_candidate in tqdm(self.all_words):
                self.branches_dict[guess_candidate] = {}
                for solution_candidate in self.all_words:
                    victory, metrics = self.evaluate_guess(guess_candidate, solution_candidate)

                    pruned_words = self.prune_words(self.all_words.copy(), guess_candidate, metrics)
                    num_pruned = len(self.all_words) - len(pruned_words)
                    self.branches_dict[guess_candidate][solution_candidate] = num_pruned

                candidate_scores[guess_candidate] = np.mean(list(self.branches_dict[guess_candidate].values()))
                # print("\n",guess_candidate, candidate_scores[guess_candidate])
            # find best candidate, i.e. the key with the largest value associated with it
            best_candidate = max(candidate_scores, key=candidate_scores.get)


        return best_candidate, candidate_scores

    def advise_and_guess(self, best_candidate, candidate_scores):
        """Print out advice and then get user's guess.

        Returns
        -------
        guess : string
            Current guess for the word.
        candidate_scores : dict
            Dictionary of word (string) : score (float)
        """

        print("\nI'd advise guessing **" + best_candidate + "**")
        random_odds = round((1./len(self.all_words))*100.,3)
        print(len(self.all_words), "possible words")
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

    def evaluate_guess(self, guess, solution, verbose = False):
        """Check victory.

        Parameters
        ----------
        guess : string
            Current guess for the word.
        solution : string
            Five letter solution word.
        verbose : bool
            Whether to print metrics

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

        if verbose:
            print(printed_metrics)

        return victory, metrics

    def input_evaluation(self):
        """Get evaluation metrics from the user
        
        Returns
        -------
        victory : bool
            True if victory was achieved
        metrics : string
            Five letter string where 'o' means letter is in correct spot,
            '-' if letter in word, but not correct spot, and 'x' if the
            letter is not in the word.
        """
        print("\nInput the evaluation you received where ")
        print("'o' means letter is in correct spot (green)")
        print("'-' if letter in word, but not correct spot (yellow)")
        print("'x' if the letter is not in the word.")
        metrics = input("Input five letter evaluation then press Enter.\n")
        while len(metrics) != 5:
            print("\nERROR: input must be five characters.")
            metrics = input("Input five letter evaluation then press Enter.\n")

        victory = metrics == "ooooo"

        return victory, metrics


    def prune_words(self, all_words, guess, metrics):
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
            pruned list of all possible five letter words

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

    def end_game(self, victory, turn_count):
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

    wordle_ai = WordleAI()
    wordle_ai.play()
