# For random number generation
from random import randint

# Function to roll 5 dice except for the ones that are kept
def roll_dices(kept_dices):
    
    dices = [randint(1, 6) if i not in kept_dices else kept_dices[i] for i in range(1,6)]
    return dices

# Helper Function to calculate the score of a given dice combination and print the score sheet
def calculate_score(dice_combination):
    
    # Total sum of the dice combination
    total_sum = sum(dice_combination)
    
    # frequency of each dice number
    freq = [dice_combination.count(i) for i in range(1, 7)]
    max_freq = max(freq)
    
    # Set data structure for checking the consecutive numbers
    dice_set = set(dice_combination)

    # Dictionary structure for storing the score for each category ("category_name": score)
    score_sheet = {}
    
    # Upper Section
    score_sheet["Aces"] = freq[0]
    score_sheet["Twos"] = freq[1] * 2
    score_sheet["Threes"] = freq[2] * 3
    score_sheet["Fours"] = freq[3] * 4
    score_sheet["Fives"] = freq[4] * 5
    score_sheet["Sixes"] = freq[5] * 6
    
    # Lower Section
    score_sheet["Chance"] = total_sum
    score_sheet["Three of a Kind"] = total_sum if max_freq >= 3 else 0
    score_sheet["Four of a Kind"] = total_sum if max_freq >= 4 else 0
    score_sheet["Full House"] = 25 if 3 in freq and 2 in freq else 0
    score_sheet["Small Straight"] = 30 if is_straight(dice_set, True) else 0
    score_sheet["Large Straight"] = 40 if is_straight(dice_set, False) else 0
    score_sheet["Yahtzee"] = 50 if max_freq == 5 else 0
    
    return score_sheet

# Function to check the straight condition of the dice combination (Small Straight and Large Straight)
def is_straight(dice_set, is_small):
        
        # Small Straight
        if is_small:
            small_straight_cond = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
            for cond in small_straight_cond:
                if cond.issubset(dice_set):
                    return True
            return False
        
        # Large Straight
        else:
            large_straight_cond = [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]
            for cond in large_straight_cond:
                if cond.issubset(dice_set):
                    return True
            return False

# Function to choose the unrecorded category and record the score
def record_score(score_sheet):
    return

# Function to check the score sheet and print the score table
def check_score(score_sheet):
    
    # All categories (unrecorded categories also should be printed)
    categories = [
        "Aces", "Twos", "Threes", "Fours", "Fives", "Sixes", 
        "Chance", "Three of a Kind", "Four of a Kind", 
        "Full House", "Small Straight", "Large Straight", "Yahtzee"
    ]
    
    total_score = sum(score_sheet.get(category, 0) for category in categories)
    
    print("+----------------------+-----------+")
    print("|       Category       |   Score   |")
    print("+----------------------+-----------+")
    
    # Print the score for each category ('-' for unrecorded categories in final score sheet)
    for category in categories:
        score = score_sheet.get(category, "-")
        print(f"| {category:^20} | {score:^9} |")
    
    print("+----------------------+-----------+")
    
    return total_score

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

# Function for testing the calculate_score function and check_score function
def test_calculate_score():
    
    # Test case 1: Three of a Kind
    dice_combination = [3, 3, 3, 1, 5]
    result = calculate_score(dice_combination)
    total_score = check_score(result)
    print(f"Three of a Kind case")
    
    # Test case 2: Four of a Kind
    dice_combination = [2, 2, 2, 2, 6]
    result = calculate_score(dice_combination)
    total_score = check_score(result)
    print(f"Four of a Kind case")
    
    # Test case 3: Full House (e.g., two of one number and three of another)
    dice_combination = [4, 4, 6, 6, 6]
    result = calculate_score(dice_combination)
    total_score = check_score(result)
    print(f"Full House case")
    
    # Test case 4: Small Straight (e.g., four consecutive numbers)
    dice_combination = [1, 6, 3, 4, 2]
    result = calculate_score(dice_combination)
    total_score = check_score(result)
    print(f"Small Straight case")
    
    # Test case 5: Large Straight (e.g., five consecutive numbers)
    dice_combination = [6, 4, 5, 3, 2]
    result = calculate_score(dice_combination)
    total_score = check_score(result)
    print(f"Large Straight case")
    
    # Test case 6: Yahtzee (five of a kind)
    dice_combination = [5, 5, 5, 5, 5]
    result = calculate_score(dice_combination)
    total_score = check_score(result)
    print(f"Yahtzee case")
    
    # Test case 7: Chance (sum of all dice)
    dice_combination = [1, 2, 4, 5, 6]
    result = calculate_score(dice_combination)
    total_score = check_score(result)
    print(f"Chance case")

    return


test_calculate_score()