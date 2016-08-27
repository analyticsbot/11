from selenium import webdriver
import time, random
driver = webdriver.Firefox()
twitter_login_url =  'https://twitter.com/login/'
username = 'LeanaFaughn'
password = 'cQR4131eoztx'
email='LeannaCorrea2707383@hotmail.com'
bio = 'Author'
username = 'DebraBurkholde'
password = 'Aekei9xoo'
email='WhiteMinervAekei@outlook.com'
bio = 'Wearer of unrelated hats'
driver.get(twitter_login_url)
email_elem =  driver.find_element_by_css_selector('.js-username-field.email-input.js-initial-focus')
email_elem.send_keys(username)
pwd_elem =  driver.find_element_by_css_selector('.js-password-field')
pwd_elem.send_keys(password)
pwd_elem.submit()
HANDLE = 'Codeology' ## handle or product that has to be always upvoted 
product_hunt_tech = 'https://www.producthunt.com/tech'
driver.get(product_hunt_tech)
NUM_UPVOTES_PRODUCT_HUNT=5

voted =[]
time.sleep(10)
while True:
    upvotes = driver.find_elements_by_css_selector('.button_2I1re.smallSize_1da-r.secondaryText_PM80d.simpleVariant_1Nl54.button_2n20W')
    if len(upvotes)>0:
        break
while True:
    titles = driver.find_elements_by_css_selector('.title_2p9fd.featured_2W7jd.default_tBeAo.base_3CbW2')
    if len(titles)>0:
        break
options = [i*4 for i in range(0, (len(upvotes)/4)+1)]
try:
    while True:
        toVote = random.choice(options)
        if titles[toVote/4].text != HANDLE:
            upvotes[toVote].click()
            time.sleep(4)
            voted.append(toVote)
            break
except:
    pass
time.sleep(3)
try:
    driver.find_element_by_css_selector('.secondaryText_PM80d.inverse_1CN6F.base_3CbW2').click()
except Exception,e:
    #print str(e)
    pass

try:
    while True:
        
        driver.find_element_by_css_selector('.twitterButton_2X0Lx.loginButton_1keGm').click()
        if 'product hunt' in driver.title():
            break
except:
    pass
time.sleep(3)
## authorize the twitter application
try:
    driver.find_element_by_css_selector('.submit.button.selected').click()
    #time.sleep(10)
except Exception,e:
    print str(e)
time.sleep(3)
# check if asks for bio. usually the first time
try:
    #time.sleep(10)
    headline= driver.find_element_by_id('headline')
    headline.send_keys(bio)
    try:
        driver.find_element_by_css_selector('.button_2I1re.mediumSize_10tzU.secondaryBoldText_1PBCf.secondaryText_PM80d.techSolidColor_3JJ0o.solidVariant_2wWrf').click()
    except:
        try:
            driver.find_element_by_css_selector('.button_2I1re.mediumSize_10tzU.secondaryBoldText_1PBCf.secondaryText_PM80d.orangeSolidColor_B-2gO.solidVariant_2wWrf').click()
        except:
            pass
except Exception,e:
    #print str(e)
    pass

time.sleep(2)
try:
    topics = driver.find_elements_by_css_selector('.button_2I1re.mediumSize_10tzU.secondaryBoldText_1PBCf.secondaryText_PM80d.simpleVariant_1Nl54')
    for topic in topics:
        topic.click()
    driver.find_element_by_css_selector('.button_2I1re.mediumSize_10tzU.secondaryBoldText_1PBCf.secondaryText_PM80d.orangeSolidColor_B-2gO.solidVariant_2wWrf').click()
except:
    pass
        
    time.sleep(10)
while True:
    upvotes = driver.find_elements_by_css_selector('.button_2I1re.smallSize_1da-r.secondaryText_PM80d.simpleVariant_1Nl54.button_2n20W')
    if len(upvotes)>0:
        break
while True:
    titles = driver.find_elements_by_css_selector('.title_2p9fd.featured_2W7jd.default_tBeAo.base_3CbW2')
    if len(titles)>0:
        break
try:
    for title in titles:
        if title.text.strip() == HANDLE:
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
##                p=driver.current_window_handle
##                h=driver.window_handles
##                h.remove(p)
##                driver.switch_to_window(h.pop())
                driver.find_element_by_css_selector('.button.selected.submit').click()
##                driver.close()
##                driver.switch_to_window(p)
                time.sleep(2)
            except Exception,e:
                print str(e)
except Exception,e:
    print str(e)
time.sleep(10)
driver.get(product_hunt_tech)
time.sleep(10)
count = 0
while True:
    upvotes = driver.find_elements_by_css_selector('.button_2I1re.smallSize_1da-r.secondaryText_PM80d.simpleVariant_1Nl54.button_2n20W')
    if len(upvotes)>0:
        break
while True:
    titles = driver.find_elements_by_css_selector('.title_2p9fd.featured_2W7jd.default_tBeAo.base_3CbW2')
    if len(titles)>0:
        break
try:
    for vote in upvotes:
        driver.get(product_hunt_tech)
        time.sleep(10)
        while True:
            upvotes = driver.find_elements_by_css_selector('.button_2I1re.smallSize_1da-r.secondaryText_PM80d.simpleVariant_1Nl54.button_2n20W')
            if len(upvotes)>0:
                break
        while True:
            titles = driver.find_elements_by_css_selector('.title_2p9fd.featured_2W7jd.default_tBeAo.base_3CbW2')
            if len(titles)>0:
                break
        to_vote = random.choice(options)
        time.sleep(4)
        if to_vote not in voted:
            upvotes[to_vote].click()
            count +=1
            time.sleep(5)
            titles[to_vote/4].click()
            try:
                time.sleep(5)
                tw = driver.find_element_by_id('twitter')
                time.sleep(5)
                tw.click()
                time.sleep(5)
                driver.find_element_by_css_selector('.button_2I1re.mediumSize_10tzU.secondaryBoldText_1PBCf.secondaryText_PM80d.twitterSolidColor_G22Bs.solidVariant_2wWrf').click()
                time.sleep(2)
                driver.find_element_by_css_selector('.modal--close.v-desktop')
                time.sleep(2)
                #p=driver.current_window_handle
                #h=driver.window_handles
                #h.remove(p)
                #driver.switch_to_window(h.pop())
                time.sleep(2)
                driver.find_element_by_css_selector('.button.selected.submit').click()
                #driver.close()
                #driver.switch_to_window(p)
            except Exception,e:
                print str(e)
                #driver.close()
            driver.get(product_hunt_tech)
            time.sleep(5)
        if count == NUM_UPVOTES_PRODUCT_HUNT:
            break
except Exception,e:
    print str(e)
#button_2I1re mediumSize_10tzU secondaryBoldText_1PBCf secondaryText_PM80d simpleVariant_1Nl54
#button_2I1re mediumSize_10tzU secondaryBoldText_1PBCf secondaryText_PM80d simpleVariant_1Nl54
