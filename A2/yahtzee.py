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

# Function to print the score sheet and calculate the total score
def print_score(score_sheet):
    
    categories = score_sheet.keys()
    
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