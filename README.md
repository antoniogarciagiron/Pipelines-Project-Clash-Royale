# Clash Royale, top decks

![Portada](https://i.blogs.es/8935db/lroyale/1366_2000.jpg)

## Introduction:

Clash Royale is a game available to play in mobile phones. There are several cards to be used in the game, the player must choose a deck of 8 cards and use them during the game. The objective is to destroy the opponent's towers while you protect your own towers. There are 2 small towers and a bigger one with your king defending it. If you manage to destroy only one tower you'll get one crown at the end of the game, and if you destroy the King's one you'll get 3 crowns and win the game. For more information you can check the following [video](https://www.youtube.com/watch?v=EVMFgEwdCHc).
Each card has an elixir' cost to be summoned, a number of hitpoints the card resists before disapearing, and a damage it deals.

## Objectives:

- This is one of the projects done during the [IronHack](https://www.ironhack.com/es) Data Analytics bootcamp.
- The target of this project is to get a dataset from Kaggle and clean it. At the same time, to obtain aditional information by means of web scraping and merge it with the dataset, in order to comare and get conclusions.
- The following libraries are used: Os, Pandas, Sys, Requests, BeautifulSoup and Seaborn.

## Data:

- A dataset was taken from [Kaggle](https://www.kaggle.com/rodsaldanha/clash-royale-matches), containing information about the cards available in the game Clash Royale. The process can be directly executed with the python file "01_download_and_clean.py".
- The aditional information was found from a [website](https://statsroyale.com/decks/popular?type=tournament) by means of web scraping, and was related to the most popular card combinations for tournaments in the game. The process is can be executed with the python file "02_get_data_from_web.py".
- A set of functions were created following a data pipeline process, in order to clean and merge both datasets. Functions can be found in the "set_functions.py" file, in the src folder.
- The data is analysed and conclusions obtained. The process is carried out in the file "03 Merging data and obtaining conclusions.ipynb".

## Conclusions:

- The most popular cards are "The log", "Barbarian barrel" and the "Knight", however, the most effective in terms of victory ratios and crowns' ratios are the "Minion Horde", "Tombstone" and "Sparky".
- The most used cards have a smaller summon cost.
- The hitpoints of a card have a negative relation with the card damage, in such a wat that some cards are effective defending and others attacking.
- There is a linear relation between effectiveness and average elixir cost. Decks with higher victory and crowns ratio have average elixir costs around 4, and other decks with smaller elixir costs have less victory ratios.
- There is a direct relation between victory ratio and crown ratio. This indicates that is better to have an aggressive strategy instead of a defensive one. 
- Decks with cards with high hitpoints are less effective, again, is better to have an agressive strategy.
- Decks with cards with high damage are not necesary the best. Making a few very strong attacks is as effective as making lots of smaller attacks.