from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.support.ui import WebDriverWait

class baseclass:
    def __init__(self,driver):
        self.driver = driver
        self.timeout = 50

    def findelement(self,by,locator):
        return self.driver.find_element(by,locator)

    def findelements(self,by,locator):
        return self.driver.find_elements(by,locator)
    
    def findusingpresense(self, by, locator):
        return WebDriverWait(self.driver,self.timeout).until(Ec.presence_of_element_located((by,locator)))

    def findusingvisibility(self, by, locator):
        return WebDriverWait(self.driver,self.timeout).until(Ec.visibility_of_element_located((by,locator)))

    def findusinginvisibility(self, by, locator):
        return WebDriverWait(self.driver,self.timeout).until(Ec.invisibility_of_element((by,locator)))

    def findusingelement(self, by, locator):
        return WebDriverWait(self.driver,self.timeout).until(Ec.element_to_be_clickable((by,locator)))

    def click(self,by, locator):
        self.findusingvisibility(by,locator).click()
    
    def type(self, by, locator,value):
        val = self.findusingvisibility(by,locator)
        val.clear()
        val.send_keys(value)

    def element_visible(self,by,locator):
        return self.findusingvisibility(by,locator).is_displayed()
    
    def checked(self,by,locator):
        return self.findusingpresense(by,locator).is_selected()
    
    def get_attribute(self,by,locator,attribute):
        return self.findusingpresense(by,locator).get_attribute(attribute)
    
    def matchurl(self,actual_url, expected_url):
        assert actual_url == expected_url, f'{actual_url} is not matched with {expected_url}'  

    def window_navigate(self):
        return self.driver.current_window_handle
        
    
    


