

import pandas as pd
import re
import numpy as np
from konlpy.tag import Twitter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import os
os.chdir('D:/myworks/18-1/ssem')


mc=Twitter()

def get_nouns(doc):
    noun_list=mc.nouns(doc)
    noun_list=[noun for noun in noun_list if len(noun)>1]
    return ' '.join(noun_list)

# 정규표현식을 사용한 노이즈 제거
def delete_noise(text):
    noise = re.compile('[\t\n\r\xa0]')                
    result=noise.sub(' ',str(text))                   #  \t, \n, \r, \xa0 제거 
    result=re.sub('[^ ㄱ-ㅣ가-힣]+',' ',result)
    result=re.sub(' +<.*?>',' ',result)               # 특수문자 제거
    result=re.sub(r'[^\w]',' ',result)                # 특수문자 제거
    result=re.sub(' +',' ',result).strip()            # 여러 공백(multi space)을 하나의 공백으로 줄이기
    return result

def preprocessing_all(doc):
    result=delete_noise(doc)
    result=get_nouns(result)
    return result

def make_tf(documnet_list,tf_model):
    tf_feature_names=tf_vec.get_feature_names()
    tf=tf_model.transform(documnet_list)
    return tf,tf_feature_names


# n_topics -2 --> 1
def make_one_hot_vector(a):
    result=np.where(a.argsort()>4,1,0)
    return result


def last():
    merged=pd.read_pickle('merged.csv')
    tf_model=pd.read_pickle('tf_model.csv')
    lda=pd.read_pickle('lda.csv')
    tf_vec=pd.read_pickle('tf_vec.csv')
    return merged,tf_model,lda,tf_vec

def last2(your_input):
    # 지식인 Question으로 TF 모델 생성a
    tf_matrix,tf_feature_names=make_tf(pd.Series(preprocessing_all(your_input)),tf_model)
    prob_array=lda.transform(tf_matrix)
    ref_array=np.array(range(1,7))
    q_label=pd.Series(np.max(ref_array*make_one_hot_vector(prob_array),1))
    # return value
    print(q_label[0])


    
if __name__ == '__main__':
    merged,tf_model,lda,tf_vec=last()
    # input
    your_input=input('너의 고민은 무엇이니? ')

    last2(your_input)



