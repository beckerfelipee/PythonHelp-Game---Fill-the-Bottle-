from random import seed
from random import randint
from time import sleep

# ------------ Graphical appearance -----------

# Clear current screen to create another one (run the code at the terminal)
clear_screen = True  # If you have an error with the clear function, turn False
if clear_screen:
  from os import system, name


def clear(seconds=0.5):
  if clear_screen:
    command = 'clear'
    if name in ('nt', 'dos'):
      command = 'cls'
    sleep(seconds)
    return system(command)
  else:
    return


# Text colorization (useful for the bottle print)
ansi_color_codes = True  # Set to False if colorization doesn't work correctly


def color_text(text, color="blue"):
  if ansi_color_codes:
    blue = "\033[34m"
    reset = "\033[0m"
    if color == "blue":
      return blue + text + reset
  else:
    return text


# ------------ Game Functions -----------


# *****************************************************
# We create this function to ensure that the user's input is an integer
# preventing user input errors.
def safe_int_input(phrase):
  var = "null"
  while not var.isdigit():
    var = input(phrase)
  return int(var)


# *****************************************************
# Asks the user for three values that are important for the game
def ask_game_info():
  # The minimum quantity of liquid the bottle must have.
  min_l = safe_int_input("Minimum bottle volume: ")

  # The maximum quantity of liquid the bottle can have (capacity).
  max_l = safe_int_input("Maximum bottle volume: ")

  # The number of players playing the game.
  nr_players = safe_int_input("How many players: ")

  return min_l, max_l, nr_players


# *****************************************************
def random_fill(minimum, maximum, use_seed=0):
  # Generates and returns a random integer, in the interval [min,max].

  # seed == 0: random seed generator
  # seed != 0: specified seed generator
  # We can use a conditional statement to determine if the seed should be set.
  if use_seed != 0:
    seed(use_seed)

  r_fill = randint(minimum,
                   maximum - 1)  # to ensure the value will not start as full.
  return r_fill


# *****************************************************
def initialize_players(number):
  """
    Creates and returns an adequate data structure (you must choose the
    one that suits better your purposes) that represents players. Remember
    each player must have a name, a current number of score points (equal to
    the sum of the quantities he has already chosen), and whether it is still
    playing or has already lost.
    """

  # creating a list of players
  players = []

  # Adding Data
  for player in range(number):
    # range loops start with number 0, so we add 1 to player name.
    player_name = input(f"Name of player {player + 1}? ")
    player_data = {
        'name': player_name,
        'score': 0,
        'playing': True,
        'bonus': 0
    }

    # Adding Data to players list
    players.append(player_data)

  # return players list
  return players


# *****************************************************
# Prints a line in the standard output informing the number of the current round.
def show_round_info(nr_round=0, game_is_over=False):
  length = 15
  if game_is_over:
    print("|" + "*" * length, "Game Over!", "*" * length + "|")
    print()
  else:
    print("|" + "=" * length, "Round Number", nr_round, "=" * length + "|")


# *****************************************************
def show_bottle_info(liquid,
                     max_liquid,
                     delta_down=0.0,
                     delta_top=0.0,
                     bottle_only=False):
  current_percentage = (liquid / max_liquid) * 100

  down_fill = current_percentage - delta_down * current_percentage
  top_fill = current_percentage + delta_top * current_percentage

  down_fill = round(down_fill, 2)
  top_fill = round(top_fill, 2)

  # The minimum value of the left side of the interval is 0
  # The maximum value of the right side of the interval is 100
  # We can solve that using min and max functions
  down_fill = max(0, down_fill)  # return the max value between 0 and down_fill
  top_fill = min(100,
                 top_fill)  # return the lowest value between 100 and top_fill

  if not bottle_only:
    print(f"The bottle is between {down_fill}% and {top_fill}% full\n")

  # Print a visual representation of the bottle
  for part in range(100, 0, -10):  # bottle divided in 10 parts
    if down_fill <= part <= top_fill:
      print("|" + color_text("~~~") + "|")
    else:
      print("|   |")

  print("-----")  # bottom of the bottle
  print()  # skip one line of text


# *****************************************************
# True if the player with number nr has not yet lost the game.
# False otherwise.
def not_lost_yet(players, nr):
  return players[nr]['playing']


# *****************************************************
# Asks the user for the value of the quantity that the player number nr
# wants to add to the bottle
def ask_for_quantity(players, nr):
  quantity = safe_int_input(f"{players[nr]['name']}: how much liquid? ")
  return quantity


# *****************************************************
# Updates the accumulated score of player number nr by adding it the value of quantity
def update_player_scores(players, nr, quantity):
  players[nr]['score'] += quantity


# *****************************************************
# Updates the status of the player number nr to a looser one
def update_player_lost(players, nr):
  players[nr]['playing'] = False


# *****************************************************
# Is it the case that all the players have already lost the game?
def all_lost(players):
  # We assume that all players had lost until we check if someone is still playing
  all_players_lost = True

  for player in players:
    if player['playing']:  # If someone is still playing
      all_players_lost = False
      break  # we don't need to check others players

  return all_players_lost


# *****************************************************
# Add win bonus to the winner
def update_win_bonus(players, bonus):
  if end_game:
    for player in players:
      if player['playing']:
        player['bonus'] += bonus


# *****************************************************
# Shows the information about the outcome of the game
def show_result_info(liquid, max_liquid, players, nr_rounds):

  show_round_info(game_is_over=True)

  if all_lost(players):
    print("The game ended with no winner :(")
  else:
    print(f"The bottle is finally full. Game over!!")
    for player in players:
      if player['playing']:
        print(player['name'], "won the game in", nr_rounds, "plays")
        break  # we don't need to check others players

  # lets print the final Score
  print()
  print("FINAL SCORES:")

  # ljust() aligns the string to the left by padding it with spaces to a specified total width.
  print("NAME".ljust(20) + "SCORE".ljust(10) + "BONUS")
  for player in players:
    if player['playing']:
      print(player['name'].ljust(20) + str(player['score']).ljust(10) +
            str(player['bonus']))
    else:
      print(player['name'].ljust(20) + "Lost".ljust(10) + str(player['bonus']))

  # lets print a fully bottle.
  print()
  show_bottle_info(liquid, max_liquid, bottle_only=True)


# *****************************************************
# Want to leave program when finish?
def leave_program():
  restart_option = input(
      "\npress [Enter] to exit\n or input 'restart' to restart the game: ")
  if restart_option == "restart":
    return False
  else:
    return True


# ------------ Main Script -----------

win_bonus = 50  # The bonus to be given to the winner, if any
delta_down = 0.2  # Used to inform the user about the state of the bottle
delta_top = 0.23  # Used to inform the user about the state of the bottle

min_liquid, max_liquid, nr_players = ask_game_info()
players = initialize_players(nr_players)

# The game loop starts here, allowing the same players to participate in multiple matches.
running = True
while running:

  # Reset last match information (except names and win bonuses)
  for player in players:
    player['score'] = 0
    player['playing'] = True

  # Fill start bottle
  liquid_in_bottle = random_fill(min_liquid, max_liquid, use_seed=1)

  # End Game declaration
  end_game = liquid_in_bottle == max_liquid

  # Reset number of Rounds
  nr_rounds = 0

  # Let's play the game
  while not end_game:
    nr_rounds += 1

    # Let's play the next round
    player_turn = -1
    while player_turn < nr_players - 1 and not end_game:
      clear()  # generate a new screen (only on terminal)
      show_round_info(nr_rounds)
      print()
      show_bottle_info(liquid_in_bottle, max_liquid, delta_down, delta_top)

      player_turn += 1
      # Only players that have not yet lost, are allowed to play their turn
      if not_lost_yet(players, player_turn):
        qty = ask_for_quantity(players, player_turn)
        update_player_scores(players, player_turn, qty)
        if qty + liquid_in_bottle > max_liquid:
          update_player_lost(players, player_turn)
          print(
              "Oops! You tried to overfill the bottle! The game is over for you!\n"
          )
          sleep(
              2
          )  # give plus 2 seconds to player read the message (2.5 seconds total)
        else:
          liquid_in_bottle += qty
        # Should the game end after this turn?
        end_game = liquid_in_bottle == max_liquid or all_lost(players)

        if liquid_in_bottle == max_liquid:  # Ensure that only the winner will get the win bonus.
          for nr in range(len(players)):
            if nr != player_turn:
              update_player_lost(players, nr)

  # End Game Actions
  clear()  # generate a new screen (only on terminal)
  update_win_bonus(players, win_bonus)  # Now we account for the bonus.
  show_result_info(liquid_in_bottle, max_liquid, players, nr_rounds)

  if leave_program():
    running = False
