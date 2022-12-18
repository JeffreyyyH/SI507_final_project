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

CACHE_FILENAME = "genshin_cache.json"

def open_cache():
    ''' opens the cache file if it exists and loads the JSON into
    a dictionary, which it then returns.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    #dumped_json_cache = json.dumps(cache_dict, cls=MyEncoder, indent=4)

    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def read_json(filepath, encoding='utf-8'):
    """
    Reads a JSON document, decodes the file content, and returns a list or
    dictionary if provided with a valid filepath.
    Parameters:
        filepath (string): path to file
        encoding (string): optional name of encoding used to decode the file. The default is 'utf-8'.
    Returns:
        dict/list: dict or list representations of the decoded JSON document
    """

    f = open(filepath, encoding=encoding)
    return json.load(f)

def write_json(filepath, data):
    """
    This function dumps the JSON object in the dictionary `data` into a file on
    `filepath`.
    Parameters:
        filepath (string): The location and filename of the file to store the JSON
        data (dict): The dictionary that contains the JSON representation of the objects.
    Returns:
        None
    """

    with open(filepath, 'w') as outfile:
        json.dump(data, outfile)



if __name__ == "__main__":
    genshin_CACHE = open_cache()
    
    if 'Character' in genshin_CACHE.keys():
        Genshin_data = {}
        Genshin_data['Character'] = genshin_CACHE['Character']
    else:
        Genshin_data = {}
        url_base = 'https://genshin.gg/characters'
        strhtml_base = requests.get(url_base) # get html
        soup_base=BeautifulSoup(strhtml_base.text,'lxml')
        data_icon1 = soup_base.select('#root > div > section > div.row > main > div.character-list > a.character-portrait.new > img.character-icon')#character-icon
        data_icon2 = soup_base.select('#root > div > section > div.row > main > div.character-list > a > img.character-icon')
        data_type1 = soup_base.select('#root > div > section > div.row > main > div.character-list > a.character-portrait.new > img.character-type')#character-icon
        data_type2 = soup_base.select('#root > div > section > div.row > main > div.character-list > a > img.character-type')
        data_weapon1 = soup_base.select('#root > div > section > div.row > main > div.character-list > a.character-portrait.new > img.character-weapon')#character-icon
        data_weapon2 = soup_base.select('#root > div > section > div.row > main > div.character-list > a > img.character-weapon')

        data_icon = data_icon1 + data_icon2
        data_type = data_type1 + data_type2
        data_weapon = data_weapon1 + data_weapon2

        result = []
        for item in data_icon:
            add={
                'title':item.get('alt'),
                'link' :item.get('src')
            }
            result.append(add)

        for i in range(0, len(result)):
            result[i]['type'] =  data_type[i].get('alt')
            result[i]['weapon'] = data_weapon[i].get('alt')

        for i in range(0, len(result)):
            name = result[i]['title']
            name = ''.join(name.split()).lower() 
            url_details = f'https://genshin.gg/characters/{name}/'
            strhtml = requests.get(url_details)
            soup = BeautifulSoup(strhtml.text,'lxml')
            data_builds = soup.select('#builds > div > div > div > div > div > div > img')
            data_teams = soup.select('#teams > div > div > div > a > img.character-icon') 
            build = []
            for k in data_builds:
                build.append(k.get('alt'))
            result[i]['builds'] = build   

            teams = {}
            for j in range(0, len(data_teams)):
                if j%4 == 0:
                    teams[j//4] = []
                    teams[j//4].append(data_teams[j].get('alt'))
                else:
                    teams[j//4].append(data_teams[j].get('alt')) 
            result[i]['teams']  = teams     
            print("proceeding")
        Genshin_data['Character'] = result

    #top_teams

    if 'top_teams' in genshin_CACHE.keys():
        Genshin_data['top_teams'] = genshin_CACHE['top_teams']
    else:
        url_teams = 'https://genshin.gg/teams'
        strhtml_teams = requests.get(url_teams)
        soup_top_teams = BeautifulSoup(strhtml_teams.text,'lxml')
        data_top_teams = soup_top_teams.select('#root > div > section > div.row > main > div:nth-child(5) > div > div > div > a > img.character-icon')
        top_teams = {}
        for i in range(0, len(data_top_teams)):
            if i%4 == 0:
                top_teams[i//4] = []
                top_teams[i//4].append(data_top_teams[i].get('alt'))
            else:
                top_teams[i//4].append(data_top_teams[i].get('alt'))                    

        Genshin_data['top_teams'] = top_teams
        #print(top_teams)


    #data_tier    
    if 'tier_list' in genshin_CACHE.keys():
        Genshin_data['tier_list'] = genshin_CACHE['tier_list']
    else:        
        data_tier = []
        url_tier_list = 'https://genshin.gg/tier-list/'
        strhtml_tier = requests.get(url_tier_list)
        soup_tier = BeautifulSoup(strhtml_tier.text,'lxml')

        data_tier.append(soup_tier.select('#root > div > section > div.row > main > div:nth-child(6) > div.tier-list > a > img.character-icon'))
        data_tier.append(soup_tier.select('#root > div > section > div.row > main > div:nth-child(7) > div.tier-list > a > img.character-icon'))
        data_tier.append(soup_tier.select('#root > div > section > div.row > main > div:nth-child(8) > div.tier-list > a > img.character-icon'))
        data_tier.append(soup_tier.select('#root > div > section > div.row > main > div:nth-child(11) > div.tier-list > a > img.character-icon'))
        data_tier.append(soup_tier.select('#root > div > section > div.row > main > div:nth-child(12) > div.tier-list > a > img.character-icon'))
        data_tier.append(soup_tier.select('#root > div > section > div.row > main > div:nth-child(13) > div.tier-list > a > img.character-icon'))
        
        tier_result = {}
        for i in range(0, len(data_tier)):
            add = []
            for j in data_tier[i]:
                add.append(j.get('alt'))
            tier_result[f'{i}'] = add

        Genshin_data['tier_list'] = tier_result
    
    save_cache(Genshin_data)
