import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


Path = "Selenium Drivers/Edge_Driver/msedgedriver.exe"
home_page = "https://www.asn-online.org/"
user_data = open("./Selenium Drivers/account_data.txt")
access_data = [w[:-1] for w in user_data.readlines()]  # cleaning up new line char
user_data.close()


def main_func(address, signin_info):
    """

    :param signin_info:
    :param address:
    :return:
    """
    driver = webdriver.Edge(Path)
    driver.get(address)
    element_present = EC.presence_of_element_located((By.ID, "login_link"))
    try:
        login = WebDriverWait(driver, 10).until(element_present)
    except selenium.common.exceptions.NoSuchElementException:
        driver.quit()
        return 1
    #loginElm = driver.find_element_by_id("login_link")
    login.click()
    username(driver, signin_info[0])
    password_info(driver, signin_info[1])
    member_dir(driver, "Torrance", "CA")


def username(web_browser, user):
    """
    Submits username data
    """
    element_present = EC.presence_of_element_located((By.ID, "login_eml_address"))
    try:
        userElm = WebDriverWait(web_browser, 10).until(element_present)
        userElm.send_keys(user)
        userElm.submit()
    except selenium.common.exceptions.NoSuchElementException:
        web_browser.quit()
    #userElm = web_browser.find_element_by_id("login_eml_address")


def password_info(web_browser, password):
    """
    Submits password data
    """
    passElm = web_browser.find_element_by_class_name("toggle-password-input")
    passElm.send_keys(password)
    web_browser.implicitly_wait(1)
    web_browser.find_element_by_id("LoginButton").click()


def member_dir(web_browser, city, state):
    """

    :param web_browser:
    :return:
    """
    doctor_xpath = "/html/body/div[1]/section[2]/div/div/div[2]/div/form/div[3]/ul/li[1]"
    web_browser.find_element_by_id("membership").click()
    web_browser.find_element_by_link_text('Member Directory').click()
    cityElm = web_browser.find_element_by_id("THE_CITY")
    cityElm.send_keys(city)
    web_browser.find_element_by_xpath(f"//select[@name='THE_STATE']/option[text()='{state}']").click()
    web_browser.implicitly_wait(1)
    web_browser.find_element_by_name("search_button").click()
    result_list = web_browser.find_element_by_class_name("list1")
    doctors = result_list.find_elements_by_css_selector("li a")
    doc_data = []
    for doc in doctors:
        doc.click()
        #href = doc.get_attribute("href")
        #web_browser.execute_script("window.open('" + href +"');")
        #data_list = web_browser.find_element_by_id("member_panel")
        htmlElem = web_browser.find_element_by_xpath(doctor_xpath)
        doc_data.append(htmlElem)
        #doc_data.append(htmlElem.get_attribute("innerHtml"))
        web_browser.implicitly_wait(1)

    print(doc_data)
    return doc_data




main_func(home_page, access_data)

