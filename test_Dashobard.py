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
import pytest,time
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
        d = landingpage(driver)
        d.assertingicon()
        d.matched()
        get_localstorage()

class TestAccessingQUICKreports:
    length = 2
    open_url = 'https://plus-stage.anbetrack.com/#/'
    landing_url = 'https://quickreports-stage.anbetrack.com/reportList'
    expected_url = 'https://quickreports-stage.anbetrack.com/reportDesigner'
    model_and_attributes = [("Dash Board Chart",["Calcualted Incentive","Calculated Kw","Calculated Kwh","id"]),
                            ("Project Inhouse Anb",["id","kw","kwh","Project Code","Project Name"]),
                            ("Dash Board Chart",["Calcualted Incentive","Calculated Kw","Calculated Kwh","id","Updated By"])]
    
    @pytest.mark.skip(reason="Not Implemented")
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
                page.waitingforgridapprear()
                page.button_click()
                page.report_selection("dashboard")
                for i in range(self.length+1):
                    print("iiii",i)
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
                    # page.resize_of_the_widget(driver,i+1)
                    if i == 0:
                        page.report_save(report_name)
                        print("self.name",report_name)
                        # time.sleep(2)
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
            else:
                Testlogin.test_login(self,driver,waitforelementinvisibility,get_localstorage)
                self.test_login_quickreports(driver,set_token,waitforelementinvisibility,get_localstorage)

    # @pytest.mark.skip(reason="not implemented")
    def test_report_get(self,driver,set_token):
        set_token(self.open_url, self.landing_url,'localstorage')
        page = listpage(driver)
        page.matched()
        page.assertingicon()
        page.report_select("Lauren Lee")
        for i in range(self.length+1):  
            page1 = Widget_Creation(driver)
            time.sleep(10)
            page1.chart_edit(i)
            advancedconfigiruration = advancedconfig(driver)
            advancedconfigiruration.get_url()
            self.a,self.b = advancedconfigiruration.get_all_values(self.model_and_attributes[i][1])
            print(self.a,self.b)
            advancedconfigiruration.checktogglefilter_paginations() 
            self.title,self.sub_title = advancedconfigiruration.title_and_subtitle()
            print(self.title,self.sub_title)
            self.deciaml_places = advancedconfigiruration.attributes_in_decimal_places()
            print("decimal_places",self.deciaml_places)
            self.change_header_name = advancedconfigiruration.change_header_name()
            print("header_name",self.change_header_name)
            advancedconfigiruration.update_advanced_config()
            advancedconfigiruration.get_url()
            self.get_title_subtitle,self.get_decimal_values,self.get_header_value,self.grid_values = advancedconfigiruration.get_all_provided_values(i)
            print("header_name",self.get_title_subtitle,self.get_decimal_values,self.get_header_value)
            print("grid_values", self.grid_values)

            assert self.grid_values[0] in self.get_title_subtitle
            assert self.grid_values[1] in self.get_title_subtitle
            assert self.grid_values[2] == list(self.get_header_value.values())

            assert self.title in self.get_title_subtitle
            assert self.sub_title in self.get_title_subtitle
            assert self.change_header_name == self.get_header_value
            for key in self.deciaml_places:
                assert key in self.get_decimal_values
                assert self.deciaml_places[key] == int(self.get_decimal_values[key])
            
            header_value = []
            index = []
            for i in self.deciaml_places:
                if i in self.get_header_value:
                    value = list(self.get_header_value.keys())
                    index.append(value.index(i))
                    header_value.append(self.get_header_value[i])
            print("headerss", header_value)
            print("indexxx", index)

            for i in self.grid_values[3]:
                for j in index: 
                    value = i[j].split('.')[1]
                    assert len(value) == 5
            
                
            print(self.title,self.sub_title,self.get_title_subtitle)
            advancedconfigiruration.update_advanced_config()
            advancedconfigiruration.get_url()
        page = Widget_Creation(driver)
        page.update()
        time.sleep(3)
            
            




    



    