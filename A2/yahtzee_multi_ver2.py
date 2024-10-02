from random import randint

"""
Global variables
"""
game_mode = 1  # 1 for single player, 2 for two players
round = 1 # Current round
current_player = 1 # Current player (used in two players mode)
dice_combination = [] # Current dice combination
recorded_score_sheet = [] # Recorded score sheet for each player

"""
Helper functions
"""
## Function to roll 5 dice except for the ones that are kept
def roll_dices(kept_dices):
    return [randint(1, 6) if i not in kept_dices else kept_dices[i] for i in range(1, 6)]

## Function to calculate the score of a given dice combination and return the score sheet
def calculate_score(dice_combination):
    total_sum = sum(dice_combination)
    freq = [dice_combination.count(i) for i in range(1, 7)]  # Count the frequency of each number
    max_freq = max(freq)
    dice_set = set(dice_combination)  # Get the unique numbers set
    
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

## Function to check the straight condition of the dice combination (Small Straight and Large Straight)
def is_straight(dice_set, is_small):
    small_straight_cond = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
    large_straight_cond = [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]
    return any(cond.issubset(dice_set) for cond in (small_straight_cond if is_small else large_straight_cond))

## Function to get valid input
def get_valid_input(valid_cond, error_message, prompt="=> ", is_numeric_list=False):
    
    if is_numeric_list == False: # valid_cond is a list of valid input strings
        user_input = input(f"{prompt}").strip()
        while user_input not in valid_cond:
            user_input = input(f"\n[WARN] Invalid input. {error_message}\n{prompt}").strip()
        return user_input
    else: # valid_cond is not used, is_numeric_list is True
        user_input = input(f"{prompt}").strip()
        while True:
            user_input_list = user_input.split()
            if (user_input == "") or ( # empty input is valid
                user_input.replace(" ", "").isdigit() and # numeric input
                all(1 <= int(dice_index) <= 5 for dice_index in user_input_list) and # valid dice indexes
                len(set(user_input_list)) == len(user_input_list) # no duplicate dice indexes
            ):
                return user_input_list
            user_input = input(f"\n[WARN] Invalid input. {error_message}\n{prompt}").strip()
            
## Function to print the score table
def print_score_table(score_sheet):
    
    all_categories = [
        "Aces", "Twos", "Threes", "Fours", "Fives", "Sixes",
        "Chance", "Three of a Kind", "Four of a Kind", "Full House", "Small Straight", "Large Straight", "Yahtzee"
    ]
        
    # Print the score sheet in a tabular format
    print(
        "+----------------------+-----------+\n"
        "|       Category       |   Score   |\n"
        "+----------------------+-----------+"
    )
    for category in all_categories:
        score = score_sheet.get(category, "-")
        print(f"| {category:<20} | {score:>9} |")
    print("+----------------------+-----------+")  
    return
    
"""
Game Phases functions
"""
## Function to initialize the game
def initialize_game():
    
    # Initialize the global variables
    global game_mode, round, current_player, dice_combination, recorded_score_sheet
    game_mode = 1
    round = 1
    current_player = 1
    
    # Print the header and mode selectinon message 
    print(
        "\n\n+-------------------------------------+\n"
        "|                                     |\n"
        "|            🎲 YAHTZEE 🎲            |\n"
        "|                                     |\n"
        "+-------------------------------------+\n"
        "|                                     |\n"
        "|     Roll the dice, try your luck!   |\n"
        "|                                     |\n"
        "+-------------------------------------+\n"
        "\n\nChoose the game mode:\n"
        "1. Single Player\n"
        "2. Two Players"
    )
    
    # Get the game mode from the user and validate the input. Is valid, set the game_mode
    user_input = get_valid_input(["1", "2"], "Please enter 1 for Single Player or 2 for Two Players")
    game_mode = int(user_input)
    recorded_score_sheet = [{} for num in range(game_mode)]
    return
    
## Functinon to get the player's choice for the current round
def get_option_choice():
    
    global game_mode, round, current_player, dice_combination, recorded_score_sheet
    
    # Print the round information and instructions depending on the game mode
    if game_mode == 1: # Single Player
        print(f"\n\nRound {round}")
    else: # Two Players
        print(f"\n\nRound {round} - Player {current_player}'s turn")
    
    print(
        "Choose the option:\n"
        "1. Roll the dice\n"
        "2. Check the current score sheet"
    )
        
    user_input = get_valid_input(["1", "2"], "Please choose the option between 1 and 2")
    return int(user_input)

    
## Function for game's rolling phase
def rolling_phase():
    global game_mode, round, current_player, dice_combination, recorded_score_sheet
    
    # Initial roll of the dice
    dice_combination = roll_dices({})
    print(f"\n\nCurrent dice combination: {dice_combination}")
    
    # Can be re-rolled up to 2 times
    for roll in range(2):
        do_re_roll = get_valid_input(["y", "n"], "Please type 'y' or 'n'", "Re-roll the dice? [y/n]\n=> ").lower()
        if do_re_roll == "n":
            break
        
        # Get the dice indexes to keep and re-roll
        kept_dice_indices = get_valid_input(
                                [], # not used
                                "Please enter unique numbers between 1 and 5. (Just Enter to re-roll all the dice)", 
                                "Enter the dice indexes to keep (e.g. 1 3 5)\n=> ", 
                                True # input should be a list of integers
                            )
        kept_dices_dict = {int(dice_index): dice_combination[int(dice_index) - 1] for dice_index in kept_dice_indices}
        dice_combination = roll_dices(kept_dices_dict)
        print(f"\n\nCurrent dice combination: {dice_combination}")
    return

## Function for recording phase
def recording_phase():
    global game_mode, round, current_player, dice_combination, recorded_score_sheet
    
    # Calculate the round score of the current player
    round_score_sheet = calculate_score(dice_combination) # score of current player
    available_categories = {category: value 
                            for category, value in round_score_sheet.items()
                            if category not in recorded_score_sheet[current_player - 1]
                           }
    
    # print the score sheet
    print_score_table(available_categories)
        
    # Get the valid category to record the score, and record the score in the player's score sheet
    category_to_record = get_valid_input(
                            available_categories.keys(),
                            "Please choose the category that is not recorded",
                            "Choose the category to record the score\n=> "
                         )
    recorded_score_sheet[current_player - 1][category_to_record] = available_categories[category_to_record]
    
    # update round and current player
    if game_mode == 1:
        round += 1
    else:
        current_player = 2 if current_player == 1 else 1
        round += 1 if current_player == 1 else 0
    return

## Function to check the end of the game
def check_end_game():
    global game_mode, round, current_player, dice_combination, recorded_score_sheet
    
    if round == 14:
        print_score_info()
        input("Press Enter to start a new game.")
        initialize_game()
    return

## Function to whole score information
def print_score_info():
    global game_mode, round, current_player, dice_combination, recorded_score_sheet
    
    if round < 14:
        state = "Current"
    else:
        state = "Final"
        print(f"\nGame Over! Final Scores:\n")
    
    if game_mode == 1:
        print_score_table(recorded_score_sheet[0])
        print (f"\n{state} score: {sum(recorded_score_sheet[0].values())}")
    else:
        final_scores = [sum(score_sheet.values()) for score_sheet in recorded_score_sheet]
        for player in range(2):
            print(f"\nPlayer {player + 1}'s score:\n")
            print_score_table(recorded_score_sheet[player])
            print(f"\n{state} score: {final_scores[player]}")
        print(
            f"\n\nPlayer {1 if final_scores[0] > final_scores[1] else 2} wins!"
        )
    return

"""
Game start function
"""
def yahtzee():
    global game_mode, round, current_player, dice_combination, recorded_score_sheet
    
    initialize_game()

    while True:
        option = get_option_choice()
        
        if option == 1:
            rolling_phase()
            recording_phase()
            check_end_game()
        elif option == 2:
            print_score_info()

 ## Start the game
if __name__ == "__main__":
    yahtzee()   