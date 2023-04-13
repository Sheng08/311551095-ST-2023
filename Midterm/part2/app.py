import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

## Setup chrome options
options = Options()
# options.add_argument('--headless')  # Ensure GUI is off
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')

## Chrome Driver
service = ChromiumService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# ========================= Part A =========================
# Go to https://docs.python.org/3/tutorial/index.html
driver.get('https://docs.python.org/3/tutorial/index.html')

# Select the language options on the navigation bar (Fig. 1), and choose the Traditional Chinese option. Note that any selenium operation is legal except for changing the URL directly.
Selector_Element = Select(
    driver.find_element(
        "xpath", "//div[@role='navigation']//select[@id='language_select']"))
Selector_Element.select_by_index(8)

# Wait for lanugage translation, then use find_element to get the title and the first paragraph (Fig. 2). Print the title and the first paragraph.
time.sleep(1)
title = driver.find_element("xpath",
                            "//section[@id='the-python-tutorial']//h1").text
ctx = driver.find_element("xpath",
                          "//section[@id='the-python-tutorial']//p[1]").text
print(title)
print(ctx)

# ========================= Part B =========================
# search = driver.find_element("placeholder", "快速搜尋")
# print(search)

time.sleep(20)
# close two tabs
driver.quit()
