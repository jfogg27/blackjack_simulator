# Blackjack Simulator
A simulator to see win rates of different strategies!

A program that helps you decide the best strategy for blackjack. To test instead of spending time playing endless amounts of rounds of blackjack you can import a cvs file on how you want the program to simulate. This would save a lot of time and provide an accurate guess at the win rate of the strategy.

## Setup 
Download the main game python file (Have to have python installed) and the cvs file. Edit the cvs file to have your strategy. The top row is what the dealer is showing and the left column is what you're showing. Do not edit these. Place the CSV file in a folder along with the py file run. Now run the python file.

## Manual Test
1. Asks "Do you want to simulate type s or manual type m?:" depending of answer should simulate based on csv or let you play blackjack manual if answer not s or m then loops back to the question.
2. In both cases manual and simulate it ask how many hands to play or simulate answer should be valid integer if not loops back to question.
3. If you choose sim it should show results if manual it should put you in game. 
