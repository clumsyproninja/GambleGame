import os

def update_leaderboard(name, highest_currency):
    # Check if leaderboard file exists, if not create it
    if not os.path.isfile("leaderboard.txt"):
        with open("leaderboard.txt", "w") as leaderboard:
            leaderboard.write("")

    # Read existing scores from leaderboard file
    with open("leaderboard.txt", "r") as leaderboard:
        scores = leaderboard.readlines()
        
    # Check if the name already exists in the scores list
    name_exists = False
    for i, score in enumerate(scores):
        if name in score:
            # Update the score if the new score is higher than the existing score
            existing_currency = int(score.strip().split(",")[1])
            if highest_currency > existing_currency:
                scores[i] = f"{name},{highest_currency}\n"
            name_exists = True
            break
        
    # If the name doesn't exist in the scores list, add it
    if not name_exists and highest_currency > 0:
        scores.append(f"{name},{highest_currency}\n")

    # Sort scores by currency in descending order
    scores = sorted(scores, key=lambda x: int(x.split(",")[1]), reverse=True)

    # Keep only top 5 scores
    scores = scores[:5]

    # Write scores back to file
    with open("leaderboard.txt", "w") as leaderboard:
        leaderboard.writelines(scores)

import locale

#set the user's local currency formatting
locale.setlocale(locale.LC_ALL, '')

def display_leaderboard():
    if not os.path.isfile("leaderboard.txt"):
        print("No leaderboard at the moment. Play the game!")
        return
    with open("leaderboard.txt", "r") as leaderboard:
        scores = leaderboard.readlines()
    print("HALL OF GAMBLERS:")
    if len(scores) == 0:
        print("No rich gamblers so far. Become the first one now!")
    for i, score in enumerate(scores):
        name, highest_currency = score.strip().split(",")
        formatted_currency = locale.format_string("%d", int(highest_currency), grouping=True)
        print(f"{i+1}. {name}: {formatted_currency}")