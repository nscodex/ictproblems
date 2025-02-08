from flask import Flask,render_template,request,redirect,session,url_for
import mysql.connector


app=Flask(__name__)
app.secret_key='nihal'
connection=mysql.connector.connect(host="localhost",user="root",password="root",database='recipehub',use_pure=True)
mycursor=connection.cursor()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        return render_template('register.html')
@app.route('/button1',methods=['GET','POST'])
def button1():
     if request.method=='POST':
        query="select recipe_name from recipes where category='breakfast'"
        mycursor.execute(query)
        breakfast=list(mycursor.fetchall())
        return render_template('index.html',sqldata=breakfast)
@app.route('/button2',methods=['GET','POST'])
def button2():
     if request.method=='POST':
        query="select recipe_name from recipes where category='lunch'"
        mycursor.execute(query)
        lunch=list(mycursor.fetchall())
        return render_template('index.html',sqldata=lunch)
@app.route('/button3',methods=['GET','POST'])
def button3():
     if request.method=='POST':
        query="select recipe_name from recipes where category='dinner'"
        mycursor.execute(query)
        dinner=list(mycursor.fetchall())
        return render_template('index.html',sqldata=dinner)
@app.route('/button4',methods=['GET','POST'])
def button4():
     if request.method=='POST':
        query="select recipe_name from recipes where category='desserts'"
        mycursor.execute(query)
        desserts=list(mycursor.fetchall())
        return render_template('index.html',sqldata=desserts)

@app.route('/read',methods=['GET','POST'])
def readvalue():
    if request.method=='POST':
        getname=request.form.get("name")
        getpwd=request.form.get("pwd")
        getemail=request.form.get("email")
        query="select username from users where username=%s"
        data=(getname,)
        query1="select email from users where email=%s"
        data1=(getemail,)
        mycursor.execute(query,data)
        dup_user=mycursor.fetchone()
        mycursor.execute(query1,data1)
        dup_email=mycursor.fetchone()
        if dup_user:
            return render_template('register.html',msg="try another username")
        elif dup_email:
            return render_template('register.html',msg="email already registered")
        else:
            query="INSERT INTO users(username,password,email) VALUES(%s,%s,%s)"
            data=(getname,getpwd,getemail)
            mycursor.execute(query,data)
            connection.commit()
            return render_template('index.html')

@app.route('/readrecipe',methods=['GET','POST'])
def readrecipe():
    if request.method=='POST':
        getuser=session['user_id']
        getname=request.form.get("name")
        gettime=int(request.form.get("time"))
        getsize=int(request.form.get("size"))
        getingr=request.form.get("ingredients")
        getinst=request.form.get("instructions")
        getcat=request.form.get("category")
        query="INSERT INTO recipes(user_id,recipe_name,ingredients,instructions,cooking_time,serving_size,category) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        data=(getuser,getname,getingr,getinst,gettime,getsize,getcat)
        mycursor.execute(query,data)
        connection.commit()
        return render_template('recipes.html')
@app.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('logged in',None)
    session.pop('user_id',None)
    session.pop('name',None)
    return render_template('index.html')


@app.route('/searchresult',methods=['GET','POST'])
def searchres():
    if request.method=='POST':
        getrn=request.form.get("recipe name")
        query= "SELECT * FROM recipes where recipe_name like %s or ingredients like %s"
        mycursor.execute(query,('%'+getrn+'%','%'+getrn+'%'))
        data=mycursor.fetchall()
        if len(data)!=0:
            return render_template('searchresult.html',sqldata=data)
        else:
            return render_template('index.html',msg="no records found")  
@app.route('/userlogin', methods=['POST'])
def userlogin():
    return render_template('searchresult.html')
@app.route('/home', methods=['POST'])
def new():
    return render_template('index.html')

@app.route('/searchingredients', methods=['POST'])
def searchingredients():
    ingredients_input = request.form['ingredients']
    ingredient_list = [ingredient.strip() for ingredient in ingredients_input.split(',')]
    query = "SELECT * FROM recipes WHERE "
    conditions = []
    for ingredient in ingredient_list:
        conditions.append(f"ingredients LIKE '%{ingredient}%'")
    query += " AND ".join(conditions)
    mycursor.execute(query)
    results =mycursor.fetchall()
    if len(results)!=0:
        return render_template('searchresult.html', sqldata=results)
    else:
        return render_template('index.html',msg="no records")     
@app.route('/sample',methods=['GET','POST'])
def login():
    username=request.form["textbox3"]
    pwd=request.form["textbox4"]
    query="select username,password,user_id from users where username=%s"
    data=(username,)
    mycursor.execute(query,data)
    user=mycursor.fetchone()
    if user:
        if pwd==user[1]:
            session['logged in']=True
            session['user_id']=user[2]
            session['name']=user[0]
            return render_template('recipes.html')
        else:
            return render_template('searchresult.html',msg="wrong password")
    else:
            return render_template('searchresult.html',msg="INVALID username")
        
    

if __name__=='__main__':
    app.run()