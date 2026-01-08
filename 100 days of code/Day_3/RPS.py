import random

def get_player_choice():
    while True:  # Keep asking until valid input
        try:
            choice = int(input("What do you choose?\n Type 0 for Rock 👊\n Type 1 for Paper ✋\n Type 2 for Scissors ✌️\n"))
            if choice in [0, 1, 2]:
                return choice
            else:
                print("Invalid input! Please type 0, 1, or 2.\n")
        except ValueError:
            print("Please enter a number (0, 1, or 2)!\n")

def print_player_choice(choice):
    if choice == 0:
        print("You chose 👊 Rock")
    elif choice == 1:
        print("You chose ✋ Paper")
    else:
        print("You chose ✌️ Scissors")

def print_machine_choice(choice):
    if choice == 0:
        print("Machine chose 👊 Rock")
    elif choice == 1:
        print("Machine chose ✋ Paper")
    else:
        print("Machine chose ✌️ Scissors")

def play_round():
    player = get_player_choice()
    print_player_choice(player)
    
    machine = random.randint(0, 2)
    print_machine_choice(machine)
    
    # Check for draw
    if player == machine:
        print("\n🤝 It's a DRAW!!\n")
        print("🔄 Retrying... (New round!)\n")
        return play_round()  # Retry: start a completely new round
    else:
        # Determine winner
        if (player == 0 and machine == 2) or \
           (player == 1 and machine == 0) or \
           (player == 2 and machine == 1):
            print("\n🏆 YOU WIN!! 🎉")
        else:
            print("\n💻 MACHINE WINS!! 😎")

print("Welcome to Rock-Paper-Scissors!!\n")

play_round()

print("\nThanks for playing!")