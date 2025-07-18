from selenium import webdriver
from pages.base import baseclass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from faker import Faker
from selenium.webdriver.common.action_chains import ActionChains

class Widget_Creation(baseclass):
    click_1 = (By.XPATH,'//div[@class="el-col el-col-24 el-col-xs-12 el-col-sm-12 el-col-md-12 el-col-lg-12 tr p-t-10 p-b-10"]//button//span')
    click_2 = (By.XPATH, '//div[@class="el-col el-col-24 el-col-xs-12 el-col-sm-12 el-col-md-12 el-col-lg-12 tr p-t-10 p-b-10"]//button//span')
    invisibility = (By.XPATH,'//div[@class="el-loading-spinner"]')
    assert_chart = (By.XPATH, '//div[@class="el-row addNewSheetDialog"]//div//div[@class="el-row"]/child::div//p')
    widgetname_names = ['All Models','SQL']
    ele_visibility = (By.XPATH,'//div[@class="el-col el-col-24 text-center addNewSheetCol"]')
    ele_visibility1 = (By.XPATH,'//button[@class="el-button el-button--text is-active addSheetSelect"]')
    pre_element = (By.XPATH,'//button[contains(@class,"el-button--text") and contains(@class,"is-active")]')
    create_1 = (By.XPATH, '//span[text()="Create"]')
    pie_chart_visible = (By.XPATH,'//i[@class="etp-qr-icon pie-chart fw5"]')
    virtual_list = (By.XPATH, '//div[@class="el-vl__window el-tree-virtual-list"]')
    e_chart_select_card = (By.XPATH,'//div[@class="el-col el-col-24 el-col-lg-24 is-guttered echartSelectCard"]//span')
    click_go = (By.XPATH,'//button[@class="el-button el-button--primary fr"]')
    button_active = (By.XPATH,'//span[normalize-space(.)="Advanced Configuration"]/ancestor::button')
    update_report = (By.XPATH,'//span[normalize-space(.)="Update"]')
    click_cancel_btn = (By.XPATH,'//span[normalize-space(.)="Close"]')
    grid_layout = (By.XPATH, '//div[@class="vue-grid-layout"]')
    edit_chart = (By.XPATH,'//div[@class="vue-grid-layout"]//div[contains(@class,"cssTransforms")]')
    faker = Faker()

    def click_button(self,button_name):
        self.findusingvisibility(*self.click_1)
        self.findusinginvisibility(*self.invisibility)
        for i in self.findelements(*self.click_2):
            if i.is_displayed() and i.text.strip().lower() == button_name:
                i.click()
        
    def assert_handling(self):
        get_widget_name = self.findelements(*self.assert_chart)
        self.findusingvisibility(*self.ele_visibility)
        for i in get_widget_name:
            print("iiiii",i.text.strip())
            assert i.text.strip() in self.widgetname_names
    
    def select_chart_types(self,expected_url):
        select_widget = self.findusingvisibility(*self.ele_visibility1)
        select_widget.click()
        self.findusingpresense(*self.pre_element)
        widget_selection= self.findelement(*self.create_1)
        widget_selection.click()
        self.findusinginvisibility(*self.invisibility)
        visisble = self.findusingvisibility(*self.pie_chart_visible)
        assert visisble.is_displayed()
        print()
        # assert self.matchurl(self.driver.current_url,expected_url)

    def checking_attributes(self,model_name,attributes):
         for _ in range(5):
            scrollable_container = self.findusingvisibility(*self.virtual_list)
            self.driver.execute_script('arguments[0].scrollTop += 300;',scrollable_container)
            time.sleep(1)
            try:
                widget_selection = self.driver.find_element(By.XPATH,f'//span[normalize-space(.)="{model_name}"]/preceding-sibling::i')
                widget_selection.click()
                self.driver.execute_script('arguments[0].scrollTop += 100;',scrollable_container)
                for i in attributes:
                    try:
                        element = WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.XPATH,f'//span[normalize-space(.)="{i}"]')))
                        element.click()
                        print("elementtt", element.text) 
                        assert_ele = WebDriverWait(self.driver,2).until(EC.visibility_of_element_located((By.XPATH,f'//div[@class="el-col el-col-5 tree-card"]//span[normalize-space(.)="{i}"]/preceding-sibling::label')))
                        try:
                            assert 'is-checked' in assert_ele.get_attribute('class')
                            print("asserting", assert_ele.get_attribute('class'))
                        except Exception as e:
                            return str(e)
                    except Exception as e:
                        self.driver.execute_script('arguments[0].scrollTop += 80;',scrollable_container)
            except Exception as e:
                pass
                
    def check_attribute_selected(self,Attributes):
        attributes = self.findelements(*self.e_chart_select_card)
        for i in attributes:
            if i.text.strip().lower() != 'go':
                value = i.text.strip()
                print("valuee", value)
                assert any(value in i.strip() for i in Attributes), f'{value} is not present'

    def selected_attributes_list(self):
        attributes = self.findelements(*self.e_chart_select_card)
        attribute = []
        for i in attributes:
            attribute.append(i.text.strip())
        return attribute
            
    
    def chart_selection(self,chart_name):
        self.findusingvisibility(By.XPATH,f'//div[@id="qr-chart-list"]//button[@title="{chart_name}"]')
        self.findelement(By.XPATH,f'//div[@id="qr-chart-list"]//button[@title="{chart_name}"]').click()
        element = self.findusingvisibility(*self.click_go)
        element.click()
        self.findusinginvisibility(*self.invisibility)



    def button_not_enabled(self,button_name):
        advanced_config = self.findelement(By.XPATH,f'//span[normalize-space(.)="{button_name}"]/ancestor::button')
        assert not advanced_config.is_enabled(), f'{advanced_config} is enabled'

    def button_enabled(self,button_name):
        WebDriverWait(self.driver,self.timeout).until(lambda d: d.find_element(*self.button_active).is_enabled())
        advanced_config = self.findelement(By.XPATH,f'//span[normalize-space(.)="{button_name}"]/ancestor::button')
        assert advanced_config.is_enabled(), f'{advanced_config} is enabled'
        if button_name == "Create":
            advanced_config.click()

            
    def report_save(self, report_name, report_type="tabular"):
        random_name = lambda : self.faker.first_name()+"_"+self.faker.last_name()
        if report_type.lower() == 'dashboard':
            self.findusingvisibility(By.XPATH,'//div[@class="wrap-scrollbar chart-container"]')
            assert self.findelement(By.XPATH,'//div[@class="wrap-scrollbar chart-container"]').is_displayed()
        save_button_click = self.findelement(By.XPATH,'//button//span[normalize-space(.)="Save"]')
        save_button_click.click()
        self.findusingvisibility(By.XPATH,'//div[@class="el-dialog save-lookup saveReport"]')
        click_name = self.findelement(By.XPATH,'//input[@placeholder="Enter the Name"]')
        click_name.send_keys(report_name)
        click_description = self.findelement(By.XPATH,'//input[@placeholder="Enter the Description"]')
        click_description.send_keys(random_name())
        add_category = self.findelement(By.XPATH,'//input[@placeholder="Enter the category name"]')
        add_category.send_keys(report_name)
        click_add_category_button = self.findusingvisibility(By.XPATH,'//span[normalize-space(.)="Add Category"]')
        click_add_category_button.click()
        ele = self.findelement(By.XPATH,'//label[normalize-space(.)="Category"]/following-sibling::div//input')
        ele.click()
        ele.send_keys(report_name)
        self.findusingvisibility(By.XPATH,f'//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li//span[text()="{report_name}"]')
        select = self.findelement(By.XPATH,f'//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li//span[text()="{report_name}"]')
        select.click()
        # try:
        #     list_of_categories = [i.text.strip() for i in self.driver.find_elements(By.XPATH,'//div[@aria-hidden="false"]//ul//li')]
        #     print("list of catefories", list_of_categories)
        #     if list_of_categories[-1].text.strip() == report_name:
        #         list_of_categories[-1].click()
        # except Exception:
        #     self.findusingvisibility(By.XPATH,'//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li')
        #     for i in self.driver.find_elements(By.XPATH,'//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li'):
        #         try:
        #             print("reportname", i.text.strip())
        #             if i.is_displayed() and i.text.strip() == report_name:
        #                 i.click()
        #                 break
        #         except Exception:
        #             pass

        self.findusingvisibility(By.XPATH,'//span[normalize-space(.)="Confirm"]')
        click_save_button = self.findelement(By.XPATH,'//span[normalize-space(.)="Confirm"]')
        click_save_button.click()
        self.findusinginvisibility(*self.invisibility)
        try:
            self.findusingvisibility(By.XPATH,'//p[normalize-space(.) = "Report Created Successfully"]')
            self.findusinginvisibility(By.XPATH,'//p[normalize-space(.) = "Report Created Successfully"]')
        except Exception:
            pass
        return report_name


    def update(self):
        self.findusingvisibility(*self.update_report)
        self.findusinginvisibility(*self.invisibility)
        value = self.driver.find_element(*self.update_report)
        assert value.is_displayed()
        value.click()
        self.findusinginvisibility(*self.invisibility)
        self.findusingvisibility(By.XPATH,'//p[normalize-space(.) = "Report Updated Successfully"]')

            
    def click_cancel(self):
        value = self.findusingvisibility(*self.click_cancel_btn)
        value.click()

    def element_visible(self):
        self.findusinginvisibility(*self.click_cancel_btn)
        self.findusingvisibility(*self.grid_layout)
    
    def chart_edit(self,index):
        try:
            self.findusingvisibility(By.XPATH,'//div[@class="vue-grid-layout"]')
            value1 = self.findelements(*self.edit_chart)
            for _ in value1:
                    edit_button = self.findelement(By.XPATH,f'(//div[@class="vue-grid-layout"]//button[@title="Edit"])[{index+1}]')
                    print("valuess", self.findelement(By.XPATH,f'(//div[@class="vue-grid-layout"]//button[@title="Edit"])[{index+1}]'))
                    self.driver.execute_script("arguments[0].click();", edit_button)
        except Exception:
            return None
        
    def resize_of_the_widget(self,driver, index):
        self.findusingvisibility(By.XPATH,f'(//div[@class="vue-grid-item vue-resizable cssTransforms"]//span[@class="vue-resizable-handle"])[{index}]')
        ele = self.findelement(By.XPATH,f'(//div[@class="vue-grid-item vue-resizable cssTransforms"]//span[@class="vue-resizable-handle"])[{index}]')
        # ele = self.findelement(By.XPATH,'//div[@class="vue-grid-item vue-resizable cssTransforms"]//span[@class="vue-resizable-handle"]')
        cdd = ele.location
        print("cdddd", cdd)
        # driver.execute_script("arguments[0].scrollIntoView({'block':'center'});",ele)
        if index == 1:
            ActionChains(driver=driver).click_and_hold(ele).move_by_offset(600,300).release().perform()
        else:
            print("-(cdd['x']+100),100",-(cdd['x']+100),100)
            ActionChains(driver=driver).click_and_hold(ele).move_by_offset(-(cdd['x']+50),0).release().perform()
            time.sleep(2)
            ActionChains(driver=driver).click_and_hold(ele).move_by_offset(200,200).release().perform()


        # if cdd['x'] <= 400 and cdd['y'] <= 200:
        #     driver.execute_script("arguments[0].scrollIntoView({'block':'center'});",ele)
        #     ActionChains(driver=driver).click_and_hold(ele).move_by_offset(cdd['x']+100,cdd['y']+100).release().perform()
        # elif cdd['x'] >= 500 and cdd['y'] >= 400:
        #     print("1st",-(cdd['x']),cdd['y'])
        #     driver.execute_script("arguments[0].scrollIntoView({'block':'center'});",ele)
        #     ActionChains(driver).click_and_hold(ele).move_by_offset(-300,0).release().perform()
        # elif cdd['x'] >= 300 and cdd['y'] >= 400:
        #     print("2nd",-(cdd['x']),cdd['y'])
        #     driver.execute_script("arguments[0].scrollIntoView({'block':'center'});",ele)
        #     ActionChains(driver).click_and_hold(ele).move_by_offset(-300,0).release().perform()
        # elif cdd['x'] >= 200 and cdd['y'] >= 400:
        #     print("3nd",-(cdd['x']),cdd['y'])
        #     driver.execute_script("arguments[0].scrollIntoView({'block':'center'});",ele)
        #     ActionChains(driver).click_and_hold(ele).move_by_offset(-300,0).release().perform()
        # else:
        #     print("not changed")
        # ActionChains(driver=driver).click_and_hold(ele).move_by_offset(50,100).release().perform()


    