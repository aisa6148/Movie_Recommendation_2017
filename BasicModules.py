'''
Created on 07-Apr-2017

@author: Karthik_pc
'''
import sqlite3
import os
import math
'''import numpy as np
import matplotlib as plt
import Graphs'''
import random
#from Graphs import histogram, scatter, pie, bar, collectPies


class User():
    def __init__(self, userId):
        self.userId=userId        
        self.movies={}
        pass
    def __str__(self):
        moviesWatched=''
        for movie in self.movies:
            moviesWatched+=str(moviesClass[movie])+"\tRating: "+str(self.movies[movie])+"\n"
        return "User ID: "+str(self.userId)+" has watched\n"+moviesWatched
    def addMovieRating(self, movieId, rating):
        self.movies[movieId]=rating
        pass
    def getMoviesByGenre(self, genre):
        moviegenre={}
        for movie in self.movies.keys():
            if genre != '' and genre in moviesClass[movie].genres:
                moviegenre[movie]=self.movies[movie]
            elif genre == '':
                moviegenre[movie]=self.movies[movie]                
        return moviegenre    

class Movie():
    def __init__(self, movieId, name, genre, year):
        self.movieId=movieId
        self.name=name
        self.genres=[genre]
        self.year=year
        self.ratingNo=0
    def addInfo(self, genre):        
        self.genres.append(genre)
    def __str__(self):
        return self.name+' ('+str(self.year)+')'+' '+str(self.genres)   

def findUncommonMovies(movieList, uncommon=False, threshold=200):
    newMovieList=[]
    if not uncommon:
        return movieList
    for movie in movieList:
        if uncommon and moviesClass[movie].ratingNo < threshold and moviesClass[movie].ratingNo > 20:
            newMovieList.append(movie)
            print(moviesClass[movie],'-',moviesClass[movie].ratingNo)
    return newMovieList
def filterMovies(uncommon=False, threshold=200, genre='', invert=False):
    movieList=[]
    if genre != '' and not invert:
        for movie in moviesClass.keys():
            if genre in moviesClass[movie].genres:
                movieList.append(movie)
    else:       #invert is true
        for movie in moviesClass.keys():
            if genre not in moviesClass[movie].genres:
                movieList.append(movie)
    movieList = findUncommonMovies(movieList, uncommon=uncommon, threshold=threshold)
    return movieList    

def filterUser(movieList=[]):    
    for user in users.keys():
        tbd=[]
        for movie in users[user].movies.keys():
            if movie not in movieList:
                tbd.append(movie)
        for movie in tbd:
            del users[user].movies[movie]
        
def unionOfMovies(movieLists):
    new_list=set()    
    for movieList in movieLists:
        new_list = new_list.union(set(movieList))
    '''
    for item in new_list:
        print(moviesClass[item])
    ''' 
    return list(new_list)

def compareTwoUsers(a, b):
    common={}
    for movieId in a.movies.keys():
        if movieId in b.movies.keys():
            common[movieId]=(a.movies[movieId], b.movies[movieId])
    return common    

def compareTwoUserByGenre(a, b, genre=''):
    common={}
    movieGenre=a.getMoviesByGenre(genre)
    for movieId in movieGenre:
        if movieId in b.movies.keys():
            common[movieId]=(a.movies[movieId], b.movies[movieId])
    return common
    pass
def euclidean(common):
    sum=0
    for item in common.keys():
        #print(item)
        #print(common[item])
        sum+= pow((common[item][0] - common[item][1]), 2)
    return 1/(1+sum)*len(common)*len(common)

def pearson(common):
    n=len(common)
    sumA=0
    sumB=0
    sumsqA=0
    sumsqB=0
    pSum=0
    for item in common.keys():
        sumA+=common[item][0]
        
        sumB+=common[item][1]
        sumsqA+=pow(common[item][0], 2)
        sumsqB+=pow(common[item][1], 2)
        pSum+=common[item][0]*common[item][1]
        
    #print('SumA: ',sumA,' SumB: ',sumB)
    #print('SumSQA: ',sumsqA,' SumSQB: ',sumsqB)
    #print('pSum: ',pSum)
    num=pSum-(sumA*sumB/n)
    den=math.sqrt((sumsqA-pow(sumA,2)/n)*(sumsqB-pow(sumB,2)/n))
    if den==0: return 0
    r=num/den
    return r
    
def compareAllUsers(func, genre='', target_user=None):
    scores=[]
    for i in users.keys():    
        if users[i].userId != target_user.userId:
            #common=compareTwoUsers(target_user, users[i])
            common=compareTwoUserByGenre(target_user, users[i], genre)
            if len(common) > 0:
                scores.append((i, func(common), len(common)))
            else:
                scores.append((i, 0.00001, 0))
    return scores

def highestValue(scores):
    highest=scores[0][0]
    for i in range(len(scores)):
        if scores[i][1] > scores[highest][1]:
            highest=i
    print(scores[highest])

def top50(scores, n):
    epsilon=10e-6
    if len(scores) < n:
        n=len(scores)
    for i in range(n):
        index=i
        for j in range(i+1, len(scores)):
            if scores[j][1] > scores[index][1] or (scores[j][1] == scores[index][1] and scores[j][2] > scores[index][2]) :
                index=j
        temp=scores[index][:]
        scores[index]=scores[i][:]
        scores[i]=temp
    
    for i in range(n):
        #print(scores[i],compareTwoUsers(users[1], users[scores[i][0]]))
        pass
    
        
def filterUncommonMovies(movies, movieList, n=10):
    newList=[]
    for i in range(len(movieList)):
        if movies[movieList[i]][1] > 0.3*n:
            newList.append(movieList[i])
    return newList
def filterUncommonMoviesByGenre(movies, movieList, genre='', n=10):
    newList=[]
    
    for i in range(len(movieList)):
        if movies[movieList[i]][1] > 0.3*n and genre != '' and genre in moviesClass[movieList[i]].genres:
            newList.append(movieList[i])
        elif movies[movieList[i]][1] > 0.3*n and genre == '':
            newList.append(movieList[i])
    
    return newList
    pass
def getRecommendation(metric_score, n, m, user, genre=''):
    critics=[]
    scores={}
    movies={}
    count=0
    for item in metric_score:
        critics.append(item[0])
        scores[item[0]]=item[1]
        #scores.append(item[1])
        count+=1
        if count == n:
            break
    
    for critic in critics:                
        for movie in users[critic].getMoviesByGenre(genre):
        #for movie in users[critic].movies.keys():            
            if movie not in user.movies.keys():
                if movie not in movies.keys():
                    movies[movie]=[users[critic].movies[movie]*scores[critic], 1, scores[critic]]
                else:
                    movies[movie][0]+=users[critic].movies[movie]*scores[critic]
                    movies[movie][1]+=1
                    movies[movie][2]+=scores[critic]
                    pass
                #print(movie, end='\t')
    
    for movie in movies.keys():
        movies[movie].append(movies[movie][0]/movies[movie][2])
        #print(moviesClass[movie],movies[movie])
        count+=1
        
    movieList=list(movies.keys())
    #movieList=filterUncommonMovies(movies, movieList, n)
    #Scatter plot code starts here
    xvalues=[]
    yvalues=[]
    
    for i in range(len(movieList)):        
        xvalues.append(movies[movieList[i]][1])
        yvalues.append(movies[movieList[i]][3])
        
    
    #Scatter plot code ends here
    
    movieList=filterUncommonMoviesByGenre(movies, movieList, genre, n)
    
    if len(movieList) < m:
        m = len(movieList) 
    else:
        pass
    for i in range(m):
        index=i
        for j in range(i+1, len(movieList)):
            if movies[movieList[j]][3] > movies[movieList[index]][3]:
            #if movieList[j][3] > movieList[index][3]:
                index=j
        temp=movieList[index]
        movieList[index]=movieList[i]
        movieList[i]=temp 
    '''
    for i in range(m):
        print(movieList[i],movies[movieList[i]], moviesClass[movieList[i]])
    '''
    new_xvalues=[]
    new_yvalues=[]
    for i in range(m):
        new_xvalues.append(movies[movieList[i]][1])
        new_yvalues.append(movies[movieList[i]][3])
    new_xvalues.extend(xvalues)
    new_yvalues.extend(yvalues)
    #scatter(xvalues=new_xvalues, yvalues=new_yvalues, n=m)
    scatter_list.append((new_xvalues, new_yvalues, m))
    new_movies={}
    for i in range(m):
        new_movies[movieList[i]]=movies[movieList[i]]
    #return movies
    return new_movies

def aggregateUsers():
    movieList={}
    # Each movieID returns a List
    #['Total rating of people who have watched the movie' 'Number of people who have watched movie', 'Average rating']
    for user in users.keys():
        for movie in users[user].movies.keys():
            if movie not in movieList.keys():
                movieList[movie] = [users[user].movies[movie], 1]
            else:
                movieList[movie][0]+=users[user].movies[movie]
                movieList[movie][1]+=1
    
    for movie in movieList.keys():
        movieList[movie].append(movieList[movie][0]/movieList[movie][1])            #Average metric
    return movieList

def compareWithAggregateUsers(a, movieList, id):
    new_user=User(userId=id)
        
    for movie in movieList.keys():
        new_user.addMovieRating(movieId=movie, rating=movieList[movie][0]/movieList[movie][1])
    
    common = compareTwoUsers(a, new_user)
    return euclidean(common)
    
def setupMovies():
    if 'ml-1m' not in os.getcwd():
        os.chdir(path='./ml-1m/')
    conn=sqlite3.connect(database='movieDB.db')
    cursor=conn.cursor()    
    
    cursor.execute('SELECT * FROM movie;')
    for item in cursor.fetchall():        
        if item[0] not in moviesClass.keys():
            moviesClass[item[0]]=Movie(movieId=item[0], name=item[1], year=item[2], genre=item[3])
        else:    
            moviesClass[item[0]].addInfo(genre=item[3])
    
    cursor.execute('SELECT * FROM ratings;')
    for item in cursor.fetchall():        
        moviesClass[item[1]].ratingNo+=1
            
    conn.close()
    
def setup(ageRange='', occupation=''):    
    global users
    users={}
    conn=sqlite3.connect(database='movieDB.db')
    cursor=conn.cursor()
    query="SELECT ratings.userID, ratings.movieID, ratings.rating FROM ratings, users WHERE ratings.userID = users.userId AND users.ageRange LIKE '%"+ageRange+"%' AND users.occupation LIKE '%"+occupation+"%';"
    #print(query)
    cursor.execute(query)    
    for item in cursor.fetchall():
        #print(str(count+1)+str(item))
        if item[0] not in users.keys():
            users[item[0]]=User(userId=item[0])
        users[item[0]].addMovieRating(movieId=item[1], rating=item[2])
        moviesClass[item[1]].ratingNo+=1
            
    conn.close()    

users={}
moviesClass={}
listOfRecommendations={}

occupations=["K-12 student", "self-employed", "scientist", "executive/managerial", "writer", "homemaker", "academic/educator", "programmer", "technician/engineer", "other", "clerical/admin", "sales/marketing", "college/grad student", "lawyer", "farmer", "unemployed", "artist", "tradesman/craftsman", "customer service", "retired", "doctor/health care"]
ageRanges=["Under 18", "56+", "25-34", "45-49", "50-55", "35-44", "18-24"]
setupMovies()
setup(occupation='homemaker', ageRange='25-34')

#target_user=User(userId=-1)
'''
target_user.addMovieRating(movieId=1, rating=5)
target_user.addMovieRating(movieId=3114, rating=4)
target_user.addMovieRating(movieId=2720, rating=4)
target_user.addMovieRating(movieId=8, rating=4)
target_user.addMovieRating(movieId=552, rating=3)
'''
'''
target_user.addMovieRating(movieId=2038, rating=3)
target_user.addMovieRating(movieId=904, rating=5)
target_user.addMovieRating(movieId=2524, rating=3)
target_user.addMovieRating(movieId=1010, rating=4)
target_user.addMovieRating(movieId=1387, rating=4)
target_user.addMovieRating(movieId=260, rating=3)
target_user.addMovieRating(movieId=2013, rating=2)
target_user.addMovieRating(movieId=480, rating=2)
target_user.addMovieRating(movieId=1097, rating=5)
'''
'''
#other_user=users[6]

#common=compareTwoUsers(target_user, other_user)
common=compareTwoUserByGenre(target_user, other_user, genre='Comedy')
for item in common.keys():
    print(moviesClass[item])
print(common)
#print(common)
'''
#pearson_score=compareAllUsers(func=pearson)

def getGenreWeight(user):
    genres={}
    genresRating={}
    totalMovies=len(user.movies.keys())    
    for movie in user.movies.keys():
        for genre in moviesClass[movie].genres:
            genres[genre] = genres.get(genre, 0)+1
            genresRating[genre] = genresRating.get(genre, 0) + user.movies[movie]           #For genre average rating
    sum=0
    
    for item in genres.keys():
        genresRating[item] = genresRating[item]/genres[item]                                #genres[item] gives no of movies in that genre
        genres[item]=genres[item]/totalMovies
        sum+=genres[item]
        
    avgGenreRating=0
    for item in genres.keys():
        avgGenreRating+=genresRating[item]
    avgGenreRating=avgGenreRating/len(genres.keys())
    print(avgGenreRating)
    for item in genres.keys():
        genresRating[item]=genresRating[item]/avgGenreRating
    
    for item in genres.keys():
        genres[item]=int((genres[item]/sum *genresRating[item] *10000))/10000  
    print(genresRating)
    return genres
    
def getMovieRecommendationByGenre(target_user):
    genres=getGenreWeight(target_user)
    print(genres)
    for genre in genres.keys():        
        euclidean_score=compareAllUsers(func=euclidean, genre=genre, target_user=target_user)
        n=20
        top50(euclidean_score, n=n)
        print('For genre: ',genre)
        listOfRecommendations[genre] = getRecommendation(euclidean_score, n=n, m=20, user=target_user, genre=genre)
    

def predictUserByOccupation(target_user):
    rating={}    
    for occupation in occupations:        
        setup(occupation=occupation, ageRange='')
        movieList=aggregateUsers()
        print('For '+occupation+' users: ',end='\t')
        rating[occupation] = compareWithAggregateUsers(a=target_user, movieList=movieList, id=-5)
        print(rating[occupation])
    
    highest='scientist'
    for key in rating.keys():
        if rating[highest] < rating[key]:
            highest = key
            
    setup(occupation=highest)
    movieList=aggregateUsers()
    euclidean_score=compareAllUsers(func=euclidean, target_user=target_user)
    n=30
    top50(euclidean_score, n=n)
    print(euclidean_score[:][1])
    
    #histogram(xvalues=range(len(euclidean_score))[:10], yvalues=[score[1] for score in euclidean_score][:10], labels=[score[0] for score in euclidean_score][:10], xlimit=10, ylimit=15)
    print('The mostly likely category that the user falls under is: ',highest)
    
    listOfRecommendations['occupation']=getRecommendation(euclidean_score, n=n, m=10, user=target_user)
    #print(listOfRecommendations['occupation'][912])
    #scatter(xvalues=[listOfRecommendations['occupation'][key][1] for key in listOfRecommendations['occupation'].keys()], yvalues=[listOfRecommendations['occupation'][key][3] for key in  listOfRecommendations['occupation'].keys()], n=5)
            

def predictUserByAgeRange(target_user):      
    rating={}
    for ageRange in ageRanges:
        setup(ageRange=ageRange, occupation='')
        count=0         
        movieList=aggregateUsers()
        print('For users of age '+ageRange+': ',end='\t')
        rating[ageRange] = compareWithAggregateUsers(a=target_user, movieList=movieList, id=-5)
        print(rating[ageRange])
        
    highest='18-24'
    for key in rating.keys():
        if rating[highest] < rating[key]:
            highest = key
            
    setup(ageRange=highest)
    movieList=aggregateUsers()
    euclidean_score=compareAllUsers(func=euclidean, target_user=target_user)
    n=30
    top50(euclidean_score, n=n)
    print('The mostly likely category that the user falls under is: ',highest)
    
    listOfRecommendations['ageRange']=getRecommendation(euclidean_score, n=n, m=10, user=target_user)    
    
def summarizeMovies(listOfRecommendations, target_user):
    movieLists=[]
    weights={}
    weights['ageRange'] = 0.2
    weights['occupation'] = 0.2
    leftOverWeight = 0.6 
    genreWeights = getGenreWeight(target_user) 
    for item in genreWeights.keys():
        weights[item] = int(genreWeights[item]*leftOverWeight*10000)/10000
        
    for category in listOfRecommendations.keys():       #Category is 'Genre' , 'Age Range' ...
        movieLists.append(list(listOfRecommendations[category].keys()))
        print(listOfRecommendations[category].keys())
    finalList=unionOfMovies(movieLists)
    finalRating=[]
    noOfOccurrences=[]
    table={}
    columns=[]
    print('Index'+'\t',end='\t')
    for category in listOfRecommendations.keys():
        columns.append(category)
        try:
            print(category,str(weights[category]),end='\t')
        except KeyError as e:
            #weights[category]=0.2
            pass
        
    #print(weights.keys())
        
    print('Total')
    for i in range(len(finalList)):
        total=0
        print(str(finalList[i])+'\t', end='\t')
        table[finalList[i]] = []
        noOfOccurrences.append(0)
        for category in listOfRecommendations.keys():
            if finalList[i] in listOfRecommendations[category].keys():
                total+=int(listOfRecommendations[category][finalList[i]][3]*10000)/10000 * weights[category]
                print(str(int(listOfRecommendations[category][finalList[i]][3]*10000)/10000)+'\t\t',end='\t')
                table[finalList[i]].append(int(listOfRecommendations[category][finalList[i]][3]*10000)/10000)
                noOfOccurrences[i]+=1
            else:
                print('0\t\t',end='\t')
                table[finalList[i]].append(0)
            pass
        finalRating.append(total)
        print(str(finalRating[-1])+'\t\t'+str(noOfOccurrences[i]))
        
    #bar(yvalues=table[:20],labels=finalList[:20])
    for i in range(len(finalList)):    
        highest=i
        for j in range(i+1, len(finalList)):
            if finalRating[j] > finalRating[highest]:
                highest=j
        finalRating[i], finalRating[highest] = finalRating[highest], finalRating[i]
        finalList[i], finalList[highest] = finalList[highest], finalList[i] 
        noOfOccurrences[i], noOfOccurrences[highest] = noOfOccurrences[highest], noOfOccurrences[i]
    
    barChart(table, finalList, columns)                      #Sets up the bar chart
    file=open('log.txt','a')
    for i in range(20):
    #for i in range(len(finalList)):
        print(finalList[i],noOfOccurrences[i],finalRating[i], moviesClass[finalList[i]])
        file.write(str(finalList[i])+'\t'+str(noOfOccurrences[i])+'\t'+str(finalRating[i])+'\t')
        file.write(str(moviesClass[finalList[i]])+'\n')
    file.write('\n\n')
    file.close()
    listOfRecommendations['final']={}
    for i in range(20):
        listOfRecommendations['final'][finalList[i]] = moviesClass[finalList[i]]           
        
    #return listOfRecommendations['final']
    return listOfRecommendations
def getRecon(target_user):
    print(target_user)
    predictUserByOccupation(target_user=target_user)
    predictUserByAgeRange(target_user=target_user)
    setup()
    getMovieRecommendationByGenre(target_user)
    return summarizeMovies(listOfRecommendations, target_user)

def pieChart(target_user, finalMovies):
    genres={}    
    for movie in target_user.movies.keys():
        for genre in moviesClass[movie].genres:
            genres[genre] = genres.get(genre, 0)+1
    
    new_genres={}
    
    for movie in finalMovies.keys():
        for genre in moviesClass[movie].genres:
            new_genres[genre] = new_genres.get(genre, 0)+1
    
    collectPies(values=[list(genres.values()),list(new_genres.values())], labels=[list(genres.keys()),list(new_genres.keys())], titles=['Original', 'Recommended'])

glob_yvalues=None
glob_labels=None
glob_columns=None
scatter_list=[]

def barChart(table, finalList, columns):
    global glob_yvalues, glob_labels, glob_columns
    
    yvalues=[]
    labels=[]
    #bar(yvalues=table[:20],labels=finalList[:20])
    for i in range(20):
        yvalues.append(table[finalList[i]])
        labels.append(finalList[i])
        #print(finalList[i], table[finalList[i]])
    glob_yvalues=yvalues[:]
    glob_labels=labels[:]
    glob_columns=columns[:]
    #bar(yvalues=yvalues, labels=labels, legend=columns)
                    
#print(target_user)
#getGenreWeight(target_user)
#finalMovies = getRecon(target_user)
#pieChart(target_user)
#predictUserByOccupation(target_user)
