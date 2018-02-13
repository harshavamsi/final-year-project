# -*- coding: utf-8 -*-

import urllib3 as ul
from bs4 import BeautifulSoup
import os
import time
import csv
import re
#import requests
#import urllib2

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException


print "exec"

link = 'http://hydro.imd.gov.in/hydrometweb/(S(mwc4ktup0qmo5fz3acl1xtrl))/DistrictRaifall.aspx'
http = ul.PoolManager()
page = http.request('GET', link)
soup = BeautifulSoup(page.data)
hh = webdriver.ChromeOptions()
hh.add_argument("--start-maximized")
driver = webdriver.Firefox()
driver.get(link)  # opening the link in the driver .
locations = soup.find_all('select', id='listItems')
print locations


path = '//select[@id="listItems"]'
location_element = driver.find_element_by_xpath(path)
location_select = Select(location_element)

location_values = ['%s' % o.get_attribute(
    'value') for o in location_select.options[1:]]
print location_values


def get_district_select():
    print "indist"
    path = '//select[@id="DistrictDropDownList"]'
    district_select_elem = driver.find_element_by_xpath(path)
    district_select = Select(district_select_elem)
    return district_select


def select_location_option(value, dowait=True):
    '''
    Select state value from dropdown. Wait until district dropdown
    has loaded before returning.
    '''
    path = '//select[@id="DistrictDropDownList"]'
    district_select_elem = driver.find_element_by_xpath(path)

    def district_select_updated(driver):
        try:
            district_select_elem.text
        except StaleElementReferenceException:
            return True
        except:
            pass

        return False
    path = '//select[@id="listItems"]'
    location_element = driver.find_element_by_xpath(path)
    location_select = Select(location_element)
    location_select.select_by_value(value)

    if dowait:
        wait = WebDriverWait(driver, 20)
        wait.until(district_select_updated)

    return get_district_select()


def select_district_option(value, dowait=True):
    print "seldist"
    district_element = get_district_select()
    district_element.select_by_value(value)
#from selenium.webdriver.common.action_chains import ActionChains


def rename(values, district):
    os.rename('./weather_data/file.csv',
              './weather_data/%s_%s.csv' % (values, district))


def submit_download(values, district):
    element = driver.find_element_by_id('GridId')
    print element.text
    stripped = (line.strip() for line in element.text)
    lines = (line.split(",") for line in stripped if line)
    with open('./weather_data/file.csv', 'wb') as csvfile:
        csvfile.write(element.text)
    rename(values, district)
    # driver.find_element_by_id("cphBody_btnBack").click()


for values in location_values:
    print 'here'
    print values
    k = 1
    districts = select_location_option(values)
    district_values = ['%s' % o.get_attribute(
        'value') for o in districts.options[1:]]
    print district_values
    for district in district_values:

        if k != 1:
            select_location_option(values)
        # select_location_option(values)
        if district == 'KAVARATTI':
            continue
        print district
        select_district_option(district)
        driver.find_element_by_id("GoBtn").click()
        submit_download(values, district)
        k = k + 1
        driver.get(link)  # opening the link in the driver .
        path = '//select[@id="listItems"]'
        commodity_element = driver.find_element_by_xpath(path)
locations_select = Select(location_element)
