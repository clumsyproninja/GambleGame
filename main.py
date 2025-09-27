# Made by Andeivi

import random as rand
import locale
from leaderboard import display_leaderboard
from leaderboard import update_leaderboard
from termcolor import cprint

#set the user's locale currency formatting
locale.setlocale(locale.LC_ALL, '')

# Tuple (immutable) for deductions/bonuses
DEDUCT_MESSAGES = (
  "You must've been too busy counting your money to notice you lost some.",
  "You got played like a fool. Better luck next time.",
  "You just got scammed by a fake charity organization.",
  "You just got swindled by a street magician.",
  "You just got mugged by a group of clowns.",
  "Looks like your luck just went from 100 to 0, real quick.",
  "That's what happens when you don't read the terms and conditions.",
  "My bad, my fingers slipped and grabbed more of your coins"
)
BONUS_MESSAGES = (
  "Looks like lady luck is smilin' down on ya, partner!",
  "You must have been nice to a leprechaun, because you're getting a bonus!",
  "That bonus must have been a gift from the gambling gods!",
  "Winning never felt so good, huh?",
  "Your bank account must be feeling pretty good right about now.",
  "I don't know what you're doing, but keep doing it! It's clearly working.",
  "Geeez, you're making it rain!", "yessirr, winner winner chicken dinner!"
)

#variables
currency = 50
highest_currency = 0
round_count = 0
bonus_rate = 0.01
deduction_rate = 0.01
max_bonus = 500
max_deduct = 500

#gamble function
def gamble(currency, gamble_amount, bonus_rate, deduction_rate):
  outcome = rand.choice(["win", "lose"])
  if outcome == "win":
    currency += gamble_amount
    cprint("You won!\n", "green", attrs=["underline", "bold"])
    if rand.random() < bonus_rate:
      bonus = round(currency * rand.uniform(0.25, 0.75), 2)
      bonus = round(bonus)
      format_bonus = locale.format_string("%d", int(bonus), grouping=True)
      currency += bonus
      print(rand.choice(BONUS_MESSAGES))
      cprint(f"You earned a bonus of {format_bonus} coins!\n", "green", attrs=["dark"])
    return currency
  else:
    currency -= gamble_amount
    cprint("You lost!\n", "red", attrs=["underline", "bold"])
    if rand.random() < deduction_rate:
      deduction = round(currency * rand.uniform(0.1, 0.5), 2)
      deduction = round(deduction)
      format_deduct = locale.format_string("%d", int(deduction), grouping=True)
      currency -= deduction
      print(rand.choice(DEDUCT_MESSAGES))
      cprint(f"You lost {format_deduct} coins.\n", "red", attrs=["dark"])
    return currency

#entire game
def main():
  global currency, highest_currency, round_count, bonus_rate, deduction_rate, max_bonus, max_deduct
  cprint("Welcome to Clumsy's Gambling Game!\n", "light_cyan", attrs=["bold"])
  print("Description:\n"
        "  All in or nothing! Come one, come all and test your luck!\n"
        "  You have a 50% chance of winning or losing.\n"
        "  CAUTION! You may randomly lose/gain money the more you play.\n")
  
  #display leaderboard
  display_leaderboard()
  name = input("\nPlease enter your name: ")
  
  while True:
    cprint(f"\nYou currently have {currency:,} coins.", "blue", attrs=["bold"])
    gamble_amount = input("How many coins are you willing to gamble? (50 coins min): ")
    if not gamble_amount.isdigit():
      cprint("Invalid input. Please enter a valid number.", "magenta")
      continue
    elif int(gamble_amount) < 50:
      cprint("Minimum coins to gamble with is 50. Try again.", "magenta")
      continue
    elif int(gamble_amount) > currency:
      cprint("Not so fast, Moneybags. You're betting like a maniac! (Don't bet more than what you have)", "magenta")
      continue
    else:
      gamble_amount = int(gamble_amount)
      #run gamble
      currency = gamble(currency, gamble_amount, bonus_rate, deduction_rate)
      #calculate highest currency
      if currency > highest_currency:
        highest_currency = currency
      
      #end game if user has less than 50
      if currency < 50:
        cprint("Sorry, you do not have enough coins to gamble with!", "red", attrs=["reverse"])
        round_count += 1
        break
        
      #ask to play again
      while True:
        play_again = input("Want to gamble again? (y/n): ").lower()
        if play_again == 'n':
          round_count += 1
          break
        elif play_again == 'y':
          break
        else:
          cprint("Invalid input. Please enter 'y' or 'n'.", "magenta")
      
      #break if user does not want to play again
      if play_again == 'n':
        break
      
      #add rounds and calculate bonuses and deductions
      round_count += 1
      if round_count % 5 == 0:
        bonus_rate += 0.2
        deduction_rate += 0.05
      
      #Make sure they do not exceed maximum bonuses/deductions
      if bonus_rate > max_bonus:
        bonus_rate = max_bonus
      if deduction_rate > max_deduct:
        deduction_rate = max_deduct

  #update leaderboard
  update_leaderboard(name, highest_currency)

  #final messages
  cprint(f"Thank you for playing! Your final currency is {currency:,} coins.", "blue")
  print(f"Your highest currency earned was {highest_currency:,} coins.")
  print(f"You gambled {round_count} times.\n")

  #milestones dictionary
  milestones = {
    1e15-1: "NO WAY! A quadrill-ionaire! Since you have all that money... now I know who to ambush ;)",
    1e12-1: f"Wow {name}, you've made more money than most countries' GDP! What are you gonna do, buy your own planet?",
    1e9-1: f"Looks like you're swimming in coins, {name}. Congratulations on earning more than 1 billion!",
    1e6-1: f"Wowza! Looks like you've hit the million coin mark, {name}! You're practically a coin king/queen now!",
    5e5-1: f"Congrats {name}, you reached half a million coins! Keep stacking them, champ!",
    999: "Not bad. Congrats on making it past one thousand coins!",
    0: f"Looks like you'll have to keep trying to reach those big milestones, {name}."
  }
  
  #display milestones
  for milestone, message in milestones.items():
    if highest_currency > milestone:
      cprint("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", "green")
      print("Milestone:")
      print(message)
      break

#start game
if __name__ == "__main__":
  main()