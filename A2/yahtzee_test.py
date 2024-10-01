## import all functions from yahtzee.py
from yahtzee import *

### Testing 
## Function for testing the roll_dices function
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

## Function for testing the calculate_score function, check_score function, and print_score function
def test_calculate_score():
    
    # Test case 1: Three of a Kind
    dice_combination = [3, 3, 3, 1, 5]
    result = calculate_score(dice_combination)
    print_game_info("score", ["round", result])
    print(f"Three of a Kind case")
    
    # Test case 2: Four of a Kind
    dice_combination = [2, 2, 2, 2, 6]
    result = calculate_score(dice_combination)
    print_game_info("score", ["round", result])
    print(f"Four of a Kind case")
    
    # Test case 3: Full House (e.g., two of one number and three of another)
    dice_combination = [4, 4, 6, 6, 6]
    result = calculate_score(dice_combination)
    print_game_info("score", ["round", result])
    print(f"Full House case")
    
    # Test case 4: Small Straight (e.g., four consecutive numbers)
    dice_combination = [1, 6, 3, 4, 2]
    result = calculate_score(dice_combination)
    print_game_info("score", ["round", result])
    print(f"Small Straight case")
    
    # Test case 5: Large Straight (e.g., five consecutive numbers)
    dice_combination = [6, 4, 5, 3, 2]
    result = calculate_score(dice_combination)
    print_game_info("score", ["round", result])
    print(f"Large Straight case")
    
    # Test case 6: Yahtzee (five of a kind)
    dice_combination = [5, 5, 5, 5, 5]
    result = calculate_score(dice_combination)
    print_game_info("score", ["round", result])
    print(f"Yahtzee case")
    
    # Test case 7: Chance (sum of all dice)
    dice_combination = [1, 2, 4, 5, 6]
    result = calculate_score(dice_combination)
    print_game_info("score", ["round", result])
    print(f"Chance case")

    return

test_calculate_score()