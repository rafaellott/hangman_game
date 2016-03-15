# Hangman Challenge

## The Challenge
The assignment is to build a simple HANGMAN game that works as follows:

* Chooses a random word out of 6 words: (3dhubs, marvin, print, filament, order, layer)
* Prints the spaces for the letters of the word (eg: ​_ _ _​ _ _ for order)
* The user can try to ask for a letter and that should be shown on the puzzle (eg: asks for "r" and now it shows ​_ r _​ _ r for order)
* The user can only ask 5 letters that don't exist in the word and then it's game over
* if the user wins, congratulate him!

## How to run it
```pip install -r requirements.txt```
```python manage.py runserver```

Access ```localhost:8000``` and play it!
