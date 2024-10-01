# For random number generation
from random import randint

# Function to roll 5 dice except for the ones that are kept
def roll_dices(kept_dices):
    dices = [randint(1, 6) if i not in kept_dices else kept_dices[i] for i in range(1,6)]
    return dices

# Function to calculate the score of a given dice combination and print the score sheet
def calculate_score(dice_combination):
    return

# Function to choose the unrecorded category and record the score
def record_score(score_sheet):
    return

# Function to check the current score sheet
def check_score(score_sheet):
    return

# Function to play the game
def game_start():
    return

## Testing 
# Function for testing the roll_dices function
def test_roll_dices():
    
    # Test case 1: No dice is kept
    kept_dices = {}
    result = roll_dices(kept_dices)
    print(result)
    
    # Test case 2: Some dices are kept
    kept_dices = {1: 5, 3: 3, 5: 1}
    result = roll_dices(kept_dices)
    print(result)
    
    # Test case 3" All dices are kept
    kept_dices = {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}
    result = roll_dices(kept_dices)
    print(result)
    
    return

test_roll_dices()