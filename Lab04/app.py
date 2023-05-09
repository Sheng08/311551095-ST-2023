import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.options import Options

## Setup chrome options
options = Options()
options.add_argument('--headless')  # Ensure GUI is off
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')

## Chrome Driver
service = ChromiumService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# ========================= Part A =========================
driver.get("https://www.nycu.edu.tw/")
driver.maximize_window()

# news
driver.find_element("xpath", "//ul[@id='menu-1-9942884']//a[@title='新聞'][@class='elementor-item']").click()
time.sleep(1)

# first news
driver.find_element("xpath", "//div[@class='eael-tabs-content']//li[1]/a").click()
time.sleep(1)

# title
text = driver.find_element("xpath", '//article/header/h1').text
print(text)
print("\n")
time.sleep(1)

# content
content = driver.find_element("xpath", '//article/div').text
print(content)
time.sleep(1)

# ========================= Part B =========================
# open a new browser tab
driver.execute_script("window.open('about:blank', 'secondtab');")

# It is switching to second tab now
driver.switch_to.window("secondtab")

# open google
driver.get('https://www.google.com/')
time.sleep(2)
search = driver.find_element("name", "q")
driver.implicitly_wait(5)

# search Student ID
search.clear()
search.send_keys("311551095")
search.send_keys(Keys.RETURN)
time.sleep(2)

# search Student ID result
search_start = 1
search_count = 0
while True:
    try:
        second_search = driver.find_element("xpath", f'//*[@id="rso"]/div[{search_start}]//*[@data-sokoban-container]//h3').text
        search_count += 1
        if search_count == 2:
            print(f"\n{second_search}")
            break
    except:
        pass
    search_start += 1

# close two tabs
driver.quit()
