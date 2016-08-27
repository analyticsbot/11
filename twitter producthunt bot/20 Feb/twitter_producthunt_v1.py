from selenium import webdriver
from random import choice

driver = webdriver.Firefox()

twitter_url = 'https://twitter.com/login/'
driver.get(twitter_url)
username = 'SamathaLennertz'
password = 'iOP1839ylee'

email_elem =  driver.find_element_by_css_selector('.js-username-field.email-input.js-initial-focus')
email_elem.send_keys(username)
pwd_elem =  driver.find_element_by_css_selector('.js-password-field')
pwd_elem.send_keys(password)

##btn = driver.find_element_by_css_selector('.submit.btn.primary-btn')
##btn.click()
pwd_elem.submit()
trend_elem = driver.find_elements_by_css_selector('.trend-item.js-trend-item')
choice(trend_elem).find_element_by_tag_name('a').click()

## follow some handles
accounts = driver.find_elements_by_css_selectors('.AdaptiveStreamUserGallery.AdaptiveSearchTimeline-separationModule.js-stream-item')
for account in accounts:
    grid = account.find_element_by_css_selector('.Grid-cell.u-size1of2')
    follow = grid.find_element_by_css_selector('.button-text.follow-text')
    follow.click()

tweets = driver.find_elements_by_css_selector('.js-stream-item.stream-item.stream-item.expanding-stream-item')
numTweets = 0
while True:
    numTweets +=1
    tweet = choice(tweets)
    footer = tweet.find_element_by_css_selector('.stream-item-footer')
    rt = footer.find_element_by_css_selector('.ProfileTweet-actionButton.js-actionButton.js-actionRetweet')
    rt.click()

    if numTweets>5:
        break

## tweet some stuff
elem_tweet_box = driver.find_element_by_xpath("//*[@id=\"tweet-box-mini-home-profile\"]")
elem_tweet_box.clear()
elem_tweet_box.send_keys(tweet_new)

tweet_click_box = driver.find_element_by_xpath("//*[@id=\"timeline\"]/div[1]/div/form/div[2]/div[2]/button/span[1]")
tweet_click_box.click()

## follow some random people
account_elem = driver.find_element_by_css_selector('.flex-module')
accounts_to_follow = account_elem.find_elements_by_css_selector('.js-account-summary.account-summary.js-actionable-user')
for account in accounts_to_follow:
    follow_btn = account.find_element_by_css_selector('.small-follow-btn.follow-btn.btn.small.follow-button.js-recommended-item')
    follow_btn.click()

## load some links from product hunt
## visit product hunt using these links


