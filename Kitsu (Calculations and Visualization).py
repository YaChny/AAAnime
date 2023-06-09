import sqlite3
import plotly.graph_objects as go
import math

def calculate_stats(cur):
    stats_dic = {}
    
    cur.execute('SELECT MAX(episode_count) FROM Episode')
    maxi = cur.fetchone()[0]
    stats_dic["Maximum Number of Episode"] = maxi
    cur.execute('SELECT Popularity.title, Episode.episode_count FROM Episode JOIN Popularity ON Popularity.id = Episode.id WHERE Episode.episode_count = ' 
                + str(maxi))
    episode_max = []
    for row in cur:
        episode_max.append(row)
    stats_dic["Maximum"] = episode_max

    cur.execute('SELECT MIN(episode_count) FROM Episode')
    mini = cur.fetchone()[0]
    stats_dic["Minimum Number of Episode"] = mini
    cur.execute('SELECT Popularity.title, Episode.episode_count FROM Episode JOIN Popularity ON Popularity.id = Episode.id WHERE Episode.episode_count = ' 
                + str(mini))
    episode_min = []
    for row in cur:
        episode_min.append(row)
    stats_dic["Minimum"] = episode_min

    return stats_dic

def calculate_number(cur, stats_dic):
    diff = stats_dic["Maximum Number of Episode"] - stats_dic["Minimum Number of Episode"]
    each_diff = round(diff / 5)

    number_dic = {}
    i = 0
    begin = stats_dic["Minimum Number of Episode"]
    end = begin + each_diff - 1
    while i < 5:
        cur.execute('SELECT COUNT(*) FROM Episode WHERE episode_count >= ' + str(begin) + ' AND episode_count <= ' + str(end))
        amount = cur.fetchone()[0]
        name = str(begin) + '-' + str(end) + " Episodes"
        number_dic[name] = amount
        begin = end + 1
        end = begin + (each_diff - 1)
        i = i + 1

    cur.execute('SELECT COUNT(*) FROM Episode WHERE episode_count IS NULL')
    amount = cur.fetchone()[0]
    number_dic['To Be Determined'] = amount

    return number_dic

def calculate_percentage(cur, number_dic):
    percentage_dic = number_dic.copy()
    cur.execute('SELECT COUNT(id) FROM Episode')
    total = cur.fetchone()[0]
    for key in percentage_dic:
        percentage_dic[key] = percentage_dic[key] / int(total)

    return percentage_dic

def write_calculations(stats_dic, number_dic, percentage_dic, filename):
    with open(filename, 'w') as f:
        f.write("Maximum number of episodes: " + str(stats_dic["Maximum"]) + '\n' + '\n')
        f.write("Minimum number of episodes: " + str(stats_dic["Minimum"]) + '\n' + '\n')
        keys = list(number_dic.keys())
        categories = ", ".join(keys)
        f.write("The Categories: " + '\n' + categories + '\n' + '\n')
        f.write("Number of Anime in Each Category: " + '\n' + str(number_dic) + '\n' + '\n')
        f.write("Percentage of Anime in Each Category: " + '\n' + str(percentage_dic) + '\n')

def kitsuvisual(number_dic):
    keys = list(number_dic.keys())
    labels = keys
    values = list(number_dic.values())
    fig = go.Figure()
    fig.add_trace(go.Pie(labels = labels, values = values, hole = 0.3))
    fig.update_layout(title = 'First 100 Anime in Kitsu by Episode Count')
    fig.show()

def main():
    conn = sqlite3.connect('Animeee.db')
    cur = conn.cursor()
    filename = 'KitsuCalculation.txt'
    stats = calculate_stats(cur)
    episode_by_number = calculate_number(cur, stats)
    episode_by_percentage = calculate_percentage(cur, episode_by_number)
    write_calculations(stats, episode_by_number, episode_by_percentage, filename)
    kitsuvisual(episode_by_number)

if __name__ == '__main__':
    main()
