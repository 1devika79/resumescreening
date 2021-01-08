from os import environ
import pandas as pd
import numpy as np 
import sqlite3   
from flask_mail import Message
from sqlalchemy import create_engine
from pandas.io import sql
from flaskblog import app,mail


def automation(EP,post_id,post):
    dataFrame   = pd.DataFrame() 
    engine = create_engine('sqlite:///flaskblog/site.db')
    print(engine.table_names())
    db = pd.read_sql_table('post', engine)
    dE = pd.read_sql_table('employee', engine)
    print(db)
    print(dE)
    dE=dE[dE.id.isin(EP)]
    print(EP)
    my_dataframe = db
    my_dataframe.dropna(
        axis=0,
        how='any',
        thresh=None,
        subset=None,
        inplace=True
    )
    new_frame=db.loc[db['id'] == post_id]
    print(new_frame)
    new_data=new_frame.iloc[0]['skillsrequired']
    print(new_data)
    list1=new_data.split(',')
    print(list1)
    df=[]
    df = pd.DataFrame(df, columns =list1)
    merged = pd.concat([dE,df])
        # Python code to find Euclidean distance 
        # using dot() 

        #intializing points in 
        # numpy arrays 
        # subtracting vector 
    def all_sim(U_skills,df_skills,idf):
    #U_skills means the skills of the current user
    #df is the column containing the skills of every EMployee
    #idf is a duplicate table containing all the data of the employees
        cos_list=[]
        for item in df_skills:
            x=euclidist(U_skills,item)
            cos_list.append(x)
        idf['euclidist']=cos_list
    def euclidist(point1,point2):
        temp = np.array(point1) - np.array(point2 )

        # doing dot product 
        # for finding 
        # sum of the squares 
        sum_sq = np.dot(temp.T, temp) 

        # Doing squareroot and 
        # printing Euclidean distance 
        dist=np.sqrt(sum_sq)
        return dist

    def createdata(db_skills,curr_skills,df):
        for sk in curr_skills:
            j=0
            l1=[]
            for skill in db_skills:
                if sk in skill :
                    l1.append('1')  
                else:
                    l1.append('0')
            df[sk]=l1
        #now df contains all the data we need as per the current_logic
    createdata(merged['skills'],list1,merged)
    x=merged.iloc[:,13:].values
    new_list = [list(map(int, lst)) for lst in x]
    list2=[1]*len(list1)
    all_sim(list2,new_list,merged)
    idf_sort=merged.sort_values(['euclidist'])
    #renaming the index values to get the clear picture
    idf_rearr=idf_sort.rename(index=lambda x:x+1)
    dk=idf_rearr.reset_index()
    dk['RANKING FOR THE JOB'] = dk.index+1
    DD=dk.drop(['index','id','password'],axis=1)
    dd=DD.drop(list1,axis=1)

    dd.to_excel("flaskblog/output.xlsx")
    email=post.author.email
    print(type(email))
    e='jishaanil@gmail.com'
    print(type(e))
    subject='list of automated applied candidates'
    mesg='This attachement contain the lis of candidates in the order of Top to Bottom'
    msg=Message(subject,sender='project.main2020@gmail.com',recipients=[e])
    msg.body=mesg
    with app.open_resource('output.xlsx') as output:
        msg.attach('output.xlsx','text/xlsx',output.read())
        
    mail.send(msg)
    return

def recommand(emp_id):
    dataFrame   = pd.DataFrame() 
    engine = create_engine('sqlite:///flaskblog/site.db')
    print(engine.table_names())
    #need to add 0 or 1 to the columns if it contains the skill or not
    def createdata(db_skills,curr_skills,df):
        for sk in curr_skills:
            j=0
            l1=[]
            for skill in db_skills:
                if skill is not None:
                    if sk in skill and skill is not None :
                        l1.append('1')  
                    else:
                        l1.append('0')
                else:
                        l1.append('0')
            df[sk]=l1
        return
    #now df contains all the data we need as per the current_logic
    def cos_sim(a,b):
        dot_prod=np.dot(a,b)
        norm_a=np.linalg.norm(a)
        norm_b=np.linalg.norm(b)
        if((norm_a*norm_b)==0):
            return (0)
        else:
            return dot_prod/(norm_a*norm_b)
    def all_sim(U_skills,df_skills,idf):
    #U_skills means the skills of the current user
    #df is the column containing the skills of every EMployee
    #idf is a duplicate table containing all the data of the employees
        cos_list=[]
        for item in df_skills:
            x=cos_sim(U_skills,item)
            cos_list.append(x)
        idf['cos_similarity']=cos_list
        return
    def list_jobid(idf_rearr):
        list6=[]
        for i in range (5):
            if idf_rearr.iloc[i]['joballot'] is not None:
                list6+=list(map(int,(idf_rearr.iloc[i]['joballot']).split(',')))
        return (list6)
            
        
    db= pd.read_sql_table('employee', engine)
    print(db)
    list1=db['skills'][emp_id-1].split(',')
    df=[]
    df = pd.DataFrame(df, columns =list1)
    merged = pd.concat([db,df])
    print(type(merged['skills']))
    print(merged['skills'])
    createdata(merged['skills'],list1,merged)
    print(merged)
    x=merged.iloc[:,13:].values
    list2=[1]*len(list1)
    print(list2)
    new_list = [list(map(int, lst)) for lst in x]
    all_sim(list2,new_list,merged)
    #idf_sort is for sorting the values in cos_similarity column in ascending order
    idf_sort=merged.sort_values(['cos_similarity'], ascending=False)
    #renaming the index values to get the clear picture
    idf_rearr=idf_sort.rename(index=lambda x:x+1)
    Recommand_list=list_jobid(idf_rearr)
    mylist = list(dict.fromkeys(Recommand_list))
    mylist.sort()
    return mylist
