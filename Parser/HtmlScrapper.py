from bs4 import BeautifulSoup
import urllib.request
from time import sleep
from selenium import webdriver
import webbrowser
# webbrowser.open("http://calendar.ou.edu/")
# link = urllib.request.urlopen("http://calendar.ou.edu/")
# r = BeautifulSoup(link,"html.parser")
# print(r.prettify())

browser = webdriver.Chrome()
browser.get("http://calendar.ou.edu/#view/day/date/20170319")
sleep(4)
eventdiv = browser.find_element_by_class_name("lw_cal_event_list")
div = eventdiv.find_elements_by_tag_name("div")
EventNum = 0

for i in div:
    new = i.get_attribute("class")
    div = i.get_attribute("div")
    if new[:12] == "lw_cal_event":
        EventNum =  EventNum+1

print(EventNum)
for i in range(1,EventNum):
    print(browser.find_element_by_xpath('//*[@id="lw_cal_day_rightcol"]/div[1]/div['+ str(i) +']/div[@class = "lw_events_location"]').text)
    print(browser.find_element_by_xpath('//*[@id="lw_cal_day_rightcol"]/div[1]/div[' + str(i) + ']/div[@class = "lw_events_time"]').text)
    print(browser.find_element_by_xpath('//*[@id="lw_cal_day_rightcol"]/div[1]/div[' + str(i) + ']/div[@class = "lw_events_title"]').text)

browser.quit()

