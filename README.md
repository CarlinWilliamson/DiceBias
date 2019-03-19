# DiceBias
Deep Learning to try and determine if a dice is biased or not

## How do you test dice?
To determine if a dice is biased or not we need to roll it many times and record what faces show up. Using this information we can calculate the chi-squared value of that dice.
See https://rpg.stackexchange.com/questions/70802/how-can-i-test-whether-a-die-is-fair for a much better explaination

## Rational
I have bought cheap dice of ebay and suspect they may be poorly balance/manufactured to run games of Dungeons and Dragons. Naturally I want to know which set of dice I should give to myself and which set my friends should use...
It would also be interesting to compare these to other dice from different suppliers

## Creating datasets/collecting data
To help create datasets quicker i've created find_dice.py and process_dir.py which convert images of multiple dice into many images of singular dice.

process_dir.py takes the images in a directory and runs them through find_dice.py

find_dice.py uses opencv for very crude dice detection using only brightness. It takes a single image (presumably with multiple dice) then finds singlular die and writes a smaller cropped images of them.

# Acknowlegments
Dice type classification dataset from https://www.kaggle.com/ucffool/dice-d4-d6-d8-d10-d12-d20-images

Keras code borrowed heavily from https://www.pyimagesearch.com/2018/09/10/keras-tutorial-how-to-get-started-with-keras-deep-learning-and-python/

Maths/Stats for biased dice from https://rpg.stackexchange.com/questions/70802/how-can-i-test-whether-a-die-is-fair
