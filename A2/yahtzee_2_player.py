from random import randint

## Function to roll 5 dice except for the ones that are kept
def roll_dices(kept_dices):
    return [randint(1, 6) if i not in kept_dices else kept_dices[i] for i in range(1, 6)]

## Function to calculate the score of a given dice combination and print the score sheet
def calculate_score(dice_combination):
    total_sum = sum(dice_combination)
    freq = [dice_combination.count(i) for i in range(1, 7)]  # Count the frequency of each number
    max_freq = max(freq)
    dice_set = set(dice_combination)  # Get the unique numbers
    
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
def print_game_info(kind, items=None, mode="1", player=1):
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
    
    elif kind == "mode-select":
        print("Choose the mode:\n")
        print("1. Single Player")
        print("2. Two Players")
        return

    elif kind == "round":  # This case, items is the round number and current player
        round = items
        if mode == "1":
            print(f"\n\nRound {round}")
        else:
            print(f"\n\nRound {round} - Player {player}'s turn")
        print("Choose the option:\n")
        print("1. Roll the dice")
        print("2. Check the current score sheet")
        return
    
    elif kind == "roll":  # This case, items is the dice combination list
        print(f"\nCurrent dice combination: {items}\n")
        return
    
    elif kind == "keep":
        print("Choose all the dice numbers(indices) that you want to keep. Separate the numbers by a space.")
        return
    
    elif kind == "record":
        print("Choose the category that you want to record the score.")
        return
    
    elif kind == "score":  # This case, items is [state, score_sheet, player]
        state, score_sheet = items
        categories = [
            "Aces", "Twos", "Threes", "Fours", "Fives", "Sixes",
            "Chance", "Three of a Kind", "Four of a Kind", "Full House", "Small Straight", "Large Straight", "Yahtzee"
        ]
        
        if mode == "2":
            print(f"\n<      Player {player}'s score sheet      >\n")
    
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
            if mode == "1":
                print(f"\nCurrent score: {total_score}\n")
            else:
                print(f"\nPlayer {player}'s current score: {total_score}\n")
        elif state == "final":
            print(f"\nTotal score: {total_score}\n")
            if (mode == "2"):
                return total_score
        return
    
    elif kind == "winner":
        scores = items
        if scores[0] > scores[1]:
            print(f"\nPlayer 1 wins with {scores[0]} points!")
        elif scores[1] > scores[0]:
            print(f"\nPlayer 2 wins with {scores[1]} points!")
        else:
            print("\nIt's a tie!")
        return


## Function to play the game
def game_start():
    # Choose single-player or two-player mode
    print_game_info("welcome")
    print_game_info("mode-select")
    mode = input("=> ")
    while mode not in ('1', '2'):
        mode = input("\n[WARN] Invalid input. Please choose the mode 1 or 2.\n=> ")
    
    # Initialize player variables
    player_count = 2 if mode == '2' else 1
    player_scores = [{} for _ in range(player_count)]
    
    # Initialize the game
    round = 1
    current_player = 1
    
    # Main game loop
    while True:
        print_game_info("round", round, mode, current_player)
        
        # Check the user input option and validate the input
        option = input("=> ")
        while option not in ('1', '2'):
            option = input("\n[WARN] Invalid input. Please choose the option 1 or 2.\n=> ")
        
        # option 1: Roll the dice
        if option == "1":
            # Roll the dice and print the current dice combination
            dices = roll_dices({})
            print_game_info("roll", dices)
            
            # Roll the dice up to 3 times
            for roll in range(2):
                re_roll_state = input("Re-roll the dice? [y/n]: \n=> ").strip().lower()
                while re_roll_state not in ('y', 'n'):
                    re_roll_state = input("\n[WARN] Invalid input. Please type 'y' or 'n'.\nRe-roll the dice? [y/n]: \n=> ").strip().lower()
                
                if re_roll_state == 'n':
                    break
                
                while True:
                    print_game_info("keep")
                    kept_dices_input = input("=> ").strip()
                    
                    if kept_dices_input == "":
                        break
                    
                    if (kept_dices_input.replace(" ", "").isdigit() and
                        all(1 <= dice <= 5 for dice in map(int, kept_dices_input.split())) and
                        len(set(kept_dices_input.split())) == len(kept_dices_input.split())):
                        break
                    print("\n[WARN] Invalid input. Please enter unique numbers between 1 and 5. (Just Enter to re-roll all the dice)\n")

                kept_dices = {int(dice): dices[int(dice)-1] for dice in kept_dices_input.split()}
                dices = roll_dices(kept_dices)
                print_game_info("roll", dices)

            # Calculate the score of the dice combination
            round_score_sheet = calculate_score(dices)
            recorded_score_sheet = player_scores[current_player - 1]
            available_categories = {category: value for category, value in round_score_sheet.items() if category not in recorded_score_sheet}
            
            print_game_info("score", ["round", available_categories])
            print_game_info("record")
            
            record_category = input("=> ")
            while record_category not in available_categories.keys():
                record_category = input("\n[WARN] Invalid input. Please choose the category that is not recorded.\n=> ")
            
            # Record the score of the chosen category
            recorded_score_sheet[record_category] = round_score_sheet[record_category]
            player_scores[current_player - 1] = recorded_score_sheet
            
            # Switch player in two-player mode and increment the round based on the current player
            if mode == '2':
                current_player = 1 if current_player == 2 else 2
                round += 1 if current_player == 1 else 0
            else:
                round += 1
            
            # Check if the game is over
            if round == 14:
                print(f"\nGame Over! Final Scores:\n")
                final_scores = []
                for player, score_sheet in enumerate(player_scores, 1):
                    final_scores.append(print_game_info("score", ["final", score_sheet], mode, player))
                
                # Announce the winner
                print_game_info("winner", final_scores)
                
                input("Press Enter to start a new game.")
                round = 1
                player_scores = [{} for _ in range(player_count)]
                current_player = 1
        
        # option 2: Check the current score sheet
        elif option == "2":
            if mode == '1':
                print_game_info("score", ["check", player_scores[0]])
            else:
                print_game_info("score", ["check", player_scores[0]], mode, 1)
                print_game_info("score", ["check", player_scores[1]], mode, 2)

## Start the game
if __name__ == "__main__":
    game_start()
