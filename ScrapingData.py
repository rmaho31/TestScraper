from selenium import webdriver
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
x = 2
datalist = pd.DataFrame([],
                        columns=["VendorID", "PartNumber", "Name", "Price", "Description", "PhotoPath"])

for page in pagesrc1.find_all('li'):
    # give pagesource to beautifulsoup
    pagesrc2 = BeautifulSoup(driver.page_source, 'lxml')

    list1 = []
    # selects the elements that have the product name information contained in the div class title
    for vendor in pagesrc2.find_all('div', class_=re.compile("^merchantLogo")):
        img = vendor.find('img', alt=True)

        list1.append(str(img['alt']))\

        # end loop block

    # loop has completed add list to dataframe
    df['VendorID'] = list1

    list1 = []
    # selects the elements that have the partNumber information just made up from the image path
    for partNumber in pagesrc2.find_all('div', class_=re.compile("^col-xs-3 col-md-2 listProdImg")):
        img = partNumber.find('img')

        list1.append(re.sub(r";", "", re.search(r"\d+?;", str(img['src'])).group(0)))

        # end loop block

    # loop has completed add list to dataframe
    df['PartNumber'] = list1

    list1 = []
    # selects the elements that have the product name information contained in the div class title
    for title in pagesrc2.find_all('div', class_=re.compile("^title")):

        list1.append(str(title.string))

        # end loop block

    # loop has completed add list to dataframe
    df['Name'] = list1

    list1 = []
    # selects the price information from the div class and adds to the list
    for price in pagesrc2.find_all('div', id=re.compile("^offerPrice")):

        list1.append(re.sub(r"[$,]", "", str(price.string)))

        # end loop block

    # loop has completed add list to dataframe
    df['Price'] = list1

    list1 = []
    # selects the description information from the page and adds it to the list
    for description in pagesrc2.find_all('p', class_=re.compile("^desc")):

        list1.append(str(description.string))

        # end loop block

    # loop has completed add list to dataframe
    df['Description'] = list1
    datalist.append(df, ignore_index=True)
    link = driver.find_element_by_id(str(x))
    if link is not None:
        link.click()
    else:
        break
    x += 1
    # end loop
# end loop


# goes back one page
# driver.execute_script("window.history.go(-1)")

# end the Selenium browser session
driver.quit()

# view dataframe
print(tabulate(datalist))
