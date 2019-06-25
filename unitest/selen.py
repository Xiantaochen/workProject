from selenium import webdriver

driver = webdriver.Chrome()

driver.get("http://www.baidu.com")


source = driver.page_source()



driver.close()