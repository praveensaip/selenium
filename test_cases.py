import time, json,pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pages.login import login

from faker import Faker
import requests

faker = Faker()
random_name = lambda : faker.first_name()+ faker.last_name()
report_name = random_name()
list_of_elemenst = ["kw ","kwh ","Project Name ","Project Code "]


@pytest.mark.skip(reason="not implements")
def test_login_quick_reports(driver,waitforelement,search):
    driver.get('https://plus-stage.anbetrack.com/#/')
    data = login(driver,'praveen_inhouse','Kumar@1999')
    try:
        data.enter_username()
    except Exception as e:
        print("error",str(e))
    data.enter_password()
    data.click_login()
    element = waitforelement(By.XPATH,'//a[@class="logo"]',50)
    assert element.is_displayed()
    try:
        element = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//div[@class="text-justify calc-360 scrollable"]')))
        for _ in range(5):
            driver.execute_script('arguments[0].scrollBy(0,300);', element)
            time.sleep(0.2)
        driver.find_element(By.XPATH,'//span[text()="I have read and agree to the ANB Systems Terms of Service"]/preceding-sibling::label').click()
        driver.find_element(By.XPATH,'//span[text()="Accept"]').click()

    except Exception:
        pass
    localstoragevalue = driver.execute_script("""
        let data = {};
        for(let i=0; i<localStorage.length; i++)
        {
        let key = localStorage.key(i)
        let value = localStorage.getItem(key)
        data[key] = value
        }
        return data
                        """)
    with open('local.json','w') as file:
        json.dump(localstoragevalue, file, indent=4)
    try:
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//label[@class="el-checkbox"]//input'))
        ).click()
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button//span[text()="Accept"]/parent::button'))
        ).click()
    except Exception:
        pass
    current_window = driver.current_window_handle
    print("current_window", current_window)
    # value = search("QUICK")
    # for i in value:
    #     if i.text.strip() == 'QUICKreports':
    #         i.click()
    #         all_window = driver.window_handles
    #         print("all_window",all_window)
    #         time.sleep(5)
    #         break
    driver.close()

# @pytest.mark.skip(reason="not implements")
def test_dashboard_rendering(driver,set_token,findelement,waitforelement,waitforelementinvisibility,waitforelementelement,waitforelementvisibility,findelements):
    
    url = "https://plus-stage.anbetrack.com/#/"
    target_url = "https://quickreports-stage.anbetrack.com/reportList"
    file_name = 'local'
    try:
        set_token(url,target_url, file_name)
    except Exception as e:
        print(str(e))
     #requestss
    with open('local.json','r') as file:
        data = json.load(file)
        token = data["etp.Inhouse_Report.eTrackPlus._etp_token"]
    url = "https://api-plus-stage.anbetrack.com/core/api/v1/applications/name/eTrackPlus"
    headers = {
        "Content-Type":"application/json",
        "Authorization":f"Bearer {token}"
    }
    req = requests.get(url,headers=headers)
    response = req.json()
    data = {}
    print(headers)
    print("response",req.status_code,req.text)
    for i in response['models']:
        value = [j['displayName'] for j in i['attributes']]
        key = i['displayName']
        data[key] = value
    with open("modelattributes.json",'w') as file:
        json.dump(data,file,indent=4)
    
    with open("modelattributes.json",'r') as file:
        data = json.load(file)
    Model_name = "EE project Inhouse"
    for key,value in data.items():
        if key == Model_name:
            attributes = value
            print("attributess", attributes)
    
    waitforelementinvisibility(By.XPATH,'//div[@class="el-loading-spinner"]')
    click_button = waitforelementelement(By.XPATH,'//i[@class="etp-icon etp-add m-r-5"]')
    click_button.click()
    waitforelementvisibility(By.XPATH,'//div[@class="el-col el-col-24 newReportSelectLeft"]//p')
    for j in driver.find_elements(By.XPATH,'//div[@class="el-col el-col-24 newReportSelectLeft"]//p'):
        if j.is_displayed() and j.text.strip().lower() == "dashboard":
            j.click()
    ##dynamic data:
    # for _ in range(10):
    #     scrollable_container = waitforelementvisibility(By.XPATH, '//div[@class="el-vl__window el-tree-virtual-list"]')
    #     driver.execute_script("arguments[0].scrollBy(0,300);",scrollable_container)
    #     try:
    #         click_1 = findelement(By.XPATH,f'//span[normalize-space(.)="{Model_name}"]/preceding-sibling::i')
    #         click_1.click()
    #         for _ in range(10):
    #             for j in attributes:
    #                 try:
    #                     attr_element = findelement(By.XPATH,f'//span[normalize-space(.)="{j}"]')
    #                     attr_element.click()
    #                     time.sleep(2)
    #                 except Exception:
    #                     driver.execute_script("arguments[0].scrollBy(0,50);",scrollable_container)
    #             break
    #     except Exception:
    #         pass
    def create_multiple_widgets():
        waitforelement(By.XPATH,'//div[@class="el-col el-col-24 el-col-xs-12 el-col-sm-12 el-col-md-12 el-col-lg-12 tr p-t-10 p-b-10"]//button//span')
        buttons = findelements(By.XPATH, '//div[@class="el-col el-col-24 el-col-xs-12 el-col-sm-12 el-col-md-12 el-col-lg-12 tr p-t-10 p-b-10"]//button//span')
        for ele in buttons:
            print("elemrnt", ele.text.strip())
            if ele.text.strip() == "Widget":
                print("clicked")
                waitforelementinvisibility(By.XPATH,'//div[@class="el-loading-spinner"]')
                WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, '//span[normalize-space(.)="Widget"]')))
                ele.click()
            
        # button_validate = {
        #     "Widget":False,
        #     "Run":True,
        #     "Close":False,
        #     "Save":True,
        #     "Export":True,
        #     "Parameter":True

        # }
        # for idx, button in enumerate(buttons, 1):
        #     button_1 = button.get_attribute("disabled") is not None
        #     button_2 = button.text.strip()

        #     assert button_validate[button_2] == button_1
        #     print(button_validate[button_2])
        # try:
        #     waitforelementvisibility(By.XPATH,'//p[text()="Please add Dashboard Widgets"]')
        #     click_widget = waitforelementvisibility(By.XPATH,'(//span[text()=" Widget"])[2]')
        #     driver.execute_script('arguments[0].click();',click_widget)
        # except Exception:
        #     pass
        get_widget_name = findelements(By.XPATH, '//div[@class="el-row addNewSheetDialog"]//div//div[@class="el-row"]/child::div//button')
        widgetname_names = ['All Models','SQL']
        waitforelementvisibility(By.XPATH,'//div[@class="el-col el-col-24 text-center"]')
        for i in get_widget_name:
            namess = i.text.strip()
            print("namess", namess)
            assert namess in widgetname_names
        time.sleep(1)
        select_widget = waitforelementvisibility(By.XPATH,'//button[contains(@class,"el-button--text")]//p[text()="All Models"]')
        select_widget.click()
        waitforelement(By.XPATH,'//button[contains(@class,"el-button--text") and contains(@class,"is-active")]')
        widget_selection= driver.find_element(By.XPATH, '//span[text()="Create"]')
        widget_selection.click()

        ## Model Render
        try:
            WebDriverWait(driver,10).until(EC.visibj)
            clickc = findelement(By.XPATH,'//span[normalize-space(.)="Close"]')
            clickc.click()
            driver.refresh()
            waitforelementvisibility(By.XPATH,'//p[text()="Please add Dashboard Widgets"]')
            click_widget = waitforelementvisibility(By.XPATH,'(//span[text()=" Widget"])[2]')
            driver.execute_script('arguments[0].click();',click_widget)
            get_widget_name = findelements(By.XPATH, '//div[@class="el-row addNewSheetDialog"]//div//div[@class="el-row"]/child::div//button')
            widgetname_names = ['All Models','SQL']
            waitforelementvisibility(By.XPATH,'//div[@class="el-col el-col-24 text-center"]')
            for i in get_widget_name:
                namess = i.text.strip()
                print("namess", namess)
                assert namess in widgetname_names
            time.sleep(1)
            select_widget = waitforelementvisibility(By.XPATH,'//button[contains(@class,"el-button--text")]//p[text()="All Models"]')
            select_widget.click()
            waitforelement(By.XPATH,'//button[contains(@class,"el-button--text") and contains(@class,"is-active")]')
            widget_selection= driver.find_element(By.XPATH, '//span[text()="Create"]')
            widget_selection.click()
        except Exception:
            pass

        for _ in range(10):
            scrollable_container = waitforelementvisibility(By.XPATH, '//div[@class="el-vl__window el-tree-virtual-list"]')
            driver.execute_script('arguments[0].scrollTop += 300;',scrollable_container)
            time.sleep(1)
            try:
                widget_selection = driver.find_element(By.XPATH,'//span[text()="Project Inhouse Anb "]/preceding-sibling::i')
                widget_selection.click()
                driver.execute_script('arguments[0].scrollTop += 80;',scrollable_container)
                for i in list_of_elemenst:
                    try:
                        element = waitforelementvisibility(By.XPATH,f'//span[text()="{i}"]')
                        print("elementtt", element.text) 
                        element.click()
                        assert_ele = waitforelementvisibility(By.XPATH,f'//div[@class="el-col el-col-5 tree-card"]//span[text()="{i}"]/preceding-sibling::label')
                        try:
                            assert 'is-checked' in assert_ele.get_attribute('class')
                            print("asserting", assert_ele.get_attribute('class'))
                        except Exception as e:
                            return str(e)
                    except Exception as e:
                        pass
            except Exception as e:
                pass
    
        # asserting the values are present:
        attributes = findelements(By.XPATH,'//div[@class="el-col el-col-24 el-col-lg-24 is-guttered echartSelectCard"]//span')
        for i in attributes:
            if i.text.strip().lower() != 'go':
                value = i.text.strip()
                print("valuee", value)
                assert any(value in i.strip() for i in list_of_elemenst), f'{value} is not present'
        waitforelementvisibility(By.XPATH,'//div[@id="qr-chart-list"]//button[@title="Grid View"]')
        findelement(By.XPATH,'//div[@id="qr-chart-list"]//button[@title="Grid View"]').click()
        advanced_config = findelement(By.XPATH,'//span[normalize-space(.)="Advanced Configuration"]/ancestor::button')
        advanced_config1 = findelement(By.XPATH,'//span[normalize-space(.)="Create"]/ancestor::button')

        assert not advanced_config.is_enabled(), f'{advanced_config} is enabled' 
        assert not advanced_config1.is_enabled(), f'{advanced_config1} is enabled'
        element = waitforelementvisibility(By.XPATH,'//div[@class="el-col el-col-24 el-col-lg-24 is-guttered echartSelectCard"]//span[text()="Go"]')
        element.click()
        waitforelementinvisibility(By.XPATH,'//div[@class="el-loading-spinner"]')
        WebDriverWait(driver,10).until(lambda d: d.find_element(By.XPATH,'//span[normalize-space(.)="Advanced Configuration"]/ancestor::button').is_enabled())
        assert advanced_config.is_enabled(), f'{advanced_config} is not enabled' 
        assert advanced_config1.is_enabled(), f'{advanced_config1} is not enabled'
        advanced_config1.click()
        assert driver.current_url == 'https://quickreports-stage.anbetrack.com/dashboard'
    for _ in range(1):
        create_multiple_widgets()
    save_report_validation = lambda x: f'//span[normalize-space(.)="{x}"]/ancestor::button'
    widget_screen_button = ["Widget","Save","Parameter","Export","Run"]
    for i in widget_screen_button:
        if i.lower() != "run":
            value = driver.find_element(By.XPATH,save_report_validation(i))
            assert value.get_attribute('disabled') is None
        else:
            value = driver.find_element(By.XPATH,save_report_validation(i))
            assert value.get_attribute('disabled') is not None
    # widget_expand = findelement(By.XPATH, '//div[@class="wrap-scrollbar chart-container"]//div[@class="vue-grid-item vue-resizable cssTransforms"]')


    #Report Save:
    waitforelementvisibility(By.XPATH,'//div[@class="wrap-scrollbar chart-container"]')
    assert findelement(By.XPATH,'//div[@class="wrap-scrollbar chart-container"]').is_displayed()
    save_button_click = findelement(By.XPATH,'//button//span[normalize-space(.)="Save"]')
    save_button_click.click()
    waitforelementvisibility(By.XPATH,'//div[@class="el-dialog save-lookup saveReport"]')
    click_name = findelement(By.XPATH,'//input[@placeholder="Enter the Name"]')
    click_name.send_keys(report_name)
    click_description = findelement(By.XPATH,'//input[@placeholder="Enter the Description"]')
    click_description.send_keys(random_name())
    add_category = findelement(By.XPATH,'//input[@placeholder="Enter the category name"]')
    add_category.send_keys(report_name)
    click_add_category_button = waitforelementvisibility(By.XPATH,'//span[normalize-space(.)="Add Category"]')
    click_add_category_button.click()
    findelement(By.XPATH,'//label[normalize-space(.)="Category"]/following-sibling::div').click()
    waitforelementvisibility(By.XPATH,'//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li')
    # list_of_elements_in_category = findelements(By.XPATH,'//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li')
    for i in driver.find_elements(By.XPATH,'//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li'):
        if i.is_displayed() and i.text.strip() == report_name:
            i.click()
    # waitforelement(By.XPATH,'//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li')
    # data = [i.text.strip() for i in list_of_elements_in_category]
    # print("dataa",data)
    # list_of_elements_in_category[-1].click()
    waitforelementvisibility(By.XPATH,'//span[normalize-space(.)="Confirm"]')
    click_save_button = findelement(By.XPATH,'//span[normalize-space(.)="Confirm"]')
    click_save_button.click()
    waitforelementvisibility(By.XPATH,'//p[normalize-space(.) = "Report Created Successfully"]')
    waitforelementvisibility(By.XPATH,'//span[normalize-space(.)="Update"]//i[@class="etp-icon etp-save"]')


    ##cancel
    waitforelementvisibility(By.XPATH,'//span//i[@class="etp-icon etp-cancel"]')
    click_cancel = findelement(By.XPATH,'//span//i[@class="etp-icon etp-cancel"]')
    click_cancel.click()
    waitforelementvisibility(By.XPATH,'//span[normalize-space(.)="New Report"]')
    driver.refresh()


    ## Edit_report:
@pytest.mark.skip(reason="not wporking")
def test_data_get(driver,waitforelement,findelements,set_token,findelement,waitforelementinvisibility, waitforelementvisibility,waitforcustomfunctions):
    url = "https://plus-stage.anbetrack.com/#/"
    target_url = "https://quickreports-stage.anbetrack.com/reportList"
    file_name = 'local'
    set_token(url,target_url, file_name)
    try:
        waitforelementvisibility(By.XPATH,'(//div[@class="el-table__body-wrapper"]//tbody//tr)[1]')
    except Exception:
        driver.refresh()
    data = findelements(By.XPATH,'//div[@class="el-table__body-wrapper"]//tbody//tr')
    for ele in data:
        value = ele.find_elements(By.TAG_NAME,'td')
        value1 = [i.text for i in value][1]
        if value1 == report_name:
            print("value1", value1)
            waitforelement(By.XPATH,'.//a[@class="bold link"]')
            click_value = ele.find_element(By.XPATH,'.//a[@class="bold link"]')
            click_value.click()
            # waitforelementvisibility(By.XPATH,'//div//li[normalize-space(.)="Edit"]')
            # time.sleep(2)
            # click_value1 = findelement(By.XPATH,'//div//li[normalize-space(.)="Edit"]')
            # click_value1.click()
            # waitforelementvisibility(By.XPATH,'//div//li[normalize-space(.)="Edit"]')
            # click_value1 = findelement(By.XPATH,'//div//li[normalize-space(.)="Edit"]')
            # click_value1.click()
            break
    waitforelementinvisibility(By.XPATH,'//div[@class="el-loading-spinner"]')
    value = waitforcustomfunctions(By.XPATH,'//div[@class="vue-grid-layout"]')
    assert value.is_displayed()
    ele = findelement(By.XPATH,'//div[@class="vue-grid-layout"]')
    ele1 = ele.find_elements(By.XPATH,'.//div')
    for i in ele1:
        if i.get_attribute('class') == "vue-grid-item vue-resizable cssTransforms":
            click_edit_button = findelement(By.XPATH,'.//button[@title="Edit"]')
            click_edit_button.click()
            break
    waitforelementvisibility(By.XPATH,'//span[normalize-space(.)="Property"]')
    findelement(By.XPATH,'//label[text()="Title"]/ancestor::div[@class="el-form-item asterisk-left"]//div//input').send_keys(random_name())
    findelement(By.XPATH,'//label[text()="Sub Title"]/ancestor::div[@class="el-form-item asterisk-left"]//div//input').send_keys(random_name())
    findelement(By.XPATH,'//span//i[@class="fal fa-check p-r-5"]').click()
    
    

    @pytest.mark.skip(reason="Not implemented")
    def test_demo():
        elem = findelement(By.XPATH,'//div[@class="el-row piechartCardtype"]//div[@class="el-col el-col-24 el-col-lg-8"]//button[@title="Classic"]/ancestor::div[contains(@class,"configKpiCard")]')
        assert elem.get_attribute('class') == 'el-card is-never-shadow select configKpiCard br'
        ad_el = findelement(By.XPATH,'//div[@class="advanceConfigCollapse"]')
        validate = ad_el.find_elements(By.XPATH,'.//div')
        tt = [i.text.strip() for i in validate]
        for i in list_of_elemenst:
            assert i.strip() in set(tt)
            print(i)
        findelement(By.XPATH,'//button[@class="el-button el-button--primary"]//span[normalize-space(.)="Update"]').click()
        time.sleep(10)
        #value is added to the inputs:
        ele = findelement(By.XPATH,'//div[@class="el-switch fr"]')
        ele.click()
        assert 'is-checked' in ele.get_attribute('class')

        def drop_down(dropdownorder,value):
            ele = findelement(By.XPATH,f'(//i[@class="el-icon el-select__caret el-select__icon"])[{dropdownorder}]')
            ele.click()
            ele = findelements(By.XPATH,f'(//ul[@class="el-scrollbar__view el-select-dropdown__list"])[{dropdownorder+2}]//li')
            for i in ele:
                if i.text.strip() == value:
                    assert 'selected' in i.get_attribute('class')
        list_of_drop = ['Top - Center','Horizontal']
        for i in range(1,3):
                drop_down(i,list_of_drop[i-1])
                print(i,list_of_drop[i-1])

        # custom legend:
        ele = findelement(By.XPATH,'//i[@class="el-icon el-collapse-item__arrow"]')
        ele.click()
        assert 'is-active' in ele.get_attribute('class')

        list_of_values = ['kw','kwh']
        for i in list_of_values:
            ele = findelement(By.XPATH,f'//label[text()="{i}"]/ancestor::div[@class="el-form-item asterisk-left"]//input')
            assert ele.get_attribute('value').strip() == i
            print("ele.get_attribute('value').strip()",ele.get_attribute('value').strip())

        #leble turnon
        ele = findelement(By.XPATH,'//div[@class="el-switch"]//span[@class="el-switch__core"]')
        ele1 = findelement(By.XPATH,'//div[@class="el-switch"]')
        waitforelementvisibility(By.XPATH,'//div[@class="el-switch"]//span[@class="el-switch__core"]')
        ele.click()
        print("eee", ele1.get_attribute('class'))
        assert 'is-checked' in ele1.get_attribute('class')
        time.sleep(10)