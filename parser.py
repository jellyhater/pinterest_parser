from selenium import webdriver
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import json


class PinterestParser:
    def __init__(self, query):
        self.query = query
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(f'https://ru.pinterest.com/search/pins/?q={self.query}')

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
            src = srcset.split(' ')[-2] if srcset else link.get('src')
            prompt = link.get('alt')
            data["src"].append(src)
            data["prompt"].append(prompt)
        return data

    def save_data(self, filename, data):
        with open(f"{filename}.json", 'w') as f:
            json.dump(data, f)
