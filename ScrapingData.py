from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
from tabulate import tabulate

# launch url
url = "http://buyvia.cnxpartner.com/"

# create a new Chrome session
driver = webdriver.Chrome(executable_path='F:\Python_Workspace\TestScraper\chromedriver.exe')
driver.implicitly_wait(30)
driver.get(url)

# After opening the url clicks the link
python_link = driver.find_element_by_link_text('Appliances')
python_link.click()  # click link

# setup dataFrame
df = pd.DataFrame([],
                  columns=["VendorID", "PartNumber", "Name", "Price", "Description", "PhotoPath"])

pagesrc1 = BeautifulSoup(driver.page_source, 'lxml')

vendorList = []
partList = []
nameList = []
priceList = []
descList = []
PhotoList = []
x = 1
for page in pagesrc1.find_all('li'):
    # give pagesource to beautifulsoup
    pagesrc2 = BeautifulSoup(driver.page_source, 'lxml')

    # selects the elements that have the product name information contained in the div class title
    for vendor in pagesrc2.find_all('div', class_=re.compile("^merchantLogo")):
        img = vendor.find('img', alt=True)

        vendorList.append(str(img['alt']))\

        # end loop block

    # loop has completed add list to dataframe

    # selects the elements that have the partNumber information just made up from the image path
    for partNumber in pagesrc2.find_all('div', class_=re.compile("^col-xs-3 col-md-2 listProdImg")):
        img = partNumber.find('img')

        partList.append(re.sub(r";", "", re.search(r"\d+?;", str(img['src'])).group(0)))

        # end loop block

    # selects the elements that have the product name information contained in the div class title
    for title in pagesrc2.find_all('div', class_=re.compile("^title")):

        nameList.append(str(title.string))

        # end loop block

    # selects the price information from the div class and adds to the list
    for price in pagesrc2.find_all('div', id=re.compile("^offerPrice")):

        priceList.append(re.sub(r"[$,]", "", str(price.string)))

        # end loop block

    # selects the description information from the page and adds it to the list
    for description in pagesrc2.find_all('p', class_=re.compile("^desc")):

        descList.append(str(description.string))

        # end loop block

    print(x)
    try:
        link = driver.find_element_by_id("forward")
        link.click()
    except NoSuchElementException:
        break
    link = None
    x += 1
    # end loop
# end loop

# loop has completed add lists to dataframe
df['VendorID'] = vendorList
df['PartNumber'] = partList
df['Name'] = nameList
df['Price'] = priceList
df['Description'] = descList


# goes back one page
# driver.execute_script("window.history.go(-1)")

# end the Selenium browser session
driver.quit()

# view dataframe
print(tabulate(df))
