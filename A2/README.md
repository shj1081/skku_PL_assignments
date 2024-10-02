# Assignment 2 : Make a Yahtzee game using Python

> **Course:** SWE3006_42 Programming Languages \
> **Department:** System Management Engineering / Software \
> **ID / Name:** 2020310083 Hyungjun Shon (손형준)

## 1. Introduction

### What is Yahtzee?

Yahtzee is a popular multiplayer dice game where players roll five dice to achieve specific combinations in 13 rounds.
The objective is to score the highest by recording the results in various scoring categories.
Each round allows the player to roll the dice and optionally re-roll two more times, keeping some dice from the previous roll. Once the player records a score for a category, it cannot be changed.
The player continues for 13 rounds, after which the final score is calculated.

### Objective

1. Implement a simple “Single player” Yahtzee game using python
2. Implement "2-player" mode for extra credit

### Key Features to Implement

- **Roll option(10pt):** Roll the dice and display the two things(expected score and the numbers for each dice)
- **Score Sheet option(5pt):** Display the current player’s score for each category
- **Re-roll option(10pt):** Same as the Roll option
- **Record option(5pt):** Choose an unrecorded category and record the score

## 2. Code Explanation

### Game Setup and Structure

The game consists of several key components, including the dice rolling mechanism, score recording, and the game loop, which iterates through the 13 rounds. The core components of the game include:

- **Dice Rolling:** The dice rolling mechanism is central to the gameplay. The roll_dice() function simulates rolling five dice, generating random values for each die.
- **Game Rounds:** The game progresses through 13 rounds, during which players roll dice, check their expected score for each category, and record their results.
- **Score Recording:** The game maintains a score sheet that tracks the player's scores across the different categories. This score sheet is updated after each round when the player chooses to record their result in a specific category.

### Class: `YahtzeeGame`

The class serves as the primary structure for managing the game state.
It encapsulates all the key data and functions needed to play a Yahtzee game,
ensuring the data (like dice rolls, scores, players, etc.) is kept in one place and manipulated through its methods.

#### Attributes:

1. **`game_mode`**:

   - Type: `int`
   - Description: This tracks the mode of the game: whether it’s a single-player game (`1`) or a two-player game (`2`). This is crucial in deciding which player’s score to record and how the flow of the game proceeds.
   - Example: If `game_mode` is set to `2`, the logic for switching players will be triggered after each round.

2. **`current_round`**:

   - Type: `int`
   - Description: Tracks which round is being played. In Yahtzee, each game consists of 13 rounds, but this can be used to control any other game features, such as applying bonuses in later rounds.
   - Example: If `current_round == 14`, the game has ended, and the final scores are calculated. (Soon it will initialize to 1)

3. **`current_player`**:

   - Type: `int`
   - Description: This variable is used to alternate between two players in multiplayer mode. It toggles between `1` and `2` depending on who is playing.
   - Example: In a two-player mode, `current_player = 1` would mean Player 1 is taking a turn, and after their turn, it would be switched to Player 2.

4. **`dice_combination`**:

   - Type: `list`
   - Description: Holds the result of the current dice rolls (a list of five integers, each representing a dice face between 1 and 6). This is the central data for the turn, which will be used to calculate scores.
   - Example: `dice_combination = [2, 4, 4, 6, 1]` would represent the result of the dice after a roll.

5. **`recorded_score_sheet`**:
   - Type: `list`
   - Description: Stores the score sheet of each player in multiplayer mode. For a single-player game, it’s just one dictionary element in list, but for 2-player, there are 2 dictionaries in list for 2 players.
   - Example: In a two-player game, `recorded_score_sheet = [{"Aces": 5, "Twos": 4}, {"Aces": 6, "Twos": 10}]` would indicate Player 1 and Player 2's scores after a few turns.

---

### Method: `__init__`

This method initializes all the attributes of the `YahtzeeGame` class to their starting states.

- **`game_mode`** is set to 1 (single-player mode by default).
- **`current_round`** starts at 1, indicating the beginning of the game.
- **`current_player`** is set to 1, meaning Player 1 will always begin in multiplayer mode.
- **`dice_combination`** and **`recorded_score_sheet`** are initialized as empty lists since the game hasn’t started yet.

---

### Method: `roll_dices`

This method simulates rolling the dice for a turn. In Yahtzee, you can re-roll dice up to two times per round, but you may choose to keep some dice and re-roll the rest.

- **Parameters**:

  - **`kept_dices`** (type: `dict`): A dictionary where keys represent the dice positions (1 to 5), and values are the dice that the player chooses to keep. For example, if `kept_dices = {1: 5, 3: 2}`, the player is keeping the first and third dice, which have values 5 and 2 respectively.

- **Functionality**:

  - The method generates new values for any dice that are not kept by the player. It iterates over the range of dice positions (from 1 to 5), and for each dice, it either keeps its value from the `kept_dices` dictionary or rolls a new value using the `randint(1, 6)` function.
  - **Return Value**: The function returns a list of 5 integers representing the dice combination after the roll.

- **Example**:
  - Input: `kept_dices = {1: 5, 3: 2}`
  - Possible Output: `[5, 4, 2, 6, 1]` (Dice 1 and 3 are kept; dice 2, 4, and 5 are re-rolled).

---

### Method: `calculate_score`

This method computes the score for the current dice combination and returns a score sheet for that round. The score is based on the rules of Yahtzee, which includes multiple categories like Aces, Three of a Kind, Full House, etc.

- **Process**:

  1. **`total_sum`**: The total value of the dice combination is calculated using `sum(self.dice_combination)`. This is used for scoring categories like "Chance" or "Three of a Kind".

  2. **`freq`**: A list of length 6 is created, where each index (from 0 to 5) represents the frequency of dice values from 1 to 6. For example, if the dice combination is `[2, 2, 3, 4, 6]`, then `freq = [0, 2, 1, 1, 0, 1]`, meaning there are two 2’s, one 3, one 4, and one 6.

  3. **`max_freq`**: The highest frequency of any dice value. This is used to determine if there is a Three of a Kind, Four of a Kind, or Yahtzee.

  4. **`dice_set`**: A set of unique dice values, used in checking for straights (sequences). For example, if the dice combination is `[1, 2, 3, 4, 6]`, then `dice_set = {1, 2, 3, 4, 6}`.

- **Score Sheet**:
  - A dictionary is constructed where each key corresponds to a scoring category in Yahtzee. The values are calculated based on the current dice combination:
  - |    **Category**     |                    **Description**                    |      **Score**       |
    | :-----------------: | :---------------------------------------------------: | :------------------: |
    |      **Ones**       |                 Add up all 1s rolled.                 | Sum of all 1s rolled |
    |      **Twos**       |                 Add up all 2s rolled.                 | Sum of all 2s rolled |
    |     **Threes**      |                 Add up all 3s rolled.                 | Sum of all 3s rolled |
    |      **Fours**      |                 Add up all 4s rolled.                 | Sum of all 4s rolled |
    |      **Fives**      |                 Add up all 5s rolled.                 | Sum of all 5s rolled |
    |      **Sixes**      |                 Add up all 6s rolled.                 | Sum of all 6s rolled |
    | **Three of a Kind** | Three dice of the same number. Add total of all dice. |   Sum of all dice    |
    | **Four of a Kind**  | Four dice of the same number. Add total of all dice.  |   Sum of all dice    |
    |   **Full House**    |        Three of one number and two of another.        |      25 points       |
    | **Small Straight**  |         Four sequential dice (e.g., 1-2-3-4).         |      30 points       |
    | **Large Straight**  |        Five sequential dice (e.g., 1-2-3-4-5).        |      40 points       |
    |     **Yahtzee**     |                All five dice the same.                |      50 points       |
    |     **Chance**      |    Any combination of dice. Add total of all dice.    |   Sum of all dice    |

---

### Method: `is_straight`

This helper function checks whether the dice combination forms a straight (a sequence of consecutive numbers).

- **Parameters**:

  - **`dice_set`**: A set of unique dice values (since a straight is defined by unique numbers).
  - **`is_small`**: A boolean flag that determines whether to check for a Small Straight (4 consecutive numbers) or a Large Straight (5 consecutive numbers).

- **Functionality**:

  - For a Small Straight (`is_small == True`), the method checks if the dice set contains one of the following subsets: `{1, 2, 3, 4}`, `{2, 3, 4, 5}`, or `{3, 4, 5, 6}`.
  - For a Large Straight (`is_small == False`), the method checks if the dice set matches `{1, 2, 3, 4, 5}` or `{2, 3, 4, 5, 6}`.

- **Return Value**:
  - Returns `True` if the dice form a valid straight; otherwise, returns `False`.

---

### Method: `get_valid_input`

This method is responsible for ensuring that the user’s input is valid based on certain conditions.

- **Parameters**:

  - **`valid_cond`**: A list of valid inputs. If `is_numeric_list == False`, the input must match one of the elements in `valid_cond`.
  - **`error_message`**: A message to show when the user provides invalid input.
  - **`prompt`**: The prompt shown to the user when asking for input.
  - **`is_numeric_list`**: A boolean flag. If `True`, the function expects a list of numbers as input, which is used for keeping dice during rerolls.

- **Functionality**:

  - If `is_numeric_list == False`: The input is validated against a list of valid strings. The user is continuously prompted for input until they provide a valid option.
  - If `is_numeric_list == True`: The function expects a list of numbers between 1 and 5 (used to keep certain dice when rerolling). It checks if the numbers are unique, within the range, and valid.

- **Example**:
  - If the player is asked to keep dice 1 and 3, they would enter: `1 3`.
  - If invalid input is provided (like entering `7` or a duplicate dice index), the function would keep asking for correct input.

---

### Method: `print_score_table`

This method prints the current score sheet in a tabular format.

- **Parameters**:

  - **`score_sheet`**: A dictionary containing the player’s scores for different categories (e.g., Aces, Twos, Full House, etc.).

- **Functionality**:

  - The method creates a formatted table with two columns: `Category` and `Score`.
  - The categories include all possible scoring categories in Yahtzee: "Aces", "Twos", "Threes", etc.
  - The score for each category is retrieved from the `score_sheet`. If a score hasn’t been recorded yet, it will display a hyphen (`-`) instead of a score.

- **Example**:
  ```
  +----------------------+-----------+
  |       Category       |   Score   |
  +----------------------+-----------+
  | Aces                 |         5 |
  | Twos                 |         - |
  | Threes               |         9 |
  | Full House           |        25 |
  +----------------------+-----------+
  ```

---

### Method: `initialize_game`

This method is responsible for initializing all necessary game variables and preparing the game to start.

- **Functionality**:
  - The game mode (`1` for single player, `2` for two players) is reset to 1.
  - `current_round` and `current_player` are reset to 1, and `recorded_score_sheet` is reset as an empty list.
  - The method also prints a banner and prompts the player(s) to choose the game mode (either single player or two players).
  - The input is validated using the `get_valid_input` method, ensuring that the player provides valid input (either `1` or `2`).

---

### Method: `get_option_choice`

This method handles user input for deciding what action to take at the start of each round.

- **Functionality**:

  - It prints round-specific information and offers two choices to the player(s):
    - Roll the dice.
    - Check the current score sheet.
  - Input validation ensures the player selects either option `1` or `2`.

- **Example**:
  ```
  Choose the option:
  1. Roll the dice
  2. Check the current score sheet
  ```

---

### Method: `rolling_phase`

This is the phase where the dice are rolled and rerolled up to two times per round.

- **Functionality**:

  1. **Initial Roll**: The dice are rolled initially, using the `roll_dices` method with an empty dictionary (`{}`), meaning no dice are kept.
  2. **Rerolls**: The player is asked whether they want to reroll the dice, up to two times. If they want to reroll, they input which dice to keep. The rest of the dice are rerolled, and the new combination is displayed after each roll.
  3. **Kept Dice**: When rerolling, the player inputs which dice (by index) they want to keep. This input is handled by `get_valid_input` in list mode (`is_numeric_list = True`).

- **Example**:
  - Initial Roll: `[2, 4, 6, 1, 5]`
  - Player keeps dice 2 and 5, rerolls the rest.
  - New Roll: `[2, 4, 3, 4, 5]`

---

### Method: `recording_phase`

This phase handles the calculation of the score for the current round and updates the player’s score sheet.

- **Functionality**:

  - The dice combination from the rolling phase is scored using the `calculate_score` method.
  - The method filters out any categories that have already been recorded, ensuring the player cannot choose the same category more than once.
  - The score table is printed, showing only the available categories.
  - The player is prompted to choose which category to record their score for that round.
  - The chosen category is updated in the player's `recorded_score_sheet`.

- **Example**:
  ```
  +----------------------+-----------+
  |       Category       |   Score   |
  +----------------------+-----------+
  | Aces                 |         3 |
  | Twos                 |         4 |
  | Full House           |        25 |
  ```

---

### Method: `check_end_game`

This method checks if the game has reached its end (after 13 rounds in single-player mode or 26 turns in two-player mode).

- **Functionality**:
  - Once all rounds are complete (`current_round == 14`), the game prints the final scores and declares the winner (if in multiplayer mode).
  - If the game ends, the player(s) are prompted to press Enter to start a new game, which calls the `initialize_game` method again to reset everything.

---

### **Method: `print_score_info`**

This method prints the score sheet and total score for the player(s).

- **Functionality**:

  - It distinguishes between the current and final game state (if the game has finished, it prints "Final Score").
  - For a single-player game, it prints the player’s total score.
  - For a two-player game, it prints each player’s score and declares the winner based on the higher score after finishing all rounds.

- **Example Output**:

  ```
    +----------------------+-----------+
    |       Category       |   Score   |
    +----------------------+-----------+
    | Aces                 |         - |
    | Twos                 |         - |
    | Threes               |         - |
    | Fours                |         - |
    | Fives                |         5 |
    | Sixes                |         - |
    | Chance               |        25 |
    | Three of a Kind      |         - |
    | Four of a Kind       |         - |
    | Full House           |         - |
    | Small Straight       |         - |
    | Large Straight       |         - |
    | Yahtzee              |         - |
    +----------------------+-----------+

    Current score: 30
  ```

---

### Method: `play`

This is the main game loop where the game proceeds round-by-round. It coordinates the phases of each round and loops until the game ends.

- **Functionality**:
  1. **Game Initialization**: The game starts by calling `initialize_game`.
  2. **Round Phases**:
     - Players choose whether to roll dice or check the score sheet.
     - If rolling, the game proceeds through the rolling and recording phases.
     - After each round, the game checks if it should end.
  3. **Endgame**: After all rounds are complete, it prints the final scores and prompts the player to start a new game.

---

### Overall Flow:

1. **Game Initialization**: The game starts, and the player(s) choose a mode.
2. **Round Flow**:
   - For each round, the player(s) roll the dice, optionally reroll up to two times, and record their score for one category.
3. **Endgame**: After 13 rounds (single-player) or 26 turns (two-player), the game ends, and the winner is declared.

---

### Data Structures Summary:

1. **Lists**:

   - `dice_combination`: Stores the dice rolled in the current turn.
   - `freq`: Holds the frequency of each dice value from 1 to 6.
   - `small_straight_cond`: Defines the conditions needed to form a small straight.

2. **Dictionaries**:

   - `score_sheet`: Stores the score for each scoring category.
   - `kept_dices`: Used in the `roll_dices` function to track which dice the player wants to keep.

3. **Sets**: -`dice_set`: A set of unique dice values, used for checking straight conditions.
