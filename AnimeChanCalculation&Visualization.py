import sqlite3
import plotly.graph_objects as go

def total_char_quote(cur):
    AnimeQuote = []
    AnimeQuoteChar = []
    cur.execute('SELECT UMAnime.Anime, UMAnimeQuotes.Quote FROM UMAnime JOIN UMAnimeQuotes ON UMAnime.id = UMAnimeQuotes.anime_id')
    for row in cur:
        AnimeQuote.append(row)
    cur.execute('SELECT UMAnimeCharacter.Character, UMAnimeQuotes.Quote FROM UMAnimeCharacter JOIN UMAnimeQuotes ON UMAnimeCharacter.id = UMAnimeQuotes.character_id')
    i = 0
    for row in cur:
        newtuple = AnimeQuote[i] + (row[0],)
        AnimeQuoteChar.append(newtuple)
        i += 1
    
    dic = {}
    for item in AnimeQuoteChar:
        AnimeName = item[0]
        AnimeChar = item[2]
        if AnimeName not in dic.keys():
            dic[AnimeName] = {}
            dic[AnimeName]["quote_num"] = 1
            dic[AnimeName]["char_num"] = {}
            dic[AnimeName]["char_num"][AnimeChar] = 1

        else:
            dic[AnimeName]["quote_num"] += 1
            if AnimeChar not in dic[AnimeName]["char_num"].keys():
                dic[AnimeName]["char_num"][AnimeChar] = 1
            else:
                dic[AnimeName]["char_num"][AnimeChar] += 1
    
    return dic

def MoreThanFiveQuotes(dic):
    FiveMore = {}
    AnimeLst = list(dic.keys())
    for i in range(0,len(AnimeLst)):
        if dic[AnimeLst[i]]["quote_num"] > 5:
            FiveMore[AnimeLst[i]] = dic[AnimeLst[i]]
    return FiveMore

def percentage_char_quote(dic):
    percentage_dic = {}
    AnimeLst = list(dic.keys())
    for i in range(0,len(AnimeLst)):
        if dic[AnimeLst[i]]["quote_num"] > 5:
            percentage_dic[AnimeLst[i]] = {}
            percentage_dic[AnimeLst[i]]["quote_num"] = dic[AnimeLst[i]]["quote_num"]
            percentage_dic[AnimeLst[i]]["char_percentage"] = {}
            CharLst = list(dic[AnimeLst[i]]["char_num"].keys())
            for c in CharLst:
                percentage_dic[AnimeLst[i]]["char_percentage"][c] = round(dic[AnimeLst[i]]["char_num"][c]/percentage_dic[AnimeLst[i]]["quote_num"],2)

    return percentage_dic

def write_result(FiveMore,dic,percentage_dic,filename):
    with open(filename, 'w') as f:
        f.write("Dictionary of total number of each character's quote in each animation which name contains 'um':\n"+ str(dic)+"\n")
        f.write("\n")
        f.write("Number of animation which has more than 5 quotes: " + str(len(percentage_dic)) + "\n")
        f.write("\n")
        f.write("Dictionary of animation which has more than 5 quotes: \n" + str(FiveMore) + "\n")
        f.write("\n")
        f.write("Percentage of animation which has more than 5 quotes: " + str(round(len(percentage_dic)/len(dic),2)) + "\n")
        f.write("\n")
        f.write("Dictionary of percentage of each character's quote in each animation which has more than 5 quotes: \n" + str(percentage_dic) + "\n")

def AnimeChanVisual(FiveMore):
    AnimeLst = list(FiveMore.keys())
    for i in range(0,len(AnimeLst)):
        CharLst = []
        NumQuoLst = []
        CharLst = list(FiveMore[AnimeLst[i]]['char_num'].keys())
        for c in CharLst:
            NumQuoLst.append(FiveMore[AnimeLst[i]]['char_num'][c])
        
        fig = go.Figure(data=[go.Pie(labels=CharLst,values=NumQuoLst)])
        title_str = "The percentage of each character's quotes in '" + AnimeLst[i] + "'"
        fig.update_layout(title = title_str)
        fig.show()

def main():
    conn = sqlite3.connect('Animeee.db')
    cur = conn.cursor()
    filename = 'AnimeChanCalculation.txt'
    dic = total_char_quote(cur)
    FiveMore = MoreThanFiveQuotes(dic)
    percentage_dic = percentage_char_quote(dic)
    write_result(FiveMore,dic,percentage_dic,filename)
    AnimeChanVisual(FiveMore)

if __name__ == '__main__':
    main()
