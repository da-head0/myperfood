import pandas as pd
from pydantic import main
from pymongo import MongoClient
import json
import numpy as np
import sklearn
from sklearn.decomposition import TruncatedSVD

def compare_taste(cat_id):

    df = pd.read_csv('function/catfood_nodup.csv')
    rating = pd.read_csv('function/rating.csv')

    df['soup'] = df['brand'] +' ' + df['title']  +' ' + df['classification']  +' ' + df['content']  +' ' + df['info']
    df['soup'] = df['soup'].astype(str) # 이래야 에러가 안남

    cat_rating = rating[['고양이_ID','rating', 'title']]
    combined_foods_data = pd.merge(df,cat_rating, on='title', how='left') # 자동으로 inner가 되나.. 

    rating_crosstab = combined_foods_data.pivot_table(values='rating', index='고양이_ID', columns='soup', fill_value=0) # 없는 값은 0으로 채우기.

    rating_crosstab['favorite'] = ""
    rating_crosstab['soso'] = ""
    rating_crosstab['no'] = ""

    for i in range(len(rating_crosstab)):
        for j in range(len(rating_crosstab.columns)):
            try:
                if int(rating_crosstab.iloc[i,j]) >= 4 : # 2,5,5,1,0,5,0,...
                    rating_crosstab.iloc[i,-3] += rating_crosstab.columns[j] + ' '
                elif 3<= int(rating_crosstab.iloc[i,j]) <4 :
                    rating_crosstab.iloc[i,-2] += rating_crosstab.columns[j] + ' '
                elif 1<= int(rating_crosstab.iloc[i,j]) < 3:
                    rating_crosstab.iloc[i,-1] += rating_crosstab.columns[j] + ' '
                else:
                    pass
            except: pass

    # 해당 고양이 ID 넣으면 됨. 1.0, 2.0 ... 
    fav = rating_crosstab.loc[cat_id,'favorite']
    ss = rating_crosstab.loc[cat_id,'soso']
    nn = rating_crosstab.loc[cat_id,'no']

    df2 = df[['index', 'title', 'soup']]
    
    from math import log # IDF 계산을 위해
    docs = [fav, ss, nn]
    vocab = list(set(w for doc in df2['soup'].tolist() for w in doc.split()))
    #vocab.sort() # 이거 안하니까 할때마다 랜덤이 됐다.

    N = len(docs)

    def tf(t, d):
        return d.count(t)

    def idf(t):
        df = 0
        for f in fav:
            df += t in f
        return log(N)/(df+1)

    def tfidf(t, d):
        return tf(t,d) * idf(t)


    # tf 구하기 - DTM 데이터프레임에 저장하여 출력

    result = []
    for i in range(N):
        result.append([])
        d = docs[i]
        for j in range(len(vocab)):
            t = vocab[j]
            result[-1].append(tf(t,d))

    tf_ = pd.DataFrame(result, columns = vocab, index=['fav', 'soso', 'no'])
    tfsum = tf_.T
    tfsum['sum'] = ((tfsum['fav'] * 2) + (tfsum['soso'] * 1) + (tfsum['no'] * 0)) / 3
    avgdtm = tfsum[['sum']]
    avgdtm = avgdtm.T

    # 기존 df -> dtm으로 만들어 유사도 비교

    docs = df2['soup'].tolist()
    vocab = list(set(w for doc in docs for w in doc.split()))
    vocab.sort()

    N = len(docs)

    def tf(t, d):
        return d.count(t)

    def idf(t):
        df = 0
        for f in fav:
            df += t in f
        return log(N)/(df+1)

    def tfidf(t, d):
        return tf(t,d) * idf(t)

    result = []
    for i in range(N):
        result.append([])
        d = docs[i]
        for j in range(len(vocab)):
            t = vocab[j]
            result[-1].append(tf(t,d))

    tf_2 = pd.DataFrame(result, columns = vocab, index=df2.title.tolist())

    from numpy import dot
    from numpy.linalg import norm
    import numpy as np
    def cos_sim(A, B):
        return dot(A, B) / (norm(A)*norm(B))

    sim_scores = []
    for i in range(len(tf_2)):
        sim_scores.append((i,cos_sim(avgdtm, tf_2.iloc[i])))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]

    food_indices = [i[0] for i in sim_scores]
    
    result = df2['title'].iloc[food_indices]
    return result.tolist()


#print(compare_taste(1))