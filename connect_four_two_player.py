from itertools import cycle

#We want to create a grid.

def board_game(array):
  for row in array:
    print("| ", row[0], " | " ,row[1], " | ", row[2], " | ", row[3]," | ", row[4], " | ", row[5], " | ", row[6], " | ")
    print("-------------------------------------------")

allowed_counters = ['X', 'O']

def count_star_in_column(array, k):
  count = 0
  for i in range(len(array)):
    if array[i][k-1] == '*':
      count +=1
  return count

#Placing a counter on the board
def place_counter(array, k, counter):
  try:
    #If there are no counters in a column
    if all(array[i][k-1] == "*" for i in range(6)):
      array[5][k-1] = counter
    #If the row is full
    elif all(array[i][k-1] != '*' for i in range(len(array))):
      return False
    else:
      #Put counter on next available row
      count_stars = count_star_in_column(array, k)
      array[count_stars - 1][k-1] = counter
  except (IndexError, ValueError):
    print("This column does not exist! Please input an integer between 1 and 7.")
    return False

  return array
  
 #Checking if the board is full
def array_full(array):
    return all(cell != '*' for row in array for cell in row)

#Checking if a player has won
def player_won(array, counter):
  #Checking for win in rows ---- 
  for i in range(6):
    for j in range(4):
      if all(array[i][k] == counter for k in range(j, j+4)):
        #print(f"Horizontal win detected at row {i}, starting column {j}")
        return True
  #Checking for win in columns |
  for j in range(7):
    for i in range(3):
      if all(array[k][j] == counter for k in range(i, i+4)):
        #print(f"Vertical win detected at column {j}, starting row {i}")
        return True
  #Checking for win in upwards diagonals /
  for i in range(3, 6):
    for j in range(4):
      if all(array[i-k][j+k] == counter for k in range(0, 4)):
        #print(f"Upwards diagonal win detected starting at ({i}, {j})")
        return True
  #Checking for win in downwards diagonals \
  for i in range(3):
      for j in range(4):
        if all(array[i+k][j+k] == counter for k in range(0, 4)):
            #print(f"Downwards diagonal win detected starting at ({i}, {j})")
            return True

  return False

#Checking if the game has ended
def game_won(array):
  for counter in allowed_counters:
    if player_won(array, counter) == True:
      print("  ", 1, "   ", 2, "   ", 3, "   ", 4, "   ", 5, "   ", 6, "   ", 7, "   ")
      board_game(array)
      print("Player", counter, "has won the game! The game has ended.")
      return True
  
  return False

#Playing the game
def play_connect_4(array, counter):
    print("  ", 1, "   ", 2, "   ", 3, "   ", 4, "   ", 5, "   ", 6, "   ", 7, "   ")
    board_game(array)
    print("It is time for player", counter, "to make a move.")
    
    while True:
        try:
            k = int(input("Select a column: "))
            if 1 <= k <= 7:
                if place_counter(array, k, counter):
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

#Playing game until the game is won
while True:
    #This is the 2D list
    array = [["*"] * cols for _ in range(rows)]
    #Switching the counter between player X and player O  
    myIterator = cycle(allowed_counters)
    
    while not game_won(array) and not array_full(array):
        current_counter = next(myIterator)
        play_connect_4(array, current_counter)
    
    if array_full(array):
        print("The game is a draw!")

    # Ask if players want to restart
    print("                                     ")
    restart = input("Do you want to play again? (yes/no): ").strip().lower()
    print("                                     ")
    if restart != 'yes' and restart != 'y':
        print("Thank you for playing Connect Four!")
        break
