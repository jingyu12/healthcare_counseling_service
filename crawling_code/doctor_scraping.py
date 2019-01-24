# -*- coding: utf-8 -*-
"""
Created on Sat May 12 20:09:15 2018

@author: jingyu
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys

import os
import pandas as pd
import numpy as np
from itertools import chain

os.chdir('D:/myworks/18-1/ssem')


##################
# scraping data
##################    

# get answer_count
def scraping_at_one_page():
    title_list=[]
    question_list=[]
    answer_list=[]
    category_list=[]
    for i in range(1,21):        
        elem=driver.find_element_by_xpath('//*[@id="au_board_list"]/tr['+str(i)+']/td[1]/a')
        elem.click()
        # alarm check
        try:
            driver.switch_to_alert().accept()
        except:
            pass
        try:            
            title=driver.find_element_by_xpath('//*[@id="qna_detail_question"]/div[1]/div[1]/div[2]/div/h3/span').text
            question=driver.find_element_by_xpath('//*[@id="contents_layer_0"]/div[1]/div').text
            answer=driver.find_element_by_xpath('//*[@id="contents_layer_1"]/div[1]/div[1]').text
        
            title_list.append(title)
            question_list.append(question)
            answer_list.append(answer)
            driver.execute_script("window.history.go(-1)")
            
            category=driver.find_element_by_xpath('//*[@id="au_board_list"]/tr['+str(i)+']/td[2]').text
            category_list.append(category)
            
        except NoSuchElementException:
            driver.execute_script("window.history.go(-1)")
        
    print('{} Q&A iteration is done'.format(i))
    return category_list, title_list,question_list,answer_list
    

# scraping whole page
def scraping_full_page():
    c_l=[]
    t_l=[]
    q_l=[]
    a_l=[]

    for i in range(2,page_number):
        try:
            category,title,question,answer=scraping_at_one_page()
            driver.get(doctor_home_list+'&page='+str(i))
            c_l.append(category)
            t_l.append(title)
            q_l.append(question)
            a_l.append(answer)
        except:
            break   
        
    c_l=list(chain.from_iterable(c_l))    
    t_l=list(chain.from_iterable(t_l))
    q_l=list(chain.from_iterable(q_l))
    a_l=list(chain.from_iterable(a_l))
    
    print('One doctor iteration is done')
    return c_l,t_l,q_l,a_l


def scraping_doctors():
    c_l=[]    
    t_l=[]
    q_l=[]
    a_l=[]
    
    for j in doctor_home_list:
        category,title,question,answer=scraping_full_page()
        
        c_l.append(category)
        t_l.append(title)
        q_l.append(question)
        a_l.append(answer)    

    c_l=list(chain.from_iterable(c_l))    
    t_l=list(chain.from_iterable(t_l))
    q_l=list(chain.from_iterable(q_l))
    a_l=list(chain.from_iterable(a_l))
    
    print('All doctor iteration is done')
    
    df=pd.DataFrame({'category':c_l,"title":t_l,"question":q_l, "answer":a_l})
    return df


##################
# start scraping
##################  
driver=webdriver.Chrome()
doctor_home_list=['https://kin.naver.com/userinfo/expert/answerList.nhn?u=foesgGoCxeaoqOfW%2FGZ0lfiGi%2BETYAg41vMGC3F2TVs%3D', # 권용석 - 도박,대인기피 불안 우울
                  'https://kin.naver.com/userinfo/expert/answerList.nhn?u=HaNfIgmblpoaWZLW%2FUqzLu7EcB%2BNPc9ybXr1CIjefDI%3D', #배성범 - 심층 심리상담
                  'https://kin.naver.com/userinfo/expert/answerList.nhn?u=muRAqD6M6AZv1lFnK9HSVYdF93jaiT2ua%2FfGkO9evRU%3D', #신재현 - 심리 우울 등
                  'https://kin.naver.com/userinfo/expert/answerList.nhn?u=qcZLsqvG%2BT3sMqUUapiLQzXD%2FdwCInjtelZij9STaNk%3D', # 최인광 - 성
                  'https://kin.naver.com/userinfo/expert/answerList.nhn?u=Z%2BitweAKz3zoUvmtGcO59f%2B4JMIlcuZFZ2U%2Bwjqe2Wk%3D', # 이재원 - 중독, 치매
                  'https://kin.naver.com/userinfo/expert/answerList.nhn?u=erkXaH7nhn5z2CJiosYaYZflw%2FbPmf%2BA3zwKvS6aIWI%3D', # 김윤석 - 우울 
                  'https://kin.naver.com/userinfo/expert/answerList.nhn?u=1M6GH75rGtFog11VCDg45SNQoafAb%2FR%2FORRUDYvQwz4%3D', # 조연수 - 우울 
                  'https://kin.naver.com/userinfo/expert/answerList.nhn?u=4pfTcY9BOdbKtOSgWQPqRN5TYJ9qONHNr81BlOg5ubg%3D', # 신상헌 - 무기력 ,수면
                  ]


def run_scraping():    
    full_df=pd.DataFrame()
    for i in doctor_home_list:
        driver.get(i)
        answer_count=driver.find_element_by_xpath('//*[@id="content"]/dl/dd[1]').text
        page_number=int(np.round(int(answer_count)/20))
        print('The page number of this doctor is :',page_number)    
        df=scraping_doctors()
        full_df=full_df.append(df)
    
    return full_df

df=run_scraping()

pd.DataFrame.to_csv(df,'health_care_qa.csv')
driver.quit()