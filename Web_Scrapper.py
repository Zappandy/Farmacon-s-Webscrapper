from selenium import webdriver

Path = "Selenium Drivers/Edge_Driver/msedgedriver.exe"
home_page = "https://www.asn-online.org/"
user_data = open("./Selenium Drivers/account_data.txt")
access_data = [w[:-1] for w in user_data.readlines()]  # cleaning up new line char
user_data.close()


def sign_in(address, signin_info):
    """

    :param signin_info:
    :param address:
    :return:
    """
    driver = webdriver.Edge(Path)
    driver.get(address)
    username(driver, signin_info[0])
    password_info(driver, signin_info[1])
    member_dir(driver, "Torrance", "CA")
    return 0


def username(web_browser, user):
    """
    Submits username data
    """
    web_browser.find_element_by_id("login_link").click()
    web_browser.implicitly_wait(5)
    userElm = web_browser.find_element_by_id("login_eml_address")
    userElm.send_keys(user)
    userElm.submit()


def password_info(web_browser, password):
    """
    Submits password data
    """
    passElm = web_browser.find_element_by_class_name("toggle-password-input")
    passElm.send_keys(password)
    web_browser.implicitly_wait(5)
    web_browser.find_element_by_id("LoginButton").click()


def member_dir(web_browser, city, state):
    """

    :param web_browser:
    :return:
    """
    web_browser.implicitly_wait(5)
    web_browser.find_element_by_id("membership").click()
    web_browser.find_element_by_link_text('Member Directory').click()
    cityElm = web_browser.find_element_by_id("THE_CITY")
    cityElm.send_keys(city)
    web_browser.find_element_by_xpath(f"//select[@name='THE_STATE']/option[text()='{state}']").click()
    web_browser.find_element_by_name("search_button").click()    
    doctor_list = web_browser.find_element_by_class_name("list1")
    # for doc in doctor_list:
    #     contact_info = doc.find_elements_by_css_selector("li a")
    #     contact_info.get_attribute("href").click()
    #     break


sign_in(home_page, access_data)
