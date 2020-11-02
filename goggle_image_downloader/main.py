import os
import json
import requests
from bs4 import BeautifulSoup


GOOGLE_IMAGE = \
    'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

# The User-Agent request header contains a characteristic string 
# that allows the network protocol peers to identify the application type, 
# operating system, and software version of the requesting software user agent.
# needed for google search
usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

save_folder = 'images'

def main():
    if not os.path.exists(save_folder):
        os.mkdir(save_folder);
    download_images()
    
def download_images():
    data = input('what are you looking for? ')
    n_images = int(input('how many images do you want? '))
    
    print('searching...')
    
    searchurl = GOOGLE_IMAGE + 'q=' + data
    print(searchurl)
    
    response = requests.get(searchurl, headers=usr_agent)
    html = response.text
    
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.findAll('img', {'class':'rg_i Q4LuWd'})
    
    # imagelinks = []
    # for result in results:
    #     text= result['data-src']
    #     print(text)
    #     #link = result['data-src']
    #     #imagelinks.append(link)
    # print(imagelinks)
    
    count = 0
    links = []
    for res in results:
        try:
            link = res['data-src']
            links.append(link)
            count += 1
            if (count >= n_images): break

        except KeyError:
            continue
    
    #print(links)
    
    print(f'found {len(links)} images')
    
    print('start downloading...')
    
    for i, link in enumerate(links):
        response = requests.get(link)
        
        imagename = save_folder + '/' + data + str(i+1) + '.jpg'
        with open(imagename, 'wb') as file:
            file.write(response.content)
        

if __name__ == '__main__':
    main()