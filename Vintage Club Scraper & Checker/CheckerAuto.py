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

    def EbayAuto(Items):
        if not Items:

            print("No Items To Delete")
            PrintDateTime()
            pass
        if len(Items) == 1:
            print("there is one item in this list")
            ItemsListOne = "(" + str(Items) + ")"

            driver = uc.Chrome()
            driver.get('https://distilnetworks.com')  # starts magic


            driver.get("https://www.google.com")  #
            driver.implicitly_wait(random.randint(4, 6))
            driver.get("https://www.ebay.co.uk/sh/lst/active")
            driver.implicitly_wait(random.randint(4, 6))
            time.sleep(3)

            user = driver.find_element_by_id("userid")
            user.send_keys("jackkaybuiss@hotmail.com")
            time.sleep(1.5)
            signIn = driver.find_element_by_id("signin-continue-btn")
            signIn.click()

            time.sleep(5)

            password = driver.find_element_by_id("pass")
            password.send_keys("Trendme22!")
            time.sleep(1.5)
            signIn2 = driver.find_element_by_id("sgnBt")
            signIn2.click()

            driver.implicitly_wait(random.randint(4, 7))
            itemList = driver.find_element_by_xpath('//*[@id='"'s0-0-4-16-49-7-filters-advancedSearch[]-generic'"']/input')
            itemList.send_keys(ItemsListOne)
            time.sleep(random.randint(2, 4))
            button = driver.find_element_by_xpath("//*[@id='"'s0-0-4-16-49-7-filters'"']/form/div[4]/button[1]")
            button.click()
            time.sleep(random.randint(6, 10))
            selectAll = driver.find_element_by_xpath("//*[@id='"'shui-dt-checkall'"']")
            selectAll.click()
            time.sleep(random.randint(6, 10))

            preEnd1 = driver.find_element_by_xpath(
                "/html/body/div[6]/div[2]/div[1]/div/div[3]/div/div[2]/div[3]/div[3]/div[1]/div/div[3]/span/span/button")
            preEnd1.click()
            time.sleep(random.randint(6, 10))

            preEnd2 = driver.find_element_by_xpath("//*[@id='"'s0-0-4-16-49-bulkActionsV2-component-5-0-content-menu'"']/a[1]")
            preEnd2.click()
            time.sleep(random.randint(6, 10))


            radioButton = driver.find_element_by_xpath("/html/body/div[2]/div/div/div/table[3]/tbody/tr/td[2]/form/table/tbody/tr/td[2]/input[1]")
            time.sleep(random.randint(6, 10))
            radioButton.click()

            endButton = driver.find_element_by_xpath("/ html / body / div[2] / div / div / div / table[3] / tbody / tr / td[2] / form / input[5]")
            time.sleep(random.randint(6, 10))
            endButton.click()
            print("1 Item Successfully Deleted")

            Delete_All_Data()
            Export_Data_To_Sheets()
            PrintDateTime()
        if len(Items) >= 2:
            print("There are multiple items in this list")
            Items = "(" + str(Items) + ")"

            driver = uc.Chrome()
            driver.get('https://distilnetworks.com')  # starts magic

            driver.get("https://www.google.com")  #
            driver.implicitly_wait(random.randint(4, 6))
            driver.get("https://www.ebay.co.uk/sh/lst/active")
            driver.implicitly_wait(random.randint(4, 6))
            time.sleep(3)

            user = driver.find_element_by_id("userid")
            user.send_keys("jackkaybuiss@hotmail.com")
            time.sleep(1.5)
            signIn = driver.find_element_by_id("signin-continue-btn")
            signIn.click()

            time.sleep(5)

            password = driver.find_element_by_id("pass")
            password.send_keys("Trendme22!")
            time.sleep(1.5)
            signIn2 = driver.find_element_by_id("sgnBt")
            signIn2.click()

            driver.implicitly_wait(random.randint(4, 7))
            itemList = driver.find_element_by_xpath('//*[@id='"'s0-0-4-16-49-7-filters-advancedSearch[]-generic'"']/input')
            itemList.send_keys(Items)
            time.sleep(random.randint(2, 4))
            button = driver.find_element_by_xpath("//*[@id='"'s0-0-4-16-49-7-filters'"']/form/div[4]/button[1]")
            button.click()
            time.sleep(random.randint(6, 10))
            selectAll = driver.find_element_by_xpath("//*[@id='"'shui-dt-checkall'"']")
            selectAll.click()
            time.sleep(random.randint(6, 10))

            preEnd1 = driver.find_element_by_xpath(
                "/html/body/div[6]/div[2]/div[1]/div/div[3]/div/div[2]/div[3]/div[3]/div[1]/div/div[3]/span/span/button")
            preEnd1.click()
            time.sleep(random.randint(6, 10))

            preEnd2 = driver.find_element_by_xpath("//*[@id='"'s0-0-4-16-49-bulkActionsV2-component-5-0-content-menu'"']/a[1]")
            preEnd2.click()
            time.sleep(random.randint(6, 10))

            endItems = driver.find_element_by_xpath(
                "/html/body/div[2]/div/div/div/form[3]/table[3]/tbody/tr/td[2]/table/tbody/tr[2]/td[1]/input")
            endItems.click()
            print("Items Successfully Deleted")

            Delete_All_Data()
            Export_Data_To_Sheets()
            PrintDateTime()
    EbayAuto(unavailable_list)



RunAll()
'''
scheduler = BlockingScheduler()
scheduler.add_job(RunAll, 'cron', hour='7,9,12,15,17,18,19,20,22')
scheduler.start()
'''