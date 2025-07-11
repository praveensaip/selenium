from pages.login import login,baseclass
from selenium.webdriver.common.by import By

class landingpage(baseclass):
    expected_url = "https://plus-stage.anbetrack.com/track/#/workarea"
    etrack_login = (By.XPATH,'//a[@class="logo"]')
    invisibility = (By.XPATH,'//div[@class="el-loading-spinner"]')

    def assertingicon(self):
        self.findusingvisibility(*self.etrack_login)

    def matched(self):
        self.findusinginvisibility(*self.invisibility)
        assert self.expected_url in self.driver.current_url
    
    def element_visible(self, by, locator):
        return super().element_visible(by, locator)

    
