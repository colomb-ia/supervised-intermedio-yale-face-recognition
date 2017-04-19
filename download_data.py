import os, sys, urllib, stat
import zipfile, time
from selenium import webdriver

#check OS version: 'linux2' ,'win32' or 'darwin'(MAC)
print "Downloading dataset...\n (... it may open a chrome window, please dont close it ...)"
version = sys.platform
extension = ""
if version == 'linux2':
    from pyvirtualdisplay import Display #headless browser available only in Linux
    display = Display(visible=0, size=(800, 600))
    display.start()
    if sys.maxsize > 2**32: #it is then 64 bits
        webdriver_url = 'https://chromedriver.storage.googleapis.com/2.29/chromedriver_linux64.zip'
    else:
        webdriver_url = 'https://chromedriver.storage.googleapis.com/2.29/chromedriver_linux32.zip'
elif version == 'win32':
    extension = ".exe"
    webdriver_url = 'https://chromedriver.storage.googleapis.com/2.29/chromedriver_win32.zip'
elif version == 'darwin':
    webdriver_url = 'https://chromedriver.storage.googleapis.com/2.29/chromedriver_mac64.zip'
else:
    raise ValueError("No supported OS")

#Download now driver
chromedrive = urllib.URLopener()
chromedrive.retrieve(webdriver_url, "chromedriver.zip")

#Extract it, chmod to +x and delete zip
zip_ref = zipfile.ZipFile("chromedriver.zip", 'r')
zip_ref.extractall()
chromename = 'chromedriver'+extension
st = os.stat(chromename)
os.chmod(chromename, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
zip_ref.close()

#Configure selenium
chromedriver =  os.getcwd()+'/'+chromename
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : os.getcwd()+'/'}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

#Donwload
TRAINING_SET_URL = "http://cbcl.mit.edu/software-datasets/heisele/download/download.html"
driver.get(TRAINING_SET_URL)
driver.find_element_by_link_text("download now").click();

#Wait to download to complete
file_path = os.getcwd() + "/MIT-CBCL-facerec-database.zip"
while not os.path.exists(file_path):
    time.sleep(1)
    if os.path.exists(file_path+".crdownload"):
        statinfo = os.stat(file_path+".crdownload")
        print "{}%".format(int (statinfo.st_size/121643276.0*100))

print "DONE"
driver.quit()
if version == 'linux2':
    display.stop()
os.remove(chromename)
os.remove("chromedriver.zip")
