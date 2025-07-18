from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.base import baseclass
from pages.login import login
from pages.landinpage import landingpage
from pages.quicklistpage import listpage
from pages.widgetCreation import Widget_Creation
from pages.advanced_config import advancedconfig
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.tabular_reportDesigner import tabular_designerpage


import time
import pytest
from faker import Faker




faker = Faker()
random_name = lambda : faker.first_name()+" "+faker.last_name()
report_name = random_name()

# @pytest.mark.skip(reason="Not Implemented")
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

class TestAccessingQUICKreports():
    length = 2
    open_url = 'https://plus-stage.anbetrack.com/#/'
    landing_url = 'https://quickreports-stage.anbetrack.com/reportList'
    expected_url = 'https://quickreports-stage.anbetrack.com/reportDesigner'
    model_and_attributes = [("Dash Board Chart",["Calcualted Incentive","Calculated Kw","Calculated Kwh","id"]),
                            ("Project Inhouse Anb",["id","kw","kwh","Project Code","Project Name"]),
                            ("Dash Board Chart",["Calculated Kw","Calculated Kwh","id","Updated By"])]
    

    def test_login_quickreports(self,driver, set_token,waitforelementinvisibility,get_localstorage):
        print("self.name1", report_name)
        set_token(self.open_url, self.landing_url,'localstorage')
        error_ele = None
        try:
            error_ele = WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH,'//h1[text()="503 Service Temporarily Unavailable"]')))
            print("error_ele",error_ele)
        except Exception:
            pass
        if not error_ele:
            page = listpage(driver)
            page.matched()
            window = page.window_navigate()
            print("window", window)
            page.waitingforgridapprear()
            page.button_click()
            page.report_selection("all models")
            tabular = tabular_designerpage(driver)
            value = tabular.model_selction("Dash Board Chart")
            before_header_value = tabular.get_header_value()
            print("elemets", before_header_value)
            unique_123 = list(set([j for i in before_header_value for j in i]))
            print("unittt", unique_123)
            for i in value[1:]:
                assert i in unique_123
            page1 = Widget_Creation(driver)
            before,after = tabular.change_order()
            after_header_value = tabular.get_header_value()
            print("after_list",after_header_value[0],after)
            assert after_header_value[0] == after[0:5]
            tabular.view_preview()
            preview_header_value = tabular.get_header_value()
            tabular.click_design()
            page1.report_save(report_name)
            print("preview_header_value",preview_header_value[0])
            assert preview_header_value[0][0:5] == after[0:5]
            print("previewq", preview_header_value[0][0:5], after[0:5])
            tabular.view_preview()
            tabular.export('CSV')

        else:
            Testlogin.test_login(self,driver,waitforelementinvisibility,get_localstorage)
            self.test_login_quickreports(driver,set_token,waitforelementinvisibility,get_localstorage)
            a= baseclass(driver)
            a.window_navigate()
