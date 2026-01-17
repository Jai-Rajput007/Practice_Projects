import os
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def bidding():
    name = input("What is you name ? ")
    bid = int(input("What is you bid ? "))
    more = input("Are there any other bidders ? \n Type 'yes' or 'no' ? ")
    return name,bid,more

def auction():
    print("Welcome to the secret auction program.")
    tries = True
    auction = {}
    while tries == True :
        name,bid,more = bidding()
        auction[name] = bid
        if more == 'yes':
            clear_screen()
            continue
        else :
            ans = max(auction,key=auction.get)
            print(f"\n{ans} have won the auction with a bid of {auction[ans]}\n")
            tries = False

if __name__ == "__main__" :
    auction()
