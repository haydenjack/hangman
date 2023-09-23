import random
import requests
import json
from wonderwords import RandomWord

r = RandomWord()

hangman_art = [
"""
┌─────    
│         
│         
│     
│
└────────
""",
"""
┌────┐    
│         
│         
│     
│
└────────
""",
"""
┌────┐    
│    ●    
│         
│  
│
└────────
""",
"""
┌────┐    
│    ●    
│    |    
│ 
│
└────────
""",
"""
┌────┐    
│    ●    
│   /|    
│ 
│
└────────
""",
"""
┌────┐    
│    ●    
│   /|\    
│ 
│
└────────
""",
"""
┌────┐    
│    ●    
│   /|\    
│   /
│
└────────
""",
"""
┌────┐    
│    ●    
│   /|\    
│   / \\
│
└────────
"""
]

#Creating a HTTPS request to fetch word definitions from Words API
headers={
      "X-RapidAPI-Host": 'wordsapiv1.p.rapidapi.com',
      "X-RapidAPI-Key": '52096e3117mshca2a74992436bf8p1e7858jsn5b3e322c3f33'
      
    } 

def fetch_definition(word):
  url = "https://wordsapiv1.p.rapidapi.com/words/" + word + "/definitions"
  api_response = requests.request("GET", url, headers=headers)
  return json.loads(api_response.text)

#Defining a function that can generate a word that has a definition and prints that definition when called
def word_checker():
  definition_found = False
  quiz_word = ''
  
  while definition_found == False:
    test_word = r.word()
    definition = fetch_definition(test_word)
      
    if 'definitions' in definition:
      if definition['definitions'] == []:
        definition_found = False
      else:
        hint = definition['definitions'][0]['definition']
        print("hint: " + hint)
        quiz_word = test_word
        definition_found = True
        break
    else:
      definition_found = False
  return quiz_word

#Defining a function that tests the users input with the hidden word
def guessing_game(word):    
  print(hangman_art[0])
  blank_word = "-"*len(word)
  print(blank_word)
  strike = 0
  count = 0
  letters = []
  outcome = ""
  hinted = False
    
  while strike < 7 and outcome != "win":
    user_guess = input("Guess a letter! ").upper()
    
    if user_guess in word and len(user_guess) == 1:
      count += 1
      for i in range(len(word)):
        if word[i] == user_guess and user_guess not in letters:
          index = i
          blank_word = blank_word[:index] + user_guess + blank_word[index+1:]
      print(blank_word)
      if blank_word == word:
        print("You guessed correctly after "+ str(count) +" tries!")
        outcome = "win"
    elif len(user_guess) == len(word):
      if user_guess == word:
        print("You guessed correctly after "+ str(count) +" tries!")
        outcome = "win"
      else:
        print("Unlucky!")
        strike += 2
        count += 1
        print(hangman_art[strike])
        print(blank_word)
        if strike == 7:
          print("Unlucky! The word was " + secret_word)
          break
    elif user_guess == "*" and user_guess not in letters:
      if score > 0:
        print(random.choice(word) + " (-1 point)")
        letters.append(user_guess)
        hinted = True
      else:
        print("Not enough points")
    elif len(user_guess) != 1 or user_guess.isdigit():
      print("Invalid guess")
    elif user_guess in letters:
      print("Already guessed!")
    else:
      print("Letter not found")
      letters.append(user_guess)
      strike += 1
      count += 1
      print(hangman_art[strike])
      print(blank_word)
      if strike == 7:
        print("Unlucky! The word was " + secret_word)
        break
    
  if outcome == "win" and hinted == False:
    return "win"
  elif outcome != "win" and hinted == True:
    return "loss"
  else:
    return "neutral"

#Welcome message when the user starts the programme
print("""
                     ~-= Welcome to Hangman! =-~
      
   ~ The aim of the game is to figure out the hidden word one letter at a time before the stickman is complete!
   ~ You will be given the words definition at the start as a hint
   ~ If you're feeling lucky, you can guess the whole word (but it will cost you X2 if you're wrong!)
   ~ You can use * to reveal a hidden letter in exchange for score points!
      """)

#Initialise game setup variables
score = 0
running = True

#Initializing the game loop
while running:

  print("Generating word...")
  secret_word_lower = word_checker()
  secret_word = secret_word_lower.upper()
  result = guessing_game(secret_word)

  if result == "win":
    score += 1
  elif result == "loss":
    score -= 1
  
  print("Score: " + str(score))

  while running == True:
    play_again = str(input("Play again? Y / N ")).upper()
    if play_again == 'N':
      running = False
    elif play_again == 'Y':
      break
    else:
      print("Invalid choice")

    