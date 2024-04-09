
#import numpy as np
import os
#from numpy.core.multiarray import dtype
import re
import datetime
import sqlite3

occupation_map={0:  "other",
      1:  "academic/educator",
      2:  "artist",
      3:  "clerical/admin",
      4:  "college/grad student",
      5:  "customer service",
      6:  "doctor/health care",
      7:  "executive/managerial",
      8:  "farmer",
      9:  "homemaker",
     10:  "K-12 student",
     11:  "lawyer",
     12:  "programmer",
     13:  "retired",
     14:  "sales/marketing",
     15:  "scientist",
     16:  "self-employed",
     17:  "technician/engineer",
     18:  "tradesman/craftsman",
     19:  "unemployed",
     20:  "writer"}

age_map={1:  "Under 18",
     18:  "18-24",
     25:  "25-34",
     35:  "35-44",
     45:  "45-49",
     50:  "50-55",
     56:  "56+"}

def toString(bin_str):    
    reg_str=''
    for char in bin_str:
        reg_str+=chr(char)
    reg_str=reg_str.strip()
    return reg_str

def movieFormat(reg_str):
    dict={}
    li=reg_str.split('::')
    try:
        dict['movieId']=int(li[0])
    except ValueError as v:
        print(li[0])
        dict['movieId']=li[0]
    #Extracting year and title from column[1]
    year=re.findall(r'\(\d{4}\)', string=li[1])    
    dict['movieTile']=li[1][ : li[1].find(year[0])].strip()
    dict['year']=int(year[0][1:-1])
    
    #Extracting the genres
    genres=li[2].split('|')
    dict['movieGenre']=genres
    return dict
    
def movieToDB(dict, cursor):
    for genre in dict['movieGenre']:
        try:
            cursor.execute("INSERT INTO movie VALUES(:1, :2, :3, :4);",(dict['movieId'], dict['movieTile'], dict['year'], genre))
            print(dict['movieId'],' ',dict['movieTile'],' ',dict['year'],' ',genre)
        except sqlite3.IntegrityError as I:
            pass
    pass
def ratingsFormat(reg_str):
    dict={}
    li=reg_str.split('::')
    dict['userId']=int(li[0])
    dict['movieId']=int(li[1])
    dict['rating']=int(li[2])    
    dict['timestamp']=datetime.datetime.fromtimestamp(int(li[3])).strftime('%Y-%m-%d %H:%M:%S')    
    return dict

def ratingsToDB(dict, cursor):
    try:
        cursor.execute("INSERT INTO ratings VALUES(:1, :2, :3, :4);",(dict['userId'], dict['movieId'], dict['rating'], dict['timestamp']))
    except sqlite3.IntegrityError as I:
        pass
    pass
def usersFormat(reg_str):
    dict={}
    li=reg_str.split('::')
    dict['userId']=int(li[0])
    dict['gender']=li[1]
    dict['agerange']=age_map[int(li[2])]
    dict['occupation']=occupation_map[int(li[3])]
    try:
        dict['zipCode']=int(li[4])
    except ValueError as v:
        dict['zipCode']=int(li[4].strip('-')[0])    
    return dict
    
def userstoDB(dict, cursor):
    try:
        cursor.execute("INSERT INTO users VALUES(:1, :2, :3, :4, :5);",(dict['userId'], dict['gender'], dict['agerange'], dict['occupation'], dict['zipCode'],))
    except sqlite3.IntegrityError as I:
        pass
    pass
os.chdir(path='./ml-1m/')
file=open('ratings.dat','rb')

conn=sqlite3.connect(database='movieDB.db')
cursor=conn.cursor()

for i in iter(file):    
    #bin_str=file.readline()
    bin_str=i
    reg_str=toString(bin_str)    
    #dict=movieFormat(reg_str)    
    #movieToDB(dict, cursor)
    dict=ratingsFormat(reg_str)
    print(dict)
    ratingsToDB(dict, cursor)
    #dict=usersFormat(reg_str)
    #print(dict)
    #userstoDB(dict, cursor)
# cursor.execute('SELECT * FROM sqlite_master;')
# rows=cursor.fetchall()
# for row in rows:
#     print(row)
conn.commit()
conn.close()
