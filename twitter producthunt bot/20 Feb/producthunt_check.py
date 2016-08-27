from selenium import webdriver

driver = webdriver.Firefox()
driver.get('https://www.producthunt.com/')

product_hunt_tech = 'https://www.producthunt.com/tech'
product_hunt_games = 'https://www.producthunt.com/games'
product_hunt_books = 'https://www.producthunt.com/books'
product_hunt_home = 'https://www.producthunt.com/'

username = 'SamathaLennertz'
password = 'iOP1839ylee'

#driver.get(product_hunt_tech)
#driver.find_element_by_css_selector('.buttonContainer_wTYxi')

twitter_login_url = 'https://twitter.com/login/'
driver.get(twitter_login_url)
email_elem =  driver.find_element_by_css_selector('.js-username-field.email-input.js-initial-focus')
email_elem.send_keys(username)
pwd_elem =  driver.find_element_by_css_selector('.js-password-field')
pwd_elem.send_keys(password)
pwd_elem.submit()
driver.get(product_hunt_tech)
a =driver.find_elements_by_css_selector('.button_2I1re.smallSize_1da-r.secondaryText_PM80d.simpleVariant_1Nl54.button_2n20W')
a[0].click()
driver.find_element_by_css_selector('.secondaryText_PM80d.inverse_1CN6F.base_3CbW2').click()
titles = driver.find_elements_by_css_selector('.title_2p9fd.featured_2W7jd.default_tBeAo.base_3CbW2')
try:
    driver.find_element_by_css_selector('.submit.button.selected')
except:
    pass
try:
    driver.find_element_by_css_selector('.submit.button.selected').click()
except:
    pass
try:
    aa = 'DESIGN HERETIC, OPTIMIZATION SOOTHSAYER. I LOVE NEW YORK MORE THAN EVER.'
    headline= driver.find_element_by_id('headline')
    headline.send_keys(aa)
    driver.find_element_by_css_selector('.button_2I1re.mediumSize_10tzU.secondaryBoldText_1PBCf.secondaryText_PM80d.techSolidColor_3JJ0o.solidVariant_2wWrf').click()
except:
    pass

tw =driver.find_element_by_id('twitter')
tw.click()

p=driver.current_window_handle
h=driver.window_handles
h.remove(p)
driver.switch_to_window(h.pop())
driver.find_element_by_css_selector('.button.selected.submit').click()
driver.switch_to_window(p)
