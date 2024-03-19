# This is a program to read a spreadsheet from google drive and look up 
# the stock ticker and use alpha vantage api to retrieve the stock price.

import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import requests

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

  if not values:
    print('No data found.')
  else:
    for row in values:
      # Print columns A and B, which correspond to indices 0 and 1.
      print(f"{row[0]}, {row[1]}")

  alpha_vantage_url = "https://www.alphavantage.co/query"

  alpha_vantage_parameters = {
      "function": "TIME_SERIES_DAILY",
      "symbol": "MSFT",
      "apikey": os.environ['ALPHA_VANTAGE_API_KEY']
  }

  response = requests.get(alpha_vantage_url, params=alpha_vantage_parameters)
  data = response.json()  # Or response.text if you need raw content

  print(data)


if __name__ == '__main__':
  main()
