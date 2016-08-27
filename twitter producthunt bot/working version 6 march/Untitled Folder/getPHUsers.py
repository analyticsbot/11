from selenium import webdriver
import string, time, os, requests, shutil
import pandas as pd

def downloadProfileImage(link, name):
    response = requests.get(url, stream=True)
    with open(images_folder + '/' + name.replace('/','') + '.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    
driver = webdriver.Firefox()
alphabets = string.ascii_lowercase

images_folder = 'images'
if not os.path.exists(images_folder):
    os.makedirs(images_folder)

for search in alphabets:
    url = 'https://www.producthunt.com/search?q='+search+'&qType=users'
    count = 1

    df = pd.DataFrame(columns=['image', 'username', 'name', 'userUrl', 'headline'])
    driver.get(url)
    numProfiles = [1,2,3]
    while True:
        user_elements = driver.find_elements_by_css_selector('.user-card-list--item')
        numProfiles.append(len(user_elements))
        if numProfiles[-2] == numProfiles[:-1] == numProfiles[:-3]:
            break

        for elem in user_elements:
            try:
                try:
                    img = elem.find_element_by_css_selector('.user-image.user-card--image.v-big').find_element_by_tag_name('img').get_attribute('src')
                except:
                    img = 'NA'
                try:
                    username = elem.find_element_by_css_selector('.user-card--username').text
                except:
                    username = 'NA'
                try:
                    name = elem.find_element_by_css_selector('.user-card--name').text
                except:
                    name = 'NA'
                try:
                    user_url = 'https://www.producthunt.com/'+username
                except:
                    user_url = 'NA'
                try:
                    headline = elem.find_element_by_css_selector('.user-card--headline').text
                except:
                    headline = 'NA'
                try:
                    downloadProfileImage(img, name)
                except:
                    pass
                if df.query('username == "' + username + '"').shape[0] == 0:
                    row = df.shape[0]
                    df.loc[row+1] = [img, username, name, user_url, headline]

                    if row>1008576:
                        df.to_csv(search + '_' + str(count) + '.csv', index = False)
                        df = pd.DataFrame(columns=['image', 'username', 'name', 'userUrl', 'headline'])
                        count+=1
            except Exception,e:
                print str(e)
                pass
            
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    df.to_csv(search + '_' + str(count) + '.csv', index = False)
