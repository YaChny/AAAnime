import sqlite3
import json
import os
import requests

def load_data(url):
    dataset = {}
    times = 0
    i = 0
    offset = 0

    while times < 5:
        params = {"page[limit]": 20, "page[offset]": offset}
        
        headers = {
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json"
            }
            
        request = requests.get(url, params=params, headers=headers)
        data = json.loads(request.text)
                
        for anime in data["data"]:
            dataset[i] = [anime["attributes"]["canonicalTitle"], anime["attributes"]["averageRating"], anime["attributes"]["userCount"], anime["attributes"]["episodeCount"]]
            i = i + 1
            
        offset = i
        
        times = times + 1
    
    return dataset

def create_table(cur, conn, data):
    cur.execute("CREATE TABLE IF NOT EXISTS Popularity (id INTEGER PRIMARY KEY, title TEXT, average_rating TEXT, user_count INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS Episode (id INTEGER PRIMARY KEY, episode_count INTEGER)")

    try:
        cur.execute('SELECT id FROM Popularity WHERE id = (SELECT MAX(id) FROM Popularity)')
        s = cur.fetchone()
        s = s[0]
    except:
        s = 0

    id = 1
    i = 0

    while i < 25:
        anime_id = id + s
        cur.execute("INSERT OR IGNORE INTO Popularity (id, title, average_rating, user_count) VALUES (?, ?, ?, ?)", (anime_id, data[anime_id - 1][0], data[anime_id - 1][1], data[anime_id - 1][2]))
        cur.execute("INSERT OR IGNORE INTO Episode (id, episode_count) VALUES (?, ?)", (anime_id, data[anime_id - 1][3]))
        id = id + 1
        i += 1

    conn.commit()

def main():
    conn = sqlite3.connect('Animeee.db')
    cur = conn.cursor()
    url = "https://kitsu.io/api/edge/anime"
    dataset = load_data(url)
    create_table(cur, conn, dataset)
    cur.close()

if __name__ == '__main__':
    main()