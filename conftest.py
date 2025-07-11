import pytest, json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    option = Options()
    option.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=option)
    yield driver
    driver.quit()

@pytest.fixture
def waitforelement(driver):
    def _element(by,elements,timeout=50):
        element = WebDriverWait(driver,timeout).until(EC.presence_of_element_located((by,elements)))
        return element
    return _element

@pytest.fixture
def waitforcustomfunctions(driver):
    def _element(by,elements,timeout=50):
        element = WebDriverWait(driver,timeout).until(lambda d: d.find_element(by,elements))
        return element
    return _element

@pytest.fixture
def waitforelementvisibility(driver):
    def _element(by,elements,timeout=50):
        element = WebDriverWait(driver,timeout).until(EC.visibility_of_element_located((by,elements)))
        return element
    return _element

@pytest.fixture
def waitforelementelement(driver):
    def _element(by,elements,timeout=50):
        element = WebDriverWait(driver,timeout).until(EC.element_to_be_clickable((by,elements)))
        return element
    return _element

@pytest.fixture
def waitforelementinvisibility(driver):
    def _element(by,elements,timeout=50):
        element = WebDriverWait(driver,timeout).until(EC.invisibility_of_element_located((by,elements)))
        return element
    return _element

@pytest.fixture
def findelement(driver):
    def _element(by,elements):
        element = driver.find_element(by,elements)
        return element
    return _element

@pytest.fixture
def findelements(driver):
    def _element(by,elements):
        element = driver.find_elements(by,elements)
        return element
    return _element

@pytest.fixture
def search(driver):
    def _a(value,timeout = 50):
        element = WebDriverWait(driver,timeout).until(EC.element_to_be_clickable((By.XPATH,'//i[@class="etp-icon etp-hamburger fs-16"]')))
        element.click()
        element1 = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,'//input[@placeholder="Search here"]')))
        element1.send_keys(value)
        elementss = driver.find_elements(By.XPATH,'//ul[@class="el-menu el-menu--vertical el-menu-vertical"]//li//span')
        return elementss
    return _a

@pytest.fixture
def set_token(driver):
    def _set_token(open_url, set_url, file_name):
        driver.get(open_url)
        with open(f'{file_name}.json','r') as file:
            data = json.load(file)
        tokenning = data["etp.Inhouse_Report.eTrackPlus._etp_token"]
        token = "_token"
        driver.get(set_url)
        driver.execute_script("window.localStorage.setItem(arguments[0],arguments[1]);",token,tokenning)
        driver.refresh()
    return _set_token

@pytest.fixture
def get_localstorage(driver):
    def _get_localstorage():
        localstorage = driver.execute_script("""
        let data={};
        for (let i = 0; i < localStorage.length; i++){
            let key  = localStorage.key(i);
            let value = localStorage.getItem(key);
            data[key] = value
        }
        return data;
""")
        with open('localstorage.json','w') as file:
            json.dump(localstorage,file,indent=4)
    return _get_localstorage