import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base import baseclass

class login(baseclass):
    def __init__(self,driver, username, password):
        super().__init__(driver)
        self.driver = driver
        self.username = username
        self.password = password
        self.u_xpath = (By.XPATH,'//input[@id="name"]')
        self.p_xpath = (By.XPATH,'//input[@type="password"]')
        self.l_xpath = (By.XPATH,'//span[text()="Sign In "]')

    
    def enter_username(self):
        self.type(*self.u_xpath,self.username)

    def enter_password(self):
        self.type(*self.p_xpath,self.password)
    
    def click_login(self):
        self.click(*self.l_xpath)



