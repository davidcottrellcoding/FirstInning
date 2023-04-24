import requests
import pandas as pd
import io
from datetime import date, timedelta
import csv
import json
import os
import shutil

headers = ['Time', 'Location', 'Team', 'xRuns', 'Pitcher', 'Status', 'RunScored', 'Probability','FairOdds', 'DraftKings', 'DraftKingsEV', 'BetOnline', 'BetOnlineEV', 'Bovada', 'BovadaEv', 'Bet365', 'Bet365EV', 'Fanduel', 'FanduelEV', 'BetMGM', 'BetMGMEV', 'Fliff','FliffEV', 'HardRock', 'HardRockEV', 'Caesars', 'CaesarsEv', 'Betfred', 'BetfredEV', 'Kambi', 'KambiEV', 'Bookmaker', 'BookmakerEV', 'WynnBet', 'WynnBetEV', 'Bet99', 'Bet99EV', 'Superbook', 'SuperbookEV']
today = date.today() 

fileLocation = './GameData/{}/{}'.format(today, today)

def createDailyDirectory():
    # create the directory
    if not os.path.exists('./GameData/{}/'.format(today)):
        os.mkdir('{}'.format('./GameData/{}'.format(today)))

def createCsv():    

    formatted_date = today.strftime("%B %d RFI").replace(" ", "%20")

    # set the URL of the public Google Sheet document and tab name
    url = 'https://docs.google.com/spreadsheets/d/1gH26groo3OiP2-sMY4LdNtfG4Iq6ElUuFSYAWpJaGH4/gviz/tq?tqx=out:csv&sheet={}'.format(formatted_date)

    # read the data from the sheet into a pandas dataframe
    df = pd.read_csv(url, index_col=0, usecols=range(39))

    # convert any non-ASCII characters to ASCII
    df = df.applymap(lambda x: x.encode('ascii', 'ignore').decode() if isinstance(x, str) else x)



    if os.path.exists('./GameData/{}/'.format(today)):
        shutil.rmtree('./GameData/{}/'.format(today))
        os.mkdir('{}'.format('./GameData/{}'.format(today)))
    # export the dataframe to a CSV file

    df.to_csv('{}.csv'.format(fileLocation))

def addHeaders():
    #Add headers to the CSV
    df = pd.read_csv('{}.csv'.format(fileLocation))

    df.columns = headers
    df.to_csv('{}.csv'.format(fileLocation))

def stripBadData():
    with open('{}.csv'.format(fileLocation), 'r') as file:
        reader = csv.reader(file)
        # Skip the first 4 lines
        for i in range(4):
            next(reader)
        # Get the remaining lines
        lines = [line for line in reader]

    with open('{}.csv'.format(fileLocation), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(lines)

def combineRows(row, nextRow):
    newJson = {}
    if row['Time']:
        newJson['Game'] = {
            'Time': row['Time'],
            'Home': row,
            'Away': nextRow,
        }

        print(newJson, '\n\n')

def writeJson():
    csv_file = open('{}.csv'.format(fileLocation), 'r')
    json_file = open('{}.json'.format(fileLocation), 'w')

    # Read the CSV file
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        try:
            nextRow = next(csv_reader)
            # process rows 1 and 2 together
            combineRows(row, nextRow)
        except StopIteration:
            # end of file, break out of loop
            break
            
    # Convert CSV to JSON
    json_data = json.dumps(list(csv_reader))

    # Write the JSON data to a file
    json_file.write(json_data)

    # Close the files
    csv_file.close()
    json_file.close()

def getRFIData():
    createDailyDirectory()
    createCsv()
    stripBadData()
    addHeaders()
    writeJson()


getRFIData()