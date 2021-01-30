import os
import pandas as pd
import sys
import re
import numpy as np

def download_dataset():
    '''Downloads a dataset from kaggle and only keeps the csv in your data file. Beware of your own data structure:
    this creates a data directory and also moves all the .csv files next to your jupyter notebooks to it.
    Takes: url from kaggle
    Returns: a folder with the downloaded csv
    '''
    
    #Gets the name of the dataset.zip
    url = input("Introduce la url: ")
    
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


