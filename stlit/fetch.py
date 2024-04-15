import pandas as pd

def fetch_data():
    # open dataset.csv
    with open('dataset.csv', 'r') as f:
        data = pd.read_csv(f)
        df = pd.DataFrame(data)
        return df
        # read the data



def getlists():
    df = fetch_data()

    # create a list of dictionaries
    Names = df['Name'].tolist()
    Age = df['Age'].tolist()
    Gender = df['Gender'].tolist()
    Hobby1 = df['Hobby1'].tolist()
    Hobby2 = df['Hobby2'].tolist()
    Personality = df['MBTI'].tolist()
    State = df['State'].tolist()

    data = [Names, Age, Gender, Hobby1, Hobby2, Personality, State]
    return data

