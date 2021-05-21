import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import style
from gtts import gTTS
import uuid
import playsound
import speech_recognition as sr
import os
import re
import webbrowser
import smtplib
from time import ctime
import bs4
import requests
def listen():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("I am listening..")
        audio=r.listen(source,phrase_time_limit=5)
    data=""
    try:
        data=r.recognize_google(audio,language='en-US')
        print(data)
    except sr.UnknownValueError:
        print("I dont know")
    except sr.RequestError as e:
        print("Request Failed")
    return data
def respond(string):
    print(string)
    tts=gTTS(text=string,lang="en")
    filename ='Spech%s.mp3' %str(uuid.uuid4())
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)
def abilities(data):
    if "show only" in data.casefold():
        df=new.original
        cols=list(df.columns)
        cols_lower=[x.lower() for x in cols]
        print(cols)
        respond("How many columns do you want to show")
        count=listen()
        if count[:2]=='Tu':
            respond('Did you mean 2?')
            boolean=listen()
            if boolean=='yes':
                count='2'
            else:
                count=listen()
        if count[:3]=='aur':
            respond('Did you mean 4?')
            boolean=listen()
            if boolean=='yes':
                count='4'
            else:
                count=listen()
        while count.isdecimal()!=True:
            respond("Try saying a number!")
            count=listen()
            if count[:2]=='Tu':
                respond('Did you mean 2?')
                boolean=listen()
                if boolean=='yes':
                    count='2'
            if count[:3]=='aur':
                respond('Did you mean 4?')
                boolean=listen()
                if boolean=='yes':
                    count='4'
        respond("Specify your required {} columns one by one  from the above list".format(count))
        required_cols=[]
        count=int(count)
        while(count>0):
            temp_col=listen()
            if temp_col.lower() in cols_lower:
                required_cols.append(temp_col.lower())
                count-=1
                continue
            respond("{} column is not present in the data ,try another".format(temp_col))
        useless_cols=[]
        for x in cols:
            if x.lower() in required_cols:
                continue
            useless_cols.append(x)
        df.drop(useless_cols,axis=1,inplace=True)
        excel.dataframe=df
        print(df.head())
        respond("I just showed you only 5 rows. Do you want to see the complete data?")
        boolean=listen()
        if 'yes' in boolean.casefold():
                print(df)
        new.dataframe=df
        print("___________________________________________________________________________________________________")
        return True
    
    if "show data" in data.casefold():
        df=new.dataframe
        cols=list(df.columns)
        lower_cols=[x.lower() for x in cols]
        print(cols)
        respond('Select a column to choose a criteria')
        criteria_col=listen()
        while True:
            if criteria_col.lower() in lower_cols:
                break
            respond("{} column is not present in the data".format(criteria_col))
            criteria_col=listen()
        for x in cols:
            if x.lower()==criteria_col.lower():
                criteria_col=x
        criteria_list=df[criteria_col].unique()
        lower_criteria_list=[x.lower() for x in criteria_list]
        print(criteria_list)
        print()
        respond("Select a criteria from {} in the above list".format(criteria_col))
        criteria=listen()
        while True:
            if criteria.lower() in lower_criteria_list:
                break
            respond("{} column is not present in the data".format(criteria))
            criteria=listen()
        for x in criteria_list:
            if x.lower()==criteria.lower():
                criteria=x
        df=df.loc[df[criteria_col]==criteria]
        print(df.head())
        new.dataframe=df
        print("___________________________________________________________________________________________________")
        return True
    if "pie" in data.casefold():
        df=new.dataframe
        cols=list(df.columns)
        cols_lower=[x.lower() for x in cols]
        print(cols)
        respond("Specify the column for category axis")
        category_col=listen()
        while True:
            if category_col.lower() in cols_lower:
                break
            respond("{} column is not present in the data".format(category_col))
            category_col=listen()

        respond("specify the column which contain numerical data for value axis")
        value_col=listen()
        while True:
            if value_col.lower() in cols_lower:
                break
            respond("{} column is not present in the data".format(value_col))
            value_col=listen()
        for x in cols:
            if x.lower()==category_col.lower():
                category_col=x
                continue
            if x.lower()==value_col.lower():
                value_col=x
        df=df.groupby(category_col)[value_col].sum().reset_index()
        df=df.set_index(category_col)
        df.plot.pie(subplots=True,autopct='%1.0f%%', figsize=(5, 5))
        plt.show()
        print("___________________________________________________________________________________________________")
        return True

    if "graphically represent" in data.casefold():
        if new.issummed==True:
            df=new.dataframe
            new_df=df
        else:
            respond("Do you want to sum up the data for a period of time ")
            boolean=listen()
            while(True):
                if 'yes' in boolean.casefold():
                    temp=abilities('numerical values')
                    df=new.dataframe
                    new_df=df
                    break
                elif 'no' in boolean.casefold():
                    df=new.dataframe
                    cols=list(df.columns)
                    lower_cols=[x.lower() for x in cols]
                    print(cols)
                    respond('set up your index or X-axis column')
                    index_col=listen()
                    while True:
                        if index_col.lower() in lower_cols:
                            break
                        respond("{} column is not present in the data".format(index_col))
                        index_col=listen()
                    respond('set up your Y-axis column')
                    y_col=listen()
                    while True:
                        if y_col.lower() in lower_cols:
                            break
                        respond("{} column is not present in the data".format(y_col))
                        y_col=listen()
                    for x in cols:
                        if (x.lower()==index_col.lower()):
                            index_col=x
                            continue
                        if(x.lower()==y_col.lower()):
                            y_col=x
                            continue
                    new_df= pd.DataFrame(zip(df[index_col],df[y_col]),columns=[index_col,y_col])
                    new_df=new_df.groupby(index_col)[y_col].sum().reset_index()
                    print(new_df.head())
                    new_df=new_df.set_index(index_col)
                    break
                else:
                    respond("Try saying YES or NO")
                    boolean=listen()
        respond("How do you want to plot ? line Graph , Dot Graph ,Bar Graph or Area Graph?")
        k=listen()
        while(True):
            if "bar" in k.lower():
                new_df.plot.bar()
                plt.show()
                break
            elif "area" in k.lower():
                new_df.plot.area()
                plt.show()
                break
            elif "line" in k.lower():
                plt.plot(new_df)
                plt.show()
                break
            elif "dot" in k.lower():
                plt.plot(new_df,'.')
                plt.show()
                break
            else:
                respond("Choose from the above list")
                k=listen()
        print("___________________________________________________________________________________________________")
        return True
    if "numerical values" in data.casefold():
        df=new.dataframe
        cols=list(df.columns)
        lower_cols=[x.lower() for x in cols]
        print(cols)
        respond("Specify the column that contains date time Index")
        Notfound=True
        while(Notfound):
            date_col=listen()
            if date_col.lower() in lower_cols:
                Notfound=False
        respond("Specify the column whose data to be summed up")
        Notfound=True
        while(Notfound):
            sum_col=listen()
            if sum_col.lower() in lower_cols:
                Notfound=False
        useless_cols=[]
        for x in cols:
            if (x.lower()==date_col.lower()):
                date_col=x
                continue
            if(x.lower()==sum_col.lower()):
                sum_col=x
                continue
            useless_cols.append(x)
        df.drop(useless_cols,axis=1,inplace=True)
        df=df.groupby(date_col)[sum_col].sum().reset_index()
        df=df.set_index(date_col)
        respond("Specify the period of time. Daily ,Monthly, Quarterly , yearly")
        period=listen()
        if period.lower()=='monthly':
            df=df[sum_col].resample('M').sum()
        elif period.lower()=='quarterly':
            df=df[sum_col].resample('Q').sum()
        elif period.lower()=='yearly':
            df=df[sum_col].resample('Y').sum()
        else:
            print('Remains Same')
        print(df.head())
        new.issummed=True
        new.dataframe=df
        print("___________________________________________________________________________________________________")
        return True
    if "restart" in data.casefold():
        new.dataframe=new.original
        new.issummed=False
        print("___________________________________________________________________________________________________")
        return True
    if "nothing" in data.casefold():
        return False
        
class excel():
    def __init__(self,df):
        self.dataframe=df
        self.original=df
        self.issummed=False
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'r'

df = pd.read_excel("Superstore .xls")

new=excel(df)

respond("Hey sukumar, How can I help you with the data analysis? I can do the following things.")
print()
listening=True
while listening==True:
    print("Show only specific columns")
    print("Show data that satisfy the required criteria")
    print("Graphically represent the data")
    print("Sum up the numerical values for a period of time")
    print("Draw a pie chart")
    choice=listen()
    listening=abilities(choice)
    if listening:
        print()
        respond("What else you want me to do with this new data?")
        print()
        print("To Use the Original data, Say restart")
        
respond("Have a nice day")
