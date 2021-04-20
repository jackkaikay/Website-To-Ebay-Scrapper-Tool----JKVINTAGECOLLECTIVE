import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
import undetected_chromedriver as uc
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# here enter the id of your google sheet
SAMPLE_SPREADSHEET_ID_input = '1LPRV4RqIvVZ0EySNSmP4hRjmWRUj43ncfjgg9vOhvHQ'
SAMPLE_RANGE_NAME = 'A1:AA100000'

def RunAll():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    # here enter the id of your google sheet
    SAMPLE_SPREADSHEET_ID_input = '1LPRV4RqIvVZ0EySNSmP4hRjmWRUj43ncfjgg9vOhvHQ'
    SAMPLE_RANGE_NAME = 'A1:AA100000'

    def main():
        global values_input, service
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES) # here enter the name of your downloaded JSON file
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                    range=SAMPLE_RANGE_NAME).execute()
        values_input = result_input.get('values', [])

        if not values_input and not values_expansion:
            print('No data found.')

    main()

    df=pd.DataFrame(values_input[1:], columns=values_input[0])

    print(df)

    # change this by your sheet ID
    SAMPLE_SPREADSHEET_ID_input = '1LPRV4RqIvVZ0EySNSmP4hRjmWRUj43ncfjgg9vOhvHQ'
    gsheetId = '1LPRV4RqIvVZ0EySNSmP4hRjmWRUj43ncfjgg9vOhvHQ'
    # change the range if needed
    SAMPLE_RANGE_NAME = 'A1:AA1000'
    data = df

    def prepare_soup(link):
        html = requests.get(link)
        if html.status_code == 200:
            return BeautifulSoup(html.text,"html.parser")
        else:
            return False

    def product_available(link):
        soup = prepare_soup(link)
        if not soup:
            return False
        if soup.find('button', {
            'class': 'ProductForm__AddToCart Button Button--secondary Button--full'}).text.strip().lower().__contains__(
                'sold out'):
            return False
        return True


    unavailable_list = []

    links = []
    for ind in data.index:
        links.append(data['item url'][ind])


    print(links)




    def ULRLISTS(code):

        if not product_available(code):
            unavailable_list.append(code)
            print('Item Sold')
            print(code)

    with Pool(5) as p:
        lol = p.map(ULRLISTS, links)

    for ind in data.index:


        code = data['Code'][ind]
        link = data['item url'][ind]
        print(ind)
        if not product_available(link):
            unavailable_list.append(code)
            data = data.drop([ind])
            print('Item Sold')

    print(data)



    def Create_Service(client_secret_file, api_service_name, api_version, *scopes):
        global service
        SCOPES = [scope for scope in scopes[0]]
        # print(SCOPES)

        cred = None

        if os.path.exists('token_write.pickle'):
            with open('token_write.pickle', 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
                cred = flow.run_local_server()

            with open('token_write.pickle', 'wb') as token:
                pickle.dump(cred, token)

        try:
            service = build(api_service_name, api_version, credentials=cred)
            print(api_service_name, 'service created successfully')
            # return service
        except Exception as e:
            print(e)
            # return None

    # change 'my_json_file.json' by your downloaded JSON file.
    Create_Service('credentials.json', 'sheets', 'v4', ['https://www.googleapis.com/auth/spreadsheets'])

    def Export_Data_To_Sheets():
        response_date = service.spreadsheets().values().clear(

            spreadsheetId=gsheetId,
            valueInputOption='RAW',
            range=SAMPLE_RANGE_NAME,
            body=dict(
                majorDimension='ROWS',
                values=data.T.reset_index().T.values.tolist())
        ).execute()
        print('Sheet successfully Updated')

    def PrintDateTime():
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

    def Delete_All_Data():

        body = {}
        resultClear = service.spreadsheets().values().clear(spreadsheetId=gsheetId, range=SAMPLE_RANGE_NAME,
                                                            body=body).execute()
        print('Data Cleared')

    def Export_Data_To_Sheets():
        response_date = service.spreadsheets().values().update(

            spreadsheetId=gsheetId,
            valueInputOption='RAW',
            range=SAMPLE_RANGE_NAME,
            body=dict(
                majorDimension='ROWS',
                values=data.T.reset_index().T.values.tolist())
        ).execute()
        print('Sheet successfully Updated')

    print(unavailable_list)

    print('https://docs.google.com/spreadsheets/d/1LPRV4RqIvVZ0EySNSmP4hRjmWRUj43ncfjgg9vOhvHQ/edit?usp=drive_web&ouid=103549851300883063646')



    Delete_All_Data()
    Export_Data_To_Sheets()
    PrintDateTime()

from multiprocessing import Pool
import concurrent.futures

'''
def runaller():
    POOL_SIZE = multiprocessing.cpu_count() * 2
    print(f"allotting {POOL_SIZE} threads for multiprocessing")
    with concurrent.futures.ProcessPoolExecutor as executor:
        executor.submit(RunAll)
'''






RunAll()

