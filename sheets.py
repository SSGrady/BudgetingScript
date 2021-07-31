import mintapi
import pandas as pd
import gspread
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
from config import username, password, Spreadsheet_Key

def main():
	mint = mintapi.Mint(
		username, # Email used to log in to Mint
		password, # password used to log in to mint
		mfa_method='sms',
		headless=False,
		mfa_input_callback=None,
		session_path=None,
		imap_account=None,
		imap_password=None,
		imap_folder='INBOX',
		wait_for_sync=False,
		wait_for_sync_timeout=300,
		)

	transactions = mint.get_transactions()
	transactions = transactions.drop(["labels", 'notes', 'original_description'], axis=1)
	transactions.loc[(transactions.transaction_type == 'debit'), 'transaction_type'] = 'Expense'
	transactions.loc[(transactions.transaction_type == 'credit'), 'transaction_type'] = 'Income'

	scope = ['https://spreadsheets.google.com/feeds']
	creds = ServiceAccountCredentials.from_json_keyfile_name('creds_mint.json', scope)
	client = gspread.authorize(creds)
	d2g.upload(transactions, Spreadsheet_Key, "RAW_DATA", credentials = creds, row_names=True)
	

if __name__ == '__main__':
	main()