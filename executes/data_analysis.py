import pandas as pd

def char_word_count():
    file_path = "ygocardlist.xlsx"
    data = pd.read_excel(file_path, sheet_name="Sheet1")

    filter_data = data[data["Type"] != "Normal Monster"] #exclude Normal Monster due to not having effect text but flavor text
    filter_data["Release"] = pd.to_datetime(filter_data["Release"], errors="coerce")
    filter_data["Year"] = filter_data["Release"].dt.year #sort by year

    filter_data["Char_Count"] = filter_data["Description"].str.len() #count character amount of effect text
    filter_data["Word_Count"] = filter_data["Description"].str.split().str.len() #count word count of effect text

    #create, sort and round averages
    char_word_count_average = filter_data.groupby("Year").agg({
        "Char_Count": "mean",
        "Word_Count": "mean"
    }).reset_index() 
    char_word_count_average = char_word_count_average.sort_values(by="Year")
    char_word_count_average['Char_Count'] = char_word_count_average['Char_Count'].round()
    char_word_count_average['Word_Count'] = char_word_count_average['Word_Count'].round()


    output_file = "mean_char_word_count.xlsx"
    with pd.ExcelWriter(output_file, engine="openpyxl") as f:
        char_word_count_average.to_excel(f, index=False, sheet_name="Average Description Amount")



if __name__ == "__main__":
    char_word_count()
