'''
Finds the best starting word for Wordl according to the following criteria:
    - must be a 5 letter word
    - must contain only english letters
    - must not have repeating letters

Words are scored according to how frequently occurring each letter is in the english language
'''

# open up a list of english words
# courtesy of https://github.com/dwyl/english-words
# and: https://web.archive.org/web/20131118073324/http://www.infochimps.com/datasets/word-list-350000-simple-english-words-excel-readable
with open('words.txt') as f:
    lines = f.readlines()

# dictionary containing scores for each letter in the alphabet, based on frequency
freq = {
    'e': 26,
    't': 25,
    'a': 24,
    'o': 23,
    'i': 22,
    'n': 21,
    's': 20,
    'h': 19,
    'r': 18,
    'd': 17,
    'l': 16,
    'c': 15,
    'u': 14,
    'm': 13,
    'w': 12,
    'f': 11,
    'g': 10,
    'y': 9,
    'p': 8,
    'b': 7,
    'v': 6,
    'k': 5,
    'j': 4,
    'x': 3,
    'q': 2,
    'z': 1,
}

candidateScores = {}

# loop through each word in the english language and pick out words of length 5 with no repeating characters
for word in lines:
    candidate = word.replace('\n', '').lower() # get rid of newline token and convert to lowercase

    # check if candidate word is 5 letters long and doesn't have repeating letters
    if len(candidate) == 5 and len(set(candidate)) == len(candidate) and candidate.isalpha():
        score = sum([freq[letter] for letter in list(candidate)]) # add up frequency scores from each letter
        candidateScores[candidate] = score # save result in a Dict

# find best candidate, i.e. the key with the largest value associated with it
bestCandidate = max(candidateScores, key=candidateScores.get)

# print out the best World starter word!
print('Best Wordl starter is: ' + bestCandidate + ' with a score of ' + str(candidateScores[bestCandidate]))

# print out all candidate words sorted in order of increasing score
print({k: v for k, v in sorted(candidateScores.items(), key=lambda item: item[1])})

with open("fiveletterwords.txt", 'w') as f:
    for key in candidateScores.keys():
        f.write(key + "\n")
