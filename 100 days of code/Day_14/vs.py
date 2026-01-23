import random
import os
famous_celebs = {
    "Cristiano Ronaldo": ("Portuguese football legend, goal machine", 670_000_000),
    "Lionel Messi": ("Argentine soccer icon, World Cup winner", 500_000_000),
    "Selena Gomez": ("Singer, actress, mental health advocate", 430_000_000),
    "Kylie Jenner": ("Beauty mogul, reality TV star", 395_000_000),
    "Dwayne Johnson": ("Actor, wrestler, motivational icon", 390_000_000),
    "Ariana Grande": ("Pop superstar, vocal powerhouse", 380_000_000),
    "Kim Kardashian": ("Reality TV queen, entrepreneur", 360_000_000),
    "Beyoncé": ("Music legend, cultural icon", 320_000_000),
    "Taylor Swift": ("Singer-songwriter, global superstar", 280_000_000),
    "Justin Bieber": ("Pop singer, youth icon", 295_000_000),
    "Virat Kohli": ("Indian cricket captain, batting legend", 270_000_000),
    "Khloé Kardashian": ("Reality star, businesswoman", 220_000_000),
    "Zendaya": ("Actress, fashion icon, Euphoria star", 176_000_000),
    "Neymar Jr": ("Brazilian footballer, flair master", 220_000_000),
    "Jennifer Lopez": ("Singer, actress, J.Lo brand", 250_000_000),
    "Nicki Minaj": ("Rap queen, bold performer", 230_000_000),
    "Miley Cyrus": ("Singer, actress, reinventor", 180_000_000),
    "Tom Holland": ("Spider-Man actor, British star", 65_000_000),   # younger but massive movie following
    "Millie Bobby Brown": ("Stranger Things actress, producer", 70_000_000),
    "Chris Hemsworth": ("Thor actor, fitness star", 60_000_000)
}
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def random_celeb():
    celeb = random.choice(list(famous_celebs.keys()))
    desc, followers = famous_celebs[celeb]
    return celeb,desc,followers

def vs_game():
    game = True
    print("Welcome to higher lower game !!")
    count = 0
    while game == True:
        print(f"Your current score is : {count}")
        celeb_1,desc_1,followers_1 = random_celeb()
        celeb_2,desc_2,followers_2 = random_celeb()
        if celeb_1 == celeb_2:
            celeb_2,desc_2,followers_2 = random_celeb()
        print(f"Compare A : {celeb_1} , {desc_1} .")
        print("Vs")
        print(f"Against B : {celeb_2} , {desc_2} .")
        sol = input("Who has more followers? Type 'A' or 'B' : ")
        if sol == 'A':
            if followers_1 > followers_2:
               count += 1
               print("You are right !!")
               clear_screen()
            else :
               game = False
               clear_screen()
               print(f"You are wrong , your score : {count}")
        else :
            if followers_2 > followers_1:
               count += 1
               print("You are right !!")
               clear_screen()
            else :
               game = False
               clear_screen()
               print(f"You are wrong , your score : {count}")
           
vs_game()

