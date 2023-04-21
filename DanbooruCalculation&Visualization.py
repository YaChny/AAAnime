import sqlite3
import matplotlib.pyplot as plt
import numpy as np


def visual():
    # create connection to Animeeee.db
    conn = sqlite3.connect('Animeee.db')
    cur = conn.cursor()
    # create a sql statement for selected tag data table category and post_counts and
    # inner join the artist data table by id conditional
    sql = '''
                SELECT  tag_data.category, tag_data.post_count FROM tag_data join artist_data on tag_data.id = artist_data.id
               '''
    cur.execute(sql)
    # get the data from database
    rows = cur.fetchall()

    conn.commit()
    conn.close()
    # calculate the total amount of post under the same category
    dic = {}
    for row in rows:
        category = row[0]
        post_count = row[1]
        if category not in dic.keys():
            dic[category] = post_count
        else:
            dic[category] += post_count
    # mapd is the original map over category
    mapd = {0: 'General',
            1: 'Artist',
            3: 'Copyright',
            4: 'Character',
            5: 'Meta'}
    dicdraw = {}
    # save the calculated results to DanbooruCalculation.txt
    with open('DanbooruCalculation.txt', 'w') as f:
        for k in mapd.keys():
            try:
                s = f'category: {k}  ==== post_count: {dic[k]} \n'
                dicdraw[k] = dic[k]
            except:
                s = f'category: {k}  ==== post_count: 0 \n'
                dicdraw[k] = 0

            f.write(s)

    # draw the histogram

    fig, ax = plt.subplots()

    fruits = [mapd[k]  for k in  dicdraw.keys()]

    counts = dicdraw.values()

    bar_colors = ['tab:green', 'tab:blue', 'tab:red','tab:purple', 'tab:orange']

    ax.bar(fruits, counts,  color=bar_colors)

    ax.set_ylabel('post_count')

    ax.set_title('Number of Posts in Each Category')
    # save the fig to fig.jpg
    plt.savefig('./fig.jpg')
    plt.show()

if __name__ == '__main__':
    visual()
