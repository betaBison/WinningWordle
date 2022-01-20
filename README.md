# WinningWordle
Searching the English language for the best starting word for the game, [Wordle](https://www.powerlanguage.co.uk/wordle/)

## play.py

Play wordle with `python3 play.py`

Allows you to play wordle with an advisor. Words are ranked based on
the probability that each letter appears in each of the five letter
positions.

Based on that ranking, the best first word is: `cares`

## main.py
The rules are simple:
<ol>
  <li>The word must have 5 only letters</li>
  <li>The word cannot contain repeated letters</li>
</ol>

Words are ranked based on how likey each of their letters are to show up in the English language. Words are not ranked based on how likely the word itself is to appear. We're only concerned with finding the word to maximize hints out of the gate.

## Results
I found four words that tie for best Wordl starter:
<ul>
  <li>Aneto</li>
  <li>Atone</li>
  <li>Eaton</li>
  <li>Oaten</li>
</ul>

Based on the fact that Wordl generally chooses common words, I would put my money on:

### Atone
