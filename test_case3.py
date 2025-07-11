from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.base import baseclass
from pages.login import login
from pages.landinpage import landingpage
from pages.quicklistpage import listpage
import pytest

import time

@pytest.mark.skip(reason="Not Implemented")
class Testlogin:
    def test_login(self,driver,waitforelementinvisibility,get_localstorage):
        driver.get('https://plus-stage.anbetrack.com/#/')
        l_page = login(driver,'praveen_inhouse','Kumar@1999')
        l_page.enter_username()
        l_page.enter_password()
        l_page.click_login()
        waitforelementinvisibility(By.XPATH,'//div[@class="el-loading-spinner"]')
        d = landingpage(driver)
        d.assertingicon()
        d.matched()
        get_localstorage()

class TestAccessingQUICKreports:
    open_url = 'https://plus-stage.anbetrack.com/#/'
    landing_url = 'https://quickreports-stage.anbetrack.com/reportList'
    report_path = (By.XPATH,'//span[normalize-space(.)="New Report"]')
    select_report = (By.XPATH,'//div[@class="el-col el-col-24 newReportSelectLeft"]//p')
    grid_visible = (By.XPATH,'//table//tbody')

    def test_login_quickreports(self,driver, set_token):
        set_token(self.open_url, self.landing_url,'localstorage')
        driver.refresh()
        a = baseclass(driver)
        a.findusingelement(*self.grid_visible)
        a.click(*self.report_path)
        a.findusingvisibility(*self.select_report)
        da = a.findelements(*self.select_report)
        count = 0
        for index,value in enumerate(da):
            if value.text.strip() == 'All Models':
                count +=1
                if count == 1:
                    value.click()
                    time.sleep(10)
            
        




    



    