import requests
from bs4 import BeautifulSoup
import re

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_data(spreadsheet_url, worksheet_name):
    credentials_path = 'key.json'
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    gc = gspread.authorize(creds)
    sh = gc.open_by_url(spreadsheet_url)
    worksheet = sh.worksheet(worksheet_name)
    datas = worksheet.get_all_values()
    datas = datas[1:]

    return datas

def update_col(spreadsheet_url, worksheet_name, row_no, col_no, val):
    credentials_path = 'key.json'
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    gc = gspread.authorize(creds)
    sh = gc.open_by_url(spreadsheet_url)
    worksheet = sh.worksheet(worksheet_name)
    worksheet.update_cell(row_no, col_no, val)


def extract_emails_from_webpage(url, headers=None):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 403:
            # Access denied
            return []
        response.raise_for_status()

        content = response.text
        soup = BeautifulSoup(content, 'html.parser')

        # Refined regex pattern for email extraction
        email_pattern = r'''
            [a-zA-Z0-9._%+-]+          # Local part
            @
            [a-zA-Z0-9.-]+            # Domain part
            \.
            [a-zA-Z]{2,}              # Top-level domain
            \b                        # Word boundary
        '''
        emails = re.findall(email_pattern, soup.get_text(), re.VERBOSE)
        return emails
    except requests.exceptions.RequestException as e:
        # Log the exception
        print(f"Request failed: {e}")
        return []


def find_emails(base_url, headers=None):
    emails = extract_emails_from_webpage(base_url, headers)

    if not emails:
        contact_us_patterns = [
            "/contact",
            "/contact-us",
            "/contact-me",
            "/pages/contact",
            "/pages/contact-us",
            "/pages/contact-me",
        ]
        for pattern in contact_us_patterns:
            contact_url = base_url.rstrip('/') + pattern
            emails = extract_emails_from_webpage(contact_url, headers)
            if emails:
                break

    return ', '.join(emails) if emails else ''


def get_email(website):
    if website:
        # Ensure the URL starts with https://www.
        if not website.startswith(('https://www.', 'http://www.')):
            website = f'https://www.{website}'

        emails = find_emails(website, headers)
        return emails
    return 'Invalid website'


# Example usage
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# datas = get_data('https://docs.google.com/spreadsheets/d/1MWCyGVEv_ZsoIKlcD058FLDj0ULyq027TXGnH6je0X4/edit?gid=1835136499#gid=1835136499', 'Google Map Leads')
# for i, data in enumerate(datas, start=2):
#     website = data[-1]
#     if website != '':
#         print(website)
#         if 'https://www.' not in website and 'http://www.' not in website:
#             website = f'https://www.{website}'
#         emails = find_emails(website, headers)
#         if emails != '':
#             update_col('https://docs.google.com/spreadsheets/d/1MWCyGVEv_ZsoIKlcD058FLDj0ULyq027TXGnH6je0X4/edit?gid=1835136499#gid=1835136499', 'Google Map Leads', i, 7, emails)
#             print(emails)
def CityNames():
    cities = [
        "New York City, NY",
        "Los Angeles, CA",
        "Chicago, IL",
        "Houston, TX",
        "Phoenix, AZ",
        "Philadelphia, PA",
        "San Antonio, TX",
        "San Diego, CA",
        "Dallas, TX",
        "San Jose, CA",
        "Austin, TX",
        "Jacksonville, FL",
        "Fort Worth, TX",
        "Columbus, OH",
        "Charlotte, NC",
        "San Francisco, CA",
        "Indianapolis, IN",
        "Seattle, WA",
        "Denver, CO",
        "Washington, DC",
        "Boston, MA",
        "El Paso, TX",
        "Nashville, TN",
        "Detroit, MI",
        "Oklahoma City, OK",
        "Portland, OR",
        "Las Vegas, NV",
        "Memphis, TN",
        "Louisville, KY",
        "Baltimore, MD",
        "Milwaukee, WI",
        "Albuquerque, NM",
        "Tucson, AZ",
        "Fresno, CA",
        "Mesa, AZ",
        "Sacramento, CA",
        "Atlanta, GA",
        "Kansas City, MO",
        "Colorado Springs, CO",
        "Miami, FL",
        "Raleigh, NC",
        "Omaha, NE",
        "Long Beach, CA",
        "Virginia Beach, VA",
        "Oakland, CA",
        "Minneapolis, MN",
        "Tulsa, OK",
        "Arlington, TX",
        "Tampa, FL",
        "New Orleans, LA",
        "Wichita, KS",
        "Cleveland, OH",
        "Bakersfield, CA",
        "Aurora, CO",
        "Anaheim, CA",
        "Honolulu, HI",
        "Santa Ana, CA",
        "Riverside, CA",
        "Corpus Christi, TX",
        "Lexington, KY",
        "Stockton, CA",
        "Henderson, NV",
        "Saint Paul, MN",
        "St. Louis, MO",
        "Cincinnati, OH",
        "Pittsburgh, PA",
        "Greensboro, NC",
        "Anchorage, AK",
        "Plano, TX",
        "Lincoln, NE",
        "Orlando, FL",
        "Irvine, CA",
        "Newark, NJ",
        "Durham, NC",
        "Chula Vista, CA",
        "Toledo, OH",
        "Fort Wayne, IN",
        "St. Petersburg, FL",
        "Laredo, TX",
        "Jersey City, NJ",
        "Chandler, AZ",
        "Madison, WI",
        "Lubbock, TX",
        "Scottsdale, AZ",
        "Reno, NV",
        "Buffalo, NY",
        "Gilbert, AZ",
        "Glendale, AZ",
        "North Las Vegas, NV",
        "Winston-Salem, NC",
        "Chesapeake, VA",
        "Norfolk, VA",
        "Fremont, CA",
        "Garland, TX",
        "Irving, TX",
        "Hialeah, FL",
        "Richmond, VA",
        "Boise, ID",
        "Spokane, WA",
        "Baton Rouge, LA"
    ]

    return cities