#########################################
##### Name:     Junjie Huang        #####
##### Uniqname:   hjunjie           #####
#########################################

import requests
import json
import webbrowser 
import asyncio
import genshin
from bs4 import BeautifulSoup
from final_project import *

def Character_builds(answer, data):
    if int(answer) in range(0, len(data['Character'])):
        character_name = data['Character'][int(answer)]['title'] 
        y_or_n= input(f'Are you want to search for {character_name}?')

        if y_or_n in {"yes", "y", "yup", "sure"}:
            while True:
                answer_1 = input("Which information you want to know?\n 1.picture\n 2.element type\n 3.weapon type\n 4.suitable weapons\n 5.suitable artifacts\n 6.suitable teams\n 7.tier level\n")
                if int(answer_1) == 1 :
                    link = data['Character'][int(answer)]['link'] 
                    print(f'The picture link for {character_name} is {link}')
                elif int(answer_1) == 2:
                    Type = data['Character'][int(answer)]['type'] 
                    print(f'The element type for {character_name} is {Type}')
                elif int(answer_1) == 3:
                    weapon_type = data['Character'][int(answer)]['weapon'] 
                    print(f'The weapon type for {character_name} is {weapon_type}')
                elif int(answer_1) == 4:
                    suitable_weapons = data['Character'][int(answer)]['builds'][0:2]
                    print(f'The suitable weapons for {character_name} is {suitable_weapons}')
                elif int(answer_1) == 5:
                    suitable_artifaccters = data['Character'][int(answer)]['builds'][2:] 
                    print(f'The suitable artifacts for {character_name} is {suitable_artifaccters}')
                    answer_3 = input("Do you want to know the scores of the team?")

                elif int(answer_1) == 6:
                    suitable_teams = data['Character'][int(answer)]['teams'] 
                    print(f'The suitable teams for {character_name} is {suitable_teams}')

                elif int(answer_1) == 7:
                    if character_name in data['tier_list']['0']:     
                        tier_level = 'SS+'
                    if character_name in data['tier_list']['1']:     
                        tier_level = 'S+'
                    if character_name in data['tier_list']['2']:     
                        tier_level = 'S'
                    if character_name in data['tier_list']['3']:     
                        tier_level = 'A'
                    if character_name in data['tier_list']['4']:     
                        tier_level = 'B'
                    if character_name in data['tier_list']['5']:     
                        tier_level = 'C'
                    print(f'The tier_level for {character_name} is {tier_level}')    
                else:
                    print("enter wrong information, please try it again")  
                
                answer2 = input(f"Do you still want to ask other things about {character_name}?")            
                if answer2 in {'yes', 'y', 'sure'}: 
                    pass
                else:    
                    break               
        else:
            print("enter wrong information, please try it again")
    else:
        print("enter wrong information, please try it again")

def top_teams(answer, data):
    if int(answer) == 1:
        while True:
            character_id = input("Which character do you want to know?\n Please enter the character's list id \n")
            if int(character_id) in range(0, len(data['Character'])):
                character_name = data['Character'][int(character_id)]['title'] 
                y_or_n = input(f'Are you want to search for {character_name}?')

                if y_or_n in {"yes", "y", "yup", "sure"}:
                    a = []
                    for team in data['top_teams']:
                        for character in data['top_teams'][team]:
                            if character_name in character:
                                a.append(data['top_teams'][team]) 
                    if a == []:
                        print(f'The current best teams don\'t include {character_name}')
                    else:
                        print(f'The current best teams for {character_name} exist: {a}')  
            else:
                print("enter wrong information, please try it again")
            
            answer2 = input(f"Do you still want to ask the current best teams for other character?")            
            if answer2 in {'yes', 'y', 'sure'}: 
                pass
            else:    
                break      

    elif int(answer) == 2:
        print('The current top teams are:')
        for team in data['top_teams']:
            print(data['top_teams'][team]) 

def tier_list(answer, data):
    if int(answer) == 1:
        while True:
            character_id = input("Which character do you want to know?\n Please enter the character's list id \n")
            if int(character_id) in range(0, len(data['Character'])):
                character_name = data['Character'][int(character_id)]['title'] 
                y_or_n = input(f'Are you want to search for {character_name}?')

                if y_or_n in {"yes", "y", "yup", "sure"}:
                    for idx in data['tier_list']:
                        for character in data['tier_list'][idx]:
                            if character_name in character:
                                if idx == '0':
                                    print(f'{character_name}\'s tier level is SS+')
                                elif idx == '1':
                                    print(f'{character_name}\'s tier level is S+')
                                elif idx == '2':
                                    print(f'{character_name}\'s tier level is S')
                                elif idx == '3':
                                    print(f'{character_name}\'s tier level is A')
                                elif idx == '4':
                                    print(f'{character_name}\'s tier level is B')
                                elif idx == '5':
                                    print(f'{character_name}\'s tier level is C')
            else:
                print("enter wrong information, please try it again")
            
            answer2 = input(f"Do you still want to ask the current best teams for other character?")            
            if answer2 in {'yes', 'y', 'sure'}: 
                pass
            else:    
                break      

    elif int(answer) == 2:
        print('The current tier list are:')
        for team in data['tier_list']:
            data_tier = data['tier_list']
            if team == '0':
                print(f'SS+ : {data_tier[team]}')
            elif team == '1':
                print(f'S+ : {data_tier[team]}')
            elif team == '2':
                print(f'S : {data_tier[team]}')
            elif team == '3':
                print(f'A : {data_tier[team]}')
            elif team == '4':
                print(f'B : {data_tier[team]}')
            elif team == '5':
                print(f'C : {data_tier[team]}')

def main():
    """provide information recommendations based on user’s current character"""
    print('Welcome to Genshin helper!')
    
    load_file_name = 'genshin_cache.json'
    data = read_json(load_file_name)
    name_list = input('Do you want to know all the character\'s name list?')
    if name_list in {'yes', 'y', 'sure'}:
        for i in range(0, len(data['Character'])):
            character_name = data['Character'][i]['title'] 
            print(f'Id:{i}, character name: {character_name}')

    while True:
        answer = input("What do you want to know about today?\n 1.Character builds\n 2.top teams recommendation\n 3.tier list\n")
        if int(answer) == 1:
            answer1 = input("Which character do you want to know?\n Please enter the character's list id \n")
            Character_builds(answer1, data)
        elif int(answer) == 2:
            answer2 = input("1.Do you want to know the current best teams for a certain character? 2.Or you want to know all current top teams?\n")
            top_teams(answer2, data)
        elif int(answer) == 3:
            answer3 = input("1.Do you want to know the tier level of a certain character? 2.Or you want to know all characters of a certain tier level?\n")            
            tier_list(answer3, data)
        else:
            print("enter wrong inforamtion, thank you and bye!")

        answer4 = input("Do you want to ask other things?")            
        if answer4 in {'yes', 'y', 'sure'}: 
            pass
        else:    
            print('Thank you!')
            break



if __name__ == "__main__":
    main() 