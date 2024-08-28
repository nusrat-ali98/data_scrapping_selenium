import gspread
from oauth2client.service_account import ServiceAccountCredentials

def remove_duplication(spreadsheet_url, worksheet_name):
    credentials_path = 'key.json'
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    gc = gspread.authorize(creds)
    sh = gc.open_by_url(spreadsheet_url)
    worksheet = sh.worksheet(worksheet_name)
    data = worksheet.get_all_values()

    header = data[0]
    rows = data[1:]

    unique_rows = []
    seen = []

    for row in rows:
        if row[4] not in seen:
            seen.append(row[4])
            unique_rows.append(row)
    unique_data = [header] + unique_rows
    worksheet.clear()
    worksheet.update(range_name="A1", values=unique_data)


remove_duplication('https://docs.google.com/spreadsheets/d/1MWCyGVEv_ZsoIKlcD058FLDj0ULyq027TXGnH6je0X4/edit?gid=1729675550#gid=1729675550', 'Consultant_GoogleMap')