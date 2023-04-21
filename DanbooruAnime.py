import sqlite3
import json
import os
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver


def GetArtistname():
    # use selenium to request the artist Json data as request lib cannot get the Json data
    driver = webdriver.Chrome()
    driver.get(
        "https://danbooru.donmai.us/artists.json?login=zhiyew0106&api_key=PmSnM9x5qbFD8eR3ExjbbJqs&limit=120&page=1")
    content = driver.page_source
    data = re.match('(.*?)pre-wrap;">\[(.*?)\]</pre></body></html>', content).group(2)
    # handle the Json data and get the name and other names in Json data
    dic = {'name': [], 'other_names': []}
    for i in data.split('id'):
        try:
            if 'name' in i:
                v = i.split(',')[2].split(':')[1].replace('\"', '')
                dic['name'].append(v)
            if 'other_names' in i:
                v1 = eval(i.split(',"other_names":')[1].split('}')[0])
                dic['other_names'].append(v1)
        except:
            pass
    # close the web driver
    driver.quit()

    return dic


def GetArtist(artist_data, cur, conn):
    # create table and create insert sql line
    cur.execute('''CREATE TABLE IF NOT EXISTS artist_data (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    name_ VARCHAR(100), 
                    other_names VARCHAR(100));
                    ''')
    sql = '''
            INSERT INTO artist_data (name_, other_names)
            VALUES
            (?, ?);
           '''

    names = artist_data['name']
    onms = artist_data['other_names']

    # get the id form tag data table and use the id to store the new 25 items
    try:
        cur.execute('SELECT id FROM artist_data WHERE id = (SELECT MAX(id) FROM artist_data)')
        start = cur.fetchone()
        start = start[0]
    except:
        start = 0

    for i in range(start, start + 25):
        try:
            tmp = onms[i][0]
        except:
            tmp = 'none'
        cur.execute(sql, (names[i], tmp))

    conn.commit()


def GetTagartist():
    # use selenium to request the tag Json data as request lib cannot get the Json data
    driver = webdriver.Chrome()
    driver.get(
        "https://danbooru.donmai.us/tags.json?login=zhiyew0106&api_key=PmSnM9x5qbFD8eR3ExjbbJqs&limit=120&&page=1")
    content = driver.page_source
    data = re.match('(.*?)pre-wrap;">\[(.*?)\]</pre></body></html>', content).group(2)

    dic = {'name': [], 'category': [], 'post_count': []}
    for i in data.split('{"id"'):
        try:
            if 'name' in i:
                v = eval(i.split(',')[1].split(':')[1])
                dic['name'].append(v)
            if 'category' in i:
                v1 = int(i.split(',')[3].split(':')[1])
                dic['category'].append(v1)

            if 'post_count' in i:
                v2 = int(i.split(',')[2].split(':')[1])
                dic['post_count'].append(v2)
        except:
            pass

    driver.quit()

    return dic


def GetTag(tag_data, cur, conn):
    # create tag data table and create insert sql line
    cur.execute('''
                    CREATE TABLE IF NOT EXISTS tag_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name_ VARCHAR(100), 
                        category INTEGER,
                        post_count INTEGER
                    );
                        ''')
    sql = '''
                INSERT INTO tag_data (name_, category,post_count)  VALUES  (?, ?, ?);
               '''

    names = tag_data['name']
    category = tag_data['category']
    post_count = tag_data['post_count']
    # l = 25 if len(names) > 25 else len(names)

    try:
        cur.execute('SELECT id FROM tag_data WHERE id = (SELECT MAX(id) FROM tag_data)')
        start = cur.fetchone()
        start = start[0]
    except:
        start = 0

    for i in range(start, start + 25):
        cur.execute(sql, (names[i], category[i], post_count[i]))

    conn.commit()


def main():
    conn = sqlite3.connect('Animeee.db')
    cur = conn.cursor()
    
    artist_data = GetArtistname()
    GetArtist(artist_data, cur, conn)

    tag_data = GetTagartist()
    GetTag(tag_data, cur, conn)

    cur.close()


if __name__ == '__main__':
    main()
