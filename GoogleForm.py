from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from time import sleep
from datetime import datetime

def cureent_time():
    now = datetime.now()
    formatted_now = now.strftime("%H:%M:%S")

    return formatted_now

def openSite():

    service = Service(r'chromedriver.exe')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    chrome_options.add_argument(f"--user-agent={user_agent}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    driver.get(f'https://forms.gle/2c3Jhkzvw1aPb5SA8')


    return driver




def FillResponses(driver):
    gender = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="listitem"][1]//div[@role="radio"]')))
    gender_random = random.randint(0, 1)
    driver.execute_script("arguments[0].scrollIntoView();", gender[gender_random])
    gender[gender_random].click()

    age = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="listitem"][2]//div[@role="radio"]')))
    age_random = random.randint(0, 5)
    driver.execute_script("arguments[0].scrollIntoView();", age[age_random])
    age[age_random].click()

    qualification = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="listitem"][3]//div[@role="radio"]')))
    if age_random == 0 or age_random == 1:
        qualification_random = random.randint(0, 1)
    else:
        qualification_random = random.randint(1, 2)
    driver.execute_script("arguments[0].scrollIntoView();", qualification[qualification_random])
    qualification[qualification_random].click()

    martial_status = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="listitem"][4]//div[@role="radio"]')))
    if age_random == 0 and gender_random == 1:
        martial_status_random = random.randint(0, 1)
    elif age_random == 0 and gender_random == 0:
        martial_status_random = 0
    elif age_random > 0 and gender_random == 1:
        martial_status_random = 1
    else:
        martial_status_random = random.randint(0, 1)
    driver.execute_script("arguments[0].scrollIntoView();", martial_status[martial_status_random])
    martial_status[martial_status_random].click()

    monthly_income = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="listitem"][5]//div[@role="radio"]')))
    if age_random == 0:
        monthly_income_random = 0
    elif age_random == 1:
        monthly_income_random = random.randint(1, 2)
    elif age_random == 2 or age_random == 3:
        monthly_income_random = random.randint(2, 3)
    else:
        monthly_income_random = 3
    driver.execute_script("arguments[0].scrollIntoView();", monthly_income[monthly_income_random])
    monthly_income[monthly_income_random].click()

    brand = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="listitem"][6]//div[@role="radio"]')))
    brand_random = random.randint(0, 7)
    driver.execute_script("arguments[0].scrollIntoView();", brand[brand_random])
    brand[brand_random].click()

    for i in range(8, 37):
        try:
            rating = WebDriverWait(driver, 2).until(EC.presence_of_all_elements_located((By.XPATH, f'//div[@role="listitem"][{i}]//div[@role="radio"]')))
            rating_random = random.randint(0, 4)
            driver.execute_script("arguments[0].scrollIntoView();", rating[rating_random])
            rating[rating_random].click()
        except:
            pass

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Submit"]'))).click()

driver = openSite()
for i in range(15):
    FillResponses(driver)
    sl = random.randint(300, 600)
    time_taken = f'{int(sl/60)}: {sl%60}'
    print(f'Iteration: {i + 1} -  Time Taken: {time_taken} - Current Time: {cureent_time()}')
    sleep(sl)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[text()="Submit another response"]'))).click()

driver.quit()
