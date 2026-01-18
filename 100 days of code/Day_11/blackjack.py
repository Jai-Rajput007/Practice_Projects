import random
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def random_card_provider():
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
    return random.choice(cards)

def converter(card):
    if card in ["J", "Q", "K"]:
        return 10
    if card == "A":
        return 11
    return int(card)   # changed to always return int

def calculate_hand_value(hand):
    total = sum(converter(card) for card in hand)
    aces = hand.count("A")
    
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def single_game():
    clear_screen()
    
    # Player's turn
    user_cards = [random_card_provider(), random_card_provider()]
    user_total = calculate_hand_value(user_cards)
    
    print(f"Your cards: {user_cards}")
    print(f"Current score: {user_total}")
    
    # Dealer's first card
    computer_cards = [random_card_provider()]
    print(f"Computer's first card: {computer_cards[0]}")
    
    # Player can hit multiple times
    while user_total < 21:
        another_card = input("Type 'y' to get another card, type 'n' to pass: ").lower()
        if another_card != 'y':
            break
            
        new_card = random_card_provider()
        user_cards.append(new_card)
        user_total = calculate_hand_value(user_cards)
        
        print(f"Your cards: {user_cards}")
        print(f"Current score: {user_total}")
        
        if user_total > 21:
            print("Bust! You went over 21. You lose 😢")
            return

    # Dealer's turn (only if player didn't bust)
    print("\nDealer's turn...")
    print(f"Dealer's cards: {computer_cards}")
    
    dealer_total = calculate_hand_value(computer_cards)
    
    while dealer_total < 17:
        new_card = random_card_provider()
        computer_cards.append(new_card)
        dealer_total = calculate_hand_value(computer_cards)
        print(f"Dealer draws: {new_card}")
        print(f"Dealer's cards: {computer_cards} → {dealer_total}")
    
    print(f"\nYour final hand: {user_cards} → {user_total}")
    print(f"Dealer's final hand: {computer_cards} → {dealer_total}")
    
    # Decide winner
    if dealer_total > 21:
        print("Dealer bust! You win! 🎉")
    elif user_total > dealer_total:
        print("You win! 🎉")
    elif user_total == dealer_total:
        print("It's a push (tie)! 🤝")
    else:
        print("Dealer wins 😔")

def black_jack():
    clear_screen()
    print("""
    ____    ____    ____    ____
    |2   |  |A   |  |Q   |  |T   |
    |(\/)|  | /\ |  | /\ |  | &  |
    | \/ |  | \/ |  |(__)|  |&|& |
    |   2|  |   A|  | /\Q|  | | T|    
    `----`  `----'  `----'  `----'
      
    Welcome to the Black jack Game
    """)
    
    while True:
        single_game()
        play_again = input("\nDo you want to play again? (y/n): ").lower()
        if play_again != 'y':
            print("Thanks for playing! 👋")
            break
        clear_screen()

# Start the game
black_jack()