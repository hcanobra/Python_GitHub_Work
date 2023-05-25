#DigiPetWten.py
import random
import math
#use a class with several variables and functions
#to keep a pet alive; feed, walk, pet, play, treat, etc
#Have trackers; happiness, Food level, Health, etc
#Inlude this and input

class DigiPet:
    def __init__(self):
        self.healthLevel = 100
        self.happyLevel = 100
        self.foodLevel = 100
        self.OverallScore = 100

    def overall_track(self):
        self.OverallScore = float(self.healthLevel) + float(self.happyLevel) + float(self.foodLevel) / 3   ### ADDED self. TO UPDATE THE CLASS VALUE

    def health_track(self):
        self.healthLevel += random.randint(3,8)
        self.happyLevel -= random.randint(3,5)
        self.foodLevel -= random.randint(3,6)
        
    def happy_track(self):
        self.healthLevel -= random.randint(4,6)
        self.happyLevel += random.randint(4,10)
        self.foodLevel -= random.randint(3,6)

    def food_track(self):
        self.healthLevel -= random.randint(2,5)
        self.happyLevel -=random.randint(4,6)
        self.foodLevel +=random.randint(6,9)
        

#main program
petclass = DigiPet()
print('Welcome to Digipet!')
petName = input('Name you DigiPet: ')


while petclass.OverallScore != 0:
    try:
        print(petName + "'s Levels:", 'Health=' + str(petclass.healthLevel) + ' Happiness=' + str(petclass.happyLevel) + ' Food=' + str(petclass.foodLevel))
        print('1-feed, 2-walk, 3-pet, 4-treat, 5-play')

        choice = float(input('What would you like to do today? '))
        if choice == 1:
            petclass.food_track()
            petclass.overall_track()
            print (petclass.OverallScore) # ADDED PRINT LINE SO YOU CAN TRACK THE HEALTH VALUE
            
        elif choice == 2:               # ADDED ON EACH OPTION A elif INSTEAD OF JUST IF
            petclass.health_track()
            petclass.overall_track()
            print (petclass.OverallScore) # ADDED PRINT LINE SO YOU CAN TRACK THE HEALTH VALUE

        elif choice == 3:
            petclass.happy_track()
            petclass.overall_track()
            print (petclass.OverallScore) # ADDED PRINT LINE SO YOU CAN TRACK THE HEALTH VALUE

        elif choice == 4:
            petclass.happy_track()
            petclass.overall_track()
            print (petclass.OverallScore) # ADDED PRINT LINE SO YOU CAN TRACK THE HEALTH VALUE

        elif choice == 5:
            petclass. health_track()
            petclass.overall_track()
            print (petclass.OverallScore) # ADDED PRINT LINE SO YOU CAN TRACK THE HEALTH VALUE

        #break   ------------------- REMOVE BREAK STATEMENT AND MOVE IT AFTER EXCEPT
    except:
        print('Invalid Input')
        break
        
