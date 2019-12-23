##made by aldric LIOTTIER
##contact aldric.liottier@epitech.eu or aldric.liottier@gmail.com
##web scapper to check the warranty status
import os
from selenium import webdriver as driver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from sys import exit

#when i = 1 the program exit
i = 0
#path.mdma is file that can be opened with txt, it contain the important pathes for the script to work
path = open("path.mdma", "r").read()  
pathes = path.split('\n')
passtime = 0

#the scrapper script for dell
def scrapper_dell(file, line):
  try:
   #pathes[0] is the path for chrome and can be modified in path.mdma
   CHROME_PATH = pathes[0]
   #pathes[1] is the path for the chrome webdriver used by selenium
   CHROMEDRIVER_PATH = pathes[1]
   WINDOW_SIZE = "1920,1080"
   chrome_options = Options()
   #headless option allow chrome to be opened but not seen
   chrome_options.add_argument("--headless")
   chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
   chrome_options.binary_location = CHROME_PATH
   d = driver.Chrome(executable_path=CHROMEDRIVER_PATH,
                          chrome_options=chrome_options)
   #for dell (and only dell) the path to the website is always the same with the exception of the harware serial number, so i just put it in between
   d.get("https://www.dell.com/support/home/fr/fr/frdhs1/product-support/servicetag/" + line[19] + "/overview")
   #i check is a select word is in the source page
   if ("Date d’expiration" not in d.page_source):
    try:
     #i select the warranty status in the page before writing it
     warrant = d.find_element_by_xpath('//*[@id="warrantyExpiringLabel"]').text
     file.write(warrant)
     file.write("->")
     #then i write the important information
     file.write(line[3])
     file.write("\n")
    except:
      #sometime a probleme can appear and the script won't know why, so it write status unknown, the user will have to check himself
      file.write("Status Unknown")
      file.write("->")
      file.write(line[3])
      file.write("\n")
   d.close()
  except:
   passtime = 0

def scrapper_lenovo(file, line):
  try:
   CHROME_PATH = pathes[0]
   CHROMEDRIVER_PATH = pathes[1]
   WINDOW_SIZE = "1920,1080"
   chrome_options = Options()  
   chrome_options.add_argument("--headless")
   chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
   chrome_options.binary_location = CHROME_PATH
   d = driver.Chrome(executable_path=CHROMEDRIVER_PATH,
                          chrome_options=chrome_options)  
   #go to lenovo main page to look up warranty
   d.get("https://pcsupport.lenovo.com/fr/fr/warrantylookup")
   #since unlike dell for lenovo the website path change, here i select the scearch bar and enter the hardware serial number
   search_bar = d.find_element_by_xpath('//*[@id="input_sn"]')
   search_bar.send_keys(line[19])
   search_bar.send_keys(Keys.RETURN)
   #i leave some time for the page to load
   time.sleep(4)
   try:
    warrant = d.find_element_by_xpath('//*[@id="W-Warranties"]/section/div/div/div[1]/div[1]/div[1]/p[1]/span').text
    if (warrant[0] == '0'):
     file.write(warrant)
     file.write("->")
     file.write(line[3])
     file.write("\n")
   except:
      file.write("Status Unknown")
      file.write("->")
      file.write(line[3])
      file.write("\n")
   d.close()
  except:
   passtime = 0

def scrapper_HP(file, line):
  try:
      CHROME_PATH = pathes[0]
      CHROMEDRIVER_PATH = pathes[1]
      WINDOW_SIZE = "1920,1080"
      chrome_options = Options()  
      chrome_options.add_argument("--headless")
      chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
      chrome_options.binary_location = CHROME_PATH
      d = driver.Chrome(executable_path=CHROMEDRIVER_PATH,
                             chrome_options=chrome_options)
      #go to HP french (if you want to look up foreign computer do it yourself (or ask me i am quite nice)) main warranty lookup page  
      d.get("https://support.hp.com/fr-fr")
      search_bar = d.find_element_by_xpath('//*[@id="directionTracker"]/app-layout/app-home/div[2]/app-detect-device/div/div/div/div[2]/div/div/div[1]/app-pfinder/div/app-one-box-search/div/div[1]/div/input')
      search_bar.send_keys(line[19])
      search_bar.send_keys(Keys.RETURN)
      time.sleep(4)
      try:
        warrant = d.find_element_by_xpath('//*[@id="remainingDuration"]').text
        if warrant[0] == '0':
          file.write(warrant)
          file.write("->")
          file.write(line[3])
          file.write("\n")
      except:
         file.write("Status Unknown")
         file.write("->")
         file.write(line[3])
         file.write("\n")
      d.close()
  except:
   passtime = 0

def check_lines(lines):
   n = 1
   num_lines = len(lines)
   #open and create the file that will contain the output
   file = open(pathes[2],"a+")
   #check every line to see if one of the three website as of 2019 that display warranty status contain information about the product
   while n < len(lines):
     try:
      line = lines[n].split('\t')
      if "Dell Inc" in line[17]:
         scrapper_dell(file, line)
      elif "LENOVO" in line[17]:
         scrapper_lenovo(file, line)
      elif "Hewlett-Packard" in line[17] or "HP" in line[17]:
         scrapper_HP(file, line)
      n = n + 1
      print(n, "file done in ", num_lines)
     except:
      n = n + 1
   file.close()
   n = n + 1

def application():
    global i
    #get current path, it is legacy code kept just in case
    place = os.getcwd()
    #go to the content folder (folder containing the output and input files)
    os.chdir(pathes[3])
    try:
       #if the output file already exist, remove it
       os.remove(pathes[2])
    except:
      i = 0
    #look at the content folder
    directory = os.listdir()
    #open the first file found, legacy code kept in case the boss want to be able to do multiple files at once
    file = open(directory[0], "r")
    lines = file.readlines()
    check_lines(lines)
    file.close()
    #i = 1 before an exit quit the code without error
    i = 1
    exit(0)

def main():
  
   try:
    application()

main()