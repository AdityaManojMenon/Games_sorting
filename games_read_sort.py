#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 19:17:11 2023

@author: adi
"""

################################################################################
#Write a function that opens 2 types of csv file one for games and other for discount. If file is not valid it will display an error till the user inputs a valid file.
#Write a read functions for game and discount each and return a dictionary based on formatting.
#Write other functions ask to return a list of game names by filtering through specific values/ creterias.
#The main rquires to call the functoins based on the options inputted by user and to perform the desire function.
################################################################################
import csv
from operator import itemgetter


MENU = '''\nSelect from the option: 
        1.Games in a certain year 
        2. Games by a Developer 
        3. Games of a Genre 
        4. Games by a developer in a year 
        5. Games of a Genre with no discount 
        6. Games by a developer with discount 
        7. Exit 
        Option: '''
        
      
        
def open_file(s):
    ''' Prompt user to input a valid csv filename and returns a file pointer. If the file is invalid then it will return a error message.'''
    while True:
        filename = input(f"\nEnter {s} file: ")
        try:
            fp = open(filename,"r",encoding='UTF-8')
            return fp

        except:
            print('\nNo Such file')


def read_file(fp_games):
    ''' Makes a dictionary by editing each column apart from names to instructed format. The key of the dictionary is the name and the rest are values/specification for each name.'''
    dict_game={}
    reader = csv.reader(fp_games)
    next(reader)
    
    for line in reader:
        support_list = []
        name = line[0]
        date = line[1]
        developers = line[2].split(";")#makes a list by splitting by ';'
        genre = line[3].split(";")
        player_mode_list = line[4].split(";")
        multiplayer = "multi-player" 
        if player_mode_list[0].lower() == multiplayer:
            player_mode = 0
        else:
            player_mode = 1
            
        try:
            price = line[5].replace(",","")#repalce the commas for numeric strings at that index
            price = float(price)
            price = price*0.012
        except:
            price = 0.0
        overall_review = line[6]
        reviews = int(line[7])
        percent_positive = line[8].replace("%","")
        percent_positive = int(percent_positive)
        if line[9] == "1":
            support_list.append("win_support")
        if line[10] == "1":
            support_list.append("mac_support")
        if line[11] == "1":
            support_list.append("lin_support")

        game_info = [date, developers, genre, player_mode, price, overall_review, reviews, percent_positive, support_list]# put rest of the values in a list so its easier to make a dictionary containing all the values.
        dict_game[name] = game_info#shows that name is the key and rest are values
    return dict_game
         
            
def read_discount(fp_discount):
    ''' Returns a dictionary where the game name is the key of the dictionary and the %discount is the value. It takes the discount file pointer as the argument. '''
    dict_discount={}
    reader = csv.reader(fp_discount)
    next(reader)
    for line in reader:
        name = line[0]
        discount = round(float(line[1]),2) #converts to flaot and round to 2 decimal places
        dict_discount[name] = discount #shows that name is the key and
    return dict_discount

def in_year(master_D,year):
    ''' This fuctoin returns a list of game names that are from a specific year(agrument) in alphabetical order.'''
    year_game=[]
    for name in master_D:#name is the key 
        if int(master_D[name][0][-4:]) == year:# this only takes the year form the master_D 0th column.
            year_game.append(name)
            year_game=sorted(year_game)#sorts in alphabetrical order
    return year_game


def by_genre(master_D,genre): 
    ''' This fuctoin returns a list of game names that are from a specific genre(agrument) in order of highest to lowest positive review percentage.'''
    genre_game_dict={}
    ordered_titles = []
    for name in master_D:
        if genre in master_D[name][2]:
            genre_game_dict[name]=master_D[name][7]
    sorted_list = sorted(genre_game_dict.items(),key = itemgetter(1), reverse= True)# reverse since in decending order
    for i in sorted_list:
        ordered_titles.append(i[0])#the zeroth index is the name since it was the key.

    return ordered_titles


    
        
def by_dev(master_D,developer): 
    ''' This fuctoin returns a list of game names that are from a specific developer(agrument) in order of latest to oldest games.'''
    developer_dict = {}
    ordered_titles = []
    for name in master_D:
        if developer in master_D[name][1]:
            developer_dict[name] = int(master_D[name][0][-4:])
    sorted_list = sorted(developer_dict.items(), key = itemgetter(1), reverse = True)#sorted form latest to oldest games
    for i in sorted_list:
        ordered_titles.append(i[0])
    return ordered_titles

def per_discount(master_D,games,discount_D): 
    ''' This function return a list of the discounted prices for games that are in both master_D game dicitonary and discount_D the discount dictionary.'''
    discounted_prices = []
    for game in games:
        if game in master_D:
            price = master_D[game][4]
            if game in discount_D:
                discount = discount_D[game]
                discounted_price = (1-(discount/100))*price#discount formula
                discounted_price = round(discounted_price,6)#round to 6th decimal place
                discounted_prices.append(discounted_price)
            else:#for no discount
                discounted_price = price
                discounted_price = round(discounted_price,6)
                discounted_prices.append(discounted_price)
                

    return discounted_prices

    
            

def by_dev_year(master_D,discount_D,developer,year):
    ''' This function returns a list of game names sorted in increasing prices by sorting by specific developers and year and then check ig the games in dicounted dictionary and sort by price while taking dicounted prices into consideration.'''
    dict_price = {}
    ordered_titles=[]
    for games in master_D:
        price = master_D[games][4]
        if developer in master_D[games][1]:
            if int(master_D[games][0][-4:]) == year:
                if games in discount_D:
                    discount = discount_D[games]
                    discounted_price = (1-(discount/100))*price
                    dict_price[games] = discounted_price
                else:
                    discounted_price = price
                    dict_price[games] = discounted_price
    sorted_list = sorted(dict_price.items(), key = itemgetter(1))#sorts in terms of price which is the first index.
    for games in sorted_list:
        ordered_titles.append(games[0])
    return ordered_titles
        

    

def by_genre_no_disc (master_D, discount_D, genre):                      
    ''' This function returns a list of game names sorted by genre that don't have discounted prices avaliable and ordered by cheapest to most expensive price and if the prices are the same then the game names are sorted by percentage of positive review in decending order.'''
    
    dict_prices = {}
    dict_percentages = {}
    modified_list=[]

    sorted_by_percentage = by_genre(master_D,genre)   
    for names in sorted_by_percentage:
        if names not in discount_D:
            modified_list.append(names)#list contains name of games that are form specified genre and not in dicount_D dictionary.


    for games in modified_list:
        if games in master_D:
            price = master_D[games][4]
            positive_percentage= master_D[games][7]
            dict_prices[games] = price
            dict_percentages[games] = positive_percentage
    
    flipped = {}
    
    for key, value in dict_prices.items():
        if value not in flipped:
            flipped[value] = [key]
        else:
            flipped[value].append(key)#contains both percentage and price with name being the key 
    dict_dict={}
    for key,val in flipped.items():
        dict_sort_percentage = {}
        for i in val:
            dict_sort_percentage[i] = dict_percentages[i]
        dict_dict[key] = sorted(dict_sort_percentage.items(),key = itemgetter(1),reverse = True)#sort by percentage in desending order.
    dict_dict = sorted(dict_dict.items(), key = itemgetter(0))
    titles=[]
    
    for tup1 in dict_dict:
        for tup2 in tup1[1]:#indexing 
            titles.append(tup2[0])
    return titles# returns list of game details.



def by_dev_with_disc(master_D,discount_D,developer):
    ''' This function returns a list of game names sorted by developer that have discounted prices avaliable and ordered by cheapest to most expensive price and if the prices are the same then keep as the same order as the original dicitonary.'''

    dict_prices = {}
    modified_list=[]
    ordered_titles=[]

    sorted_by_year = by_dev(master_D,developer)
    for names in sorted_by_year:
        if names in discount_D:
            modified_list.append(names)
    
    for games in modified_list:
        if games in master_D:
            price = master_D[games][4]
            dict_prices[games] = price
    
    sorted_list = sorted(dict_prices.items(),key = itemgetter(1))#sorted by cheapest to most expensive prices
    for games in sorted_list:
        ordered_titles.append(games[0])
    return ordered_titles



def main():
    ''' The main function opens both the game and discount file and then prompts user to pick and option form 1 to 7. Option 7 being the program quitting option. For the other options the pervious functions are called to carry out the tasks based on the instructions. The output for each of the options is a string of game names seperated by commas that are filtered and sorted by the called functions. '''

    fp_games = open_file("games")
    fp_discount = open_file("discount")
    master_D = read_file(fp_games)
    discount_D = read_discount(fp_discount)
    list_options = [1,2,3,4,5,6,7]
    while True:
        option = input(MENU)
        try:
            option = int(option)
        except:
            print("\nInvalid option")
            continue
        if option in list_options:

            if option == 1:
                while True:
                    year = input('\nWhich year: ')
                    try:
                        year = int(year)
                        break
                    except:
                        print("\nPlease enter a valid year")
                        continue
                for name in master_D:
                    if year == int(master_D[name][0][-4:]):
                        year = year

                list_year=in_year(master_D,year)
                if len(list_year) != 0:
                    list_year.sort()
                    print(f"\nGames released in {year}:")
                    for i in range(len(list_year)):
                        print(list_year[i], end="")
                        if i != len(list_year) - 1:
                            print(", ", end="")
                    print()
                else:
                    print("\nNothing to print")
                    
            
            elif option == 2:
                developer = input('\nWhich developer: ')
                
                dev_sorted = by_dev(master_D,developer)
                if len(dev_sorted) != 0:
                    print(f"\nGames made by {developer}:")
                    for i in range(len(dev_sorted)):
                        print(dev_sorted[i], end="")
                        if i != len(dev_sorted) - 1:
                            print(", ", end="")
                    print()
                else:
                    print("\nNothing to print")    
                    
            
            elif option == 3:
                genre = input('\nWhich genre: ')
                
                genre_sorted = by_genre(master_D,genre)
                if len(genre_sorted) != 0:
                    print(f"\nGames with {genre} genre:")
                    print(*genre_sorted, sep = ", ")
                else:
                    print("\nNothing to print") 

            elif option == 4:
                developer = input('\nWhich developer: ')
                year = input('\nWhich year: ')
                try:
                    year = int(year)
                except:
                    print("\nPlease enter a valid year")
                
                dev_sorted_by_year = by_dev_year(master_D,discount_D,developer,year)
                if len(dev_sorted_by_year) != 0:
                    print(f"\nGames made by {developer} and released in {year}:")
                    print(*dev_sorted_by_year, sep = ", ")
                else:
                    print("\nNothing to print") 

            
            elif option == 5:
                genre = input('\nWhich genre: ')
                
                genre_no_discount = by_genre_no_disc (master_D, discount_D, genre)
                if len(genre_no_discount) != 0:
                    print(f"\nGames with {genre} genre and without a discount:")
                    for i in range(len(genre_no_discount)):
                        print(genre_no_discount[i], end="")
                        if i != len(genre_no_discount) - 1:
                            print(", ", end="")
                    print()
                else:
                    print("\nNothing to print")  
            
            elif option == 6:
                developer = input('\nWhich developer: ')
                
                dev_with_discount = by_dev_with_disc(master_D,discount_D,developer)
                if len(dev_with_discount) != 0:
                    print(f"\nGames made by {developer} which offer discount:")
                    for i in range(len(dev_with_discount)):
                        print(dev_with_discount[i], end="")
                        if i != len(dev_with_discount) - 1:
                            print(", ", end="")
                    print()
                else:
                    print("\nNothing to print")  
            
            elif option == 7:
                print("\nThank you.")
                break
        else:
            print("\nInvalid option")    
                
            

if __name__ == "__main__":
    main()