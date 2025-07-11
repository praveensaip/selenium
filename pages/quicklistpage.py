from pages.login import login,baseclass
from selenium.webdriver.common.by import By
import time

class listpage(baseclass):
    expected_url = "https://quickreports-stage.anbetrack.com/reportList"
    etrack_login = (By.XPATH,'//table/tbody')
    report_button = (By.XPATH,'//span[normalize-space(.)="New Report"]')
    reportselection = (By.XPATH,'//div[@class="el-col el-col-24 newReportSelectLeft"]//p')
    reportclick = (By.XPATH,'//div[@class="el-col el-col-24 newReportSelectLeft"]//p')
    invisibility = (By.XPATH,'//div[@class="el-loading-spinner"]')

    def assertingicon(self):
        self.findusingvisibility(*self.etrack_login)

    def waitingforgridapprear(self):
        self.findusingvisibility(*self.etrack_login)

    def matched(self):
        self.matchurl(self.driver.current_url,self.expected_url)

    def button_click(self):
        self.findusinginvisibility(*self.invisibility)
        self.click(*self.report_button)

    def report_selection(self, report_name):
        self.findusinginvisibility(*self.invisibility)
        self.findusingvisibility(*self.reportselection)
        for i in self.driver.find_elements(*self.reportclick):
            if i.is_displayed() and i.text.strip().lower() == report_name:
                i.click()
    
    def report_select(self, report_name):
            self.findusingvisibility(By.XPATH,'//table//tbody//tr')
            try:
                for ele in self.driver.find_elements(By.XPATH,'//table//tbody//tr//td//a'):
                    if ele.text.strip() == report_name:
                        ele.click()
                        break
                    
            except Exception:
                self.driver.refresh()
                for ele in self.driver.find_elements(By.XPATH,'//table//tbody//tr'):
                    print(ele)
                    data = list(ele.find_elements(By.TAG_NAME,'td'))
                    report_name1 = data[1].text.strip()
                    if report_name1 == report_name:
                        data[1].click()
                        break
                