from datetime import timedelta, datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import csv
from webdriver_manager.chrome import ChromeDriverManager
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
from ch import standardize_url
from ch import find_business_email
from datetime import datetime

def get_day_with_suffix():
    current_date = datetime.now()
    day = current_date.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

    day_suffix = str(day) + suffix
    return current_date.strftime(f"{day_suffix} %B, %Y")


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

def SheetData(spreadsheet_url, rows_data, headers, worksheet_name):
    while True:
        try:
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
            client = gspread.authorize(creds)
            spreadsheet = client.open_by_url(spreadsheet_url)

            try:
                worksheet = spreadsheet.worksheet(worksheet_name)
            except gspread.exceptions.WorksheetNotFound:
                worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows="100", cols="20")
                worksheet.insert_row(headers, 1)


            worksheet.append_rows(rows_data)
            break
        except:
            sleep(2)
            continue

def openSite(bussiness, State, Country):
    q = f'{bussiness} in {State}, {Country}'
    q = q.replace(" ", "+")
    service = Service(r'chromedriver.exe')
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    chrome_options.add_argument(f"--user-agent={user_agent}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    driver.get(f'https://www.google.com/maps/search/{q}')


    return driver


def getDetails(driver, bussines, state, country):
    scrollable_div = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]')))

    def is_at_bottom():
        return driver.execute_script(
            "return arguments[0].scrollTop + arguments[0].clientHeight >= arguments[0].scrollHeight", scrollable_div)
    while not is_at_bottom():
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
        sleep(5)

    all_links = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="feed"]//div[contains(@class, "fontHeadlineSmall")]/ancestor::div[7]/preceding-sibling::a')))
    print(len(all_links))
    datas = []
    for link in all_links:
        try:
            rev = link.find_element(By.XPATH, './following-sibling::div//span[@role="img"]//span/following-sibling::span').text
            rev = rev.replace('(', '').replace(')', '')
            try:
                rev = int(rev)
            except:
                rev = 0
        except:
            rev = 0
        if rev <= 50:
            while True:
                try:

                    driver.execute_script("arguments[0].scrollIntoView();", link)
                    driver.execute_script("arguments[0].click();", link)
                    sleep(4)
                    try:
                        h1s = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="tablist"]/ancestor::div[2]/preceding-sibling::div[1]//h1')))
                    except:
                        h1s = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="region"]/preceding-sibling::div[3]//h1')))


                    if h1s[0].text == 'Sponsored':
                        bussiness_name = h1s[1].text
                    else:
                        bussiness_name = h1s[0].text
                    try:
                        stars = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@role="tablist"]/ancestor::div[2]/preceding-sibling::div[1]//span[contains(@aria-label, "stars")]/preceding-sibling::span'))).text
                    except:
                        stars = ''
                    try:
                        reviews = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@role="tablist"]/ancestor::div[2]/preceding-sibling::div[1]//span[contains(@aria-label, "reviews")]'))).text
                        reviews = reviews.replace('(', '').replace(')', '')
                        reviews = reviews.replace(', ', '')
                        reviews = int(reviews)
                    except:
                        reviews = 0
                    try:
                        website_ = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@aria-label, "Information for")]//a//div[contains(@class, "fontBodyMedium")]/ancestor::a')))
                        website = website_.get_attribute('href')
                        website = standardize_url(website)
                        email = find_business_email(website)

                    except:
                        email = ''
                        website = ''
                    try:
                        address = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@aria-label, "Information for")]//button[contains(@aria-label, "Address:")]//div[contains(@class, "fontBodyMedium")]'))).text
                    except:
                        address = ''
                    try:
                        number = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@aria-label, "Information for")]//button[contains(@aria-label, "Phone:")]//div[contains(@class, "fontBodyMedium")]'))).text
                    except:
                        number = ''
                    data = [bussines, f'{state}, {country}', get_day_with_suffix(), '', bussiness_name, number, website, stars, reviews, address, email]
                    if reviews <= 50 and data not in datas:
                        datas.append(data)
                        print(data)
                    break
                except Exception as e:
                    print('Exception')
                    sleep(3)
                    continue
    headers = ['Targeted Business', 'Targeted State & Country', 'Scrapping Date', 'Phone Owner Name', 'Bussiness Name', 'Number', 'Website', 'Ratings', 'Reviews Count', 'Address', 'Email', 'Client Updates', 'Email Send Status']
    SheetData('https://docs.google.com/spreadsheets/d/1MWCyGVEv_ZsoIKlcD058FLDj0ULyq027TXGnH6je0X4/edit?pli=1&gid=515691484#gid=515691484', datas, headers, f'{bussines.replace(' ', '_')}_GoogleMap')
    
def start(bussines, state, country):
    driver = openSite(bussines, state, country)
    getDetails(driver, bussines, state, country)
    driver.quit()



with open('top_300_us_cities.csv', mode='r', newline='') as file:
    csv_reader = list(csv.reader(file))





    for i, row in enumerate(csv_reader[48: ], start=1):
        print(row)
        print(f'{i}: {row[0]}, {row[1]}')
        start('Consultant', f'{row[0]}, {row[1]}', 'USA')



