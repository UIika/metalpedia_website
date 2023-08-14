from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time

urls = (
    # 'https://www.metal-archives.com/bands/Slayer/72',
    # 'https://www.metal-archives.com/bands/Havok/34723',
    # 'https://www.metal-archives.com/bands/Metallica/125',
    # 'https://www.metal-archives.com/bands/Megadeth/138',
    'https://www.metal-archives.com/bands/Bredor/69019',
    # 'https://www.metal-archives.com/bands/DragonForce/2289',
    )

firefox_options = Options()
firefox_options.add_argument("--window-size=1920,1080")

def getbandsdata(url, browser):
    
    browser.get(url)
    time.sleep(2)

    band_name = browser.find_element(By.CSS_SELECTOR, 'h1.band_name').text.replace('/', '\\')

    country = browser.find_element(By.CSS_SELECTOR, 'dl.float_left>dd').text
    
    try:
        found_year = int(browser.find_elements(By.CSS_SELECTOR, 'dl.float_left>dd')[3].text)
    except:
        found_year = None
    
    try:
        breakup_year = int(browser.find_element(By.CSS_SELECTOR, 'dl.clear>dd').text[-4:])
    except:
        breakup_year = None
    
    logo = browser.find_element(By.CSS_SELECTOR, '#logo>img').get_attribute('src')
    
    band_photo = browser.find_element(By.CSS_SELECTOR, '#photo>img').get_attribute('src')
    
    genre = browser.find_element(By.CSS_SELECTOR, 'dl.float_right>dd').text

    albums_hrefs = [album.get_attribute('href') for album in browser.find_elements(By.CLASS_NAME, 'album')[::3]]

    albumslist = []
    
    for album in albums_hrefs:
        browser.get(album)
        album_name = browser.find_element(By.CLASS_NAME, 'album_name').text.replace('/', '\\')
        album_year = browser.find_elements(By.CSS_SELECTOR, 'dl.float_left>dd')[1].text[-4:]
        album_cover = browser.find_element(By.CSS_SELECTOR, 'a.image>img').get_attribute('src')
        songslist = []
        songs = browser.find_elements(By.CSS_SELECTOR, 'td.wrapWords')
        song_durations = browser.find_elements(By.CSS_SELECTOR, 'td[align="right"]')
        song_durations = [song_durations[i].get_attribute('innerHTML') for i,v in enumerate(song_durations)
                            if len(song_durations[i].get_attribute('innerHTML'))<9]
        for num, song in enumerate(songs):
            song_num = num+1
            song_name = song.text.replace('/', '\\')
            song_duration = song_durations[num]
            songslist.append({'song_name':song_name,
                                'song_duration':song_duration,
                                'song_num':song_num})
            if song_name in ('...', '-', '!!!','???', '!', '?', '.', '..'):
                songslist.pop()
        albumslist.append({'album_name':album_name,
                            'album_year':album_year,
                            'album_cover':album_cover,
                            'songslist':songslist
                            })
        
    browser.get(url)
    
    members_hrefs = [member.get_attribute('href') for member in \
        browser.find_elements(By.CSS_SELECTOR, '#band_tab_members_current .lineupRow a')]
    memberslist = []
    
    for member in members_hrefs:
        browser.get(member)
        member_name = browser.find_element(By.CSS_SELECTOR, 'h1.band_member_name').get_attribute('innerHTML').replace('/', '\\')
        member_prof = browser.find_element(By.CSS_SELECTOR, '.member_in_band_role strong').\
            get_attribute('innerHTML').replace('/', '\\')
        member_age = browser.find_elements(By.CSS_SELECTOR, 'dl.float_left dd')[1].\
            get_attribute('innerHTML').strip()
        try:
            member_rip = browser.find_elements(By.CSS_SELECTOR, 'dl.float_left dd')[2].\
                get_attribute('innerHTML').strip()
        except:
            member_rip = None
        try:
            member_photo = browser.find_element(By.CSS_SELECTOR, 'a.image img').get_attribute('src')
        except:
            member_photo = None
        memberslist.append({'member_name':member_name,
                            'member_prof':member_prof,
                            'member_age':member_age,
                            'member_rip':member_rip,
                            'member_photo':member_photo,
                            })
    
    browser.get(url)
        
    exmembers_hrefs = [member.get_attribute('href') for member in \
        browser.find_elements(By.CSS_SELECTOR, '#band_tab_members_past .lineupRow a')]
    exmemberslist = []
    
    for exmember in exmembers_hrefs:
        browser.get(exmember)
        exmember_name = browser.find_element(By.CSS_SELECTOR, 'h1.band_member_name').get_attribute('innerHTML').replace('/', '\\')
        exmember_prof = browser.find_element(By.CSS_SELECTOR, '#artist_tab_past .member_in_band_role strong').\
            get_attribute('innerHTML').replace('/', '\\')
        exmember_age = browser.find_elements(By.CSS_SELECTOR, 'dl.float_left dd')[1].\
            get_attribute('innerHTML').strip()
        try:
            exmember_rip = browser.find_elements(By.CSS_SELECTOR, 'dl.float_left dd')[2].\
                get_attribute('innerHTML').strip()
        except:
            exmember_rip = None
        try:
            exmember_photo = browser.find_element(By.CSS_SELECTOR, 'a.image img').get_attribute('src')
        except:
            exmember_photo = None
        exmemberslist.append({'exmember_name':exmember_name,
                            'exmember_prof':exmember_prof,
                            'exmember_age':exmember_age,
                            'exmember_rip':exmember_rip,
                            'exmember_photo':exmember_photo,
                            })
    
    return({'name': band_name,
                    'country': country,
                    'found_year': found_year,
                    'breakup_year': breakup_year,
                    'logo': logo,
                    'band_photo': band_photo,
                    'genre': genre,
                    'albumslist':albumslist,
                    'memberslist':memberslist,
                    'exmemberslist':exmemberslist,
                    'link': url
                    })
    
if __name__ == '__main__':
    getbandsdata(urls)