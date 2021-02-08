from myPackage.demo import linear_congruence
import re

def check_user_input(message, allowed_values, type_of_check):
    """Check user input is alligned with allowed values and type of check."""
    while True: 
        try: 
            if type_of_check=='Number': output = int(input(message))
            elif type_of_check=='Letter': output = input(message)

            if(output == allowed_values[0] or output == allowed_values[1]): return output
            else:
                print("Please input either {} or {}".format(allowed_values[0], allowed_values[1]))
        except ValueError:
            print("Please input either {} or {}".format(allowed_values[0], allowed_values[1]))

def get_comp_move(prev_player_move, throw00, throw01, throw10, throw11):
    """Return the next computer move."""
    difference = throw10 - throw00 if prev_player_move == 0 else throw11 - throw01
    return next(rand) if difference == 0 else 0 if difference > 0 else 1

def display_intermediate_result(player_move, computer_move, machine_points, player_points):
    """Display the result in the command line after a turn in the game."""
    if player_move == computer_move:
        machine_points += 1
        print("Player move: {}, Machine move: {}, machine wins this point! \nYou: {}, Machine: {} \nPLAYER: {} \nCOMPUTER: {}".format(player_move, computer_move, player_points, machine_points, "*"*player_points, "*"*machine_points))
    else: 
        player_points += 1 
        print("Player move: {}, Machine move: {}, you win this point! \nYou: {}, Machine: {} \nPLAYER: {} \nCOMPUTER: {}".format(player_move, computer_move, player_points, machine_points, "*"*player_points, "*"*machine_points))
    return machine_points, player_points

def print_final_results(machine_points, player_points, machine_wins, player_wins, game_difficulty):
    """Display the final results of the game in the command line"""
    if(machine_points>player_points):
        machine_wins += 1
    elif(machine_points<player_points):
        player_wins += 1
    print("\n{}\n{} \nFinal score: \nHuman: {} – Computer: {}".format('Computer wins!' if machine_points > player_points else 'You win!' if machine_points < player_points else 'Tie', 'Easy Game is Over!' if game_difficulty==1 else 'Hard Game is Over!', player_points, machine_points))
    return machine_wins, player_wins

def update_throw_patterns(prev_player_move, player_move, throw00, throw01, throw10, throw11):
    """Update the throw values according to the newest move"""
    throw00 += 1 if prev_player_move == 0 and player_move == 0 else 0
    throw01 += 1 if prev_player_move == 0 and player_move == 1 else 0
    throw10 += 1 if prev_player_move == 1 and player_move == 0 else 0
    throw11 += 1 if prev_player_move == 1 and player_move == 1 else 0
    prev_player_move = player_move
    return prev_player_move, throw00, throw01, throw10, throw11
    
def get_move_number():
    """Get the number of moves as input from the user and check the value is a positive integer."""
    while True:
        try:
            moves = int(input("Enter the number of moves: "))
            if(moves>0): return moves
            else: print("Please enter a positive integer")
        except ValueError:
            print("Please print a valid integer")

#begin the game and get main parameters from user
print("Welcome to Human Behaviour Prediction by Charlotte Dalenbrook")
game_difficulty = check_user_input("Choose the type of game you would like (1: Easy, 2: Difficult): ", [1, 2], "Number")
moves = get_move_number()

#initialize game variables 
rand = linear_congruence(1234)
throw10, throw00, throw11, throw01, player_wins, machine_wins = (0,0,0,0,0,0)

#start main game loop 
while True:
    print("\n********************\nStarting new game...\n********************\n")
    machine_points, player_points = (0, 0) 
    if game_difficulty == 1: 
        for turn in range(moves):
            #repeat calculating computer move, getting user move and printing results for number of moves
            computer_move = next(rand)
            player_move = check_user_input("\nRound {}. Choose your move for round {} (0 or 1): ".format(turn+1, turn+1), [0, 1], "Number")
            machine_points, player_points = display_intermediate_result(player_move, computer_move, machine_points, player_points)   
        
    if game_difficulty == 2:
        prev_player_move = next(rand)
        for turn in range(moves):
            #repeat calculating computer move, getting user move, updating player throw patterns and printing results for number of moves
            computer_move = get_comp_move(prev_player_move, throw00, throw01, throw10, throw11)
            player_move = check_user_input("\nRound {}. Choose your move for round {} (0 or 1): ".format(turn+1, turn+1), [0, 1], "Number")  
            prev_player_move, throw00, throw01, throw10, throw11 = update_throw_patterns(prev_player_move, player_move, throw00, throw01, throw10, throw11)
            machine_points, player_points = display_intermediate_result(player_move, computer_move, machine_points, player_points)

    machine_wins, player_wins = print_final_results(machine_points, player_points, machine_wins, player_wins, game_difficulty)  
    
    if 'N' == check_user_input("\nDo you want to start a new game? Yes (Y) No (N): ", ['Y', 'N'], "Letter"):
        break

#display final results of all rounds
print("\n***********************\nGame Over! \nTotal Player Wins: {} \nTotal Computer Wins: {}\n***********************\n".format(player_wins, machine_wins))
