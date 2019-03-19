import sys
from scipy.stats import chisquare

# https://rpg.stackexchange.com/questions/70802/how-can-i-test-whether-a-die-is-fair

dice_rolls = list(map(int, sys.argv[1:])) # throw out the program name

max_roll = 0 # our counter
n_rolls = len(dice_rolls)

# create a array whose values are the number of
# occurances of each roll
cumulative_rolls = [0] * max(dice_rolls)
for roll in dice_rolls:
	if (roll > max_roll):
		max_roll = roll
	cumulative_rolls[roll - 1] = cumulative_rolls[roll - 1] + 1

expected_occurances = float(n_rolls)/float(max_roll)

x2 = 0.0
for r in cumulative_rolls:
	x2 = x2 + (r-expected_occurances)**2/expected_occurances
print(x2)

results = chisquare(f_obs=cumulative_rolls, f_exp=expected_occurances)
print(results)
ans = round(100 - results[1]*100, 3)
print("This dice has a score of {}%. lower scores correspond to more bias".format(ans))

