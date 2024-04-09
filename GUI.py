import os
import sqlite3 
from BasicModules import *
from tkinter import *
import random
import tkinter as tk 
from PIL import Image,ImageTk
import BasicModules

target_user = User(userId = -1)

class RateMovies(Frame):
    def __init__(self, master=None, movies=[]):
        Frame.__init__(self, master)         
        self.pack()
        self.grid()
        self.create_widgets()
        self.movies=movies
    def create_widgets(self):
        movieRating=[]
        for i in range(len(self.movies)):
            movieRating.append(IntVar())
            for j in range(1, 6):
                Radiobutton(self, text=str(j), var=movieRating[i], value=str(j)).grid(row=i, column=j)

                
class Application(Frame):
    def __init__(self,master):
        super(Application,self).__init__(master)
        self.configure(background="#CC0001")
        self.grid()
        
        self.movieRating=[]
        
        self.create_widgets()
        

    # Create main GUI window
    def create_widgets(self):

        self.search_var = StringVar()
        self.search_var.trace("w", lambda name, index, mode: self.update_list())
        Label(self, text="Movie Recommendtion System", background="#CC0001", font= ("Comic Sans MS",16)).grid(row=0, column=0, padx=200)        
        self.entry = Entry(self, textvariable=self.search_var, width=30, font= ("Comic Sans MS",9))
        self.lbox = Listbox(self, width=45, height=15, selectmode="multiple", font=("Comic Sans MS",9), background="Black", fg="white",selectbackground="#F9D12B",highlightcolor="#F9D12B")
         
        self.entry.grid(row=4, column=0, sticky=W, padx=90, pady=10)
        self.lbox.grid(row=5, column=0, columnspan=6,sticky=W, padx=25, pady=10)
        
        self.b1=Button(self, text='Done', command=self.submit, bg="#F9D12B", font=("Comic Sans MS",12))
        self.b1.grid(row=7, column=0, padx=155, pady=7, sticky=W)
        
        self.b2=Button(self, text='Add', command=self.click, bg="#F9D12B", font=("Comic Sans MS",12))
        self.b2.grid(row=7, column=0, sticky=W, padx=40, pady=7)
        #photo=PhotoImage(file='Like-2-icon.png')
        #self.b1.config(image=photo, height="20", width="20")
         
        # Function for updating the list/doing the search.
        # It needs to be called here to populate the listbox.
        self.update_list()

    def update_list(self):
        search_term = self.search_var.get()
     
        self.lbox.delete(0, END)
        global latest_sel
        latest_sel=[]
     
        for item in movies:
            if search_term.lower() in item.lower():
                self.lbox.insert(END, item)
                latest_sel.append(item)                
    def click(self):        
        for item in self.lbox.curselection():
            if latest_sel[item] not in user_movies:
                print(latest_sel[item],name_to_id[latest_sel[item]])
                user_movies.append(latest_sel[item])
                
                self.movieRating.append(IntVar())
                Label(self, text=latest_sel[item],bg="#CC0001", font=("Comic Sans MS",10)).grid(row=len(self.movieRating)+8, column=0, padx=100, sticky=W)
                for j in range(1, 6):
                    r1=Radiobutton(self, text=str(j), var=self.movieRating[-1], value=str(j),bg="#CC0001", font=("Comic Sans MS",10))
                    r1.grid(row=len(self.movieRating)+8, column=j, sticky=W)
                    r1.select()
        
        pass    
    
    def submit(self):
        global target_user        
        
        self.b3=Button(self, text='Submit', command=self.submitRating, bg="#F9D12B", font=("Comic Sans MS",12))
        self.b3.grid(row=7, column=0, padx=270, sticky=W)
        
        
    def submitRating(self):
        global target_user
        for i in range(len(self.movieRating)):
            target_user.addMovieRating(movieId=name_to_id[user_movies[i]], rating=self.movieRating[i].get())
        print(target_user)        
        #getMovieRecommendationByGenre(target_user)
        
        self.destroy()
        f=Recomm(root)
        
class Recomm(Frame):
    
    def __init__(self,master):
        super(Recomm,self).__init__(master)
        self.configure(background="#CC0001")
        self.grid()
        Label(self, text="Movie Recommendtions", background="#CC0001", font= ("Comic Sans MS",12)).grid(row=0, column=0)        
        
        self.lbox1 = Listbox(self, width=60, height=21, selectmode="multiple", font=("Comic Sans MS",9), background="Black", fg="white",selectbackground="#F9D12B",highlightcolor="#F9D12B")
        self.lbox1.grid(row=3, column=0, columnspan=6,sticky=W, padx=25, pady=10)

        Label(self, text="Filters:", background="#CC0001", font= ("Comic Sans MS",14)).grid(row=4, column=0)
        '''Label(self, text="Reasoning", background="#CC0001", font= ("Comic Sans MS",12)).grid(row=0, column=6)

        self.lbox1 = Listbox(self, width=45, height=20, selectmode="multiple", font=("Comic Sans MS",9), background="Black", fg="white",selectbackground="#F9D12B",highlightcolor="#F9D12B")
        self.lbox1.grid(row=3, column=6, columnspan=6,sticky=W, padx=25, pady=10)'''
        self.b4=Button(self, text='Genre',command=self.filterByGenre, bg="#F9D12B", font=("Comic Sans MS",12))
        self.b4.grid(row=4, column=1, sticky=W, padx=10, pady=7)
        
        self.b5=Button(self, text='Occupation',command=self.filterByOccupation, bg="#F9D12B", font=("Comic Sans MS",12))
        self.b5.grid(row=4, column=2, sticky=W, padx=10, pady=7)

        self.b7=Button(self, text='Age',command=self.filterByAge, bg="#F9D12B", font=("Comic Sans MS",12))
        self.b7.grid(row=5, column=1, sticky=W, padx=10, pady=7)
        
        self.b7=Button(self, text='Popularity',command=self.filterByRating, bg="#F9D12B", font=("Comic Sans MS",12))
        self.b7.grid(row=5, column=2, sticky=W, padx=10, pady=7)

        '''Label(self, text="Graphs:", background="#CC0001", font= ("Comic Sans MS",14)).grid(row=6, column=0)

        self.b8=Button(self, text='gram', command=self.Graph, bg="#F9D12B", font=("Comic Sans MS",12))
        self.b8.grid(row=6, column=1, sticky=W, padx=10, pady=7)

        self.b9=Button(self, text='Pie Chart', command=self.Graph, bg="#F9D12B", font=("Comic Sans MS",12))
        self.b9.grid(row=6, column=2, sticky=W, padx=10, pady=7)
        
        self.b10=Button(self, text='Scatter Graph', command=self.scattergraph, bg="#F9D12B", font=("Comic Sans MS",12))
        self.b10.grid(row=7, column=1, sticky=W, padx=10, pady=7)

        self.b7=Button(self, text='Bar Graph', command=self.barGraph, bg="#F9D12B", font=("Comic Sans MS",12))
        self.b7.grid(row=7, column=2, sticky=W, padx=10, pady=7)'''
        
        self.b12= tk.Button(self, text = 'Back to Home!', width = 25, command=self.back, bg="#F9D12B", font=("Comic Sans MS",12))        
        self.b12.grid(row=0, column=6, sticky=W, padx=50)
        
        self.finalMovies=None
        self.clicks=0
        self.populateListBox()

    def populateListBox(self):
        global target_user
                
        self.finalMovies=getRecon(target_user)
        
        self.lbox1.delete(0, END)

        for item in self.finalMovies['final'].keys():
            print(self.finalMovies['final'][item])
            #print(moviesClass[new_list[item]])
            self.lbox1.insert(END, self.finalMovies['final'][item])
        
    def filterByAge(self):
        self.lbox1.delete(0, END)
        for item in self.finalMovies['ageRange'].keys():            
            self.lbox1.insert(END, moviesClass[item])
    
    def filterByOccupation(self):
        self.lbox1.delete(0, END)
        for item in self.finalMovies['occupation'].keys():            
            self.lbox1.insert(END, moviesClass[item])
            
    def filterByRating(self):
        self.lbox1.delete(0, END)
        for item in self.finalMovies['final'].keys():            
            self.lbox1.insert(END, self.finalMovies['final'][item])
            
    def filterByGenre(self):
        self.lbox1.delete(0, END)
        key = list(self.finalMovies.keys())
        while key[self.clicks] == 'final' or key[self.clicks] == 'ageRange' or key[self.clicks] == 'occupation':
            self.clicks = (self.clicks+1)%len(self.finalMovies.keys())
        self.lbox1.insert(END, key[self.clicks]+' Genre')
        for item in self.finalMovies[key[self.clicks]].keys():            
            self.lbox1.insert(END, moviesClass[item])
        self.clicks = (self.clicks+1)%len(self.finalMovies.keys())
        
    def Filterclick(self):
        Label(self, text="Filter Applied", background="#CC0001", font= ("Comic Sans MS",12)).grid(row=0, column=6)        
        self.lbox1 = Listbox(self, width=45, height=20, selectmode="multiple", font=("Comic Sans MS",9), background="Black", fg="white",selectbackground="#F9D12B",highlightcolor="#F9D12B")
        self.lbox1.grid(row=3, column=6, columnspan=6,sticky=W, padx=25, pady=10)

    '''def barGraph(self):
        bar(yvalues=BasicModules.glob_yvalues, labels=BasicModules.glob_labels, legend=BasicModules.glob_columns)
        pass
    def scattergraph(self):
        Graphs.collectScatter()
    def Graph(self):
        global target_user
        pieChart(target_user, self.finalMovies['final'])'''
    
    def back(self):            
        self.destroy()
        f=Application(root)
        
        
        
       
#os.chdir(path='./ml-1m/')
conn=sqlite3.connect(database='movieDB.db')
cursor=conn.cursor()

cursor.execute('SELECT * FROM movie;')
    
movies=[]
selected=[]
latest_sel=[]
user_movies=[]
name_to_id={}
for item in cursor.fetchall():    
    if item[1] not in movies:
        movies.append(item[1])
        name_to_id[item[1]] = item[0] 

movies.sort() 
'''
root = Tk()
root.title("Movie Recommendation System")
root.geometry("500*700")

app = Application(master=root)
app.mainloop()
'''

root=Tk()
root.geometry("1240x700")
root.title("movie")
root.configure(background="#CC0001")
load = Image.open('movie.jpg')
render = ImageTk.PhotoImage(load)
img = tk.Label(root, image = render)
img.image = render
img.place(x=0,y=0,relwidth=1,relheight=1)


f=Application(root)
f.mainloop()


