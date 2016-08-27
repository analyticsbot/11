from random import choice

## start product hunt action. Upvote product. Tweet product.
## visit product page
def productHuntAction(driver, username, password, bio, product_hunt_tech, c_producthunt):
    logging.info("Starting Product hunt action for " +  username)
    product_hunt_url = getProductHuntUrl(c_producthunt)
    logging.info("Going to the product hunt url == "+ product_hunt_url)
    driver.get(product_hunt_url)
    time.sleep(random.randint(10,20))
    driver.get(product_hunt_tech)
    logging.info("Going to the product hunt tech url == "+ product_hunt_tech)
    time.sleep(random.randint(15,20))
    ## click on the upvote button
    voted =[]
    upvotes = driver.find_elements_by_css_selector('.button_2I1re.smallSize_1da-r.secondaryText_PM80d.simpleVariant_1Nl54.button_2n20W')
    titles = driver.find_elements_by_css_selector('.title_2p9fd.featured_2W7jd.default_tBeAo.base_3CbW2')
    logging.info("Number of upvotes possible on this "+ len(upvotes) + ' titles total : ' +  len(titles))
    options = [i*4 for i in range(0, (len(upvotes)/4)+1)]
    try:
        while True:
            toVote = random.choice(options)
            if titles[toVote/4].text != HANDLE:
                upvotes[toVote].click()
                time.sleep(4)
                voted.append(toVote)
                logging.info("Upvoted the handle == "+ titles[toVote/4].text)
                break
    except:
        logging.info("Did not find handle == "+ HANDLE)
    time.sleep(10)
    ## click on the twitter login button
    try:
        driver.find_element_by_css_selector('.secondaryText_PM80d.inverse_1CN6F.base_3CbW2').click()
        logging.info("Logging in using twitter "+ username)
    except:
        pass
    time.sleep(3)
    ## authorize the twitter application
    try:
        driver.find_element_by_css_selector('.submit.button.selected').click()
        logging.info("Authotizing login using twitter "+ username)
        time.sleep(10)
    except:
        pass

    # check if asks for bio. usually the first time
    try:
        time.sleep(10)
        headline= driver.find_element_by_id('headline')
        headline.send_keys(bio)
        driver.find_element_by_css_selector('.button_2I1re.mediumSize_10tzU.secondaryBoldText_1PBCf.secondaryText_PM80d.techSolidColor_3JJ0o.solidVariant_2wWrf').click()
        logging.info("Adding a bio to the account "+ username)        
    except:
        pass
    time.sleep(10)
    titles = driver.find_elements_by_css_selector('.title_2p9fd.featured_2W7jd.default_tBeAo.base_3CbW2')
    upvotes = driver.find_elements_by_css_selector('.button_2I1re.smallSize_1da-r.secondaryText_PM80d.simpleVariant_1Nl54.button_2n20W')
    try:
        for title in titles:
            if title.text.strip() == HANDLE:
                logging.info("Upvoted the handle == "+ HANDLE)
                upvotes[titles.index(title)*4].click()
                voted.append(titles.index(title)*4)
                title.click()
                time.sleep(2)
                try:
                    tw = driver.find_element_by_id('twitter')
                    tw.click()
                    time.sleep(5)
                    driver.find_element_by_css_selector('.button_2I1re.mediumSize_10tzU.secondaryBoldText_1PBCf.secondaryText_PM80d.twitterSolidColor_G22Bs.solidVariant_2wWrf').click()
                    time.sleep(2)
                    driver.find_element_by_css_selector('.modal--close.v-desktop')
                    p=driver.current_window_handle
                    h=driver.window_handles
                    h.remove(p)
                    driver.switch_to_window(h.pop())
                    driver.find_element_by_css_selector('.button.selected.submit').click()
                    driver.close()
                    driver.switch_to_window(p)
                    time.sleep(2)
                except:
                    pass
    except:
        logging.error("Cant Upvoted the handle == "+ HANDLE)
    time.sleep(10)
    driver.get(product_hunt_tech)
    logging.info("Going to url "+ product_hunt_tech)        
    time.sleep(10)
    count = 0
    upvotes = driver.find_elements_by_css_selector('.button_2I1re.smallSize_1da-r.secondaryText_PM80d.simpleVariant_1Nl54.button_2n20W')
    try:
        for vote in upvotes:
            driver.get(product_hunt_tech)
            time.sleep(10)
            titles = driver.find_elements_by_css_selector('.title_2p9fd.featured_2W7jd.default_tBeAo.base_3CbW2')
            upvotes = driver.find_elements_by_css_selector('.button_2I1re.smallSize_1da-r.secondaryText_PM80d.simpleVariant_1Nl54.button_2n20W')
            to_vote = random.choice(options)
            time.sleep(2)
            if to_vote not in voted:
                upvotes[to_vote].click()
                count +=1
                time.sleep(5)
                titles[to_vote/4].click()
                logging.info("upvoted "+ titles[to_vote/4].text) 
                try:
                    tw = driver.find_element_by_id('twitter')
                    time.sleep(5)
                    tw.click()
                    time.sleep(5)
                    driver.find_element_by_css_selector('.button_2I1re.mediumSize_10tzU.secondaryBoldText_1PBCf.secondaryText_PM80d.twitterSolidColor_G22Bs.solidVariant_2wWrf').click()
                    time.sleep(2)
                    driver.find_element_by_css_selector('.modal--close.v-desktop')
                    time.sleep(2)
                    p=driver.current_window_handle
                    h=driver.window_handles
                    h.remove(p)
                    driver.switch_to_window(h.pop())
                    driver.find_element_by_css_selector('.button.selected.submit').click()
                    driver.close()
                    driver.switch_to_window(p)
                except:
                    pass
                driver.get(product_hunt_tech)
                time.sleep(5)
            if count == NUM_UPVOTES_PRODUCT_HUNT:
                break
    except:
        pass

    driver.get(product_hunt_games)
    time.sleep(15)
    driver.get(product_hunt_books)
    time.sleep(15)
    driver.get(product_hunt_home)
    time.sleep(15)
    
    ## logout from producthunt
    driver.find_element_by_css_selector('.placeholderHidden_pb7Bz').click()
    driver.find_element_by_css_selector('li.option_2XMGo:nth-child(6) > a:nth-child(1)').click()
    time.sleep(5)

    logging.info("logged out from product hunt for user name "+ username) 
    

    ## logout from twitter
    try:
        driver.get('https://twitter.com/')
        time.sleep(5)
        driver.find_element_by_css_selector('.btn.js-tooltip.settings.dropdown-toggle.js-dropdown-toggle').click()
        driver.find_element_by_css_selector('#signout-button').click()
        time.sleep(2)
    except:
        pass

    logging.info("logged out from twitter for user name "+ username) 
