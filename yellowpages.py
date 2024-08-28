from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from check import get_email
from remove_duplicates import remove_duplication
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from datetime import datetime
from check import CityNames
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

def SheetData(spreadsheet_url, data, worksheet_name):
    credentials_path = 'key.json'
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    gc = gspread.authorize(creds)
    sh = gc.open_by_url(spreadsheet_url)
    worksheet = sh.worksheet(worksheet_name)
    worksheet.append_rows(data)


cookies = {
    'vrid': 'd9bdfce0-c340-4d28-baac-22fdd71ec97a',
    '_ga': 'GA1.1.798524117.1721409714',
    's_ecid': 'MCMID%7C64186042559463483800470315401258406388',
    's_prop70': 'July',
    's_prop71': '29',
    'location': 'geo_term%3ALos%20Angeles%2C%20CA%7Clat%3A34.0522342%7Clng%3A-118.2436849%7Ccity%3ALos%20Angeles%7Cstate%3ACA%7Cdisplay_geo%3ALos%20Angeles%2C%20CA',
    's_nr': '1721409742555',
    '__gsas': 'ID=18e69de77ef3bc50:T=1721409744:RT=1721409744:S=ALNI_MZGi9cLqkPuLg7v16pcMQXcXXghIw',
    'bucket': 'ypu%3Aypu%3Adefault',
    'bucketsrc': 'default',
    's_otb': 'false',
    'zone': '300',
    'AMCVS_A57E776A5245AEA80A490D44%40AdobeOrg': '1',
    'AMCV_A57E776A5245AEA80A490D44%40AdobeOrg': '-1303530583%7CMCIDTS%7C19930%7CMCMID%7C64186042559463483800470315401258406388%7CMCAAMLH-1722618538%7C9%7CMCAAMB-1722618538%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1722020938s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.3.0',
    's_cc': 'true',
    'search_terms': 'gym',
    'sorted': 'false',
    '_pbjs_userid_consent_data': '3524755945110770',
    '_lr_retry_request': 'true',
    '_lr_env_src_ats': 'false',
    'pbjs-unifiedid': '%7B%22TDID%22%3A%221b4f2d70-8d43-4b2c-893c-44740664a7ca%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222024-06-26T17%3A16%3A18%22%7D',
    'pbjs-unifiedid_last': 'Fri%2C%2026%20Jul%202024%2017%3A16%3A19%20GMT',
    'panoramaId_expiry': '1722100579447',
    '_cc_id': 'b1d1a02bfbcf3b385df3cc36fb5da350',
    'panoramaId': '73a211f9dfda8dfac6b799208f9da9fb927adfd50a8019bb9f8ebacd534b4380',
    '__gads': 'ID=b703c0b02327df2f:T=1722013781:RT=1722014650:S=ALNI_MZm9yp24vr6yIlVGHp9qjk8ykxArg',
    '__gpi': 'UID=00000eb4763283ea:T=1722013781:RT=1722014650:S=ALNI_MYw__nvbrppneRar7GRTH3mVFrdeQ',
    '__eoi': 'ID=8f480580ea60f592:T=1722013781:RT=1722014650:S=AA-Afjb2wqVqUr9NQxB8iekh2cWe',
    'express:sess': 'eyJka3MiOiI1ODkyNzIwNy1mY2Q4LTQ3NzQtOWM0Yy0yNmQ2MmI5OWFhMTIiLCJmbGFzaCI6e30sInByZXZpb3VzUGFnZSI6InNycCJ9',
    'express:sess.sig': 'OhIEoFp7ZJHi9J2Fj5BVGXmR1d8',
    's_prop49': 'search_results',
    's_sq': '%5B%5BB%5D%5D',
    '_ga_0EQTJQH34W': 'GS1.1.1722013738.4.1.1722015068.60.0.0',
    's_tp': '7942',
    's_ppv': 'search_results%2C8%2C8%2C641',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': 'vrid=d9bdfce0-c340-4d28-baac-22fdd71ec97a; _ga=GA1.1.798524117.1721409714; s_ecid=MCMID%7C64186042559463483800470315401258406388; s_prop70=July; s_prop71=29; location=geo_term%3ALos%20Angeles%2C%20CA%7Clat%3A34.0522342%7Clng%3A-118.2436849%7Ccity%3ALos%20Angeles%7Cstate%3ACA%7Cdisplay_geo%3ALos%20Angeles%2C%20CA; s_nr=1721409742555; __gsas=ID=18e69de77ef3bc50:T=1721409744:RT=1721409744:S=ALNI_MZGi9cLqkPuLg7v16pcMQXcXXghIw; bucket=ypu%3Aypu%3Adefault; bucketsrc=default; s_otb=false; zone=300; AMCVS_A57E776A5245AEA80A490D44%40AdobeOrg=1; AMCV_A57E776A5245AEA80A490D44%40AdobeOrg=-1303530583%7CMCIDTS%7C19930%7CMCMID%7C64186042559463483800470315401258406388%7CMCAAMLH-1722618538%7C9%7CMCAAMB-1722618538%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1722020938s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.3.0; s_cc=true; search_terms=gym; sorted=false; _pbjs_userid_consent_data=3524755945110770; _lr_retry_request=true; _lr_env_src_ats=false; pbjs-unifiedid=%7B%22TDID%22%3A%221b4f2d70-8d43-4b2c-893c-44740664a7ca%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222024-06-26T17%3A16%3A18%22%7D; pbjs-unifiedid_last=Fri%2C%2026%20Jul%202024%2017%3A16%3A19%20GMT; panoramaId_expiry=1722100579447; _cc_id=b1d1a02bfbcf3b385df3cc36fb5da350; panoramaId=73a211f9dfda8dfac6b799208f9da9fb927adfd50a8019bb9f8ebacd534b4380; __gads=ID=b703c0b02327df2f:T=1722013781:RT=1722014650:S=ALNI_MZm9yp24vr6yIlVGHp9qjk8ykxArg; __gpi=UID=00000eb4763283ea:T=1722013781:RT=1722014650:S=ALNI_MYw__nvbrppneRar7GRTH3mVFrdeQ; __eoi=ID=8f480580ea60f592:T=1722013781:RT=1722014650:S=AA-Afjb2wqVqUr9NQxB8iekh2cWe; express:sess=eyJka3MiOiI1ODkyNzIwNy1mY2Q4LTQ3NzQtOWM0Yy0yNmQ2MmI5OWFhMTIiLCJmbGFzaCI6e30sInByZXZpb3VzUGFnZSI6InNycCJ9; express:sess.sig=OhIEoFp7ZJHi9J2Fj5BVGXmR1d8; s_prop49=search_results; s_sq=%5B%5BB%5D%5D; _ga_0EQTJQH34W=GS1.1.1722013738.4.1.1722015068.60.0.0; s_tp=7942; s_ppv=search_results%2C8%2C8%2C641',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

def get_links(cookies, headers, targeted_business, city_state):
    i = 1
    while True:
        try:
            params = {
                'search_terms': targeted_business,
                'geo_location_terms': city_state,
                'page': f'{i}',
            }

            response = requests.get('https://www.yellowpages.com/search', params=params, cookies=cookies, headers=headers)
            if response.status_code == 200:
                tree = html.fromstring(response.content)

                if tree.xpath('//h1[contains(text(), "No results found for")]'):
                    break
                cards = tree.xpath('//div[@class="v-card"]')
                links = []
                for l in cards:
                    link = l.xpath('.//h2//a/@href')[0] if l.xpath('.//h2//a/@href') else ''
                    link = f'https://www.yellowpages.com/{link}'
                    reviews = l.xpath('.//div[@class="ratings"]//span[@class="count"]/text()')[0] if l.xpath('.//div[@class="ratings"]//span[@class="count"]/text()') else ''
                    try:
                        reviews = reviews.replace('(', '').replace(')', '')
                        reviews = int(reviews)
                    except:
                        reviews = 0
                    if reviews <= 10:
                        links.append(link)
                # links = tree.xpath('//div[@class="v-card"]//h2//a/@href')
                # links = [f'https://www.yellowpages.com/{link}' for link in links]
                print(f'{i}: {links}')
                GetDetails(cookies, headers, links, targeted_business, city_state)

                i += 1
            else:
                print(response.status_code)
        except:
            input('Change VPN')
def GetDetails(cookies, headers, links, targeted_business, city_state):
    datas = []
    for link in links:
        while True:
            try:
                response = requests.get(link, cookies=cookies, headers=headers)
                if response.status_code == 200:
                    tree = html.fromstring(response.content)
                    business_name = tree.xpath('//h1/text()')[0] if tree.xpath('//h1/text()') else ''
                    phone = tree.xpath('//section[@id="details-card"]//span[text()="Phone: "]/ancestor::p[1]/text()')[0] if tree.xpath('//section[@id="details-card"]//span[text()="Phone: "]/ancestor::p[1]/text()') else ''
                    address = tree.xpath('//section[@id="details-card"]//span[text()="Address: "]/ancestor::p[1]/text()')[0] if tree.xpath('//section[@id="details-card"]//span[text()="Address: "]/ancestor::p[1]/text()') else ''
                    website = tree.xpath('//section[@id="details-card"]//span[text()="Website: "]/following-sibling::a/@href')[0] if tree.xpath('//section[@id="details-card"]//span[text()="Website: "]/following-sibling::a/@href') else ''
                    email = tree.xpath('//section[@id="business-info"]//dd//a[@class="email-business"]/@href')[0].replace('mailto:', '') if tree.xpath('//section[@id="business-info"]//dd//a[@class="email-business"]/@href') else ''
                    # if email == '' and website != '':
                    #     email = get_email(website)
                    extra_phone = tree.xpath('//section[@id="business-info"]//dd[@class="extra-phones"]//p//span[2]/text()')
                    extra_phone = ', '.join(extra_phone)
                    if phone != '' and extra_phone != '' and phone not in extra_phone:
                        phone = f'{phone}, {extra_phone}'
                    elif phone != '' and extra_phone != '' and phone in extra_phone:
                        phone = extra_phone
                    elif phone == '' and extra_phone != '':
                        phone = extra_phone
                    other_links = tree.xpath('//section[@id="business-info"]//dd[@class="weblinks"]//p//a/@href')
                    other_links = ', '.join(other_links)
                    if website != '' and other_links != '' and website not in other_links:
                        website = f'{website}, {other_links}'
                    elif website != '' and other_links != '' and website in other_links:
                        website = other_links
                    elif website == '' and other_links != '':
                        website = other_links

                    general_info = tree.xpath('//section[@id="business-info"]//dd[@class="general-info"]/text()')[0] if tree.xpath('//section[@id="business-info"]//dd[@class="general-info"]/text()') else ''

                    categories = tree.xpath('//section[@id="business-info"]//dd[@class="categories"]//a/text()')
                    categories = ', '.join(categories)
                    other_infos = tree.xpath('//section[@id="business-info"]//dd[@class="other-information"]//p')
                    other_infos = ', '.join([other_info.text_content().replace('\xa0', '') for other_info in other_infos])

                    data = [targeted_business, city_state, get_day_with_suffix(), business_name, phone, address, website, email, general_info, categories, other_infos]
                    print(data)
                    datas.append(data)
                    break
                else:
                    print(response.status_code)
            except:
                input('Change VPN')
                continue
    SheetData('https://docs.google.com/spreadsheets/d/1MWCyGVEv_ZsoIKlcD058FLDj0ULyq027TXGnH6je0X4/edit?gid=1729675550#gid=1729675550', datas, 'YellowPages')


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

# rows = rows[15:]
for i, row in enumerate(rows):
    # if row[0].lower() != "kingshill".lower():
        # for i, city in enumerate(cities):
    print(f'{i}: {row[0]}, {row[1]}')
    get_links(cookies, headers, 'Plumbers', f'{row[0]}, {row[1]}')

# cities = CityNames()
# cities.pop(1)
# for city in cities:
#     get_links(cookies, headers, 'Gym', city)
remove_duplication('https://docs.google.com/spreadsheets/d/1MWCyGVEv_ZsoIKlcD058FLDj0ULyq027TXGnH6je0X4/edit?gid=1729675550#gid=1729675550', 'YellowPages')