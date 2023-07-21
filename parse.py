from selenium import webdriver
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import time
import pandas as pd
import json


class PinterestParser:
    def __init__(self, query, scrollnum=1, sleeptimer=10):
        self.query = query
        self.scrollnum = scrollnum
        self.sleeptimer = sleeptimer

        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(options=options)

        self.driver.get(f'https://ru.pinterest.com/search/pins/?q={self.query}')
        time.sleep(10)

    def find_by_xpath(self, obj, attr, name):
        xpath = f"//{obj}[@{attr}='{name}']"
        return self.driver.find_element(By.XPATH, xpath)

    def authorize(self, login, password):
        login_button = self.find_by_xpath("div", "data-test-id", "login-button")
        login_button.click()
        # find and enter email
        email_input_area = self.find_by_xpath("input", "id", "email")
        email_input_area.send_keys(login)
        # find and enter password
        password_input_area = self.find_by_xpath("input", "id", "password")
        password_input_area.send_keys(password)
        # submit
        submit_button = self.find_by_xpath("button", "type", "submit")
        submit_button.click()

        time.sleep(10)

    def scroll(self):
        self.driver.execute_script("window.scrollTo(1,100000)")
        print("scroll-down")

    def get_data(self):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        data = {
            "src": [],
            "prompt": []
        }
        # first pic is account avatar; skip
        for link in soup.findAll('img')[1:]:
            srcset = link.get('srcset')
            # get last link from srcset
            src = srcset.split(' ')[-2]
            prompt = link.get('alt')
            data["src"].append(src)
            data["prompt"].append(prompt)
        return data

    def save_data(self, filename, data):
        ext = filename.split(".")[-1]
        if ext == "json":
            with open(filename, 'w') as f:
                json.dump(data, f)
        elif ext == "csv":
            df = pd.DataFrame(data)
            df.to_csv(filename)
        else:
            print("Unknown extention")


if __name__ == "__main__":
    parser = PinterestParser("khokhloma")
    parser.authorize("login", "password")
    for _ in range(3):
        parser.scroll()
        time.sleep(10)
        data = parser.get_data()
        parser.save_data(f"dataset_{_}.csv", data)


# for link in soup.findAll('a'):
#     pin = link.get('href')
#     if 'pin/' in pin:
#         print(pin)
