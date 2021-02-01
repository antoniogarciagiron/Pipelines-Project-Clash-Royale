import os
import pandas as pd
import sys
import re
import numpy as np
import requests
from bs4 import BeautifulSoup
import json

def download_dataset():
    '''Downloads a dataset from kaggle and only keeps the csv in your data file. Beware of your own data structure:
    this creates a data directory and also moves all the .csv files next to your jupyter notebooks to it.
    Takes: url from kaggle
    Returns: a folder with the downloaded csv
    '''
    
    #Gets the name of the dataset.zip
    url = "https://www.kaggle.com/rodsaldanha/clash-royale-matches"
    
    #Gets the name of the dataset.zip
    endopint = url.split("/")[-1]
    user = url.split("/")[-2]
    
    #Download, decompress and leaves only the csv
    download = f"kaggle datasets download -d {user}/{endopint}"
    decompress = f"tar -xzvf {endopint}.zip"
    delete = f"del -rf {endopint}.zip"
    make_directory = "mkdir data"
    lista = "dir >> archivos.txt"
    
    for i in [download, decompress, delete, make_directory, lista]:
        os.system(i)
    
    #Gets the name of the csv (you should only have one csv when running this code)
    lista_archivos = open('archivos.txt').read()
    nueva = lista_archivos.split("\n")
    nueva_2 = " ".join(nueva)
    nueva_3 = nueva_2.split(" ")
    
    #Moves the .csv into the data directory
    for i in nueva_3:
        if i.endswith(".csv"):
            move = f"move {i} data/{i}"
            delete = f"del archivos.txt"
            os.system(move) 
            return os.system(delete)

def clean_clash_dataset():
    '''Takes the csv file as downloaded from Kaggle, creates new columns with the card types, 
    average values for the cards hitpoints and damage per elixir and creates a clean table.
    Takes: the csv file with the cards
    Returns: the clean csv file
    '''

    #Opens the file with Pandas
    sys.path.append("../")
    royale = pd.read_csv("data/cardsInfo.csv",encoding = "ISO-8859-1")
    
    #Adds the column with card type, there are 4 class of fighter cards plus the spells. Common cards can start from level 1, rare cards from level 3, epic cards from level 6
    #and epic cards from level 9. If the cards have hitpoints they are class fighters, otherwise they are spells.
    royale["cardtype"] = royale.apply(lambda x: "Common" if x.hitpoints1 else "Rare" if x.hitpoints3 else "Epic" if x.hitpoints6 else "Legendary" if x.hitpoints9 else "Spell", axis = 1)

    #Changing the NaN values for "0" and prepare to calculate
    royale.dropna(axis=0, how="all")
    royale.fillna(0)
    royale.damage14.astype(float)
    royale.elixir.astype(float)

    #Calculate max damage per elixir
    royale["max_damage_per_elixir"] = royale.apply(lambda x: round((x.damage14/x.elixir), 1) if x.elixir != 0 else 0, axis=1)

    #Calculate max hitpoints per elixir
    royale["max_hitpoints_per_elixir"] = royale.apply(lambda x: round((x.hitpoints14/x.elixir), 1) if x.elixir != 0 else 0, axis=1)

    #Return a clean table
    final_royale = royale[["name", "elixir", "cardtype", "hitpoints14", "max_hitpoints_per_elixir", "damage14", "max_damage_per_elixir"]]
    return final_royale.to_csv("royale_clean", sep=',')

def get_deck (soup):
    '''Obtains the deck of 8 cards from the selected website and adds the card names to a list.
    Takes: the soup file from the selected website
    Returns: a list with 8 card names
    '''

    listdeck = soup.select("div.popularDecks__decklist")[0]
    grouplist=listdeck.find_all("a")
    links=[]
    for item in grouplist:
        link = item.get("href")
        links.append(link)
    deck = []
    for link in links:
        separated = link.split("/")
        card = separated[-1]
        card = card.replace("+", " ")
        deck.append(card)
    return deck

def get_wins (soup):
    '''Obtains the win ratio for a selected deck.
    Takes: the soup file from the selected website
    Returns: the win ratio value
    '''

    wins = soup.select("div.popularDecks__footer div.ui__headerBig")[0]
    ratiowin = float(wins.text.strip()[:-1])
    return ratiowin

def get_crowns (soup):
    '''Obtains the crowns ratio for a selected deck. 
    The target of the game is to destroy the deffensive towers of the opponent. 
    Each tower down gives a crown. 
    Destroying the King's tower wins the battle and gives 3 crowns.
    Takes: the soup file from the selected website
    Returns: the crowns ratio value
    '''

    crowns = soup.select("div.popularDecks__footer div.ui__mediumText")[1]
    ratiocrowns = float(crowns.text.split(" ")[0])
    return ratiocrowns

def get_info(soup):
    '''Uses get_deck, get_wins and get_crowns functions to obtain and merge together the cards of a selected deck, the average wins and the average crowns.
    Takes: NaN
    Returns: a list with the information of a selected deck
    '''


    deck = get_deck(soup)
    wins = get_wins(soup)
    crowns = get_crowns(soup)
    fullinfo = []
    for card in deck:
        fullinfo.append(card)
    fullinfo.append(wins)
    fullinfo.append(crowns)
    return fullinfo

def get_all_sets():
    '''Uses get_info to obtain all the 50 top used decks from the website with their related information and creates a new table.
    Takes: an url from the website with the 50 top used decks in Clash Royale
    Returns: a csv file with the most used decks in Clash Royale and their information
    '''

    url = "https://statsroyale.com/decks/popular?type=tournament"
    response = requests.get(url)
    soup = BeautifulSoup(response.content)
    card_sets = soup.select("div.popularDecks_deckWrapper")

    #Apply the functions to get the cards and the victory and crown ratios
    all_decks = [get_info(deck) for deck in card_sets]

    #Transform into Pandas dataset
    df = pd.DataFrame(all_decks)
    df.columns = ["card_1", "card_2", "card_3", "card_4", "card_5", "card_6", "card_7", "card_8", "victory_ratio", "crowns_ratio"]
    return df.to_csv("final_decks_list", sep=',')
    

def obtain_info_from_decks(best_decks, cards):
    '''Takes information from the top decks list and the cards list. 
    Calculates the number of times the card is used, the average victory and crown ratio of each card.
    Takes: two Pandas files, one with the top decks and another with the cards information
    Returns: a Pandas file with the cards, enriched with more information
    '''


    #Creates a list with the cards, victory ratio and crowns ratio for each deck in the top 50
    individual_decks = best_decks.apply(lambda x: [[x.card_1, x.card_2, x.card_3, x.card_4, x.card_5, x.card_6, x.card_7, x.card_8], x.victory_ratio, x.crowns_ratio], axis=1)

    #This iterates all cards in the game and checks if the card appears in one deck. Counts the number of times the card is used and calculates the average victory and crown ratios
    card_use=[]
    for card in cards["name"]:
        counter = 0
        victory = 0
        crown = 0
        for deck in individual_decks:
            if card in deck[0]:
                counter += 1
                victory += deck[1]
                crown += deck[2]
        if counter != 0:
            card_use.append([card, counter, round(victory/counter, 2), round(crown/counter, 2)])
        else:
            card_use.append([card, 0, 0, 0])

    #Transforms the result into a Pandas dataframe and joins the original cards dataframe with the info obtained from the decks dataframe
    usage = pd.DataFrame(card_use)
    usage.columns = ["name_2", "Use", "Victory_ratio", "Crowns_ratio"]
    usage = usage.drop("name_2", axis = 1)
    cards = cards.join(usage, how = "right")
    return cards

def obtain_info_from_card_list(best_decks, cards):
    '''Takes information from the top decks list and the cards list. 
    Calculates the total and average values of elixir, hitpoints and damage for each deck and adds it to the file.
    Takes: two Pandas files, one with the top decks and another with the cards information
    Returns: a Pandas file with the top used decks, enriched with more information
    '''


    #Creates a two lists from both tables with the elements to iterate
    individual_decks = best_decks.apply(lambda x: [[x.card_1, x.card_2, x.card_3, x.card_4, x.card_5, x.card_6, x.card_7, x.card_8], x.victory_ratio, x.crowns_ratio], axis=1)
    cards["name"] = cards["name"].astype(str)
    card_list = cards.apply(lambda x: [x["name"], x.elixir, x.hitpoints14, x.damage14], axis=1)

    #Iterates all the elements of each deck and checks if all the 8 cards are in the list of cards (There are new cards and the list is from 2020)
    #It calculates que total an average values of the deck for: elixir, damage, hitpoints. If the 8 cards are in the list, it adds the values. Otherwise it drops all 0s to the element
    deck_stats = []
    for deck in individual_decks:
        total_elixir = 0
        total_hitpoints = 0
        total_damage = 0
        counter = 0
        for card in deck[0]:
            for card_name in card_list:
                if card == card_name[0]:
                    counter += 1
                    total_elixir += card_name[1]
                    total_hitpoints += card_name[2]
                    total_damage += card_name[3]
        if counter == 8: 
            deck_stats.append([counter, total_elixir, round(total_elixir/8, 2), total_hitpoints, total_damage, round(total_hitpoints/8, 2), round(total_damage/8, 2)])
        else:    
            deck_stats.append([counter, 0, 0, 0, 0, 0, 0])
    
    #Adds the new calculated values to the deck table
    deck_stats_list = pd.DataFrame(deck_stats)
    deck_stats_list.columns = ["cards_in_list", "total_elixir", "average_elixir", "total_hitpoints", "total_damage", "average_hitpoints", "average_damage"]
    best_decks = best_decks.join(deck_stats_list, how = "right")
    return best_decks
