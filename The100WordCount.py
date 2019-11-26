from bs4 import BeautifulSoup as soup
import requests
import pandas as pd
from pathlib import Path

"""
    Obtain the number of spoken words by the characters of the Series The 100.
"""

season_1 = ["Pilot", "Earth_Skills", "Earth_Kills", "Murphy's_Law", "Twilight's_Last_Gleaming", "His_Sister's_Keeper",
            "Contents_Under_Pressure", "Day_Trip", "Unity_Day", "I_Am_Become_Death", "The_Calm", "We_Are_Grounders_(Part 1)",
            "We_Are_Grounders_(Part 2)"]

season_2 = ["The_48", "The_Inclement_Weather", "Reapercussions", "Many_Happy_Returns", "Human_Trials", "Fog_of_War",
            "Long_Into_an_Abyss", "Spacewalker", "Remember_Me", "Survival_of_the_fittest", "Coup_de_Grâce", "Rubicon",
            "Resurrection", "Bodyguard_of_Lies", "Blood_Must_Have_Blood_(Part 1)", "Blood_Must_Have_Blood_(Part 2)"]

season_3 = ["Wanheda_(Part 1)", "Wanhead_(Part 2)", "Ye_Who_Enter_Here", "Watch_the_Thrones", "Hakeldama", "Bitter_Harvest",
            "Thirteen", "Terms_and_Conditions", "Stealing_Fire", "Fallen", "Nevermore", "Demons", "Join_or_Die",
            "Red_Sky_at_Morning", "Perverse_Instantiation _Part 1)", "Perverse_Instantiation_(Part 2)"]

season_4 = ["Echoes", "Heavy_lies_The_Crown", "The_Four_Horsemen", "A_Lie_Guarded", "The_Tinder_Box", "We_Will_Rise",
            "Gimme_Shelter", "God_Complex", "DNR", "Die_All,_Die_Merrily", "The_Other_Side", "The_Chosen", "Praimfaya"]

season_5 = ["Eden", "Red_Queen", "Sleeping_Giants", "Pandora's_box", "Shifting_Sands", "Exit_Wounds", "Acceptable_Losses",
            "How_We_Get_To_Peace", "Sic_Semper_Tyrranis", "The_Warriors_Will", "The_Dark_Year", "Damocles_(Part 1)",
            "Damocles_(Part 2)"]


"""
    Function: getWordCount
    Objective: Clean and sort the data obtained from The 100 Wiki so it can be stored in a csv file.
    Parameters: 
        - season_list: A list of the episodes of a season.
        - season_number: The number of the season.
"""


def getWordCount(season_list, season_number):
    totalepisodes = len(season_list)
    finished = 0
    for x in season_list:
        df = pd.DataFrame()
        print("The chapter is " + x)
        link = "https://the100.fandom.com/wiki/"+x+"/Transcript"
        r = requests.get(link)
        page_soup = soup(r.text, "lxml")
        data = page_soup.findAll('tr')
        characterlist = []
        wordlist = []

        for i in range(3, len(data)):
            output = data[i].text.splitlines()
            if len(output) == 2 and len(output[0]) != 0 and output[1][0] is not "[":
                characterlist.append(output[0])
                wordlist.append(len(output[1]))
        df["Character"] = characterlist
        df["Words"] = wordlist
        df = df.groupby(["Character"]).sum()
        df = df.sort_values(["Words"], ascending=False)
        finished += 1
        print("Finished " + str(round((finished/totalepisodes) * 100, 2)) + "%" + "\n")
        path = Path(season_number + "/Episode " + str(finished) + ".csv")
        print(path)
        df.to_csv(path)


getWordCount(season_1, "Season 1")
getWordCount(season_2, "Season 2")
getWordCount(season_3, "Season 3")
getWordCount(season_4, "Season 4")
getWordCount(season_5, "Season 5")

