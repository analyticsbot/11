from selenium import webdriver
import time, random
twitter_login_url = 'https://twitter.com/login/'
driver = webdriver.Firefox()
driver.get(twitter_login_url)
email_elem =  driver.find_element_by_css_selector('.js-username-field.email-input.js-initial-focus')
email_elem.send_keys('MeJeremy99')
pwd_elem =  driver.find_element_by_css_selector('.js-password-field')
pwd_elem.send_keys('Ju3Thiequ')
pwd_elem.submit()
time.sleep(3)
trend_elem = driver.find_elements_by_css_selector('.trend-item.js-trend-item.context-trend-item')
print len(trend_elem)

from random import choice
link= choice(trend_elem).find_element_by_tag_name('a').get_attribute('href')
driver.get(link)
g = driver.find_elements_by_css_selector('.js-tweet-text-container')
for i in g:
    
    try:
        i.click()
        time.sleep(1)
        a = driver.find_element_by_css_selector('.permalink-inner.permalink-tweet-container')
        b = a.find_element_by_css_selector('.ProfileTweet-actionButton.js-actionButton.js-actionRetweet')
        b.click()
        time.sleep(2)
        driver.find_element_by_css_selector('.btn.primary-btn.retweet-action').click()
        time.sleep(2)
        a.find_element_by_css_selector('.button-text.follow-text').click()
        numTweets +=1
        try:
            f = driver.find_element_by_css_selector('#permalink-overlay')
            f.click()
        except:
            pass
        try:
            driver.find_element_by_css_selector('.PermalinkProfile-dismiss').click()
        except:
            pass
        time.sleep(random.randint(2,5))
    except:
        pass
    
