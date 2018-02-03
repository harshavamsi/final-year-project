# -*- coding: utf-8 -*-

import urllib3 as ul
from bs4 import BeautifulSoup
import os
import time

#import requests
#import urllib2

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException


print "exec"

link = 'http://agmarknet.gov.in/PriceTrends/SA_Pri_Month.aspx'
http = ul.PoolManager()
page = http.request('GET', link)
soup = BeautifulSoup(page.data, "html.parser")
hh = webdriver.ChromeOptions()
hh.add_argument("--start-maximized")
driver = webdriver.Chrome()
driver.get(link)  # opening the link in the driver .
commodities = soup.find_all('select', id='cphBody_Commodity_list')
print commodities


path = '//select[@id="cphBody_Commodity_list"]'
commodity_element = driver.find_element_by_xpath(path)
commodity_select = Select(commodity_element)

commodity_values = ['%s' % o.get_attribute(
    'value') for o in commodity_select.options[2:]]
print commodity_values


def get_year_select():
    path = '//select[@id="cphBody_Year_list"]'
    year_select_elem = driver.find_element_by_xpath(path)
    year_select = Select(year_select_elem)
    return year_select


def get_month_select():
    path = '//select[@id="cphBody_Month_list"]'
    month_select_elem = driver.find_element_by_xpath(path)
    month_select = Select(month_select_elem)
    return month_select


def select_commodity_option(value, dowait=True):
    '''
    Select state value from dropdown. Wait until district dropdown
    has loaded before returning.
    '''
    path = '//select[@id="cphBody_Year_list"]'
    year_select_elem = driver.find_element_by_xpath(path)

    def year_select_updated(driver):
        try:
            year_select_elem.text
        except StaleElementReferenceException:
            return True
        except:
            pass

        return False
    path = '//select[@id="cphBody_Commodity_list"]'
    commodity_element = driver.find_element_by_xpath(path)
    commodity_select = Select(commodity_element)
    commodity_select.select_by_value(value)

    if dowait:
        wait = WebDriverWait(driver, 20)
        wait.until(year_select_updated)

    return get_year_select()


def select_year_option(value, dowait=True):
    '''
    Select state value from dropdown. Wait until district dropdown
    has loaded before returning.
    '''
    path = '//select[@id="cphBody_Month_list"]'
    month_select_elem = driver.find_element_by_xpath(path)

    def month_select_updated(driver):
        try:
            month_select_elem.text
        except StaleElementReferenceException:
            return True
        except:
            pass

        return False

    year_select = get_year_select()
    year_select.select_by_value(value)

    if dowait:
        wait = WebDriverWait(driver, 20)
        wait.until(month_select_updated)

    return get_month_select()


def select_month_option(value, dowait=True):
    month_element = get_month_select()
    month_element.select_by_value(value)

#from selenium.webdriver.common.action_chains import ActionChains


def rename(commodity, year, month):
    os.rename('/Users/hackintosh/Downloads/Agmarknet_State_wise_Wholesale_Prices_Monthly_Analysis.xls',
              '/Users/hackintosh/Downloads/%s_%s_%s.xls' % (commodity, year, month))


def submit_download(values, year, month):
    select_month_option(month)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.find_element_by_id("cphBody_But_Submit").click()
    time.sleep(5)
    driver.find_element_by_id("cphBody_Button1").click()
    time.sleep(5)
    rename(values, year, month)
    # driver.find_element_by_id("cphBody_btnBack").click()


#import time

accepted_list = ['17', '3', '1', '19', '78', '24', '35', '22', '25', '27']
accepted_years = ['2012', '2013', '2014', '2015', '2016']
for values in commodity_values:
    print 'here'
    print values
    if values in accepted_list:
        k = 1
        years = select_commodity_option(values)
        years_values = ['%s' % o.get_attribute(
            'value') for o in years.options[1:]]
        print years_values
        for year in years_values:
            if year in accepted_years:
                w = 0
                if k != 1:
                    select_commodity_option(values)
                months = select_year_option(year)
                month_values = ['%s' % o.get_attribute(
                    'value') for o in months.options[1:]]
                for month in month_values:
                    if os.path.exists('/Users/hackintosh/Downloads/%s_%s_%s.xls' % (values, year, month)):
                        continue
                    w = w + 1
                    if w != 1:
                        select_commodity_option(values)
                        select_year_option(year)
                    select_month_option(month)
                    submit_download(values, year, month)
                    k = k + 1
                    driver.get(link)  # opening the link in the driver .
                    path = '//select[@id="cphBody_Commodity_list"]'
                    commodity_element = driver.find_element_by_xpath(path)
            else:
                continue
    else:
        continue
commodity_select = Select(commodity_element)
