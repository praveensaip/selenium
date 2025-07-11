from pages.base import baseclass
from pages.widgetCreation import Widget_Creation
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from faker import Faker
import time

faker = Faker()
class advancedconfig(baseclass):
    url = "https://quickreports-stage.anbetrack.com/reportDesigner"
    attribute_left = (By.XPATH,'//div[@class="advanceConfigCollapse"]//p')
    attribute_locator = (By.XPATH,'//div[@class="advanceConfigCollapse"]/div')
    list_of_values = []

    def random_name(self):
        return faker.first_name() + faker.last_name()


    def get_url(self):
        self.findusingvisibility(By.XPATH,'//span[normalize-space(.)="Property"]')
        assert self.driver.current_url == self.url

    def get_all_values(self,values):
        value = self.findelements(*self.attribute_left)
        value1 = [i.text.strip() for i in value]
        index1 = value1.index('Values')
        index2 = value1.index('Values')+1
        category = value1[1:index1]
        value = value1[index2:]
        for i in value1:
            if i.strip() in ('Category','Values'):
                print()
            else:
                print("valuess", values)
                print("valuess", i.strip())
                assert i.strip() in values
        return category,value

    def checktogglefilter_paginations(self):
        self.findusingvisibility(By.XPATH,'//div[contains(@class,"el-switch is-checked")]')
        for i in self.findelements(By.XPATH,'//div[contains(@class,"el-switch is-checked")]'):
            print("iii",i)
            assert 'is-checked' in i.get_attribute("class")
    
    def title_and_subtitle(self):
        random_name = lambda : faker.first_name()+faker.last_name()
        titles = ['Title','Sub Title']
        names = []
        for i in titles:
            name = random_name()
            val = self.findelement(By.XPATH,f'//label[normalize-space(.)="{i}"]/ancestor::div[@class="el-form-item asterisk-left"]//input')
            val.clear()
            val.send_keys(name)
            names.append(name)
        return names
    
    def get_title_and_subtitle_values(self):
        titles = ['Title','Sub Title']
        names = []
        for i in titles:
            value = self.findelement(By.XPATH,f'//label[normalize-space(.)="{i}"]/ancestor::div[@class="el-form-item asterisk-left"]//input')
            names.append(value.get_attribute('value'))
        return names
    
    def attributes_in_decimal_places(self):
        data={}
        self.click(By.XPATH,'//div[normalize-space(.)="Decimal Places"]/ancestor::div[@class="el-form-item asterisk-left"]//i[@class="el-icon el-select__caret el-select__icon"]')
        time.sleep(3)
        len_elements = self.findelements(By.XPATH,'//div[@class="el-popper is-pure is-light el-select__popper" and @aria-hidden="false"]//ul//li')
        for i,j in enumerate(len_elements,1):
            if i == 1:
                assert j.is_displayed()
                item_text = j.text.strip()
                j.click()
                ele = self.findelement(By.XPATH,'(//div[normalize-space(.)="Decimal Places"]/ancestor::div[@class="el-form-item asterisk-left"]//input)[2]')
                ele.clear()
                ele.send_keys(int(5))
                time.sleep(2)
                data[item_text] = 5
            else:
                self.click(By.XPATH,'//div[normalize-space(.)="Decimal Places"]/ancestor::div[@class="el-form-item asterisk-left"]//i[@class="el-icon el-select__caret el-select__icon"]')
                time.sleep(3)
                assert j.is_displayed()
                item_text = j.text.strip()
                j.click()
                ele = self.findelement(By.XPATH,'(//div[normalize-space(.)="Decimal Places"]/ancestor::div[@class="el-form-item asterisk-left"]//input)[2]')
                ele.clear()
                ele.send_keys(int(5))
                time.sleep(2)
                data[item_text] = 5
        return data
    
    def get_values_attributes_in_decimal_places(self):
        data={}
        self.click(By.XPATH,'//div[normalize-space(.)="Decimal Places"]/ancestor::div[@class="el-form-item asterisk-left"]//i[@class="el-icon el-select__caret el-select__icon"]')
        time.sleep(3)
        len_elements = self.findelements(By.XPATH,'//div[@class="el-popper is-pure is-light el-select__popper" and @aria-hidden="false"]//ul//li')
        for i,j in enumerate(len_elements,1):
            if i == 1:
                assert j.is_displayed()
                item_text = j.text.strip()
                j.click()
                ele = self.findelement(By.XPATH,'(//div[normalize-space(.)="Decimal Places"]/ancestor::div[@class="el-form-item asterisk-left"]//input)[2]')
                data[item_text] = ele.get_attribute("value")
            else:
                self.click(By.XPATH,'//div[normalize-space(.)="Decimal Places"]/ancestor::div[@class="el-form-item asterisk-left"]//i[@class="el-icon el-select__caret el-select__icon"]')
                time.sleep(3)
                assert j.is_displayed()
                item_text = j.text.strip()
                j.click()
                ele = self.findelement(By.XPATH,'(//div[normalize-space(.)="Decimal Places"]/ancestor::div[@class="el-form-item asterisk-left"]//input)[2]')
                data[item_text] = ele.get_attribute("value")
        return data
    
    def change_header_name(self):
        data={}
        self.click(By.XPATH,'//div[normalize-space(.)="Customize Column Labels"]/ancestor::div[@class="el-form-item asterisk-left"]//i[@class="el-icon el-select__caret el-select__icon"]')
        time.sleep(3)
        len_elements = self.findelements(By.XPATH,'//div[@class="el-popper is-pure is-light el-select__popper" and @aria-hidden="false"]//ul//li')
        for i,j in enumerate(len_elements,1):
            if i == 1:
                assert j.is_displayed()
                item_text = j.text.strip()
                j.click()
                name = self.random_name()
                time.sleep(2)
                ele = self.findelement(By.XPATH,'(//div[normalize-space(.)="Customize Column Labels"]/ancestor::div[@class="el-form-item asterisk-left"]//input)[2]')
                ele.clear()
                ele.send_keys(name)
                time.sleep(2)
                data[item_text] = name
            else:
                self.click(By.XPATH,'//div[normalize-space(.)="Customize Column Labels"]/ancestor::div[@class="el-form-item asterisk-left"]//i[@class="el-icon el-select__caret el-select__icon"]')
                time.sleep(3)
                assert j.is_displayed()
                item_text = j.text.strip()
                j.click()
                name = self.random_name()
                time.sleep(2)
                ele = self.findelement(By.XPATH,'(//div[normalize-space(.)="Customize Column Labels"]/ancestor::div[@class="el-form-item asterisk-left"]//input)[2]')
                ele.clear()
                ele.send_keys(name)
                time.sleep(2)
                data[item_text] = name
        return data
    
    def get_values_on_change_header_name(self):
        data={}
        self.click(By.XPATH,'//div[normalize-space(.)="Customize Column Labels"]/ancestor::div[@class="el-form-item asterisk-left"]//i[@class="el-icon el-select__caret el-select__icon"]')
        time.sleep(3)
        len_elements = self.findelements(By.XPATH,'//div[@class="el-popper is-pure is-light el-select__popper" and @aria-hidden="false"]//ul//li')
        for i,j in enumerate(len_elements,1):
            if i == 1:
                assert j.is_displayed()
                item_text = j.text.strip()
                j.click()
                name = self.random_name()
                time.sleep(2)
                ele = self.findelement(By.XPATH,'(//div[normalize-space(.)="Customize Column Labels"]/ancestor::div[@class="el-form-item asterisk-left"]//input)[2]')
                data[item_text] = ele.get_attribute("value")

            else:
                self.click(By.XPATH,'//div[normalize-space(.)="Customize Column Labels"]/ancestor::div[@class="el-form-item asterisk-left"]//i[@class="el-icon el-select__caret el-select__icon"]')
                time.sleep(3)
                assert j.is_displayed()
                item_text = j.text.strip()
                j.click()
                name = self.random_name()
                time.sleep(2)
                ele = self.findelement(By.XPATH,'(//div[normalize-space(.)="Customize Column Labels"]/ancestor::div[@class="el-form-item asterisk-left"]//input)[2]')
                data[item_text] = ele.get_attribute("value")
        return data
    
    def update_advanced_config(self):
        self.findusingvisibility(By.XPATH,'//span[normalize-space(.)="Update"]/ancestor::button[@aria-disabled="false"]')
        self.findelement(By.XPATH,'//span[normalize-space(.)="Update"]/ancestor::button[@aria-disabled="false"]').click()

    # incomplete function::::
    def validate_decimal_values(self,index_value,values):
        self.chart_edit(index_value)
        self.findusingvisibility(By.XPATH,'//span[normalize-space(.)="Property"]')
        assert 'reportDesigner' in self.driver.current_url
        self.get_all_values(values)

    def get_all_provided_values(self,index_value):
        page = Widget_Creation(self.driver)
        page.chart_edit(index_value)
        value1 = self.get_title_and_subtitle_values()
        value2 = self.get_values_attributes_in_decimal_places()
        value3 = self.get_values_on_change_header_name()
        value4 = self.validate_grid_chart()
        return value1,value2,value3,value4

    def validate_grid_chart(self):
        self.findusingvisibility(By.XPATH,'//div[@class="el-row advancedConfigRow"]')
        assert self.findelement(By.XPATH,'//div[@class="el-row advancedConfigRow"]')
        title = self.findelement(By.XPATH,'//div[@class="el-row advancedConfigRow"]//p')
        sub_title = self.findelement(By.XPATH,'//div[@class="el-row advancedConfigRow"]//p/following-sibling::span')
        headers = self.findelements(By.XPATH,'//div[contains(@class,"advancedConfigRow")]//div[@class="el-table__header-wrapper"]//thead//tr//th')
        header_value = [i.text.strip() for i in headers]
        li_array = []
        rows = self.findelements(By.XPATH,'//div[contains(@class,"advancedConfigRow")]//div[@class="el-table__body-wrapper"]//tbody//tr')
        for row in rows:
            cells = row.find_elements(By.TAG_NAME,'td')
            li_array.append([cell.text.strip() for cell in cells])
        print("li_array", li_array)

        return title.text.strip(),sub_title.text.strip(),header_value, li_array





