import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


user_data = open("./Selenium Drivers/account_data.txt")
access_data = [w[:-1] for w in user_data.readlines()]  # cleaning up new line char
user_data.close()


class Farmacon_Scrapper(object):
    Path = "Selenium Drivers/Edge_Driver/msedgedriver.exe"    

    def __init__(self, sigin_info):
        """

        :param sigin_info: sign in info stored in an iterable (list). 
        This is stored as access data on script
        """
        self.driver = webdriver.Edge(Farmacon_Scrapper.Path) 
        self.sigin_info = sigin_info
        self.no_element = selenium.common.exceptions.NoSuchElementException
        self.driver.get("https://www.asn-online.org")

    def wait_page(self, element_tup):
        """

        :param element_tup: tuple where the args for the presence method
        from the EC library are given i.e. By what trait is the element being found
        and the element itself.
        :return: 1 as a failure code otherwise, returns the found element
        """
        element_present = EC.presence_of_element_located(element_tup)
        try:
            Elm = WebDriverWait(self.driver, 10).until(element_present)
            return Elm
        except self.no_element as error:
            self.driver.quit()
            print(f"{element_tup[1]} not found\nError:{error}")
            return 1

    def login_link(self):
        """

        :return: None. Clicks on login link on homepage
        """
        self.wait_page((By.ID, "login_link")).click()

    def username(self):
        """

        :return: None. Submits username on website
        """
        userElm = self.wait_page((By.ID, "login_eml_address"))
        user = self.sigin_info[0]
        userElm.send_keys(user)
        userElm.submit()

    def password(self): 
        """

        :return: None. Submits password to website
        """
        passElm = self.wait_page((By.CLASS_NAME, "toggle-password-input"))
        passwrd = self.sigin_info[1]
        passElm.send_keys(passwrd)
        self.wait_page((By.ID, "LoginButton")).click()

    def member_dir(self, city, state):
        """

        :param city: City where doctors/members are located
        :param state: State where doctors/members are located
        :return: List of doctors/members found in the specified area
        """
        stateDropdown_xpath = f"//select[@name='THE_STATE']/option[text()='{state}']"
        self.wait_page((By.ID, "membership")).click()
        self.wait_page((By.LINK_TEXT, "Member Directory")).click()
        cityElm = self.wait_page((By.ID, "THE_CITY"))
        cityElm.send_keys(city)
        self.wait_page((By.XPATH, stateDropdown_xpath)).click()
        self.wait_page((By.NAME, "search_button")).click()
        result_list = self.wait_page((By.CLASS_NAME, "list1"))
        return result_list.find_elements_by_css_selector("li a")

    def member_data(self):
        """
        
        :return:
        """
        doctor_list = self.member_dir("Torrance", "CA")
        doc_data_xpath = "//ul[@class='list1 grey']/li[1]"#  "//*[@id='member_panel']/ul/li[1]"
        self.driver.find_element_by_css_selector("[title^='Download this info as a vCard']")
        #doctor_listXPATH = "//*[@id='results_panel']/ul"
        for e, doc in enumerate(doctor_list):
            href = doc.get_attribute("href")
            # possible issues
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.get(href)
            doc_Elm = self.wait_page((By.XPATH, doc_data_xpath))
            content = doc_Elm.get_attribute("textContent")  # innerText vs source
            #content = self.driver.execute_script('return arguments[0].textContent;', doc_Elm)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])




def test(scrapper, signin_info):
    asn = scrapper(signin_info)
    asn.login_link()
    asn.username()
    asn.password()  # access_data
    asn.member_data()

test(Farmacon_Scrapper, access_data)
