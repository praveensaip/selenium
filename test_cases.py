from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.base import baseclass
from pages.login import login
from pages.landinpage import landingpage
from pages.quicklistpage import listpage
from pages.base import baseclass
from pages.widgetCreation import Widget_Creation
from pages.advanced_config import advancedconfig
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time
import pytest
from faker import Faker




faker = Faker()
random_name = lambda : faker.first_name()+" "+faker.last_name()
report_name = random_name()

@pytest.mark.skip(reason="Not Implemented")
class Testlogin:
    def test_login(self,driver,waitforelementinvisibility,get_localstorage):
        driver.get('https://plus-stage.anbetrack.com/#/')
        l_page = login(driver,'praveen_inhouse','Kumar@1999')
        l_page.enter_username()
        l_page.enter_password()
        l_page.click_login()
        waitforelementinvisibility(By.XPATH,'//div[@class="el-loading-spinner"]')
        driver.execute_script("window.open('https://plus-stage.anbetrack.com/track/#/workarea/modelgrid/eeProjectsinhouse')")
        d = landingpage(driver)
        d.assertingicon()
        d.matched()
        get_localstorage()

class TestAccessingQUICKreports:
    length = 0
    open_url = 'https://plus-stage.anbetrack.com/#/'
    landing_url = 'https://quickreports-stage.anbetrack.com/reportList'
    expected_url = 'https://quickreports-stage.anbetrack.com/reportDesigner'
    model_and_attributes = [("Dash Board Chart",["Calcualted Incentive","Calculated Kw","Calculated Kwh","id"]),
                            ("Project Inhouse Anb",["id","kw","kwh","Project Code","Project Name"]),
                            ("Dash Board Chart",["Calculated Kw","Calculated Kwh","id","Updated By"])]
    

    def test_report_get(self,driver,set_token):
        # driver.set_window_size(1920, 1080)
        set_token(self.open_url, self.landing_url,'localstorage')
        page = listpage(driver)
        page.matched()
        page.assertingicon()
        page.report_select("query accessor check")
        WebDriverWait(driver,20).until(
            EC.visibility_of_element_located((By.XPATH,'//span[normalize-space(.)="Order and Group"]'))
        )
        assert 'reportDesigner' in driver.current_url
        ele = driver.find_element(By.XPATH,'//span[normalize-space(.)="Order and Group"]')
        ele.click()
        time.sleep(2)
        ele = driver.find_element(By.XPATH,'//div[@class="el-tree tree addColumnContent"]//span[normalize-space(.)="Context_Instance"]')
        ele1 = driver.find_element(By.XPATH,'//div[@class="el-tree tree addColumnContent"]//span[normalize-space(.)="simple_list"]')
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'})",ele)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});",ele1)
        print(ele.location)
        print(ele1.location)
        aa = ele.location
        bb = ele1.location
        ee = bb['x'] - aa['x']
        ee1 = bb['y'] - aa['y']+30
        print("Offsets to move:", ee, ee1)


        ActionChains(driver).click_and_hold(ele).pause(0.2).move_by_offset(ee,300).pause(0.2).release().perform()
        driver.find_element(By.XPATH,'//span[text()="Save"]').click()
        driver.find_element(By.XPATH,'//span[normalize-space(.)="Update"]').click()
        time.sleep(5)

        # for i in range(self.length+1):  
        #     page1 = Widget_Creation(driver)
        #     page1.chart_edit(i)
        #     page1.resize_of_the_widget(driver=driver)
        #     page1.update()

    @pytest.mark.skip(reason="Not Implemented")
    def test_login_quickreports(self,driver, set_token):
        print("self.name1",report_name )
        set_token(self.open_url, self.landing_url,'localstorage')
        page = listpage(driver)
        page.matched()
        page.waitingforgridapprear()
        page.button_click()
        page.report_selection("dashboard")
        for i in range(self.length+1):
            page = Widget_Creation(driver)
            page.click_button("widget")
            page.assert_handling()
            page.select_chart_types(expected_url=self.expected_url)
            page.checking_attributes(*self.model_and_attributes[i])
            page.check_attribute_selected(self.model_and_attributes[i][1])
            self.value = page.selected_attributes_list()
            print("valuee", self.value)
            page.button_not_enabled("Advanced Configuration")
            page.button_not_enabled("Create")
            page.chart_selection("Grid View")
            page.button_enabled("Advanced Configuration")
            page.button_enabled("Create")
            if i == 0:
                page.report_save(report_name)
                print("self.name",report_name)
                # time.sleep(2)
                page.resize_of_the_widget(driver)
                page.update()
                time.sleep(10)
            elif i == self.length:
                page.update()
                page.click_cancel()
                base = listpage(driver)
                base.waitingforgridapprear()
                time.sleep(2)
            else:
                print("updated")
                page.update()
                time.sleep(2)
            