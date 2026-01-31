
nato_alphabet = [
    "Alfa", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot", "Golf", "Hotel", "India", "Juliett", "Kilo", "Lima", "Mike",
    "November", "Oscar", "Papa", "Quebec", "Romeo", "Sierra", "Tango", "Uniform", "Victor", "Whiskey", "Xray", "Yankee", "Zulu"
]

def provide(name:str)-> list[str] :
    ans = ans = [word for char in name.upper() for word in nato_alphabet if char ==word[0] ]
    return ans

name = provide("Jai")
print(name)

