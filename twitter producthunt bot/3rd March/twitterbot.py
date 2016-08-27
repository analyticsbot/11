from selenium import webdriver
from random import choice

## function to interact with twitter. like, RT, follow, trends
def TwitterAction(driver, username, password, c_tweets):
    driver.get(twitter_login_url)
    logging.info("Logging into the twitter account ")
    email_elem =  driver.find_element_by_css_selector('.js-username-field.email-input.js-initial-focus')
    email_elem.send_keys(username)
    pwd_elem =  driver.find_element_by_css_selector('.js-password-field')
    pwd_elem.send_keys(password)

    pwd_elem.submit()
    time.sleep(2)
    logging.info("Successfully logged into the twitter account ")
    trend_elem = driver.find_elements_by_css_selector('.trend-item.js-trend-item')
    logging.info("Number of trends to play with :: " + str(NUM_TRENDS))
    num_trends = 0
    while True:
        num_trends +=1
        if num_trends>NUM_TRENDS:
            break
        time.sleep(5)
        trend_elem = driver.find_elements_by_css_selector('.trend-item.js-trend-item')
        logging.info("Interacting with trend :: " + str(choice(trend_elem).find_element_by_tag_name('a').text))
        choice(trend_elem).find_element_by_tag_name('a').click()
        time.sleep(10)

        ## follow some handles
        try:
            accounts = driver.find_elements_by_css_selector('.button-text.follow-text')
            for account in accounts:
                try:
                    account.click()
                    logging.info("Followed an account")
                except Exception,e:
                    logging.error("Error following account")
        except Exception,e:
            logging.error("Account element not found")

        tweets = driver.find_elements_by_css_selector('.js-stream-item.stream-item.stream-item.expanding-stream-item')
        numTweets = 1
        while True:    
            tweet = choice(tweets)
            try:
                footer = tweet.find_element_by_css_selector('.stream-item-footer')
                rt = footer.find_element_by_css_selector('.ProfileTweet-actionButton.js-actionButton.js-actionRetweet')
                time.sleep(5)
                rt.click()
                time.sleep(5)
                driver.find_element_by_css_selector('.btn.primary-btn.retweet-action').click()
                time.sleep(2)
                numTweets +=1
            except Exception,e:
                print str(e)
                try:
                    driver.find_element_by_css_selector('.Icon.Icon--close.Icon--medium.dismiss').click()
                except Exception,e:
                    print str(e)
            if numTweets>5:
                logging.info("RTed 5 tweets. Moving to next trend")
                break
    
    ## go to homepage
    try:
        driver.find_element_by_css_selector('#global-nav-home').find_element_by_tag_name('a').click()
        logging.info("Moving to homepage to do the next action")
    except:
        driver.get('https://twitter.com/')

    ## tweet some stuff
    tweets = getTweets(c_tweets)
    try:
        for tweet in tweets:
            logging.info("Tweeting  -- " + tweet)
            elem_tweet_box = driver.find_element_by_xpath('//*[@id="tweet-box-home-timeline"]')
            elem_tweet_box.clear()
            elem_tweet_box.send_keys(tweet)
            tweet_click_box = driver.find_element_by_xpath("//*[@id=\"timeline\"]/div[2]/div/form/div[2]/div[2]/button/span[1]/span")
            tweet_click_box.click()
    except Exception,e:
        logging.error("Error tweeting")

    ## follow some random people
    try:
        account_elem = driver.find_element_by_css_selector('.flex-module')
        accounts_to_follow = account_elem.find_elements_by_css_selector('.js-account-summary.account-summary.js-actionable-user')
        for account in accounts_to_follow:
            follow_btn = account.find_element_by_css_selector('.small-follow-btn.follow-btn.btn.small.follow-button.js-recommended-item')
            follow_btn.click()
        logging.info("Followed some random people")
    except Exception,e:
        logging.error("No one to follow")

    logging.info("Twitter Action done for account " +  username)    
