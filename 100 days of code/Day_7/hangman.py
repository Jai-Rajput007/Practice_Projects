import random
import string


words = [
"apple", "banana", "cat", "dog", "elephant", "flower", "guitar", "house", "island", "jungle",
"kite", "lemon", "mountain", "notebook", "ocean", "pencil", "queen", "river", "sun", "tree",
"umbrella", "village", "window", "xylophone", "yellow", "zebra", "airplane", "book", "car", "door",
"egg", "fish", "garden", "hat", "ice", "juice", "key", "lamp", "moon", "night",
"orange", "paper", "question", "rain", "star", "table", "unicorn", "violet", "water", "box",
"chair", "dance", "engine", "fire", "game", "hello", "internet", "jacket", "kitchen", "light",
"music", "number", "office", "phone", "quiet", "road", "school", "time", "user", "video",
"world", "year", "zoo", "cloud", "dream", "earth", "forest", "green", "happy", "idea",
"journey", "knowledge", "love", "memory", "nature", "ocean", "peace", "quiet", "rainbow", "smile",
"travel", "universe", "victory", "wonder", "youth", "animal", "beach", "city", "desert", "energy",
"family", "friend", "gold", "heart", "image", "joy", "king", "life", "magic", "night",
"open", "people", "queen", "river", "song", "time", "voice", "wind", "yesterday", "zone",
"adventure", "beauty", "challenge", "danger", "emotion", "freedom", "growth", "history", "imagination", "journey",
"knowledge", "language", "mountain", "nature", "ocean", "passion", "question", "river", "spirit", "truth",
"universe", "vision", "wisdom", "youth", "zeal", "action", "belief", "courage", "destiny", "effort",
"future", "glory", "honor", "inspiration", "justice", "kindness", "liberty", "moment", "noble", "opportunity",
"power", "quality", "respect", "strength", "talent", "unity", "value", "wealth", "x-factor", "youthful",
"zest", "amazing", "brilliant", "creative", "delight", "excellent", "fantastic", "genius", "honest", "incredible",
"joyful", "kind", "lovely", "magnificent", "nice", "outstanding", "perfect", "quality", "radiant", "superb",
"terrific", "ultimate", "victorious", "wonderful", "xceptional", "yummy", "zesty", "awesome", "beautiful", "cool",
"dream", "epic", "fun", "great", "hero", "ideal", "legend", "master", "noble", "pure"
]

def choose_word():
    return random.choice(words).upper()


def display_hangman(tries):

    stages = [
        # 6 tries left (empty)
        """
           -----
           |   |
               |
               |
               |
               |
        =========
        """,
        # 5 tries left
        """
           -----
           |   |
           O   |
               |
               |
               |
        =========
        """,
        # 4 tries left
        """
           -----
           |   |
           O   |
           |   |
               |
               |
        =========
        """,
        # 3 tries left
        """
           -----
           |   |
           O   |
          /|   |
               |
               |
        =========
        """,
        # 2 tries left
        """
           -----
           |   |
           O   |
          /|\\  |
               |
               |
        =========
        """,
        # 1 try left
        """
           -----
           |   |
           O   |
          /|\\  |
          /    |
               |
        =========
        """,
        # 0 tries left - game over
        """
           -----
           |   |
           O   |
          /|\\  |
          / \\  |
               |
        =========
        """
    ]
    return stages[6 - tries]

def play_game():
    print("=" * 50)
    print("           WELCOME TO HANGMAN")
    print("=" * 50)

    secret_word = choose_word()
    display = ["_"] * len(secret_word)
    lives = 6
    guessed = set()

    while lives > 0 and "_" in display:
        print("\n" + display_hangman(lives))
        print("  Word:  " + " ".join(display))
        print(f"  Guessed letters: {', '.join(sorted(guessed)) or 'None'}")
        print(f"  Lives left: {lives}\n")

        guess = input("Guess a letter → ").upper().strip()

        if len(guess) != 1 or not guess.isalpha():
            print("→ Please enter exactly one letter!")
            continue

        if guess in guessed:
            print("→ You already tried that letter!")
            continue

        guessed.add(guess)

        if guess in secret_word:
            print("→ Good guess!")
            for i in range(len(secret_word)):
                if secret_word[i] == guess:
                    display[i] = guess
        else:
            print("→ Wrong!")
            lives -= 1

    # ── Game finished ──
    print("\n" + "="*50)
    print(display_hangman(lives))
    print("  The word was:", secret_word)
    print("-"*50)

    if "_" not in display:
        print("  ★ CONGRATULATIONS! YOU WON! ★")
    else:
        print("  ☠️  GAME OVER - You lost  ☠️")


if __name__ == "__main__":
    play_game()

    while input("\nPlay again? (y/n): ").strip().lower() == 'y':
        print("\n" + "-"*50 + "\n")
        play_game()