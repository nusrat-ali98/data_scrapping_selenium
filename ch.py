import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import deque
import threading
import warnings
from urllib3.exceptions import InsecureRequestWarning
import time


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


def extract_emails(text):
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_regex, text)


def process_page(current_url, base_url, visited, emails, queue, lock):
    with lock:
        if current_url in visited:
            return
        visited.add(current_url)
    warnings.simplefilter('ignore', InsecureRequestWarning)
    try:
        session = requests.Session()
        retries = 0
        max_retries = 1
        retry_delay = 5
        should_retry = 'www.business.google.com' not in current_url
        while retries < max_retries:
            try:

                response = session.get(current_url , verify = False )
                soup = BeautifulSoup(response.text, 'html.parser')
                page_emails = extract_emails(response.text)
                if page_emails:
                    print(f"Emails found on {current_url}: {page_emails}")
                    with lock:
                        emails.update(page_emails)

                for a_tag in soup.find_all('a', href=True):
                    href = a_tag['href']
                    full_url = urljoin(base_url, href)
                    if urlparse(full_url).netloc == urlparse(base_url).netloc:
                        with lock:
                            if full_url not in visited:
                                queue.append(full_url)
                break
            except requests.exceptions.RequestException as e:
               if should_retry:
                    retries += 1
                    print(f"Request failed: {e}, retrying in {retry_delay} seconds... ({retries}/{max_retries})")
                    time.sleep(retry_delay)
                    continue
               else:
                   print(f"Request failed on {current_url}: {e} (no retries for this URL)")
                   break


    except Exception as e:
        print(f"An unexcepted error occurred as {e}")



def get_all_links(url, base_url, max_pages=5):
    visited = set()
    emails = set()
    queue = deque([url])
    lock = threading.Lock()
    threads = []
    page_count = 0

    while queue and page_count < max_pages:
        if len(threads) >= 5:
            for thread in threads:
                thread.join()
            threads = []

        current_url = queue.popleft()
        page_count += 1
        thread = threading.Thread(target=process_page, args=(current_url, base_url, visited, emails, queue, lock))
        thread.start()
        threads.append(thread)

    # Wait for any remaining threads to finish
    for thread in threads:
        thread.join()

    return list(emails)


def is_valid_email(email):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    if not re.match(email_pattern, email):
        return False
    local_part = email.split('@')[0]
    if local_part[0].isdigit() or re.match(r'^[a-f0-9]{30,}$', local_part):
        return False
    return True


def standardize_url(url):
    url = re.sub(r'^https?://(?:www\.)?', '', url)
    return f'https://www.{url}'


def find_business_email(base_url):
    emails = get_all_links(base_url, base_url, max_pages=5)
    emails = list(set(emails))
    valid_emails = [email for email in emails if is_valid_email(email)]
    em = ', '.join(valid_emails)
    return em



