# Automatic recipe generator!!!
# Prepare for a delicious feast.
#
# @author: Mike Gloudemans
# Date:   12/23/2014
#

import os
import random
import time
import pickle

# If preloaded is true, the chef imports a pre-learned Markov model using locally stored
# pickle files. Otherwise, the chef learns a new Markov model from the HTML files stored in the specified directory.
#
# Recipes must be stored locally in the specified directory for this to work when preloaded == False.
# I downloaded the recipes for the current version from allrecipes.com using wget.


preloaded = True


# List of possible messages at the beginning
start_messages = ["Some people tell me that some of my recipes are delicious.",
                  "23% of my recipes are delicious 100% of the time!",
                  "Critics have acclaimed my recipes as \"very interesting\". ",
                  "I've been cooking since I was just 3 hours old.",
                  "I'll put a new spin on your favorite recipes!",
                  "My cooking style brings together an eclectic variety of world cuisine.",
                  "My recipes will combine all the best elements of your long-time favorites.",
                  "My recipes are so tasty, they're illegal in the state of California."]

# List of possible messages at the very end
end_messages = ["Bon appetit! (That means \"it's yummy!\" in French).",
                "That's about it. Careful not to set any hot pads on fire :)",
                "Finally, just eat it!",
                "There you go. Time for a taste test!",
                "(You might want to have your brother test this recipe out first.)",
                "Ta-da! Enjoy!",
                "Serving suggestion: Goes well with Soylent (R)",
                "WARNING! Do not consume this recipe if you are pregnant.",
                "WARNING! Do not consume this recipe if you are easily nauseated.",
                "Note: Cheffrey (TM) is not responsible for any unknown side effects that occur while consuming this dish.",
                "Attention! If you or someone you know has become ill after consuming this recipe, you may be eligible for monetary compensation! Contact Mike Brown at 1-800-FOODILLNESS to learn more.",
                "Serving suggestion: Best consumed in very small quantities.",
                "Eat up!",
                "Time to chow down!",
                "Serving suggestion: Best enjoyed when followed by TUMS (R)",
                "Looks delicious! Cheffrey, signing out.",
                "Caution: This recipe violates health codes in 13 countries.",
                "If you like what you see, share this recipe on Twitter! #Cheffrey",
                "Note: This recipe is still pending FDA approval."]

### Introductory messages for user ###

print("Greetings! I'm Cheffrey, the intelligent cooking computer!")

print

# Print a randomly chosen welcome message
print(random.choice(start_messages))

time.sleep(2)

print

# Prompt user for recipe difficulty
print("On a scale of 1 (boring) to 3 (CRAZY!), just how risky of a recipe should we attempt today?")
print("I recommend level 2 for first-timers.")

risk_level = raw_input()

# Set the order of the Markov model (1, 2, or 3) based on the user's choice.
while True:
  try:
    risk = int(risk_level)
  except:
    print("That doesn't compute. Try again?")
    risk_level = raw_input()
    continue
  
  print
  if risk == 1:
    order = 3
    print("All right, if you insist...we'll try something relatively safe.")
    break
  elif risk == 2:
    order = 2
    print("Now we're cooking! Let's see what we can do here!")
    break
  elif risk == 3:
    order = 1
    print("That's what I'm talking about! Brace yourself, Cheffrey is pulling out all the stops this time.")
    break
  else:
    print("That doesn't compute. Try again?")
    risk_level = raw_input()
    continue

time.sleep(2)


print
    
print("I need a few seconds to refresh my memory. Sit tight!")

time.sleep(2)

print
    
print("Studying recipes to become master chef...")

### Step 1: Train the chef using known recipes ###
if not preloaded:

  os.chdir("C:/Users/Michael/Desktop/Recipe Onslaught/allrecipes.com/Recipe")

  total_learning_steps = 0    # Total number of recipe steps used for training the chef

  # Initialize dictionary to store Markov models
  dCorpus = {}
  dCorpus["_START_"] = []

  # Find every recipe HTML page, and extract the data to form a Markov model of
  # recipe sentence structure.
  for recipe in os.listdir("."):
    for target in os.listdir("./" + recipe):
    
      if target.find("Detail") == -1:
        continue
      
      with open("./{}/{}".format(recipe,target)) as fRecipe:
        strRecipe = fRecipe.read()

        try:
          content = strRecipe.split("<div id=\"msgDirections\"")[1].split("<a href")[0]
        except:
          # Recipe does not conform to standard format (rare)
          pass
          
        try:
          for step in content.split("<span class=\"plaincharacterwrap break\">")[1:]:
            
            step = step.split("</span>")[0]
            
            # Incorporate step into our recipe corpus!
            words = step.split()
            
            if len(words) < order + 1:
              continue
            
            dCorpus["_START_"].append(" ".join(words[0:order]))
            for i in range(order,len(words)):
              next_word = words[i]
              prev_word = " ".join(words[(i-order):i])
              if prev_word in dCorpus:
                dCorpus[prev_word].append(next_word)
              else:
                dCorpus[prev_word] = [next_word]
            
            final_word = " ".join(words[-order:])
            if next_word in dCorpus:
              dCorpus[final_word].append("_STOP_")
            else:
              dCorpus[final_word] = ["_STOP_"]
            
            total_learning_steps += 1
            
            # print total_learning_steps
              
            
        except:
          # Recipe does not conform to standard format
          pass
        
  print

  print("Learned chef skills from {} different recipe steps.".format(total_learning_steps))

else:
  # If recipe is preloaded, just unpickle it.
  with open("order{}.pkl".format(order)) as f:
    dCorpus = pickle.load(f)
  
print

### Step 2: Generate our random recipe! ###

# Generate random number of steps from 1 to 8
num_steps = random.randint(1,9)

for i in range(num_steps):

  # Choose random start word or words
  start = random.choice(dCorpus["_START_"])

  my_step = start
  
  last_words = start.split()
  
  while True:
    try:
      # Choose next word based on previous words.
      next_word = random.choice(dCorpus[" ".join(last_words)])
      
      # Stop if we've reached the end of the sentence
      if next_word == "_STOP_":
        break
      
      # Add new word to the sentence
      my_step += " {}".format(next_word)
      
      last_words = last_words[1:] + [next_word]
    except:
      # If no known words go here, just end the step.
      print("Error in model: impossible words reached")
      break
  
  time.sleep(1.5)
  
  # Display the next step
  print("{}) {}".format(i+1, my_step))
  print
 
time.sleep(3)
 
# Print ending message
print(random.choice(end_messages))

# Freeze to allow user to view recipe
raw_input()