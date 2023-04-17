import sqlite3
import json
import os
import requests
import re
from bs4 import BeautifulSoup

def GetUMAnimeLst():
    r = requests.get("https://animechan.vercel.app/api/available/anime")
    data = r.content
    Animelst = json.loads(data)
    UMAnimelst = []
    for anime in Animelst:
        if re.search('[Uu][Mm]',anime):
            if not re.search('[Uu][Mm]',Animelst[Animelst.index(anime)-1]):
                UMAnimelst.append(anime)
    return UMAnimelst

def GetCharacterLst():
    CharLst = []
    cur.execute('SELECT id,Anime FROM UMAnime')
    for row in cur:
        Animeid = row[0]
        AnimeName = row[1]
        url = "https://animechan.vercel.app/api/quotes/anime?title=" + AnimeName
        r = requests.get(url)
        data = r.content
        QuoteLst = json.loads(data)
        for quote in QuoteLst:
            character = quote["character"]
            if (character,Animeid) not in CharLst:
                CharLst.append((character,Animeid))
    return CharLst

def GetQuoteLst(UMAnimeLst, CharacterLst):
    QuoteLst = []
    for anime in UMAnimeLst:
        AnimeName = anime
        url = "https://animechan.vercel.app/api/quotes/anime?title=" + AnimeName
        r = requests.get(url)
        data = r.content
        QLst = json.loads(data)
        for q in QLst:
            characterid = -1
            character = q["character"]
            quote = q["quote"]
            for c in CharacterLst:
                if c[0] == character:
                    characterid = CharacterLst.index(c)
                    QuoteLst.append((quote,c[1],characterid))
    return QuoteLst

def GetUMAnimes(UMAnimeLst, cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS UMAnime(id INTEGER PRIMARY KEY, Anime TEXT)')
    try:
        cur.execute('SELECT id FROM UMAnime WHERE id = (SELECT MAX(id) FROM UMAnime)')
        start = cur.fetchone()
        start = start[0]
    except:
        start = 0
    id = 0
    for umanime in UMAnimeLst[start:start+25]:
        umanime_id = id + start
        cur.execute('INSERT OR IGNORE INTO UMAnime (id,Anime) VALUES (?,?)',(umanime_id,umanime))
        id += 1
    conn.commit()
        
def GetCharacters(CharLst, cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS UMAnimeCharacter(id INTEGER PRIMARY KEY, Character TEXT, anime_id INTEGER)')      
    try:
        cur.execute('SELECT id FROM UMAnimeCharacter WHERE id = (SELECT MAX(id) FROM UMAnimeCharacter)')
        start = cur.fetchone()
        start = start[0]
    except:
        start = 0
    id = 0
    for char in CharLst[start:start+25]:
        char_id = id + start
        cur.execute('INSERT OR IGNORE INTO UMAnimeCharacter (id,Character,anime_id) VALUES (?,?,?)',(char_id,char[0],char[1]))
        id += 1
    conn.commit()

def GetQuotes(QuoteLst, cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS UMAnimeQuotes(id INTEGER PRIMARY KEY, Quote TEXT, anime_id INTEGER, character_id INTEGER)')
    try:
        cur.execute('SELECT id FROM UMAnimeQuotes WHERE id = (SELECT MAX(id) FROM UMAnimeQuotes)')
        start = cur.fetchone()
        start = start[0]
    except:
        start = 0
    id = 0
    for quote in QuoteLst[start:start+25]:
        quote_id = id + start
        cur.execute('INSERT OR IGNORE INTO UMAnimeQuotes (id,Quote,anime_id,character_id) VALUES (?,?,?,?)',(quote_id,quote[0],quote[1],quote[2]))
        id += 1
    conn.commit()

def main():
    conn = sqlite3.connect('Animeee.db')
    cur = conn.cursor()
    UMAnimeLst = GetUMAnimeLst()
    GetUMAnimes(UMAnimeLst, cur, conn)
    CharacterLst = GetCharacterLst()
    GetCharacters(CharacterLst, cur, conn)
    QuoteLst = GetQuoteLst(UMAnimeLst, CharacterLst)
    GetQuotes(QuoteLst, cur, conn)
    cur.close()

if __name__ == '__main__':
    main()