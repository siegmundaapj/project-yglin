import requests
import pandas as pd
import csv

 #API call from ygoprodeck.com gathers card metadata

base_url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
params = {
    "misc": "yes"
    } #for release date info

csv_file = "ygocardlist.csv"
excel_file = "ygocardlist.xlsx"
txt_file = "ygotextdump.txt"

def get_base_info():
    try:
        response = requests.get(base_url, params=params) #get card metadata or specify params
        response.raise_for_status()
        if response.status_code == 200:
            card_data = response.json() #load data as json
        else:
            print(f"Response Error Code: {response.status_code}")
    except:
        return
    return card_data

def create_csv(card_data, filename=csv_file):
    if "data" not in card_data:
        return

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Description", "Race", "Type", "Attribute", "Release"]) 
        for card in card_data["data"]:
            name = card.get("name", "N/A")
            desc = card.get("desc", "N/A")
            race = card.get("race", "N/A")
            type = card.get("type", "N/A")
            attribute = card.get("attribute", "N/A"),
            release = card.get("misc_info", [{}])[0].get("tcg_date", "N/A")          
            writer.writerow([name, desc, race, type, attribute, release])
    print("csv file created.")       
    
def create_excel(card_data, filename=excel_file):
    if "data" not in card_data:
        return

    card_list = []
    for card in card_data["data"]:
        name = card.get("name", "N/A")
        desc = card.get("desc", "N/A")
        race = card.get("race", "N/A")
        type = card.get("type", "N/A")
        attribute = card.get("attribute", "N/A"),
        release = card.get("misc_info", [{}])[0].get("tcg_date", "N/A")
        card_list.append({
            "Name": name,
            "Description": desc,
            "Race": race,
            "Type": type,
            "Attribute": attribute,
            "Release": release
        })
    base_dataframe = pd.DataFrame(card_list)
    with pd.ExcelWriter(filename, engine="openpyxl") as excel:
        base_dataframe.to_excel(excel, index=False)
    print("xlsx file created.")

def create_txt(card_data, filename=txt_file): #just dumps all description text in a single txt file
    if "data" not in card_data:
        return
    with open(filename, "w", encoding="utf-8") as file:
            cards = card_data.get("data", [])
            for card in cards:
                desc = card.get("desc")  
                file.write(desc + "\n")  
    print("txt file created.")




if __name__ == "__main__":
    # params = {"name": "Spright Blue",
    #           "misc": "yes"}
    card_data = get_base_info()
    #print(card_data)
    if card_data:
        create_csv(card_data)
        create_excel(card_data)
        create_txt(card_data)
