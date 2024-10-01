## For random number generation
from random import randint

## Function to roll 5 dice except for the ones that are kept
def roll_dices(kept_dices):
    
    dices = [randint(1, 6) if i not in kept_dices else kept_dices[i] for i in range(1,6)]
    return dices

## Function to calculate the score of a given dice combination and print the score sheet
def calculate_score(dice_combination):
    
    # Total sum of the dice combination
    total_sum = sum(dice_combination)
    
    # frequency of each dice number
    freq = [dice_combination.count(i) for i in range(1, 7)]
    max_freq = max(freq)
    
    # Set data structure for checking the consecutive numbers
    dice_set = set(dice_combination)

    # Dictionary structure for storing the score for each category ("category_name": score)
    score_sheet = {
        "Aces": freq[0],
        "Twos": freq[1] * 2,
        "Threes": freq[2] * 3,
        "Fours": freq[3] * 4,
        "Fives": freq[4] * 5,
        "Sixes": freq[5] * 6,
        "Chance": total_sum,
        "Three of a Kind": total_sum if max_freq >= 3 else 0,
        "Four of a Kind": total_sum if max_freq >= 4 else 0,
        "Full House": 25 if 3 in freq and 2 in freq else 0,
        "Small Straight": 30 if is_straight(dice_set, True) else 0,
        "Large Straight": 40 if is_straight(dice_set, False) else 0,
        "Yahtzee": 50 if max_freq == 5 else 0,
    }
    
    return score_sheet

## Helper function to check the straight condition of the dice combination (Small Straight and Large Straight)
def is_straight(dice_set, is_small):
    small_straight_cond = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
    large_straight_cond = [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]
    if is_small:
        return any(cond.issubset(dice_set) for cond in small_straight_cond)
    return any(cond.issubset(dice_set) for cond in large_straight_cond)

## Function to print the score sheet and calculate the total score
def print_score(score_sheet):
    
    categories = [
        "Aces", "Twos", "Threes", "Fours", "Fives", "Sixes",
        "Chance", "Three of a Kind", "Four of a Kind", "Full House","Small Straight", "Large Straight", "Yahtzee"
    ]
    
    
    print("+----------------------+-----------+")
    print("|       Category       |   Score   |")
    print("+----------------------+-----------+")
    
    # Print the score for each category ('-' for unrecorded categories in final score sheet)
    for category in categories:
        score = score_sheet.get(category, "-")
        print(f"| {category:^20} | {score:^9} |")
    
    print("+----------------------+-----------+")
    
    total_score = sum(score_sheet.get(category, 0) for category in categories)
    
    return total_score

## Function to play the game
def game_start():
    
    round = 1
    recorded_score_sheet = {}
    kept_dices = {}
    
    print_game_info("welcome")
    
    while True:
        
        # Print the information of the current round and get the user input
        print_game_info("round", round)
        option = input("=> ")
        
        # Check if the input is either '1' or '2'
        while option not in ('1', '2'):
            print("\n[WARN] Invalid input. Please choose the option 1 or 2.\n")
            option = input("=> ")
        
        if (option == "1"):
            
            # Rerolling is allowed for 3 times
            for iteration in range(3):
                dices = roll_dices(kept_dices)
                while True:
                    print_game_info("roll", dices)
                    re_roll_state = input("=> ").strip().lower()

                # Check if the input is either 'y' or 'n'
                    if re_roll_state in ('y', 'n'):
                        break
                    else:
                        print("\n[WARN] Invalid input. Please type 'y' or 'n'.\n")
                        
                
                if re_roll_state == 'n':
                    break

                
                # Get the dice numbers that the user wants to keep and update the kept dices
                # Check if the input of kept dices is valid
                while True:
                    print_game_info("keep")
                    kept_dices_input = input("=> ").strip()

                    # Error case 1: Check whether input is valid numbers between 1 and 5
                    if not kept_dices_input.replace(" ", "").isdigit():
                        print("\n[WARN] Invalid input. Please enter numbers.\n")
                        continue

                    kept_dices_input = list(map(int, kept_dices_input.split()))

                    if not all(1 <= dice <= 5 for dice in kept_dices_input):
                        print("\n[WARN] Invalid input. Please enter numbers between 1 and 5.\n")
                        continue

                    # Error case 2: Check whether all numbers are unique
                    if len(kept_dices_input) != len(set(kept_dices_input)):
                        print("\n[WARN] Invalid input. Please enter different numbers.\n")
                        continue

                    break

                kept_dices = {dice: dices[dice-1] for dice in kept_dices_input}

                    
            # Calculate the score of the dice combination and choose the category to record the score
            round_score_sheet = calculate_score(dices)
            available_categories = [category for category in round_score_sheet.keys() if category not in recorded_score_sheet.keys()]
            print_score(available_categories)
            print_game_info("record")
            record_category = input("=> ")
            
            # If the user input is not valid (not in the category list or already recorded), then ask the user to input again
            while record_category not in available_categories.keys():
                print("\n[WARN] Invalid input. Please choose the category that is not recorded.\n")
                record_category = input("=> ")
            
            # Record the score of the chosen category
            recorded_score_sheet[record_category] = round_score_sheet[record_category]
            round += 1
            
            if round == 14:
                total_score = print_score(recorded_score_sheet)
                print_game_info("score", [True, total_score])
                
                # Initialize the game
                round = 1
                recorded_score_sheet = {}
                kept_dices = {}
        
            
        elif (option == "2"):
            total_score = print_score(recorded_score_sheet)
            print_game_info("score", [False, total_score])

## Helper function to print the text information of the game
def print_game_info(kind, items=None):
    
    if kind == "welcome":
        print("########################################")
        print("#                                      #")
        print("#             🎲 YAHTZEE 🎲            #")
        print("#                                      #")
        print("########################################")
        print("#                                      #")
        print("#     Roll the dice, try your luck!    #")
        print("#                                      #")
        print("########################################\n\n")
        
    elif kind == "round": # This case, items is the round number
        print(f"\n\nRound {items}")
        print("Choose the option:\n")
        print("1. Roll the dice")
        print("2. Check the current score sheet")
        return
    
    elif kind == "roll": # This case, items is the dice combination list
        print(f"Current dice combination: {items}\n")
        print("Re-roll the dice? [y/n]")
        return
    
    elif kind == "keep":
        print("Choose all the dice numbers(indices) that you want to keep. Separate the numbers by a space.")
        # print("If you want to keep all the dices, then type '0'.")
        return
    
    elif kind == "record":
        print("Choose the category that you want to record the score.")
        return
    
    elif kind == "score": # This case, items is [is_final_round, score]
        if items[0]:
            print(f"Final score: {items[1]}")
            print("Press Enter to continue...")
        else:
            print(f"\nCurrent score: {items[1]}")
                
## Start the game              
game_start()