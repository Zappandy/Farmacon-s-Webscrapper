# Farmacon's Webscrapper
Webscrapper to download customer data 

## Sign in data

Stored in file via bash = **echo username > account_data.txt; echo password >> account_data.txt** or **echo -e 'username\npassword' > account_data.txt**

## Driver_Setup.sh

Sets up webdriver for Microsoft Edge Version 84.0.522.40

We can access the functions on bash via source Driver_Setup.sh NAME_FUNCTION

Second one unzips file in a newly created dir and the former one fetches the driver from the downloads folder.

## Web Scrapper.py

The actual scrapper. Accesses local data with the sign in info to download the respective data


### Documentation

https://selenium-python.readthedocs.io/waits.html

https://stackoverflow.com/questions/50195971/python-element-is-not-attached-to-the-page-document/50209096

https://stackoverflow.com/questions/28110008/python-selenium-wait-until-element-is-clickable-not-working/28110129

https://medium.com/@pavel.tashev/python-and-selenium-open-focus-and-close-a-new-tab-4cc606b73388

https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.by.html
