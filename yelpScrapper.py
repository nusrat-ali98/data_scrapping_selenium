import requests
from bs4 import BeautifulSoup
import re
from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
import undetected_chromedriver as uc
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from check import CityNames
from datetime import datetime
import csv

def get_day_with_suffix():
    current_date = datetime.now()
    day = current_date.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

    day_suffix = str(day) + suffix
    return current_date.strftime(f"{day_suffix} %B, %Y")


def extract_emails_from_webpage(url, headers=None):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 403:
            print(f"Access denied to {url}")
            return []
        response.raise_for_status()
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", soup.get_text())
        return emails
    except requests.exceptions.RequestException as e:

        return []


# Single function to find emails on the main and Contact Us pages
def find_emails(base_url, headers=None):
    # Try to extract emails from the main page
    emails = extract_emails_from_webpage(base_url, headers)

    if not emails:
        contact_us_patterns = [
            "/contact",
            "/contact-us",
            "/contact-me",
            "/get-in-touch",
            "/support",
            "/customer-service"
        ]
        for pattern in contact_us_patterns:
            contact_url = base_url.rstrip('/') + pattern
            print(f"Trying {contact_url}")
            emails = extract_emails_from_webpage(contact_url, headers)
            if emails:
                break

    return ', '.join(emails)


# Example usage
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


def get_email(website):
    if website != '':
        print(website)
        if 'https://www.' not in website:
            website = f'https://www.{website}'
        emails = find_emails(website, headers)

        return emails
    else:
        return ''
def SheetData(spreadsheet_url, data, worksheet_name):
    credentials_path = 'key.json'
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    gc = gspread.authorize(creds)
    sh = gc.open_by_url(spreadsheet_url)
    worksheet = sh.worksheet(worksheet_name)
    worksheet.append_rows(data)


def openSite():
    service = Service(r'chromedriver.exe')
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--headless")
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    chrome_options.add_argument(f"--user-agent={user_agent}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    driver.get('https://www.google.com/')

    sleep(2)



    return driver

cookies = {
    'wdi': '2|98920977F23E4AEF|0x1.9a7fdfbea39d2p+30|a08906f40f764984',
    '_gcl_au': '1.1.1726664071.1721759749',
    '_scid': '5284be8b-9e0a-4319-8e51-f39e83ea0daa',
    'ndp_session_id': 'd06282c7-bf02-4d14-afdf-77a51d7b1cf7',
    '_tt_enable_cookie': '1',
    '_ttp': '-t5opXM0CdsJbGCbv83AEXKk0nb',
    '__adroll_fpc': '22f02e78e13a381e3ffcd8fd5eff1102-1721759754641',
    '_fbp': 'fb.1.1721759755106.818745453157439635',
    '_uetvid': '6338b580492211ef926821403106d9c0',
    '_ga_4DDTFPQZN7': 'GS1.1.1722277029.1.0.1722277029.0.0.0',
    '_ga_QP0D7M20RC': 'GS1.1.1722275624.4.1.1722277033.0.0.0',
    'IR_PI': 'c9a8d6ad-4dd6-11ef-b992-0b58b6936fa9%7C1722277036988',
    '_ga_MEZL1ZKM71': 'GS1.1.1722280600.2.0.1722280600.0.0.0',
    '_ga': 'GA1.2.98920977F23E4AEF',
    'hl': 'en_US',
    'bse': '4fbc78313db94e189c383067a7f807c3',
    'spses.d161': '*',
    '_ScCbts': '%5B%5D',
    '_sctr': '1%7C1723402800000',
    'recentlocations': '',
    'location': '%7B%22unformatted%22%3A+%22San+Francisco%2C+CA%22%2C+%22city%22%3A+%22San+Francisco%22%2C+%22provenance%22%3A+%22YELP_GEOCODING_ENGINE%22%2C+%22accuracy%22%3A+4%2C+%22county%22%3A+%22San+Francisco+County%22%2C+%22place_id%22%3A+%221237%22%2C+%22latitude%22%3A+37.775123%2C+%22parent_id%22%3A+371%2C+%22max_latitude%22%3A+37.81602226140252%2C+%22address2%22%3A+%22%22%2C+%22address1%22%3A+%22%22%2C+%22display%22%3A+%22San+Francisco%2C+CA%22%2C+%22min_longitude%22%3A+-122.51781463623047%2C+%22max_longitude%22%3A+-122.3550796508789%2C+%22country%22%3A+%22US%22%2C+%22location_type%22%3A+%22locality%22%2C+%22min_latitude%22%3A+37.706368356809776%2C+%22longitude%22%3A+-122.41932%2C+%22zip%22%3A+%22%22%2C+%22state%22%3A+%22CA%22%2C+%22address3%22%3A+%22%22%2C+%22borough%22%3A+%22%22%2C+%22confident%22%3A+null%2C+%22isGoogleHood%22%3A+false%2C+%22language%22%3A+null%2C+%22neighborhood%22%3A+%22%22%2C+%22polygons%22%3A+null%2C+%22usingDefaultZip%22%3A+false%7D',
    'adc': 'hGx8Ws7UTDjphQXbAWiOmQ%3Ahv-SWBMbExHo7pYdvkb_FQ%3A1723488772',
    'xcj': '1|lMQQ26Nv_LPzg4BunURXWgakXFGhYZBW5MTKOCTY10s',
    '_ga_K9Z2ZEVC8C': 'GS1.2.1723487746.11.1.1723488829.0.0.0',
    '_scid_r': '5284be8b-9e0a-4319-8e51-f39e83ea0daa',
    '_uetsid': 'b22f8cb058d911ef88d1f96abd12cc9b',
    '__ar_v4': 'BHPKS4B4ONEJJMGH4QCJZR%3A20240722%3A31%7CQB5JPFIKRZDSBOZSULG4YB%3A20240722%3A31%7C7YX6SJQ4RZAMPB6LZ7CHFF%3A20240722%3A26%7CV37VIEJOFNGMBBC7SXOK3T%3A20240722%3A2%7CHIRZJK5YAFDGLFKUFBETP6%3A20240728%3A1%7CGOWGG2YU4VC2DHG2I7IJTF%3A20240811%3A2',
    'datadome': 'yRS98qLsf6RADmb5Z_uhSxooyKyIdsI4hTrprpJKmqRjf~l0owvVWZWMcMP_ACahyNcPpnb4v443oqHgvS31PAsr84UJmSDlUSNfV1Vd2MGRhPZKd01L4FoReDm_lwhF',
    'bsi': '1%7C1d843239-0214-43f4-96cb-bd9503215bc8%7C1723489453970%7C1723487738570',
    'spid.d161': '15b0596e-ca8c-4178-9860-45f589761f9c.1721759730.9.1723489496.1722632665.452f92f9-c982-4e30-bea8-ec3421881fc9.fe3c6164-186a-4c56-aec6-5ef67ecfe3e9.f642cf80-e620-4e31-96fb-eb2f56fb8487.1723487746627.49',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+Aug+13+2024+00%3A05%3A03+GMT%2B0500+(Pakistan+Standard+Time)&version=202403.1.0&browserGpcFlag=0&isIABGlobal=false&identifierType=Cookie+Unique+Id&hosts=&consentId=31746d8a-5ec6-4a4d-a7f5-4a6db3208757&interactionCount=1&isAnonUser=1&landingPath=https%3A%2F%2Fwww.yelp.com%2Fsearch%3Ffind_desc%3DPlumbers%26find_loc%3DSan+Francisco%252C+CA&groups=BG122%3A1%2CC0003%3A1%2CC0002%3A1%2CC0001%3A1%2CC0004%3A1',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': 'wdi=2|98920977F23E4AEF|0x1.9a7fdfbea39d2p+30|a08906f40f764984; _gcl_au=1.1.1726664071.1721759749; _scid=5284be8b-9e0a-4319-8e51-f39e83ea0daa; ndp_session_id=d06282c7-bf02-4d14-afdf-77a51d7b1cf7; _tt_enable_cookie=1; _ttp=-t5opXM0CdsJbGCbv83AEXKk0nb; __adroll_fpc=22f02e78e13a381e3ffcd8fd5eff1102-1721759754641; _fbp=fb.1.1721759755106.818745453157439635; _uetvid=6338b580492211ef926821403106d9c0; _ga_4DDTFPQZN7=GS1.1.1722277029.1.0.1722277029.0.0.0; _ga_QP0D7M20RC=GS1.1.1722275624.4.1.1722277033.0.0.0; IR_PI=c9a8d6ad-4dd6-11ef-b992-0b58b6936fa9%7C1722277036988; _ga_MEZL1ZKM71=GS1.1.1722280600.2.0.1722280600.0.0.0; _ga=GA1.2.98920977F23E4AEF; hl=en_US; bse=4fbc78313db94e189c383067a7f807c3; spses.d161=*; _ScCbts=%5B%5D; _sctr=1%7C1723402800000; recentlocations=; location=%7B%22unformatted%22%3A+%22San+Francisco%2C+CA%22%2C+%22city%22%3A+%22San+Francisco%22%2C+%22provenance%22%3A+%22YELP_GEOCODING_ENGINE%22%2C+%22accuracy%22%3A+4%2C+%22county%22%3A+%22San+Francisco+County%22%2C+%22place_id%22%3A+%221237%22%2C+%22latitude%22%3A+37.775123%2C+%22parent_id%22%3A+371%2C+%22max_latitude%22%3A+37.81602226140252%2C+%22address2%22%3A+%22%22%2C+%22address1%22%3A+%22%22%2C+%22display%22%3A+%22San+Francisco%2C+CA%22%2C+%22min_longitude%22%3A+-122.51781463623047%2C+%22max_longitude%22%3A+-122.3550796508789%2C+%22country%22%3A+%22US%22%2C+%22location_type%22%3A+%22locality%22%2C+%22min_latitude%22%3A+37.706368356809776%2C+%22longitude%22%3A+-122.41932%2C+%22zip%22%3A+%22%22%2C+%22state%22%3A+%22CA%22%2C+%22address3%22%3A+%22%22%2C+%22borough%22%3A+%22%22%2C+%22confident%22%3A+null%2C+%22isGoogleHood%22%3A+false%2C+%22language%22%3A+null%2C+%22neighborhood%22%3A+%22%22%2C+%22polygons%22%3A+null%2C+%22usingDefaultZip%22%3A+false%7D; adc=hGx8Ws7UTDjphQXbAWiOmQ%3Ahv-SWBMbExHo7pYdvkb_FQ%3A1723488772; xcj=1|lMQQ26Nv_LPzg4BunURXWgakXFGhYZBW5MTKOCTY10s; _ga_K9Z2ZEVC8C=GS1.2.1723487746.11.1.1723488829.0.0.0; _scid_r=5284be8b-9e0a-4319-8e51-f39e83ea0daa; _uetsid=b22f8cb058d911ef88d1f96abd12cc9b; __ar_v4=BHPKS4B4ONEJJMGH4QCJZR%3A20240722%3A31%7CQB5JPFIKRZDSBOZSULG4YB%3A20240722%3A31%7C7YX6SJQ4RZAMPB6LZ7CHFF%3A20240722%3A26%7CV37VIEJOFNGMBBC7SXOK3T%3A20240722%3A2%7CHIRZJK5YAFDGLFKUFBETP6%3A20240728%3A1%7CGOWGG2YU4VC2DHG2I7IJTF%3A20240811%3A2; datadome=yRS98qLsf6RADmb5Z_uhSxooyKyIdsI4hTrprpJKmqRjf~l0owvVWZWMcMP_ACahyNcPpnb4v443oqHgvS31PAsr84UJmSDlUSNfV1Vd2MGRhPZKd01L4FoReDm_lwhF; bsi=1%7C1d843239-0214-43f4-96cb-bd9503215bc8%7C1723489453970%7C1723487738570; spid.d161=15b0596e-ca8c-4178-9860-45f589761f9c.1721759730.9.1723489496.1722632665.452f92f9-c982-4e30-bea8-ec3421881fc9.fe3c6164-186a-4c56-aec6-5ef67ecfe3e9.f642cf80-e620-4e31-96fb-eb2f56fb8487.1723487746627.49; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Aug+13+2024+00%3A05%3A03+GMT%2B0500+(Pakistan+Standard+Time)&version=202403.1.0&browserGpcFlag=0&isIABGlobal=false&identifierType=Cookie+Unique+Id&hosts=&consentId=31746d8a-5ec6-4a4d-a7f5-4a6db3208757&interactionCount=1&isAnonUser=1&landingPath=https%3A%2F%2Fwww.yelp.com%2Fsearch%3Ffind_desc%3DPlumbers%26find_loc%3DSan+Francisco%252C+CA&groups=BG122%3A1%2CC0003%3A1%2CC0002%3A1%2CC0001%3A1%2CC0004%3A1',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}


def GetLinks(cookies, headers, target_bussiness, Target_City):
    driver = openSite()
    i = 0
    filtered_links = []
    filtered_names = []
    while True:
        if i == 0:

            # target_link = f'https://www.yelp.com/search?find_desc={target_bussiness}&find_loc={Target_City.replace(',', '%2C').replace(' ', '+')}'
            params = {
                'find_desc': target_bussiness,
                'find_loc': Target_City,
            }
        else:
            # target_link = f'https://www.yelp.com/search?find_desc={target_bussiness}&find_loc={Target_City.replace(',', '%2C').replace(' ', '+')}&start={i}'
            params = {
                'find_desc': target_bussiness,
                'find_loc': Target_City,
                'start': f'{i}',
            }

        print(params)
        response = requests.get('https://www.yelp.com/search', params=params, cookies=cookies, headers=headers)
        # pagesource = openSite(target_link)
        if response.status_code == 200:
            tree = html.fromstring(response.content)
            if tree.xpath("//*[contains(text(), 'the page of results you requested is unavailable.')]"):
                break
            links = tree.xpath('//ul[contains(@class,"list")]//li//h3//a/@href')
            bussines_names = tree.xpath('//ul[contains(@class,"list")]//li//h3//a/text()')
            datas = []
            for link, bussines_name in zip(links, bussines_names):
                link = f'https://www.yelp.com{link}'
                if link not in filtered_links and bussines_name not in filtered_names:
                    filtered_links.append(link)
                    filtered_names.append(bussines_name)
                    data = GetDetails(driver, bussines_name, link)
                    if len(data) > 0:
                        datas.append([target_bussiness, Target_City, get_day_with_suffix()] + data)

            SheetData('https://docs.google.com/spreadsheets/d/1MWCyGVEv_ZsoIKlcD058FLDj0ULyq027TXGnH6je0X4/edit?gid=0#gid=0', datas, 'Yeld Leads')
            print([len(filtered_links), len(filtered_names)])

            i += 10

        else:
            print(response.text)
            print(response.status_code)


def GetDetails(driver, name, link):
    # response = requests.get(link, cookies=cookies, headers=headers)
    # if response.status_code == 200:
    driver.get(link)
    sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(1)

    # pagesource = openSite(link)
    tree = html.fromstring(driver.page_source)
    reviews = tree.xpath('//a[@href="#reviews"]/text()')[0] if tree.xpath('//a[@href="#reviews"]/text()') else ''
    ratings = tree.xpath('//a[@href="#reviews"]/ancestor::span/preceding-sibling::span/text()')[0] if tree.xpath('//a[@href="#reviews"]/ancestor::span/preceding-sibling::span/text()') else ''
    website = tree.xpath('//p[text()="Business website"]/following-sibling::p//a/text()')[0] if tree.xpath('//p[text()="Business website"]/following-sibling::p//a/text()') else ''
    phone = tree.xpath('//p[text()="Phone number"]/following-sibling::p/text()')[0] if tree.xpath('//p[text()="Phone number"]/following-sibling::p/text()') else ''
    address = tree.xpath('//a[text()="Get Directions"]/ancestor::p/following-sibling::p/text()')[0] if tree.xpath('//a[text()="Get Directions"]/ancestor::p/following-sibling::p/text()') else ''
    owner_name = tree.xpath('//p[text()="Business Owner"]/ancestor::div[1]/preceding-sibling::p/text()')[0] if tree.xpath('//p[text()="Business Owner"]/ancestor::div[1]/preceding-sibling::p/text()') else ''
    bussiness_details = tree.xpath('//button[@aria-label="More information about the business. Opens a modal."]/preceding::div[1]//p//span//span/text()')
    bussiness_details = '\n'.join(bussiness_details)

    if reviews != '':
        reviews = reviews.replace('(', '').replace(')', '').replace(' review', '')
        reviews = reviews.replace('s', '')
        reviews = int(reviews)
    else:
        reviews = 0

    if website != '' and reviews <= 15:
        email = ''
    else:
        email = ''

    if reviews <= 15:
        data = [name, owner_name, reviews, ratings, website, email, phone, address, bussiness_details, link]
        print(data)
        return data
    else:
        return []


# //p[text()="Business Owner"]/ancestor::div[1]/preceding-sibling::p

cities = CityNames()

ch = []
rows = []
with open('us_cities_states_counties.csv', mode='r', newline='') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    # Read the rest of the rows
    for row in csv_reader:
        r = row[0].split('|')
        if r[0] not in ch and r[1] != 'PR':
            rows.append(r)
            ch.append(r[0])

for i, row in enumerate(rows):
    # if row[0].lower() != "kingshill".lower():
        # for i, city in enumerate(cities):
    print(f'{i}: {row[0]}, {row[1]}')
    GetLinks(cookies, headers, 'Plumbers', f'{row[0]}, {row[1]}')

# for city in cities:
#     GetLinks(cookies, headers, 'Fitness Studios and Gyms', city)