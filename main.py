# This is a program to read a spreadsheet from google drive and look up
# the stock ticker and use alpha vantage api to retrieve the stock price.

import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import requests
import pandas as pd
from datetime import datetime


# Use the environment variable
SERVICE_ACCOUNT_INFO = json.loads(os.environ.get('GOOGLE_CREDENTIALS'))
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SPREADSHEET_ID = '1ex4bRiP5aryneQnJBYKdhGDvWxlH_WSs41dzOEvguNc'  # Replace with your actual spreadsheet ID
RANGE_NAME = 'Sheet1'  # Change as needed


def main():
  creds = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO,
                                                scopes=SCOPES)
  service = build('sheets', 'v4', credentials=creds)

  # Call the Sheets API
  sheet = service.spreadsheets()
  result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                              range=RANGE_NAME).execute()
  values = result.get('values', [])

  row_cnt = 0
  output_df = pd.DataFrame()

  if not values:
    print('No data found.')
  else:
    for row in values:
      # Print columns A and B, which correspond to indices 0 and 1.
      # print(f"{row[0]}, {row[1]}")

      if row_cnt == 0:
        pass
      else:
        transaction_date = row[0]
        stock_ticker = row[1]
        print('stock ticker is ' + stock_ticker)

        alpha_vantage_url = "https://www.alphavantage.co/query"

        alpha_vantage_parameters = {
            "function": "TIME_SERIES_DAILY",
            "symbol": stock_ticker,
            "outputsize": "full",
            "apikey": os.environ['ALPHA_VANTAGE_API_KEY']
        }

        # response = requests.get(alpha_vantage_url, params=alpha_vantage_parameters)
        # data = response.json()  # Or response.text if you need raw content
        data = {
          "Meta Data": {
              "1. Information": "Daily Prices (open, high, low, close) and Volumes",
              "2. Symbol": "IBM",
              "3. Last Refreshed": "2024-03-18",
              "4. Output Size": "Compact",
              "5. Time Zone": "US/Eastern"
          },
          "Time Series (Daily)": {
              "2024-03-18": {
                  "1. open": "191.7000",
                  "2. high": "193.2300",
                  "3. low": "190.3200",
                  "4. close": "191.6900",
                  "5. volume": "5410562"
              },
              "2024-03-15": {
                  "1. open": "191.9900",
                  "2. high": "193.0573",
                  "3. low": "190.7000",
                  "4. close": "191.0700",
                  "5. volume": "8828184"
              },
              "2024-03-14": {
                  "1. open": "196.9500",
                  "2. high": "197.7480",
                  "3. low": "192.1200",
                  "4. close": "193.4300",
                  "5. volume": "4102202"
              },
              "2022-03-16": {
                  "1. open": "197.5500",
                  "2. high": "198.1000",
                  "3. low": "195.3200",
                  "4. close": "196.7000",
                  "5. volume": "3960737"
              }
          }
        }

        print(data)
        df = pd.DataFrame(data)
        print(df.info())
        print(df.shape)
        print(df.head())
        print(df.tail())

        df_meta = pd.DataFrame.from_dict(data['Meta Data'], orient='index')

        print(df_meta.info())
        print(df_meta)

        df_data = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')

        df_data.index = pd.to_datetime(df_data.  index)

        df_data.columns = ['open', 'high', 'low', 'close', 'volume']

        df_data = df_data.astype({'open': 'float', 'high': 'float', 'low': 'float', 'close': 'float', 'volume': 'float'})

        print(df_data)

        print('the transaction date is ' + transaction_date)

        # transaction_datetime = datetime.strptime(transaction_date, '%Y-%m-%d')
        # print(transaction_datetime)

        # need to handle exception for Saturday and Sunday, if the date is not available, go for the next available date
        lookup_date_close_unitprice = df_data.loc[transaction_date, 'close']

        print(lookup_date_close_unitprice)

        current_date = df_data.index[0]
        print(current_date)

        current_date_close_unitprice = df_data.loc[df_data.index[0], 'close']
        print(current_date_close_unitprice)

        output_row = {'transaction_date':transaction_date, 'stock_ticker':stock_ticker, 'purchase_unitprice':lookup_date_close_unitprice,'current_date':current_date,'current_unitprice':current_date_close_unitprice}

        print(type(df))
        output_df = output_df._append(output_row, ignore_index=True)

      row_cnt = row_cnt + 1

      print(output_df)

     # sheet.update([output_df.columns.values.tolist()] + output_df.values.tolist())
      

if __name__ == '__main__':
  main()
