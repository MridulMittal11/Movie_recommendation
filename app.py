from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os
import pickle
import numpy as np
import pandas as pd

app=Flask(__name__)
app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host='localhost', database='movie_recommendation', user='root', password='123456')
cursor=conn.cursor()




@app.route('/')
def login():
    return render_template('login.html')




@app.route('/register')
def register():
    return render_template('register.html')




@app.route('/home')
def home():
    if 'userid' in session:
        return render_template('home.html')
        #  return render_template('index.html',
        #                    movie_names= list(popular_movies['title'].values),
        #                    director=list(popular_movies['author'].values),
        #                    votes=list(popular_movies['num_ratings'].values),
        #                    ratings=list(popular_movies['avg_ratings'].values),
        #                    images=list(popular_movies['image'].values))
    else: 
        return redirect('/')



@app.route('/login_validation', methods=['POST'])
def login_validation():
    userid=request.form.get('userid')
    password=request.form.get('password')
    
    cursor.execute("select * from users where userid='{}' and password='{}';".format(userid, password))
    users=cursor.fetchall()
    if len(users)==1:
        session['userid']=users[0][0]
        return redirect('/home')
    else:
        return redirect('/')
    


    
@app.route('/add_user', methods=['POST'])
def add_user():
    userid=request.form.get('new_userid')
    password=request.form.get('new_password')
    cursor.execute("select * from users where userid='{}';".format(userid))
    validate_user=cursor.fetchall()
    if len(validate_user)>0:
        return redirect('/')
    else:
        cursor.execute("insert into users values('{}', '{}');".format(userid, password))
        conn.commit()

        cursor.execute("select * from users where userid='{}' and password='{}';".format(userid, password))
        new_user=cursor.fetchall()
        session['userid']=new_user[0][0]
        return redirect('/home')




@app.route('/logout')
def logout():
    session.pop('userid')
    return redirect('/')



@app.route('/about_us')
def about_us():
    return render_template('about_us.html')



@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')




# @app.route('/recommend_movies', methods=["post"])
# def recommend():
#     # user_input= request.form.get("user_input")
#     # movie_index = np.where(movie_pivot.index == user_input)[0][0]
#     # suggested_items = sorted(list(enumerate(similarity_score[movie_index])), key=lambda x: x[1], reverse=True)[1:5]
#     # movie_list = list(movies["title"].values)

#     # data = []
#     # for i in suggested_items:
#     #     item = []
#     #     temp = movies[movies["title"] == movies_pivot.index[i[0]]]
#     #     item.extend(temp.drop_duplicates("title")['title'].values)
#     #     item.extend(temp.drop_duplicates("title")['author'].values)
#     #     item.extend(temp.drop_duplicates("title")['image'].values)

#     #     data.append(item)
#     return render_template('recommend.html', data=data)




if __name__=="__main__":
    app.run(debug=True, port=8001)