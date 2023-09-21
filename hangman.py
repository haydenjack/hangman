import random
import requests
from random_word import RandomWords
import json

r = RandomWords()

headers={
      "X-RapidAPI-Host": 'wordsapiv1.p.rapidapi.com',
      "X-RapidAPI-Key": '52096e3117mshca2a74992436bf8p1e7858jsn5b3e322c3f33'
      
    } 

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


def fetch_definition(word):
      url = "https://wordsapiv1.p.rapidapi.com/words/" + word + "/definitions"
      api_response = requests.request("GET", url, headers=headers)
      return json.loads(api_response.text)

running = True

while running:

  def word_checker():
    definition_found = False
    quiz_word = ''
    while definition_found == False:
      
      test_word = r.get_random_word()
     
      definition = fetch_definition(test_word)
      
      if 'definitions' in definition:
        if definition['definitions'] == []:
          definition_found = False
        else:
          print(definition['definitions'])
          quiz_word = test_word
          definition_found = True
          break
      else:
        definition_found = False
    
    return quiz_word


  secret_word_lower = word_checker()
  secret_word = secret_word_lower.upper()


  def guessing_game(word):
    print(hangman_art[0])
    blank_word = "-"*len(word)
    print(blank_word)
    strike = 0
    count = 0
    while strike < 7:
      user_guess = input("Guess a letter! ").upper()
      if user_guess in word and len(user_guess) == 1:
        count += 1
        for i in range(len(word)):
          if word[i] == user_guess:
            index = i
            blank_word = blank_word[:index] + user_guess + blank_word[index+1:]
        print(blank_word)
        if blank_word == word:
          print("You guessed correctly after "+ str(count) +" tries!")
          break
      elif len(user_guess) != 1 or user_guess.isdigit():
        print("Invalid guess")
      else:
        print("Letter not found")
        strike += 1
        count += 1
        print(hangman_art[strike])
        print(blank_word)
        if strike == 7:
          print("Unlucky! The word was " + secret_word)
          break

    
  guessing_game(secret_word)

  play_again = str(input("Play again? Y / N "))
  if play_again == 'N' or play_again == 'n':
    running = False