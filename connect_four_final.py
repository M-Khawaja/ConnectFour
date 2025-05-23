from itertools import cycle
from copy import deepcopy
import random
import time 
from textwrap import dedent


#We want to create a grid.

def board_game(array):
  for row in array:
    print("| ", row[0], " | " ,row[1], " | ", row[2], " | ", row[3]," | ", row[4], " | ", row[5], " | ", row[6], " | ")
    print("-------------------------------------------")

#This function counts the number of unfilled entries in column k
def count_star_in_column(array, k):
  count = 0
  for i in range(len(array)):
    if array[i][k-1] == '*':
      count +=1
  return count

#This function places a counter on the board in column k
def place_counter(array, k, counter, mode):
    #Renaming the counter in computer mode
    if mode == 'A':
        if counter == computer_counter:
            moving_counter = computer_counter
        else:
            moving_counter = counter
    else:
        moving_counter = counter

    try:
        #If there are no counters in a column
        if all(array[i][k-1] == "*" for i in range(6)):
            array[5][k-1] = moving_counter
        #If the row is full
        elif all(array[i][k-1] != '*' for i in range(len(array))):
            return False
        else:
            #Put counter on next available row
            count_stars = count_star_in_column(array, k)
            array[count_stars - 1][k-1] = moving_counter
    except (IndexError, ValueError):
        print("This column does not exist! Please input an integer between 1 and 7.")
        return False

    return array
  
#This function checks if the board is full
def array_full(array):
    return all(cell != '*' for row in array for cell in row)

#This function checks if a player has won
def player_won(array, counter):
  #Checking for win in rows ---- 
  for i in range(6):
    for j in range(4):
      if all(array[i][k] == counter for k in range(j, j+4)):
        return True
  #Checking for win in columns |
  for j in range(7):
    for i in range(3):
      if all(array[k][j] == counter for k in range(i, i+4)):
        return True
  #Checking for win in upwards diagonals /
  for i in range(3, 6):
    for j in range(4):
      if all(array[i-k][j+k] == counter for k in range(0, 4)):
        return True
  #Checking for win in downwards diagonals \
  for i in range(3):
      for j in range(4):
        if all(array[i+k][j+k] == counter for k in range(0, 4)):
            return True

  return False

#This function checks if the game has ended
#The checking slightly differs based on the game mode
def game_won(array):
    if mode == 'A':
        for counter in chosen_counters:
            if player_won(array, counter) == True:
                print("  ", 1, "   ", 2, "   ", 3, "   ", 4, "   ", 5, "   ", 6, "   ", 7, "   ")
                board_game(array)
                print("\nPlayer {} has won the game! The game has ended.".format(counter))
                return True
    if mode == 'B':
        for counter in allowed_counters:
            if player_won(array, counter) == True:
                print("  ", 1, "   ", 2, "   ", 3, "   ", 4, "   ", 5, "   ", 6, "   ", 7, "   ")
                board_game(array)
                print("\nPlayer {} has won the game! The game has ended.".format(counter))
                return True
  
    return False


#This function enables the computer to check for a potential win
#without altering the game array
def checking_for_win(array, k, counter):
    # Creating a shallow copy of the array (only copying rows, not deep copying everything)
    simulated_array = [row[:] for row in array]  # This avoids deep copying the whole structure
    
    if count_star_in_column(simulated_array, k) != 0:  
        place_counter(simulated_array, k, counter, mode)
        if player_won(simulated_array, counter):
            return True
    return False

#This function plays the game (vs the computer)
def play_connect_4(array, counter):
    print("  ", 1, "   ", 2, "   ", 3, "   ", 4, "   ", 5, "   ", 6, "   ", 7, "   ")
    board_game(array)
    
    if counter == computer_counter:
        print("\n")
        print("The computer is making a move.")
        time.sleep(0.5)
    else:
        print("\n")
        print("It is time for player", counter, "to make a move.")
    
    while True:
        try:
            if counter == computer_counter:
                #If the computer makes the first move in the game then it places the counter in the middle of the board.
                if len(player_moves) == 0:
                    k = random.randint(3,4)
                            
                else:
                    #Initialising k
                    k = None
                    #Looking for a potential win
                    for j in range(1,8):
                        #print("Debugging: Checking for win in column ", j)
                        if checking_for_win(array, j, counter):
                            #print(j)
                            k = j
                            break
                    
                    #Telling the computer to check if the player is close to a win
                    for j in range(1,8):
                        if checking_for_win(array, j, player_counter):
                            #Want computer to randomly choose whether to stop player winning
                            k = random.choice([j, None])
                    
                    if k is None:

                        last_player_move = player_moves[-1]
                        #First dealing the edge cases k = 1 and k = 7.
                        
                        #Suppose the last counter placed by the player was in column 1 or 7.
                        if last_player_move == 1 or last_player_move == 7:
                            #If column 1 or 7 is not full then the computer will place their counter in that column.
                            if last_player_move not in full_columns:
                                k = last_player_move
                            elif last_player_move in full_columns:
                                #If column 1 is full but column 2 is not full, then the computer will place their counter in column 2.
                                if last_player_move == 1 and 2 not in full_columns:
                                    k = 2
                                #If column 7 is full but column 6 is not full, then the computer will place their counter in column 6.
                                elif last_player_move == 7 and 6 not in full_columns:
                                    k = 6
                            else:
                                #Otherwise, the computer will place a counter in a randomly chosen unfilled column.
                                not_full_columns = [m for m in range(7) if m not in full_columns]
                                k = random.choice(not_full_columns)
                            #Dealing with the other columns
                        elif last_player_move != 1 and last_player_move != 7:
                            adjacent_unfilled_columns = [i for i in range(last_player_move - 1, last_player_move + 1) if i not in full_columns]
                            #The computer will player the counter in a randomly chose unfilled adjacent column if available.
                            if len(adjacent_unfilled_columns) > 0:
                                k = random.choice(adjacent_unfilled_columns)
                            else:
                            #Otherwise, the computer will place a counter in a randomly chosen unfilled column.
                                not_full_columns = [m for m in range(7) if m not in full_columns]
                                k = random.choice(not_full_columns)
                
                if place_counter(array, k, counter, mode):
                    #Communicating computer's move to player
                    print("\nThe computer is placing a counter in column {}.\n".format(k))
                    if count_star_in_column(array, k) == 0:
                        full_columns.append(k)

                    break
                
            #Player moves depends on player input
            else:
                k = int(input("\033[1mPlease select a column: \033[0m"))
                print("\n")
                if 1 <= k <= 7:
                    if place_counter(array, k, counter, mode):
                        if count_star_in_column(array, k) == 0:
                            full_columns.append(k)
                        #Recording the player's move in the list player_moves
                        player_moves.append(k)
                        time.sleep(0.5)           #Pause for 0.5 seconds
                        break  # Exit the loop if the counter is placed successfully
                    elif all(array[i][k-1] != '*' for i in range(len(array))):
                        print("This column is full! Please choose another column.")
                else:
                    print("Please input an integer between 1 and 7.")
        except ValueError:
            print("Please input an integer between 1 and 7.")

#This function allows us to iterate between both counters in the game
def iterate_elements(lst, start_with):
    # Find the starting index
    current_index = lst.index(start_with)
    
    # Infinite loop to yield elements indefinitely
    while True:
        yield lst[current_index]  # Yield the current element as a string
        current_index = (current_index + 1) % 2  # Move to the next element

#This function plays the two-player version of the game
def play_connect_4_two_player(array, counter):
    print("  ", 1, "   ", 2, "   ", 3, "   ", 4, "   ", 5, "   ", 6, "   ", 7, "   ")
    board_game(array)
    print("It is time for player", counter, "to make a move.")
    
    while True:
        try:
            k = int(input("Select a column: "))
            print("")
            if 1 <= k <= 7:
                if place_counter(array, k, counter, mode):
                    break  # Exit the loop if the counter is placed successfully
                elif all(array[i][k-1] != '*' for i in range(len(array))):
                    print("This column is full! Please choose another column.")
            else:
                print("Please input an integer between 1 and 7.")
        except ValueError:
            print("Please input an integer between 1 and 7.")

#There are 6 rows and 7 columns 
#in a Connect Four grid
rows, cols = (6, 7)   

if __name__ == "__main__":

    #Playing game until the game is won
    while True:
        print("\nWelcome to Connect Four.\n")

        instructions = str(input("\033[1mWould you like to see the instructions for the game? (yes/no): \033[0m")).lower()
        print("\n")
        
        while True:
            if instructions == 'yes' or instructions == 'y':
                print(dedent("""
                Instructions for the game:

                1. Each player takes their turn to drop their counter into any column in a 7 x 6 grid.

                2. The counter always falls to the lowest possible position in the column.

                3. A player wins if they align four of their counters together; either in a row, a column, or diagonally.

                4. If the grid fills up without a player winning then the game ends in a draw.
                """))
                input("\033[1mPress any key to begin the game.\033[0m\n")

                break
            else:
                break

        #The player chooses whether to play against computer or play a two-player game

        print(dedent("""
        There are two ways to play the game.
        A) Play against the computer.
        B) Play a two-player game.
        """))

        while True:
            try:
                mode = str(input("\033[1mPlease enter 'A' for Option A) or enter 'B' for Option B): \033[0m")).upper()
                print("")
                #Exit loop if correct mode is chosen.
                if mode == 'A' or mode == 'B':
                    break
            except ValueError:
                print("")

        #Playing against the computer
        if mode == 'A':

            #There are only two counters in the game
            allowed_counters = ['R', 'Y']

            chosen_counters = []
            #This is the 2D list
            array = [["*"] * cols for _ in range(rows)]
            #Asking the player to choose a counter
            while True:
                try:
                    player_counter = str(input("\033[1mPlease choose a counter out of R and Y: \033[0m"))
                    print("\n")
                    if player_counter == 'R' or player_counter == 'Y':
                        chosen_counters.append(player_counter)
                        counters_left = [counter for counter in allowed_counters if counter != player_counter]
                        computer_counter = counters_left[0]
                        chosen_counters.append(computer_counter)
                        break
                    #else:
                        #print("Invalid input.")
                except ValueError:
                    print(" ")

            #Want to track the player's moves
            #This list will contain the column numbers where the player has successfully stored a counter
            player_moves = []
            
            #Tracking the columns that become filled.
            #This list will contain the columns which are full.
            full_columns = []

            #Giving the player the opportunity to begin the game

            player_starts = str(input("\033[1mWould you like to make the first move of the game? (yes/no): \033[0m")).lower()
            print("\n")

            if player_starts == 'yes' or player_starts == 'y':
                starting_counter = player_counter
            else:
                starting_counter = computer_counter

            my_iterator = iterate_elements(chosen_counters, start_with=starting_counter)
            
            #Playing the game
            while not game_won(array) and not array_full(array):
                current_counter = next(my_iterator)
                play_connect_4(array, current_counter)
            
            if array_full(array):
                print("The game is a draw!")
                break

        #Playing two-player game
        if mode == 'B':

            allowed_counters = ['R', 'Y']

            #This is the 2D list
            array = [["*"] * cols for _ in range(rows)]
            #Switching the counter between player R and player Y
            myIterator = cycle(allowed_counters)

            
            while not game_won(array) and not array_full(array):
                current_counter = next(myIterator)
                play_connect_4_two_player(array, current_counter)
            
            if array_full(array):
                print("The game is a draw!")
                break

        # Ask if players want to restart
        print("\n")
        restart = input("\033[1mDo you want to play again? (yes/no): \033[0m").strip().lower()
        print("\n")
        if restart != 'yes' and restart != 'y':
            print("Thank you for playing Connect Four!\n")
            break
    

