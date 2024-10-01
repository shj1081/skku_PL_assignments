## For random number generation
from random import randint

## Function to roll 5 dice except for the ones that are kept
def roll_dices(kept_dices):
    return [randint(1, 6) if i not in kept_dices else kept_dices[i] for i in range(1,6)]

## Function to calculate the score of a given dice combination and print the score sheet
def calculate_score(dice_combination):
    
    total_sum = sum(dice_combination)
    freq = [dice_combination.count(i) for i in range(1, 7)] # Count the frequency of each number
    max_freq = max(freq)
    dice_set = set(dice_combination) # Get the unique numbers
    
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
    return any(cond.issubset(dice_set) for cond in (small_straight_cond if is_small else large_straight_cond))

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
        print(f"\nCurrent dice combination: {items}\n")
        return
    
    elif kind == "keep":
        print("Choose all the dice numbers(indices) that you want to keep. Separate the numbers by a space.")
        # print("If you want to keep all the dices, then type '0'.")
        return
    
    elif kind == "record":
        print("Choose the category that you want to record the score.")
        return
    
    elif kind == "score": # This case, items is [state, score_sheet]
        state, score_sheet = items
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
        
        if state == "check":
            print(f"\nCurrent score: {total_score}\n")
        elif state == "final":
            print(f"\nTotal score: {total_score}\n")
        return

## Function to play the game
def game_start():
    
    # Initialize the game
    round = 1
    recorded_score_sheet = {}
    print_game_info("welcome")
    
    # Main game loop
    while True:
        
        print_game_info("round", round)
        
        # Check the user input option and validate the input
        option = input("=> ")
        while option not in ('1', '2'):
            option = input("\n[WARN] Invalid input. Please choose the option 1 or 2.\n=> ")
        
        # option 1: Roll the dice
        if (option == "1"):
            
            # Roll the dice and print the current dice combination
            dices = roll_dices({})
            print_game_info("roll", dices)
            
            # Roll the dice up to 3 times
            for roll in range(2):
                
                # Check if the user wants to reroll the dice and validate the input
                re_roll_state = input("Re-roll the dice? [y/n]: \n=> ").strip().lower()
                while re_roll_state not in ('y', 'n'):
                    re_roll_state = input("\n[WARN] Invalid input. Please type 'y' or 'n'.\nRe-roll the dice? [y/n]: \n=> ").strip().lower()
                
                # Stop re-rolling if the user chooses 'n'
                if re_roll_state == 'n':
                    break
                
                # Get the indices of the dice that the user wants to keep and validate the input
                while True:
                    print_game_info("keep")
                    kept_dices_input = input("=> ").strip()
                    
                    # if the input is empty, then reroll all the dices
                    if kept_dices_input == "":
                        break

                    # digits only, numbers between 1-5, and all unique
                    if (kept_dices_input.replace(" ", "").isdigit() and
                        all(1 <= dice <= 5 for dice in map(int, kept_dices_input.split())) and
                        len(set(kept_dices_input.split())) == len(kept_dices_input.split())):
                        break
                    print("\n[WARN] Invalid input. Please enter unique numbers between 1 and 5. (Just Enter to re-roll all the dice)\n")

                # Update the kept dices
                kept_dices = {int(dice): dices[int(dice)-1] for dice in kept_dices_input.split()}
                
                # re-roll the dice
                dices = roll_dices(kept_dices)
                print_game_info("roll", dices)

                    
            # Calculate the score of the dice combination
            round_score_sheet = calculate_score(dices)
            available_categories = {category:value for category, value in round_score_sheet.items() if category not in recorded_score_sheet}
            print_game_info("score", ["round", available_categories])
            print_game_info("record")
            
            # Choose the category to record the score and validate the input
            record_category = input("=> ")
            while record_category not in available_categories.keys():
                record_category = input("\n[WARN] Invalid input. Please choose the category that is not recorded.\n=> ")
            
            # Record the score of the chosen category
            recorded_score_sheet[record_category] = round_score_sheet[record_category]
            round += 1
            
            # Check if the game is over
            if round == 14:
                print_game_info("score", ["final", recorded_score_sheet])
                input("Press Enter to start a new game.")
                
                # Initialize the game and start a new game
                round = 1
                recorded_score_sheet = {}
                kept_dices = {}
        
        # option 2: Check the current score sheet
        elif (option == "2"):
            print_game_info("score", ["check", recorded_score_sheet])
                
## Start the game
if __name__ == "__main__":
    game_start()