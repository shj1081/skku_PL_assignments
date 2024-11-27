from random import randint

class YahtzeeGame:
    """
    Game Variables (Initializations)
    """
    def __init__(self):
        self.game_mode = 1  # 1 for single player, 2 for two players
        self.current_round = 1  # Current round
        self.current_player = 1  # Current player (used in two players mode)
        self.dice_combination = []  # Current dice combination
        self.recorded_score_sheet = []  # Recorded score sheet for each player

    """
    Helper functions
    """
    ## Function to roll 5 dice except for the ones that are kept
    def roll_dices(self, kept_dices):
        return [kept_dices.get(i, randint(1, 6)) for i in range(1, 6)]

    ## Function to calculate the score of a given dice combination and return the score sheet
    def calculate_score(self):
        total_sum = sum(self.dice_combination)
        freq = [self.dice_combination.count(i) for i in range(1, 7)]  # Count the frequency of each number
        max_freq = max(freq)
        dice_set = set(self.dice_combination)  # Get the unique numbers set

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
            "Small Straight": 30 if self.is_straight(dice_set, True) else 0,
            "Large Straight": 40 if self.is_straight(dice_set, False) else 0,
            "Yahtzee": 50 if max_freq == 5 else 0,
        }

        return score_sheet

    ## Function to check the straight condition of the dice combination (Small Straight and Large Straight)
    def is_straight(self, dice_set, is_small):
        small_straight_cond = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
        large_straight_cond = [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]
        return any(cond.issubset(dice_set) for cond in (small_straight_cond if is_small else large_straight_cond))

    ## Function to get valid input
    def get_valid_input(self, valid_cond, error_message, prompt="=> ", is_numeric_list=False):
        # valid_cond is a list of valid input strings
        if is_numeric_list == False:
            user_input = input(f"{prompt}").strip()
            while user_input not in valid_cond:
                user_input = input(f"\n[WARN] Invalid input. {error_message}\n{prompt}").strip()
            return user_input
        
        # valid_cond is not used, is_numeric_list is True
        else:
            user_input = input(f"{prompt}").strip()
            while True:
                user_input_list = user_input.split()
                if (user_input == "") or (  # empty input is valid
                    user_input.replace(" ", "").isdigit() and  # numeric input
                    all(1 <= int(dice_index) <= 5 for dice_index in user_input_list) and  # valid dice indexes
                    len(set(user_input_list)) == len(user_input_list)  # no duplicate dice indexes
                ):
                    return user_input_list
                user_input = input(f"\n[WARN] Invalid input. {error_message}\n{prompt}").strip()

    ## Function to print the score table
    def print_score_table(self, score_sheet):
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
    def initialize_game(self):
        # Initialize the global variables
        self.game_mode = 1
        self.current_round = 1
        self.current_player = 1

        # Print the header and mode selection message
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
        user_input = self.get_valid_input(["1", "2"], "Please enter 1 for Single Player or 2 for Two Players")
        self.game_mode = int(user_input)
        self.recorded_score_sheet = [{} for num in range(self.game_mode)]
        return

    ## Function to get the player's choice for the current round
    def get_option_choice(self):
        # Print the round information and instructions depending on the game mode
        if self.game_mode == 1:  # Single Player
            print(f"\n\nRound {self.current_round}")
        else:  # Two Players
            print(f"\n\nRound {self.current_round} - Player {self.current_player}'s turn")

        print(
            "Choose the option:\n"
            "1. Roll the dice\n"
            "2. Check the current score sheet"
        )

        user_input = self.get_valid_input(["1", "2"], "Please choose the option between 1 and 2")
        return int(user_input)

    ## Function for game's rolling phase
    def rolling_phase(self):
        # Initial roll of the dice
        self.dice_combination = self.roll_dices({})
        print(f"\n\nCurrent dice combination: {self.dice_combination}")

        # Can be re-rolled up to 2 times
        for roll in range(2):
            do_re_roll = self.get_valid_input(["y", "n"], "Please type 'y' or 'n'", "Re-roll the dice? [y/n]\n=> ").lower()
            if do_re_roll == "n":
                break

            # Get the dice indexes to keep and re-roll
            kept_dice_indices = self.get_valid_input(
                [],  # not used
                "Please enter unique numbers between 1 and 5. (Just Enter to re-roll all the dice)",
                "Enter the dice indexes to keep (e.g. 1 3 5)\n=> ",
                True  # input should be a list of integers
            )
            kept_dices_dict = {int(dice_index): self.dice_combination[int(dice_index) - 1] for dice_index in kept_dice_indices}
            self.dice_combination = self.roll_dices(kept_dices_dict)
            print(f"\n\nCurrent dice combination: {self.dice_combination}")
        return

    ## Function for recording phase
    def recording_phase(self):
        # Calculate the round score of the current player
        round_score_sheet = self.calculate_score()  # score of current player
        available_categories = {category: value
                                for category, value in round_score_sheet.items()
                                if category not in self.recorded_score_sheet[self.current_player - 1]}

        # print the score sheet
        self.print_score_table(available_categories)

        # Get the valid category to record the score, and record the score in the player's score sheet
        category_to_record = self.get_valid_input(
            available_categories.keys(),
            "Please choose the category that is not recorded",
            "Choose the category to record the score\n=> "
        )
        self.recorded_score_sheet[self.current_player - 1][category_to_record] = available_categories[category_to_record]

        # update round and current player
        if self.game_mode == 1:
            self.current_round += 1
        else:
            self.current_player = 2 if self.current_player == 1 else 1
            self.current_round += 1 if self.current_player == 1 else 0
        return

    ## Function to check the end of the game
    def check_end_game(self):
        # after the player's (player 2 in 2-player mode) turn end in round 14, round becomes 14
        if self.current_round == 14:
            self.print_score_info()
            input("Press Enter to start a new game.")
            self.initialize_game()
        return

    ## Function to whole score information
    def print_score_info(self):
        # Define the state of the game (Current or Final)
        if self.current_round < 14:
            state = "Current"
        else:
            state = "Final"
            print(f"\nGame Over! Final Scores:\n")

        # Print the score sheet of the player(s) and the total score
        if self.game_mode == 1:
            self.print_score_table(self.recorded_score_sheet[0])
            print(f"\n{state} score: {sum(self.recorded_score_sheet[0].values())}")
            
        else:
            final_scores = [sum(score_sheet.values()) for score_sheet in self.recorded_score_sheet]
            for player in range(2):
                print(f"\nPlayer {player + 1}'s score:\n")
                self.print_score_table(self.recorded_score_sheet[player])
                print(f"\n{state} score: {final_scores[player]}")
                
            if (self.current_round == 14):                
                print(
                    f"\n\nPlayer {1 if final_scores[0] > final_scores[1] else 2} wins!"
                )
        return

    """
    Game start function
    """
    def play(self):
        self.initialize_game()

        while True:
            option = self.get_option_choice()

            if option == 1:
                self.rolling_phase()
                self.recording_phase()
                self.check_end_game()
            elif option == 2:
                self.print_score_info()


## Start the game
if __name__ == "__main__":
    game = YahtzeeGame()
    game.play()