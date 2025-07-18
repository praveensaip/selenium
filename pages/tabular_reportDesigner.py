from pages.base import baseclass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class tabular_designerpage(baseclass):
    invisibility = (By.XPATH,'//div[@class="el-loading-spinner"]')

    def model_selction(self,model_name):

        value = []
        parent = WebDriverWait(self.driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="el-vl__window el-tree-virtual-list"]')))
        for _ in range(5):
            self.driver.execute_script("arguments[0].scrollBy(0,200);",parent)
            try:
                ele = WebDriverWait(self.driver,20).until(EC.visibility_of_element_located((By.XPATH,f'//span[text()="{model_name}"]')))
                ele.click()
                try:
                    ele1 = WebDriverWait(self.driver,20).until(EC.visibility_of_element_located((By.XPATH,'//div[@class="el-tree-node is-focusable is-checked"]//i')))
                    ele1.click()
                    WebDriverWait(self.driver,20).until(EC.visibility_of_element_located((By.XPATH,'//div[contains(@class,"is-checked")]')))
                    for _ in range(5):
                        value = []
                        try:
                            ele1 = WebDriverWait(self.driver,20).until(lambda x: x.find_elements(By.XPATH,'//div[@aria-checked="true"]//span[@class="el-tooltip__trigger"]'))
                            print("elleeee", ele1)
                            if ele1:
                                for i in ele1:
                                    val = i.text.strip()
                                    if val != '':
                                        value.append(val)
                            self.driver.execute_script("arguments[0].scrollBy(0,60);",parent)
                        except Exception:
                            continue
                    print("demooo", value, len(value))
                except Exception:
                    pass
                break
            except Exception:
                print("continueddd")
                continue
        return value
    
    def get_header_value(self):
        WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH,'//div[@class="tabulator-headers"]//div[@class="tabulator-col-title"]')))
        elements = []
        for _ in range(10):
            ele = [ i.text.strip() for i in self.driver.find_elements(By.XPATH,'//div[@class="tabulator-headers"]//div[@class="tabulator-col-title"]') if i.text.strip() !='']
            elements.append(ele)
            ele = WebDriverWait(self.driver,10).until(lambda d: d.find_element(By.XPATH,'//div[@class="tabulator-tableholder"]'))
            self.driver.execute_script("arguments[0].scrollLeft +=300;",ele)
        return elements
    
    def change_order(self):
        self.findusingvisibility(By.XPATH,'//span[normalize-space(.)="Order and Group"]')
        ele = self.findelement(By.XPATH,'//span[normalize-space(.)="Order and Group"]')
        ele.click()
        self.findusingvisibility(By.XPATH,'//div[@class="addGroupColumnPanel side-property-panel el-drawer rtl open"]')
        ele1 = WebDriverWait(self.driver,20).until(lambda d : d.find_elements(By.XPATH,'//div[@class="el-tree tree addColumnContent"]//div/div/div'))    
        before = [ i.text.strip() for i in ele1 if ele1]
        values = [ i for i in ele1 if ele1]
        location = [ i.location for i in ele1 if ele1]
        xx = location[0]
        yy = location[1]
        print("xxxx",xx,yy)
        x_offset = yy['x'] - xx['x']
        y_offset = yy['y'] - xx['y']+30 
        self.driver.execute_script("arguments[0].scrollIntoView(true);",values[0])
        self.driver.execute_script("arguments[0].scrollIntoView(true);",values[1])
        ActionChains(self.driver).click_and_hold(values[0]).move_by_offset(x_offset,y_offset).release().perform()
        print("valuesss", values, location)
        self.findelement(By.XPATH,'//span[text()="Save"]').click()

        self.findusingvisibility(By.XPATH,'//span[normalize-space(.)="Order and Group"]')
        ele = self.findelement(By.XPATH,'//span[normalize-space(.)="Order and Group"]')
        ele.click()
        self.findusingvisibility(By.XPATH,'//div[@class="addGroupColumnPanel side-property-panel el-drawer rtl open"]')
        ele1 = WebDriverWait(self.driver,20).until(lambda d : d.find_elements(By.XPATH,'//div[@class="el-tree tree addColumnContent"]//div/div/div'))    
        after = [i.text.strip() for i in ele1 if ele1]
        self.findusingvisibility(By.XPATH,'//span[text()="Save"]')
        self.findelement(By.XPATH,'//span[text()="Save"]').click()

        return before,after
    
    def view_preview(self):
        ele = WebDriverWait(self.driver,20).until(lambda d: d.find_element(By.XPATH,'//span[text()="Preview"]'))
        ele.click()
        self.findusinginvisibility(*self.invisibility)
        ele = self.findusingvisibility(By.XPATH,'//p[@class="m-t-0 m-b-0"]//span')
        page_count = ele.get_attribute("textContent")
        assert page_count != 0
        print("page count", page_count)

    def export(self,file_format):
        self.findusinginvisibility(*self.invisibility)
        self.findusingvisibility(By.XPATH,'//span[text()="Export"]/ancestor::button')
        ele = self.findelement(By.XPATH,'//span[text()="Export"]/ancestor::button')
        value = ele.get_attribute('aria-disabled')
        assert value == 'false'
        ele.click()
        self.choose_file_format(file_format)
        # if file_format != 'EXCEL':
        #     ele.send_keys(Keys.TAB)
        #     ele.send_keys(Keys.ENTER)
        #     value = WebDriverWait(self.driver,20).until(lambda d: d.find_elements(By.XPATH,'//div[@aria-hidden="false"]//ul//li'))
        #     for i in value:
        #         if i.text.strip() == 'CSV':
        #             value1 = i.get_attribute("class")
        #             assert 'selected' in value1
        #             print("value1", value1)
                    
    
    def click_design(self):
        self.findelement(By.XPATH,'//span[text()="Design"]').click()

    def choose_file_format(self,file_format):
        self.findusingvisibility(By.XPATH,'//div[@class="el-dialog save-lookup executeReport multi-sheet-export"]')
        ele_click = self.findelement(By.XPATH,'//label[text()="Select the file type"]/ancestor::div[contains(@class,"el-form-item")]//input')
        ele_click.click()
        ele = self.findelements(By.XPATH,'//div[@aria-hidden="false"]//ul//li')
        for i in ele:
            print("iiii", i.text.strip())
            if i.text.strip() == file_format and file_format == 'EXCEL':
                self.driver.execute_script("arguments[0].click();",i)
                self.findusingvisibility(By.XPATH,'//span[text()="Execute"]')
                self.findelement(By.XPATH,'//span[text()="Execute"]').click()
                self.findusinginvisibility(By.XPATH,'//div[@class="loadingText"]')
                assert self.findelement(By.XPATH,'//span[text()="Export"]/ancestor::button').get_attribute('aria-disabled') == 'false'
                break
            else:
                action = ActionChains(driver=self.driver)
                action.click(ele_click).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()
                value = self.findelements(By.XPATH,'//div[@aria-hidden="false"]//ul//li')
                for i in value:
                    if i.text.strip() == "Comma":
                        assert 'selected' in i.get_attribute('class')
                self.findusingvisibility(By.XPATH,'//span[text()="Execute"]')
                self.findelement(By.XPATH,'//span[text()="Execute"]').click()
                self.findusinginvisibility(By.XPATH,'//div[@class="loadingText"]')
                assert self.findelement(By.XPATH,'//span[text()="Export"]/ancestor::button').get_attribute('aria-disabled') == 'false'
                break
    



