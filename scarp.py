import pandas as pd
import requests, urllib
url = 'https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies3.html'
response = requests.get(url)

from bs4 import BeautifulSoup
soup = BeautifulSoup(response.text, 'lxml')



url_list = []
for Url in soup.find_all('a'):
    url_list.append(Url.get('href'))
    
    
    def plot_text(soup):
    start = soup.find('h2').find_next('p')
    plot = start.text.strip()
    for elem in start.next_siblings:
        if elem.name != 'p':
            break
        plot += elem.text.strip()
    return plot

def intro_text(soup):
    start = soup.find('p')
    intro = start.text.strip()
    for elem in start.next_siblings:
        if elem.name != 'p':
            break
        intro += elem.text.strip()
    return intro
columns =['Wikipedia Url', 'title', 'intro', 'plot','Directed by','Produced by','Written by','Screenplay by','Story by','Based on','Starring','Narrated by','Music by','Cinematography','Edited by','Production','company','Distributed by','Release date','Running time','Country','Language','Budget','Box','office']
df = pd.DataFrame(columns=columns)


import random, time

not_able_to_scarp = {}
j = 0
for link in url_list[:20]:
    try:
        html_wiki = urllib.request.urlopen(link).read()
        soup = BeautifulSoup(html_wiki ,'html.parser')
        df.loc[j , 'Wikipedia Url'] = link
        df.loc[j , 'title'] = soup.find('h1').get_text()
        df.loc[j ,'intro'] =  intro_text(soup)
        if df.loc[j ,'intro']=='':
            try:
                df.loc[j ,'intro'] =soup.find('p').find_next_sibling('p').text.strip()
            except:
                pass    
        
        
        for x,y in  zip(soup.find('table', class_="infobox vevent").find_all('th') , soup.find('table', class_="infobox vevent").find_all('td')):
                if x.text.strip() in columns:
                    df.loc[j , x.text.strip()] = y.text.strip()
        try:
            df.loc[j ,'plot'] = plot_text(soup)
            
        
        
        except:
            pass
        
    except requests.exceptions.RequestException as e:
        not_able_to_scarp[link] = e
    time.sleep(random.uniform(1,5))
    j+=1 
