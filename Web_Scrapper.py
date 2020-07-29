import os
import pandas as pd
import re
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import vobject


user_data = open("./Selenium Drivers/account_data.txt")
access_data = [w[:-1] for w in user_data.readlines()]  # cleaning up new line char
user_data.close()


class FarmaconScrapper(object):
    Path = "Selenium Drivers/Edge_Driver/msedgedriver.exe"    

    def __init__(self, sigin_info):
        """

        :param sigin_info: sign in info stored in an iterable (list). 
        This is stored as access data on script
        """
        self.driver = webdriver.Edge(FarmaconScrapper.Path)
        self.sigin_info = sigin_info
        self.no_element = selenium.common.exceptions.NoSuchElementException
        self.timeout = selenium.common.exceptions.TimeoutException
        self.driver.get("https://www.asn-online.org")
        self.backup_downloads = []

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
        except (self.timeout, self.no_element) as error:
            self.driver.quit()
            print(f"{error}")
            exit()  #sys.exit(1)

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
        
        :return: an iterable containing the links where the data in Vcard format is. 
        User may need to be signed in, though. Therefore why this method 
        downloads them to the default directory when using MS Edge
        """
        doctor_list = self.member_dir("Torrance", "CA")
        for e, doc in enumerate(doctor_list):
            href = doc.get_attribute("href")
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.get(href)
            vCard = self.wait_page((By.CLASS_NAME, "alignright"))
            link_href = vCard.get_attribute("href")
            self.backup_downloads.append(link_href)
            vCard.click()
            self.driver.implicitly_wait(10)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            #TODO: create vcard class or function https://stackoverflow.com/questions/35825919/vcard-parser-with-python
            # http://vobject.skyhouseconsulting.com/epydoc/  https://github.com/eventable/vobject
        return self.backup_downloads  


class VCardParser(object):
    doc_num = 0

    def __init__(self, address):
        """

        :param address: local dir path where the downloads folder is located
        """
        self.fileRegex = re.compile(r".vcf$")
        self.address = address
        self.doctors = {}
        self.df = pd.DataFrame({'Empty' : []})

    def __str__(self):
        return self.df.to_string(index=False)

    def __repr__(self):
        return self.df.to_string(index=False)

    def data_parser(self):
        """
        Finds every vcf file in given path and parses them to clean their data
        Mutates the initialized dataframe with the vcf data.
        """
        for file in os.listdir(self.address):
            if self.fileRegex.search(file):
                VCardParser.doc_num += 1
                match = open(self.address + file, 'r')
                match_stored = match.read()
                match.close()
                vcard = vobject.readOne(match_stored)
                vcard_data = vcard.contents.copy()
                self.key_cleaner(vcard_data)
                self.value_cleaner(vcard_data)
                self.doctors.setdefault(f"doctor {VCardParser.doc_num}", vcard_data)
                #vcard.prettyPrint()
          self.df = pd.DataFrame.from_dict(self.doctors, orient='index')      

    @staticmethod
    def key_cleaner(data_strct):
        """
        cleans up the keys from the initialized dictionary
        """
        data_strct['Phone'] = data_strct.pop('tel')
        data_strct['Full name'] = data_strct.pop('fn')
        data_strct['Organization'] = data_strct.pop('org')
        data_strct['Email'] = data_strct.pop('email')
        data_strct['Address'] = data_strct.pop('adr')
        data_strct['Title'] = data_strct.pop('title')
        data_strct.pop('version')
        data_strct.pop('n')

    @staticmethod
    def value_cleaner(data_strct):
        """
        cleans up the values from the initialized dictionary
        if they are empty, they are stored as NaN and if they are mutable
        iterables of length one they are unpacked.
        """
        for k, v in data_strct.items():
            if v[0].value == '':
                data_strct[k] = 'NaN'
            elif len(v) == 1:
                v[0].value = "".join(v[0].value) if type(v[0].value) is list else v[0].value
                data_strct[k] = v[0].value
            else:
                data_strct[k] = [i.value for i in v]
