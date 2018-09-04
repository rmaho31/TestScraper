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
driver.implicitly_wait(5)
driver.get(url)

# setup dataFrame
df = pd.DataFrame([],
                  columns=["VendorID", "PartNumber", "Name", "Price", "Description", "PhotoPath"])

# initializing lists
vendorList = []
partList = []
nameList = []
priceList = []
descList = []
PhotoList = []

# new page source
pagesrc1 = BeautifulSoup(driver.page_source, 'lxml')\

for link in pagesrc1.find_all('li'):

    # locates category and clicks
    cat_link = driver.find_element_by_link_text(str(link.string))
    cat_link.click()  # click link

    # new page source
    pagesrc2 = BeautifulSoup(driver.page_source, 'lxml')

    # prepare category list
    categories = pagesrc2.find('ul', class_="attribute-box", id=False)

    idx1 = 0
    for link2 in categories.find_all('a'):
        # locate and click category
        category = driver.find_element_by_link_text(str(link2.string))
        category.click()

        # new page source
        pagesrc3 = BeautifulSoup(driver.page_source, 'lxml')

        # prepare vendor list
        vendors = pagesrc3.find('ul', id="storesList")

        idx2 = 0
        for link3 in vendors.find_all('a'):
            # locate and click vendors
            vendor = driver.find_element_by_link_text(str(link3.string))
            vendor.click()

            pagesrc4 = BeautifulSoup(driver.page_source, 'lxml')

            idx3 = 0
            for page in pagesrc4.find_all('li'):
                # new page source
                pagesrc5 = BeautifulSoup(driver.page_source, 'lxml')

                # selects the elements that have the product name information contained in the div class title
                for vendor in pagesrc5.find_all('div', class_=re.compile("^merchantLogo")):
                    img = vendor.find('img', alt=True)

                    vendorList.append(str(img['alt']))\

                    # end loop block

                # loop has completed add list to dataframe

                # selects the elements that have the partNumber information just made up from the image path
                for partNumber in pagesrc5.find_all('div', class_=re.compile("^col-xs-3 col-md-2 listProdImg")):
                    img = partNumber.find('img')

                    partList.append(re.sub(r";", "", re.search(r"\d+?;", str(img['src'])).group(0)))

                    # end loop block

                # selects the elements that have the product name information contained in the div class title
                for title in pagesrc5.find_all('div', class_=re.compile("^title")):

                    nameList.append(str(title.string))

                    # end loop block

                # selects the price information from the div class and adds to the list
                for price in pagesrc5.find_all('div', id=re.compile("^offerPrice")):

                    priceList.append(re.sub(r"[$,]", "", str(price.string)))

                    # end loop block

                # selects the description information from the page and adds it to the list
                for description in pagesrc5.find_all('p', class_=re.compile("^desc")):

                    descList.append(str(description.string))

                    # end loop block

                idx3 += 1
                try:
                    link = driver.find_element_by_id("forward")
                    link.click()
                except NoSuchElementException:
                    break
                link = None

                # end loop

            # steps backwards by index counter
            driver.execute_script("window.history.go(-" + str(idx3) + ")")

            # end loop

        idx2 += 1
        # steps backwards by index counter
        driver.execute_script("window.history.go(-" + str(idx2) + ")")

        # end loop

    idx1 += 1
    # steps backwards by index counter
    driver.execute_script("window.history.go(-" + str(idx1) + ")")

    # end loop

# end loop

# loop has completed add lists to dataframe
df['VendorID'] = vendorList
df['PartNumber'] = partList
df['Name'] = nameList
df['Price'] = priceList
df['Description'] = descList


# end the Selenium browser session
driver.quit()

# view dataframe
print(tabulate(df))
