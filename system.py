from itertools import count
from flask import *
from werkzeug.utils import secure_filename
import os
#import magic
import urllib.request
from datetime import datetime
import pymysql



app = Flask(__name__)

app.secret_key = 'themostsecretivekeyeverinthemultiversecreatedbyjemuki'
#app.secret_key = "caircocoders-ednalan"


UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'jfif', 'mp4', 'mp3' ])


def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from clip1   "
    cursor = connection.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    
    return render_template('index.html', data = row)



@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']
        
        if len(password1) < 8 :
            return render_template('signup.html', message = "Password must be atleast 8 characters")
        elif password1 != password2 :
            return render_template('signup.html', message = "Your password did not match")
        else:
            connection = pymysql.connect(host ='localhost', user ='root', password ='', database ='jemuki.com')
            cursor = connection.cursor()
            try:
                cursor.execute('insert into signup(username,email,password)values(%s,%s,%s)', (username, email, password2))
                connection.commit()
                return redirect('/login')
            except:
                return render_template('signup.html', message = "Please try another email")
    else:
        return render_template('signup.html')
            


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        connection = pymysql.connect(host='localhost', user='root', password='', database='jemuki.com')
        
        cursor = connection.cursor()
        cursor.execute('select * from signup where email = %s and password =%s', (email, password))
        
        
        if cursor.rowcount == 0 :
            return render_template('login.html', message = "Wrong details, please try again.")
        elif cursor.rowcount == 1 :
            row = cursor.fetchone()
            username = row[0]
            bio = row[3]
            dp = row[4]
            followers = row[5]
            following = row[6]
            likes = row[7]
            session['key'] = email
            session['key1'] = username
            session['key2'] = bio
            session['key3'] = dp
            session['key5'] = followers
            session['key6'] = following
            session['key7'] = likes
            
            
            
            
            
            
            
            return redirect('/home')
        else:
            return render_template('login.html', message = "Something went wrong, please try again")
    else:
        return render_template('login.html')
        

@app.route('/signout')
def signout():
    session.pop('key', None)
    return redirect('/')   # take user to home route after logout



@app.route('/home')
def homepage():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from memeclip   "
    cursor = connection.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    
    sql = "select * from icons   "
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    
    
    
    return render_template('home.html', data = row, data2 = rows)


    



@app.route('/j')
def j():
    return render_template('j.html')


@app.route('/profile')
def profile():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from signup  where email = %s  "
    cursor = connection.cursor()
    cursor.execute(sql, (session['key']))
    
    if cursor.rowcount == 0 :
        return render_template('profile.html', message = "No user uploaded yet")
    else:
        row = cursor.fetchone()
        return render_template('profile.html', data = row)

@app.route('/myfollowers')
def myfollowers():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from following   where following = %s  "
    cursor = connection.cursor()
    cursor.execute(sql, (session['key']))
    
    if cursor.rowcount == 0 :
        return render_template('funnyfollowers.html', message = "No  followers yet")
    else:
        rows = cursor.fetchall()
        return render_template('funnyfollowers.html', data = rows )



@app.route('/addchallenge')
def challengeuploads():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from challenge   where email = %s  "
    cursor = connection.cursor()
    cursor.execute(sql, (session['key']))
    
    if cursor.rowcount == 0 :
        return render_template('addchallenge.html', message = "No  uploads yet")
    else:
        rows = cursor.fetchall()
        return render_template('addchallenge.html', data = rows )




@app.route('/addfunny')
def funnyuploads():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from funny  where email = %s order by funny_id DESC "
    cursor = connection.cursor()
    cursor.execute(sql, (session['key']))
    
    if cursor.rowcount == 0 :
        return render_template('addfunny.html', message = "No  uploads yet")
    else:
        rows = cursor.fetchall()
        return render_template('addfunny.html', data = rows )




@app.route('/addrespect')
def respectuploads():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from respect  where email = %s order by respect_id DESC "
    cursor = connection.cursor()
    cursor.execute(sql, (session['key']))
    
    if cursor.rowcount == 0 :
        return render_template('addrespect.html', message = "No  uploads yet")
    else:
        rows = cursor.fetchall()
        return render_template('addrespect.html', data = rows )












@app.route('/addmemes')
def memesuploads():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from memes  where email = %s order by meme_id DESC "
    cursor = connection.cursor()
    cursor.execute(sql, (session['key']))
    
    if cursor.rowcount == 0 :
        return render_template('addmemes.html', message = "No  uploads yet")
    else:
        rows = cursor.fetchall()
        return render_template('addmemes.html', data = rows )



@app.route('/addher')
def heruploads():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from her  where email = %s order by her_id DESC "
    cursor = connection.cursor()
    cursor.execute(sql, (session['key']))
    
    if cursor.rowcount == 0 :
        return render_template('addher.html', message = "No  uploads yet")
    else:
        rows = cursor.fetchall()
        return render_template('addher.html', data = rows )





@app.route('/addmusic')
def musicuploads():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from music  where email = %s order by music_id DESC "
    cursor = connection.cursor()
    cursor.execute(sql, (session['key']))
    
    if cursor.rowcount == 0 :
        return render_template('addmusic.html', message = "No  uploads yet")
    else:
        rows = cursor.fetchall()
        return render_template('addmusic.html', data = rows )




@app.route('/addcars')
def caruploads():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from cars  where email = %s order by car_id DESC "
    cursor = connection.cursor()
    cursor.execute(sql, (session['key']))
    
    if cursor.rowcount == 0 :
        return render_template('addcars.html', message = "No  uploads yet")
    else:
        rows = cursor.fetchall()
        return render_template('addcars.html', data = rows )





    
@app.route('/editname', methods = ['POST', 'GET'])
def editname():
    if request.method == 'POST':
        username = request.form['username']
        
        connection = pymysql.connect(host='localhost', user='root', password='', database='jemuki.com')
        sql = 'UPDATE signup SET  username=%s WHERE email=%s '
        cursor = connection.cursor()
        cursor.execute(sql, (username, session['key'] ))
        connection.commit()
        
        sql = 'UPDATE posts SET  username=%s WHERE email=%s '
        cursor = connection.cursor()
        cursor.execute(sql, (username, session['key'] ))
        connection.commit()
        
        sql = 'UPDATE following SET  username=%s WHERE email=%s '
        cursor = connection.cursor()
        cursor.execute(sql, (username, session['key'] ))
        connection.commit()
       
       
        return redirect('/profile')
    else:
        return render_template('profile.html')   

        
@app.route('/editbio', methods = ['POST', 'GET'])
def editbio():
    if request.method == 'POST':
        bio = request.form['bio']
        
        connection = pymysql.connect(host='localhost', user='root', password='', database='jemuki.com')
        sql = 'UPDATE signup SET  bio=%s WHERE email=%s '
        cursor = connection.cursor()
        cursor.execute(sql, (bio, session['key'] ))
        connection.commit()
        # row = cursor.fetchone()
        # bio = row[3]
        # session['key2'] = bio
           
        return redirect('/profile')
    
    
        # email should be equal to place holder
            # cursor execute sql, session key 
    else:
        return render_template('profile.html')   



@app.route('/editdp', methods = ['POST', 'GET'])
def editdp():
    connection = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'jemuki.com')
    cursor = connection.cursor()
      
    now = datetime.now()
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        #print(files)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cursor.execute('UPDATE signup SET  dp=%s, dpuploaded_on=%s WHERE email=%s ',[filename, now, session['key']])
                connection.commit()
                print(file)
        cursor.close()
        
   
        flash('your  dp has been  updated successfully')
    return render_template('editdp.html')



#cur.execute("INSERT INTO signup (dp, dpuploaded_on)  VALUES (%s, %s)  ",[filename, now])
                
# your 'no words' dp has been successfully uploaded


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/ideas')
def ideas():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from ideas order by rand() LIMIT 60  "
    cursor = connection.cursor()
    cursor.execute(sql)
    
    if cursor.rowcount == 0 :
        return render_template('ideas.html', message = "No ideas uploaded yet")
    else:
        rows = cursor.fetchall()
        return render_template('ideas.html', data = rows )

    
    

@app.route('/readidea/<idea_id>')
def readidea(idea_id):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from ideas where idea_id=%s order by uploaded_on DESC  "
    cursor = connection.cursor()
    cursor.execute(sql, (idea_id))
    
    if cursor.rowcount == 0 :
        return render_template('readidea.html', message = "No ideas uploaded yet")
    else:
        row = cursor.fetchone()
        return render_template('readidea.html', data = row )



@app.route('/memeimages')
def memeimages():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from memeimages order by rand() LIMIT 10  "
    cursor = connection.cursor()
    cursor.execute(sql)
    
    if cursor.rowcount == 0 :
        return render_template('memeimages.html', message = "No images uploaded yet")
    else:
        rows = cursor.fetchall()
        return render_template('memeimages.html', data = rows )




@app.route('/addmemeimg', methods = ['POST', 'GET'])
def addmemeimg():
    connection = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'jemuki.com')
    cursor = connection.cursor()
    now = datetime.now()
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        caption = request.form['caption']
        #print(files)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cursor.execute('insert into memeimages(email, caption, image, username, dp, uploaded_on ) VALUES(%s, %s, %s, %s, %s, %s) ',[session['key'], caption, filename, session['key1'], session['key3'], now ])
                connection.commit()
                print(file)
        cursor.close()
        flash('your meme image has been uploaded successfully')
    return redirect('/memeimages')



    
    
    
@app.route('/sparkclips')
def sparkclips():
    return render_template('sparkclips.html')


@app.route('/bgsounds')
def bgsounds():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from bgsounds order by rand() LIMIT 60  "
    cursor = connection.cursor()
    cursor.execute(sql)
    
    if cursor.rowcount == 0 :
        return render_template('bgsound.html', message = "No sounds uploaded yet")
    else:
        rows = cursor.fetchall()
        return render_template('bgsound.html', data = rows )

@app.route('/searchsound', methods = ['POST', 'GET'])
def searchsound():
    if request.method == 'POST':
        search = request.form['search']
        
        connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
        sql = "select  * from bgsounds where caption like '%{}%' order by rand() LIMIT 50  ".format(search)
        cursor = connection.cursor()
        cursor.execute(sql)
        if cursor.rowcount == 0 :
            return render_template('bgsound.html', message = "No matching results")
        else:
            rows = cursor.fetchall()
            return render_template('bgsound.html', data2 = rows)



@app.route('/addbgsound', methods = ['POST', 'GET'])
def addbgsounds():
    connection = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'jemuki.com')
    cursor = connection.cursor()
    now = datetime.now()
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        caption = request.form['caption']
        #print(files)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cursor.execute('insert into bgsounds(email, caption, sound, username, dp, uploaded_on ) VALUES(%s, %s, %s, %s, %s, %s) ',[session['key'], caption, filename, session['key1'], session['key3'], now ])
                connection.commit()
                print(file)
        cursor.close()
        flash('your background sound  has been uploaded successfully')
    return redirect('/bgsounds')



@app.route('/challenge')
def challenge():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from challenge  "
    cursor = connection.cursor()
    cursor.execute(sql)
    
    if cursor.rowcount == 0 :
        return render_template('challenge.html', message = "No challenges uploaded yet")
    else:
        rows = cursor.fetchall()
        return render_template('challenge.html', data = rows )

    
    

@app.route('/chatalentreplies/<chalenge_id>')
def chatalentreplies():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from challenge  "
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    return render_template('challenge.html', data = rows )

    
    
    
    

@app.route('/chalegends')
def chalegends():
    return render_template('chalegends.html')

@app.route('/chalegendreplies')
def chalegendreplies():
    return render_template('chalegendreplies.html')


@app.route('/chainsane')
def chainsane():
    return render_template('chainsane.html')

@app.route('/chainsanereplies')
def chainsanereplies():
    return render_template('chainsanereplies.html')

@app.route('/chagods')
def chagods():
    return render_template('chagods.html')

@app.route('/chagodsreplies')
def chagodsreplies():
    return render_template('chagodsreplies.html')


@app.route('/funny')
def funny():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from funny where category = '' ORDER by rand()  LIMIT 10"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
        
    
    sql2 = "select * from funactive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    return render_template('funny.html', data = rows, x = row)

    

    
    

@app.route('/funlegends')
def funlegends():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from funny where category = 'legends' ORDER by rand() LIMIT 10 "
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
        
    
    sql2 = "select * from funactive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    
    
    return render_template('funlegends.html', data = rows, x=row )



@app.route('/funinsane')
def funinsane():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from funny where category = 'insane' ORDER by rand() LIMIT 10 "
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    
    sql2 = "select * from funactive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    
    
    return render_template('funinsane.html', data = rows, x=row )




@app.route('/fungods')
def fungods():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from funny where category = 'gods' ORDER by rand() LIMIT 10 "
    cursor = connection.cursor()
    cursor.execute(sql)
    
    rows = cursor.fetchall()
    
    sql2 = "select * from funactive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    
    
    
    return render_template('fungods.html', data = rows, x=row )

   

@app.route('/respect')
def respect():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from respect where category = '' ORDER by rand()  LIMIT 10"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
        
    
    sql2 = "select * from resactive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    return render_template('respect.html', data = rows, x = row)

    
    
    

@app.route('/reslegends')
def reslegends():
   connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
   sql = "select * from respect where category = 'legends' ORDER by rand() LIMIT 10 "
   cursor = connection.cursor()
   cursor.execute(sql)
   rows = cursor.fetchall()
    

   sql2 = "select * from resactive "
   cursor2 = connection.cursor()
   cursor2.execute(sql2)
   row = cursor2.fetchone()



   return render_template('reslegends.html', data = rows, x=row )




@app.route('/resinsane')
def resinsane():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from respect where category = 'insane' ORDER by rand() LIMIT 10 "
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    
    sql2 = "select * from resactive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    
    
    return render_template('resinsane.html', data = rows, x=row )



@app.route('/resgods')
def resgods():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from respect where category = 'gods' ORDER by rand() LIMIT 10 "
    cursor = connection.cursor()
    cursor.execute(sql)
    
    rows = cursor.fetchall()
    
    sql2 = "select * from resactive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    
    
    
    return render_template('resgods.html', data = rows, x=row )

   



@app.route('/memes')
def memes():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from memes where category = '' ORDER by rand()  LIMIT 10"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
        
    
    sql2 = "select * from memeactive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    return render_template('memes.html', data = rows, x = row)

    

@app.route('/memeslegends')
def memeslegends():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from memes where category = 'legends' ORDER by rand() LIMIT 10 "
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
        
    
    sql2 = "select * from memeactive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    
    
    return render_template('memeslegends.html', data = rows, x=row )



    

@app.route('/memesinsane')
def memesinsane():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from memes where category = 'insane' ORDER by rand() LIMIT 10 "
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    
    sql2 = "select * from memeactive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    
    
    return render_template('memesinsane.html', data = rows, x=row )



@app.route('/memesgods')
def memesgods():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from memes where category = 'gods' ORDER by rand() LIMIT 10 "
    cursor = connection.cursor()
    cursor.execute(sql)
    
    rows = cursor.fetchall()
    
    sql2 = "select * from memeactive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    
    
    
    return render_template('memesgods.html', data = rows, x=row )

   



@app.route('/her')
def her():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from her where category = '' ORDER by rand()  LIMIT 10"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
        
    
    sql2 = "select * from heractive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    return render_template('her.html', data = rows, x = row)

    
    

@app.route('/herlegends')
def herlegends():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from her where category = 'legends' ORDER by rand() LIMIT 10 "
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
        
    
    sql2 = "select * from heractive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    
    
    return render_template('herlegends.html', data = rows, x=row )




@app.route('/herinsane')
def herinsane():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from her where category = 'insane' ORDER by rand() LIMIT 10 "
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    
    sql2 = "select * from heractive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    
    
    return render_template('herinsane.html', data = rows, x=row )



@app.route('/hergods')
def hergods():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from her where category = 'gods' ORDER by rand() LIMIT 10 "
    cursor = connection.cursor()
    cursor.execute(sql)
    
    rows = cursor.fetchall()
    
    sql2 = "select * from heractive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    
    
    
    return render_template('hergods.html', data = rows, x=row )

   


@app.route('/music')
def music():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from music where category = '' ORDER by rand()  LIMIT 10"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
        
    
    sql2 = "select * from musicactive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    return render_template('music.html', data = rows, x = row)


@app.route('/musiclegends')
def musiclegends():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from music where category = 'legends' ORDER by rand() LIMIT 10 "
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
        
    
    sql2 = "select * from musicactive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    
    
    return render_template('musiclegends.html', data = rows, x=row )




@app.route('/musicinsane')
def musicinsane():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from music where category = 'insane' ORDER by rand() LIMIT 10 "
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    
    sql2 = "select * from musicactive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    
    
    return render_template('musicinsane.html', data = rows, x=row )



@app.route('/musicgods')
def musicgods():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from music where category = 'gods' ORDER by rand() LIMIT 10 "
    cursor = connection.cursor()
    cursor.execute(sql)
    
    rows = cursor.fetchall()
    
    sql2 = "select * from musicactive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    
    
    
    return render_template('musicgods.html', data = rows, x=row )

   


@app.route('/cars')
def cars():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from cars where category = '' ORDER by rand()  LIMIT 10"
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
        
    
    sql2 = "select * from caractive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    return render_template('cartalented.html', data = rows, x = row)

    

    
    

@app.route('/carlegends')
def carlegends():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from cars where category = 'legends' ORDER by rand() LIMIT 10 "
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
        
    
    sql2 = "select * from caractive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    
    
    return render_template('carlegends.html', data = rows, x=row )



@app.route('/carinsane')
def carinsane():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from cars where category = 'insane' ORDER by rand() LIMIT 10 "
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    
    sql2 = "select * from caractive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    
    
    return render_template('carinsane.html', data = rows, x=row )




@app.route('/cargods')
def cargods():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from cars where category = 'gods' ORDER by rand() LIMIT 10 "
    cursor = connection.cursor()
    cursor.execute(sql)
    
    rows = cursor.fetchall()
    
    sql2 = "select * from caractive "
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    row = cursor2.fetchone()
    
    
    
    
    return render_template('cargods.html', data = rows, x=row )

   






@app.route('/replies')
def replies():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from posts "
    
    cursor = connection.cursor()
    cursor.execute(sql)
    
    if cursor.rowcount == 0 :
        return render_template('replies.html', message = "No posts uploaded yet")
    else:
        rows = cursor.fetchall()
        return render_template('replies.html', data = rows )

    

@app.route('/repliesx/<post_id>')
def repliesx(post_id):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from posts where post_id = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (post_id))  # replace place holder %s with reg_no
    # get the row holding the car details
    row = cursor.fetchone()
    # we return the data holding one row
    return render_template('repliesx.html', data = row)


@app.route('/addrepliesx/<post_id>', methods = ['POST', 'GET'])
def addrepliesx(post_id):
    if request.method == 'POST':
        reply = request.form['reply']
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "insert into repliesx(email,	reply,	post_id,	username,	dp,	uploaded_on) VALUES(%s, %s, %s, %s, %s, %s)"
    cursor = connection.cursor()
    now = datetime.now()
    
    cursor.execute(sql, (session['key'], reply, post_id, session['key1'], session['key3'], now ))  # replace place holder %s with reg_no
    connection.commit()
    return render_template('repliesx.html')


@app.route('/showrepliesx/<post_id>')
def showrepliesx(post_id):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from repliesx where post_id = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (post_id))  
    
    rows = cursor.fetchall()

    return render_template('repliesx.html', data = rows)



@app.route('/replylegends')
def replylegends():
    return render_template('replylegends.html')

@app.route('/legendx')
def legendx():
    return render_template('legendx.html')

@app.route('/replyinsane')
def replyinsane():
    return render_template('replyinsane.html')

@app.route('/insanex')
def insanex():
    return render_template('insanex.html')


@app.route('/replygods')
def replygods():
    return render_template('replygods.html')

@app.route('/godsx')
def godsx():
    return render_template('godsx.html')


@app.route('/addchallenge', methods=['POST', 'GET'])
def addchallenge():
    connection = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'jemuki.com')
    cursor = connection.cursor()
    now = datetime.now()
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        caption = request.form['caption']
    
        #print(files)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cursor.execute("INSERT INTO challenge   (email,	challenge,	caption,	uploaded_on) VALUES (%s, %s, %s, %s) ", [ session['key'],filename, caption, now])
                connection.commit()
                print(file)
        cursor.close()
        flash('challenge(s) successfully uploaded')
    return render_template('addchallenge.html')

   
   

@app.route('/addfunny', methods=['POST', 'GET'])
def addfunny():
    connection = pymysql.connect(host = 'localhost', password = '', user = 'root', database = 'jemuki.com')
    cursor = connection.cursor()
    now = datetime.now()
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        caption = request.form['caption']
        
        #print(files)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cursor.execute("INSERT INTO funny(email, funny, caption, uploaded_on) VALUES (%s, %s, %s, %s)", [ session['key'],filename, caption, now])
                connection.commit()
                
                cursor.execute("INSERT INTO general(email, clip, clip_caption, uploaded_on) VALUES (%s, %s, %s, %s)", [ session['key'], filename, caption, now])
                connection.commit()
                
        
                
                print(file)
                cursor.close()
                flash('funny clip(s) successfully uploaded')
            return render_template('addfunny.html')



@app.route('/flash/<funny_id>')
def flashfunny(funny_id):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "SELECT * FROM flashfunny where email = %s and funny_id = %s "
    cursor = connection.cursor()
    
    cursor.execute(sql, (session['key'], funny_id))
    
    if cursor.rowcount == 0 :
        sql = "Insert into flashfunny(email, funny_id) VALUES(%s, %s) "
        cursor = connection.cursor()
        cursor.execute(sql, (session['key'], funny_id))  
        connection.commit()
        
        sql = "UPDATE funny SET flash = flash + 1  where funny_id = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (funny_id))  
        connection.commit()
    
        return render_template('flashz.html', message = "clip flashed successfully!!")
    
    else:
        return  render_template('flashz.html', message = "clip flashed already!!")

         
        
    

@app.route('/funnycomments/<funny_id>', methods = ['POST', 'GET'])
def funnycomments(funny_id):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from funnycomments where funny_id = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (funny_id))  
    
    if cursor.rowcount == 0 :
        return render_template('funnycomments.html', message = "No comments uploaded yet")
    elif cursor.rowcount > 0 :
        rows = cursor.fetchall()
        return render_template('funnycomments.html', data = rows)
    
    if request.method == 'POST':
        comment = request.form['comment']
        
       
    sql = "INSERT INTO funnycomments(email, funny_id, comment, username, dp, uploaded_on) VALUES(%s, %s, %s, %s, %s, %s) "
    cursor = connection.cursor()
    now = datetime.now()
    cursor.execute(sql, (session['key'], funny_id, comment, session['key1'], session['key3'], now )  )
    connection.commit()
    return render_template('funnycomments.html')
   
    
    
@app.route('/accfunny/<email>')
def funnytapac(email):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from signup where email = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (email))
    
    rows = cursor.fetchall()
    for row in rows :
        sql = "select * from funny where email = %s order by flash DESC "
        cursor.execute(sql, row[1])
        row = cursor.fetchall()
        
    return render_template('tapacfunny.html', data = rows , data2 = row )


@app.route('/followfunnytapac/<email>')
def followfunnytapac(email):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select  * from following where email = %s and following = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (session['key'], email))  
    
    if cursor.rowcount == 0 :
        sql = "Insert into following(email, following, username, dp) VALUES(%s, %s, %s, %s) "
        cursor = connection.cursor()
        cursor.execute(sql, (session['key'], email, session['key1'], session['key3']))  
        connection.commit()
        
        sql = "UPDATE signup SET followers = followers + 1  where email = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (email))  
        connection.commit()
        
        sql = "UPDATE signup SET following = following + 1  where email = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (session['key']))  
        connection.commit()
    
    
        return render_template('funnyfollowers.html', message = "followed successfully")
    
    elif cursor.rowcount == 1 :
        connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
        sql = "select  * from following where following = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (email)) 
        rows = cursor.fetchall()
        return render_template('funnyfollowers.html', data = rows)

        
    
    else:
        rows = cursor.fetchall()
        return render_template('funnyfollowers.html', data = rows )
    

@app.route('/followingfunnytapac/<email>')
def followingfunnytapac(email):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select  * from following where email = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (email)) 
        
    rows = cursor.fetchall()
    return render_template('funnyfollowing.html', data = rows)





    
    




@app.route('/addrespect', methods=['POST', 'GET'])
def addrespect():
    connection = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'jemuki.com'  )
    cursor = connection.cursor()
    now = datetime.now()
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        caption = request.form['caption']
    
        #print(files)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cursor.execute("INSERT INTO respect   (email,	respect,	caption,	uploaded_on) VALUES (%s, %s, %s, %s) ", [ session['key'], filename, caption, now])
                connection.commit()
                
                
                cursor.execute("INSERT INTO general(email, clip, clip_caption, uploaded_on) VALUES (%s, %s, %s, %s)", [ session['key'], filename, caption, now])
                connection.commit()
                 
                print(file)
        cursor.close()
        flash('respect clip(s) successfully uploaded')
    return render_template('addrespect.html')

    


@app.route('/flashrespect/<respect_id>')
def flashrespect(respect_id):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "SELECT * FROM flashrespect where email = %s and respect_id = %s "
    cursor = connection.cursor()
    
    cursor.execute(sql, (session['key'], respect_id))
    
    if cursor.rowcount == 0 :
        sql = "Insert into flashrespect(email, respect_id) VALUES(%s, %s) "
        cursor = connection.cursor()
        cursor.execute(sql, (session['key'], respect_id))  
        connection.commit()
        
        sql = "UPDATE respect SET flash = flash + 1  where respect_id = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (respect_id))  
        connection.commit()
    
        return render_template('flashz.html', message = "clip flashed successfully!!")
    
    else:
        return  render_template('flashz.html', message = "clip flashed already!!")

         
        
    

@app.route('/funnycomments/<respect_id>', methods = ['POST', 'GET'])
def respectcomments(respect_id):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from funnycomments where respect_id = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (respect_id))  
    
    if cursor.rowcount == 0 :
        return render_template('funnycomments.html', message = "No comments uploaded yet")
    elif cursor.rowcount > 0 :
        rows = cursor.fetchall()
        return render_template('funnycomments.html', data = rows)
    
    if request.method == 'POST':
        comment = request.form['comment']
        
       
    sql = "INSERT INTO funnycomments(email, respect_id, comment, username, dp, uploaded_on) VALUES(%s, %s, %s, %s, %s, %s) "
    cursor = connection.cursor()
    now = datetime.now()
    cursor.execute(sql, (session['key'], respect_id, comment, session['key1'], session['key3'], now )  )
    connection.commit()
    return render_template('funnycomments.html')
   
    
    
@app.route('/accrespect/<email>')
def respecttapac(email):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from signup where email = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (email))  
    
    rows = cursor.fetchall()
    for row in rows :
        sql = "select * from respect where email = %s order by flash DESC "
        cursor.execute(sql, row[1])
        row = cursor.fetchall()
        
    return render_template('tapacres.html', data = rows , data2 = row )


@app.route('/followrespecttapac/<email>')
def followrespecttapac(email):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select  * from following where email = %s and following = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (session['key'], email))  
    
    if cursor.rowcount == 0 :
        sql = "Insert into following(email, following, username, dp) VALUES(%s, %s, %s, %s) "
        cursor = connection.cursor()
        cursor.execute(sql, (session['key'], email, session['key1'], session['key3']))  
        connection.commit()
        
        sql = "UPDATE signup SET followers = followers + 1  where email = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (email))  
        connection.commit()
        
        
        sql = "UPDATE signup SET following = following + 1  where email = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (session['key']))  
        connection.commit()
    
    
        return render_template('funnyfollowers.html', message = "followed successfully")
    
    elif cursor.rowcount == 1 :
        connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
        sql = "select  * from following where following = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (email)) 
        rows = cursor.fetchall()
        return render_template('funnyfollowers.html', data = rows)

        
    
    else:
        rows = cursor.fetchall()
        return render_template('funnyfollowers.html', data = rows )
    

@app.route('/followingrespecttapac/<email>')
def followingrespecttapac(email):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select  * from following where email = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (email)) 
        
    rows = cursor.fetchall()
    return render_template('funnyfollowing.html', data = rows)

    
   
   
@app.route('/addmemes', methods=['POST', 'GET'] )
def addmemes():
    connection = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'jemuki.com')
    cursor = connection.cursor()
    now = datetime.now()
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        caption = request.form['caption']
    
        #print(files)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cursor.execute("insert into memes(email, meme, caption, uploaded_on)  VALUES(%s, %s, %s,%s ) ", [session['key'], filename, caption, now ])
                
                connection.commit()
                
                
                cursor.execute("INSERT INTO general(email, meme, meme_caption, uploaded_on) VALUES (%s, %s, %s, %s)", [ session['key'], filename, caption, now])
                connection.commit()
                
                print(file)
        cursor.close()
        flash('your insanely crazy meme has been  uploaded successfully')
    return render_template('addmemes.html')

# cur.execute('UPDATE signup SET  memes=%s, memeuploaded_on=%s, caption=%s WHERE email=%s ',[filename, now, caption, session['key']])
  
  
  
  
  

@app.route('/flashmemes/<meme_id>')
def flashmeme(meme_id):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "SELECT * FROM flashmemes where email = %s and meme_id = %s "
    cursor = connection.cursor()
    
    cursor.execute(sql, (session['key'], meme_id))
    
    if cursor.rowcount == 0 :
        sql = "Insert into flashmemes(email, meme_id) VALUES(%s, %s) "
        cursor = connection.cursor()
        cursor.execute(sql, (session['key'], meme_id))  
        connection.commit()
        
        sql = "UPDATE memes SET flash = flash + 1  where meme_id = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (meme_id))  
        connection.commit()
    
        return render_template('flashz.html', message = "meme flashed successfully!!")
    
    else:
        return  render_template('flashz.html', message = "meme flashed already!!")

         
        
    

@app.route('/memecomments/<meme_id>', methods = ['POST', 'GET'])
def memecomments(funny_id):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from funnycomments where funny_id = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (funny_id))  
    
    if cursor.rowcount == 0 :
        return render_template('funnycomments.html', message = "No comments uploaded yet")
    elif cursor.rowcount > 0 :
        rows = cursor.fetchall()
        return render_template('funnycomments.html', data = rows)
    
    if request.method == 'POST':
        comment = request.form['comment']
        
       
    sql = "INSERT INTO funnycomments(email, funny_id, comment, username, dp, uploaded_on) VALUES(%s, %s, %s, %s, %s, %s) "
    cursor = connection.cursor()
    now = datetime.now()
    cursor.execute(sql, (session['key'], funny_id, comment, session['key1'], session['key3'], now )  )
    connection.commit()
    return render_template('funnycomments.html')
   
    
    
@app.route('/accmemes/<email>')
def memestapac(email):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from signup where email = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (email))  
    rows = cursor.fetchall()
    for row in rows :
        sql = "select * from memes where email = %s order by flash DESC "
        cursor.execute(sql, row[1])
        row = cursor.fetchall()
        
    return render_template('tapacmemes.html', data = rows , data2 = row )


@app.route('/followmemestapac/<email>')
def followmemestapac(email):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select  * from following where email = %s and following = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (session['key'], email))  
    
    if cursor.rowcount == 0 :
        sql = "Insert into following(email, following, username, dp) VALUES(%s, %s, %s, %s) "
        cursor = connection.cursor()
        cursor.execute(sql, (session['key'], email, session['key1'], session['key3']))  
        connection.commit()
        
        sql = "UPDATE signup SET followers = followers + 1  where email = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (email))  
        connection.commit()
        
        sql = "UPDATE signup SET following = following + 1  where email = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (session['key']))  
        connection.commit()
        
        
        
    
    
        return render_template('funnyfollowers.html', message = "followed successfully")
    
    elif cursor.rowcount == 1 :
        connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
        sql = "select  * from following where following = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (email)) 
        rows = cursor.fetchall()
        return render_template('funnyfollowers.html', data = rows)

        
    
    else:
        rows = cursor.fetchall()
        return render_template('funnyfollowers.html', data = rows )
    

@app.route('/followingmemestapac/<email>')
def followingmemestapac(email):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select  * from following where email = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (email)) 
        
    rows = cursor.fetchall()
    return render_template('funnyfollowing.html', data = rows)

    
    




  
  
                

@app.route('/addher', methods=['POST', 'GET'])
def addher():
    connection = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'jemuki.com')
    cursor = connection.cursor()
    now = datetime.now()
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        caption = request.form['caption']
    
        #print(files)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cursor.execute("INSERT INTO her  (email,	her,	caption,	uploaded_on) VALUES (%s, %s, %s, %s) ", [ session['key'],filename, caption, now])
                connection.commit()
                
                cursor.execute("INSERT INTO general(email, clip, clip_caption, uploaded_on) VALUES (%s, %s, %s, %s)", [ session['key'], filename, caption, now])
                connection.commit()
                
                print(file)
        cursor.close()
        flash('made her day clip(s) successfully uploaded')
    return render_template('addher.html')

    



@app.route('/flashher/<her_id>')
def flashher(her_id):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "SELECT * FROM flashher where email = %s and her_id = %s "
    cursor = connection.cursor()
    
    cursor.execute(sql, (session['key'], her_id))
    
    if cursor.rowcount == 0 :
        sql = "Insert into flashher(email, her_id) VALUES(%s, %s) "
        cursor = connection.cursor()
        cursor.execute(sql, (session['key'], her_id))  
        connection.commit()
        
        sql = "UPDATE her SET flash = flash + 1  where her_id = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (her_id))  
        connection.commit()
    
        return render_template('flashz.html', message = "clip flashed successfully!!")
    
    else:
        return  render_template('flashz.html', message = "clip flashed already!!")

         
        
    

@app.route('/funnycomments/<funny_id>', methods = ['POST', 'GET'])
def hercomments(funny_id):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from funnycomments where funny_id = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (funny_id))  
    
    if cursor.rowcount == 0 :
        return render_template('funnycomments.html', message = "No comments uploaded yet")
    elif cursor.rowcount > 0 :
        rows = cursor.fetchall()
        return render_template('funnycomments.html', data = rows)
    
    if request.method == 'POST':
        comment = request.form['comment']
        
       
    sql = "INSERT INTO funnycomments(email, funny_id, comment, username, dp, uploaded_on) VALUES(%s, %s, %s, %s, %s, %s) "
    cursor = connection.cursor()
    now = datetime.now()
    cursor.execute(sql, (session['key'], funny_id, comment, session['key1'], session['key3'], now )  )
    connection.commit()
    return render_template('funnycomments.html')
   
    
    
@app.route('/accher/<email>')
def hertapac(email):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from signup where email = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (email))  
    
    rows = cursor.fetchall()
    for row in rows :
        sql = "select * from her where email = %s order by flash DESC "
        cursor.execute(sql, row[1])
        row = cursor.fetchall()
        
    return render_template('tapacher.html', data = rows , data2 = row )


    
    
    
@app.route('/followhertapac/<email>')
def followhertapac(email):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select  * from following where email = %s and following = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (session['key'], email))  
    
    if cursor.rowcount == 0 :
        sql = "Insert into following(email, following, username, dp) VALUES(%s, %s, %s, %s) "
        cursor = connection.cursor()
        cursor.execute(sql, (session['key'], email, session['key1'], session['key3']))  
        connection.commit()
        
        sql = "UPDATE signup SET followers = followers + 1  where email = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (email))  
        connection.commit()
        
        
        sql = "UPDATE signup SET following = following + 1  where email = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (session['key']))  
        connection.commit()
    
    
        return render_template('funnyfollowers.html', message = "followed successfully")
    
    elif cursor.rowcount == 1 :
        connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
        sql = "select  * from following where following = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (email)) 
        rows = cursor.fetchall()
        return render_template('funnyfollowers.html', data = rows)

        
    
    else:
        rows = cursor.fetchall()
        return render_template('funnyfollowers.html', data = rows )
    

@app.route('/followinghertapac/<email>')
def followinghertapac(email):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select  * from following where email = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (email)) 
        
    rows = cursor.fetchall()
    return render_template('funnyfollowing.html', data = rows)

    
    










@app.route('/addmusic', methods=['POST', 'GET'])
def addmusic():
    connection = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'jemuki.com')
    cursor = connection.cursor()
    now = datetime.now()
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        caption = request.form['caption']
    
        #print(files)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cursor.execute("INSERT INTO music   (email,	music,	caption,	uploaded_on) VALUES (%s, %s, %s, %s) ", [ session['key'],filename, caption, now])
                connection.commit()
                
                cursor.execute("INSERT INTO general(email, clip, clip_caption, uploaded_on) VALUES (%s, %s, %s, %s)", [ session['key'], filename, caption, now])
                connection.commit()
                
                print(file)
        cursor.close()
        flash('music clip(s) successfully uploaded')
    return render_template('addmusic.html')

    


@app.route('/flashmusic/<music_id>')
def flashmusic(music_id):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "SELECT * FROM flashmusic where email = %s and music_id = %s "
    cursor = connection.cursor()
    
    cursor.execute(sql, (session['key'], music_id))
    
    if cursor.rowcount == 0 :
        sql = "Insert into flashmusic(email, music_id) VALUES(%s, %s) "
        cursor = connection.cursor()
        cursor.execute(sql, (session['key'], music_id))  
        connection.commit()
        
        sql = "UPDATE music SET flash = flash + 1  where music_id = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (music_id))  
        connection.commit()
    
        return render_template('flashz.html', message = "clip flashed successfully!!")
    
    else:
        return  render_template('flashz.html', message = "clip flashed already!!")

         
        
    
    
    
@app.route('/accmusic/<email>')
def musictapac(email):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from signup where email = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (email))  
    
    rows = cursor.fetchall()
    for row in rows :
        sql = "select * from music where email = %s order by flash DESC "
        cursor.execute(sql, row[1])
        row = cursor.fetchall()
        
    return render_template('tapacmusic.html', data = rows , data2 = row )


@app.route('/followmusictapac/<email>')
def followmusictapac(email):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select  * from following where email = %s and following = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (session['key'], email))  
    
    if cursor.rowcount == 0 :
        sql = "Insert into following(email, following, username, dp) VALUES(%s, %s, %s, %s) "
        cursor = connection.cursor()
        cursor.execute(sql, (session['key'], email, session['key1'], session['key3']))  
        connection.commit()
        
        sql = "UPDATE signup SET followers = followers + 1  where email = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (email))  
        connection.commit()
        
        
        sql = "UPDATE signup SET following = following + 1  where email = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (session['key']))  
        connection.commit()
    
    
        return render_template('funnyfollowers.html', message = "followed successfully")
    
    elif cursor.rowcount == 1 :
        connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
        sql = "select  * from following where following = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (email)) 
        rows = cursor.fetchall()
        return render_template('funnyfollowers.html', data = rows)

        
    
    else:
        rows = cursor.fetchall()
        return render_template('funnyfollowers.html', data = rows )
    

@app.route('/followingmusictapac/<email>')
def followingmusictapac(email):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select  * from following where email = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (email)) 
        
    rows = cursor.fetchall()
    return render_template('funnyfollowing.html', data = rows)

    
  
  
@app.route('/addcars', methods=['POST', 'GET'])
def addcars():
    connection = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'jemuki.com')
    cursor = connection.cursor()
    now = datetime.now()
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        caption = request.form['caption']
        
        #print(files)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cursor.execute("INSERT INTO cars(email, car, caption, uploaded_on) VALUES (%s, %s, %s, %s)", [ session['key'],filename, caption, now])
                connection.commit()
                
                cursor.execute("INSERT INTO general(email, clip, clip_caption, uploaded_on) VALUES (%s, %s, %s, %s)", [ session['key'], filename, caption, now])
                connection.commit()
                
        
                
                print(file)
                cursor.close()
                flash('car clip(s) successfully uploaded')
            return render_template('addcars.html')



@app.route('/flashcars/<car_id>')
def flashcars(car_id):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "SELECT * FROM flashcars where email = %s and car_id = %s "
    cursor = connection.cursor()
    
    cursor.execute(sql, (session['key'], car_id))
    
    if cursor.rowcount == 0 :
        sql = "Insert into flashcars(email, car_id) VALUES(%s, %s) "
        cursor = connection.cursor()
        cursor.execute(sql, (session['key'], car_id))  
        connection.commit()
        
        sql = "UPDATE cars SET flash = flash + 1  where car_id = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (car_id))  
        connection.commit()
    
        return render_template('flashz.html', message = "clip flashed successfully!!")
    
    else:
        return  render_template('flashz.html', message = "clip flashed already!!")

         
        
    

@app.route('/carcomments/<funny_id>', methods = ['POST', 'GET'])
def carcomments(funny_id):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from funnycomments where funny_id = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (funny_id))  
    
    if cursor.rowcount == 0 :
        return render_template('funnycomments.html', message = "No comments uploaded yet")
    elif cursor.rowcount > 0 :
        rows = cursor.fetchall()
        return render_template('funnycomments.html', data = rows)
    
    if request.method == 'POST':
        comment = request.form['comment']
        
       
    sql = "INSERT INTO funnycomments(email, funny_id, comment, username, dp, uploaded_on) VALUES(%s, %s, %s, %s, %s, %s) "
    cursor = connection.cursor()
    now = datetime.now()
    cursor.execute(sql, (session['key'], funny_id, comment, session['key1'], session['key3'], now )  )
    connection.commit()
    return render_template('funnycomments.html')
   
    
    
@app.route('/acccars/<email>')
def cartapac(email):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from signup where email = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (email))
    
    rows = cursor.fetchall()
    for row in rows :
        sql = "select * from cars where email = %s order by flash DESC "
        cursor.execute(sql, row[1])
        row = cursor.fetchall()
        
    return render_template('tapaccars.html', data = rows , data2 = row )


@app.route('/followcarstapac/<email>')
def followcarstapac(email):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select  * from following where email = %s and following = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (session['key'], email))  
    
    if cursor.rowcount == 0 :
        sql = "Insert into following(email, following, username, dp) VALUES(%s, %s, %s, %s) "
        cursor = connection.cursor()
        cursor.execute(sql, (session['key'], email, session['key1'], session['key3']))  
        connection.commit()
        
        sql = "UPDATE signup SET followers = followers + 1  where email = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (email))  
        connection.commit()
        
        sql = "UPDATE signup SET following = following + 1  where email = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (session['key']))  
        connection.commit()
    
    
        return render_template('funnyfollowers.html', message = "followed successfully")
    
    elif cursor.rowcount == 1 :
        connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
        sql = "select  * from following where following = %s "
        cursor = connection.cursor()
        cursor.execute(sql, (email)) 
        rows = cursor.fetchall()
        return render_template('funnyfollowers.html', data = rows)

        
    
    else:
        rows = cursor.fetchall()
        return render_template('funnyfollowers.html', data = rows )
    




@app.route('/addpost', methods= ['POST','GET'])
def addpost():
    connection = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'jemuki.com')
    cursor = connection.cursor()
    now = datetime.now()
    if request.method == 'POST':
        post = request.form['post']
        files = request.files.getlist('files[]')
       
        #print(files)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cursor.execute("INSERT INTO posts  (email, post, postimg, username, dp, uploaded_on) VALUES (%s, %s, %s, %s, %s, %s) ", [ session['key'], post, filename, session['key1'] , session['key3'], now])
                connection.commit()
                print(file)
        cursor.close()
        flash('made her day clip(s) successfully uploaded')
    return redirect('/replies')





@app.route('/addidea', methods = ['POST', 'GET'])
def addidea():
    if request.method == 'POST':
        caption = request.form['caption']
        idea = request.form['idea']
        
        connection = pymysql.connect(host='localhost', user='root', password='', database='jemuki.com')
        now = datetime.now()
        sql = 'insert into ideas(email, caption, idea, username, dp, uploaded_on)  VALUES(%s, %s, %s, %s, %s, %s) '
        cursor = connection.cursor()
        
        cursor.execute(sql, (session['key'],caption, idea, session['key1'], session['key3'], now ))
        connection.commit()
        # row = cursor.fetchone() 
        # bio = row[3]
        # session['key2'] = bio
           
        return redirect('/ideas')


@app.route('/searchidea', methods = ['POST', 'GET'])
def searchidea():
    if request.method == 'POST':
        search = request.form['search']
        
        connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
        sql = "select  * from ideas where caption like '%{}%' order by rand() LIMIT 50 ".format(search)
        cursor = connection.cursor()
        cursor.execute(sql)
        if cursor.rowcount == 0 :
            return render_template('ideas.html', message = "No matching results")
        else:
            rows = cursor.fetchall()
            return render_template('ideas.html', data2 = rows)







@app.route('/about')
def about():
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select  * from about "
    cursor = connection.cursor()
    cursor.execute(sql)
    row = cursor.fetchall()
    
    return render_template('about us.html', data = row)






@app.route('/settings', methods = ['POST', 'GET'])
def settings():
    return render_template('settings.html')


@app.route('/feedback', methods = ['POST', 'GET'])
def feedback():
    if request.method == 'POST':
        feedback = request.form['feedback']    
    
        connection = pymysql.connect(host ='localhost', user ='root', password ='', database ='jemuki.com')
        cursor = connection.cursor()
        try:
            cursor.execute('insert into feedback(email, feedback) values(%s,%s)', ( session['key'], feedback))
            connection.commit()
            return redirect('/settings')
        except:
            return render_template('feedback.html', message = "try again")
    else:
        return render_template('settings.html')
        
   


@app.route('/changepassword', methods = ['POST', 'GET'])
def changepassword():
    if request.method == 'POST':
        oldpassword = request.form['oldpassword']
        newpassword = request.form['newpassword']
        
        connection = pymysql.connect(host='localhost', user='root', password='', database='jemuki.com')
        
        cursor = connection.cursor()
        cursor.execute('select * from signup where email = %s and password = %s', (session['key'], oldpassword))
        
        
        if cursor.rowcount == 0 :
            return render_template('settings.html', message = "Wrong old password, please try again.")
        elif cursor.rowcount == 1 :
            connection = pymysql.connect(host='localhost', user='root', password='', database='jemuki.com')
        
            cursor = connection.cursor()
            cursor.execute('UPDATE signup SET password = %s where email = %s ', (newpassword, session['key']))
        
            
            return redirect('/settings')
        else:
            return render_template('settings.html', message = "Something went wrong, please try again")
    else:
        return render_template('settings.html')
        

@app.route('/search', methods = ['POST', 'GET'])
def search():
    if request.method == 'POST':
        search = request.form['search']
        
        connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
        sql = "select  * from signup where username  like '%{}%' order by followers DESC ".format(search)
        cursor = connection.cursor()
        cursor.execute(sql) 
        rows1 = cursor.fetchall()
        if cursor.rowcount == 0 :
            sql = "select  * from general where  clip_caption like '%{}%'".format(search)

            cursor = connection.cursor()
            cursor.execute(sql) 
            rows2 = cursor.fetchall()
            
            sql = "select  * from general where meme_caption like '%{}%'".format(search)
            cursor = connection.cursor()
            cursor.execute(sql) 
            rows = cursor.fetchall()
            
            return render_template('searchscreen.html',  data2 = rows2, data3 = rows)
        
        else:
            return render_template('searchscreen.html', data1 = rows1)
    



         
    
@app.route('/resultscontent/<email>')
def content(email):
    connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
    sql = "select * from signup where email = %s "
    cursor = connection.cursor()
    cursor.execute(sql, (email))  
    
    rows = cursor.fetchall()
    for row in rows :
        sql = "select * from general where email = %s order by uploaded_on DESC "
        cursor.execute(sql, (row[1]) )
        row = cursor.fetchall()
        
    return render_template('resultscontent.html', x = rows , data = row)








# Transition to legends

# funny transition
@app.route('/funlegendstrigger')
def funlegendstransition():
    # To legends
    connection = pymysql.connect(host='localhost', user='root', password='', database='jemuki.com')
    cursor = connection.cursor()
    sql = 'select * from funny  '
    cursor.execute(sql)
    if cursor.rowcount > 500 :
        connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
        cursor = connection.cursor()
        sql = "select * from funny where category = '' order by flash DESC LIMIT 50"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            sql = "update funny set  category= 'legends' where funny_id = %s "
            cursor.execute(sql, row[0])
            connection.commit()
        
        #To insane
        cursor = connection.cursor()
        sql = "select * from funny where category = 'legends' order by flash DESC LIMIT 20"
        cursor.execute(sql)
        rowsinsane = cursor.fetchall()
        for row in rowsinsane:
            sql = "update funny set  category= 'insane' where funny_id = %s "
            cursor.execute(sql, row[0])
            connection.commit()
        
        # To gods
        cursor = connection.cursor()
        sql = "select * from funny where category = 'insane' order by flash DESC LIMIT 10"
        cursor.execute(sql)
        rowsgods = cursor.fetchall()
        for row in rowsgods:
            sql = "update funny set  category= 'gods' where funny_id = %s "
            cursor.execute(sql, row[0])
            connection.commit()
        return 'Repositioning done successfully'   
    else:
        return 'Repositioning not done since funny clips are less than 500'
            
        

        
        
# respect transition         
@app.route('/reslegendstrigger')
def reslegendstransition():
    # To legends
    connection = pymysql.connect(host='localhost', user='root', password='', database='jemuki.com')
    cursor = connection.cursor()
    sql = 'select * from respect  '
    cursor.execute(sql)
    if cursor.rowcount > 500 :
        connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
        cursor = connection.cursor()
        sql = "select * from respect where category = '' order by flash DESC LIMIT 50"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            sql = "update respect set  category= 'legends' where respect_id = %s "
            cursor.execute(sql, row[0])
            connection.commit()
        
        #To insane
        cursor = connection.cursor()
        sql = "select * from respect where category = 'legends' order by flash DESC LIMIT 20"
        cursor.execute(sql)
        rowsinsane = cursor.fetchall()
        for row in rowsinsane:
            sql = "update respect set  category= 'insane' where respect_id = %s "
            cursor.execute(sql, row[0])
            connection.commit()
        
        # To gods
        cursor = connection.cursor()
        sql = "select * from respect where category = 'insane' order by flash DESC LIMIT 10"
        cursor.execute(sql)
        rowsgods = cursor.fetchall()
        for row in rowsgods:
            sql = "update respect set  category= 'gods' where respect_id = %s "
            cursor.execute(sql, row[0])
            connection.commit()
        return 'Repositioning done successfully'   
    else:
        return 'Repositioning not done since respect clips are less than 500'


# memes transition
@app.route('/memeslegendstrigger')
def memeslegendstransition():
    # To legends
    connection = pymysql.connect(host='localhost', user='root', password='', database='jemuki.com')
    cursor = connection.cursor()
    sql = 'select * from memes  '
    cursor.execute(sql)
    if cursor.rowcount > 500 :
        connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
        cursor = connection.cursor()
        sql = "select * from memes where category = '' order by flash DESC LIMIT 50"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            sql = "update memes set  category= 'legends' where meme_id = %s "
            cursor.execute(sql, row[0])
            connection.commit()
        
        #To insane
        cursor = connection.cursor()
        sql = "select * from memes where category = 'legends' order by flash DESC LIMIT 20"
        cursor.execute(sql)
        rowsinsane = cursor.fetchall()
        for row in rowsinsane:
            sql = "update memes set  category= 'insane' where meme_id = %s "
            cursor.execute(sql, row[0])
            connection.commit()
        
        # To gods
        cursor = connection.cursor()
        sql = "select * from memes where category = 'insane' order by flash DESC LIMIT 10"
        cursor.execute(sql)
        rowsgods = cursor.fetchall()
        for row in rowsgods:
            sql = "update memes set  category= 'gods' where meme_id = %s "
            cursor.execute(sql, row[0])
            connection.commit()
        return 'Repositioning done successfully'   
    else:
        return 'Repositioning not done since memes are less than 500'    
        


# her transition
@app.route('/herlegendstrigger')
def herlegendstransition():
    # To legends
    connection = pymysql.connect(host='localhost', user='root', password='', database='jemuki.com')
    cursor = connection.cursor()
    sql = 'select * from her  '
    cursor.execute(sql)
    if cursor.rowcount > 500 :
        connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
        cursor = connection.cursor()
        sql = "select * from her where category = '' order by flash DESC LIMIT 50"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            sql = "update her set  category= 'legends' where her_id = %s "
            cursor.execute(sql, row[0])
            connection.commit()
        
        #To insane
        cursor = connection.cursor()
        sql = "select * from her where category = 'legends' order by flash DESC LIMIT 20"
        cursor.execute(sql)
        rowsinsane = cursor.fetchall()
        for row in rowsinsane:
            sql = "update her set  category= 'insane' where her_id = %s "
            cursor.execute(sql, row[0])
            connection.commit()
        
        # To gods
        cursor = connection.cursor()
        sql = "select * from her where category = 'insane' order by flash DESC LIMIT 10"
        cursor.execute(sql)
        rowsgods = cursor.fetchall()
        for row in rowsgods:
            sql = "update her set  category= 'gods' where her_id = %s "
            cursor.execute(sql, row[0])
            connection.commit()
        return 'Repositioning done successfully'   
    else:
        return 'Repositioning not done since her clips are less than 500'
            
        


# music transition
@app.route('/musiclegendstrigger')
def musiclegendstransition():
    # To legends
    connection = pymysql.connect(host='localhost', user='root', password='', database='jemuki.com')
    cursor = connection.cursor()
    sql = 'select * from music  '
    cursor.execute(sql)
    if cursor.rowcount > 500 :
        connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
        cursor = connection.cursor()
        sql = "select * from music where category = '' order by flash DESC LIMIT 50"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            sql = "update music set  category= 'legends' where music_id = %s "
            cursor.execute(sql, row[0])
            connection.commit()
        
        #To insane
        cursor = connection.cursor()
        sql = "select * from music where category = 'legends' order by flash DESC LIMIT 20"
        cursor.execute(sql)
        rowsinsane = cursor.fetchall()
        for row in rowsinsane:
            sql = "update music set  category= 'insane' where music_id = %s "
            cursor.execute(sql, row[0])
            connection.commit()
        
        # To gods
        cursor = connection.cursor()
        sql = "select * from music where category = 'insane' order by flash DESC LIMIT 10"
        cursor.execute(sql)
        rowsgods = cursor.fetchall()
        for row in rowsgods:
            sql = "update music set  category= 'gods' where music_id = %s "
            cursor.execute(sql, row[0])
            connection.commit()
        return 'Repositioning done successfully'   
    
    else:
        return 'Repositioning not done since music clips are less than 500'
            
            
            
            
# Car lovers transition
@app.route('/carlegendstrigger')
def carlegendstransition():
    # To legends
    connection = pymysql.connect(host='localhost', user='root', password='', database='jemuki.com')
    cursor = connection.cursor()
    sql = 'select * from cars  '
    cursor.execute(sql)
    if cursor.rowcount > 500:
        connection = pymysql.connect(host='localhost',user='root', password='', database='jemuki.com')
        cursor = connection.cursor()
        sql = "select * from cars where category = '' order by flash DESC LIMIT 50"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            sql = "update cars set  category= 'legends' where car_id = %s "
            cursor.execute(sql, row[0])
            connection.commit()
        
        #To insane
        cursor = connection.cursor()
        sql = "select * from cars where category = 'legends' order by flash DESC LIMIT 20"
        cursor.execute(sql)
        rowsinsane = cursor.fetchall()
        for row in rowsinsane:
            sql = "update cars set  category= 'insane' where car_id = %s "
            cursor.execute(sql, row[0])
            connection.commit()
        
        # To gods
        cursor = connection.cursor()
        sql = "select * from cars where category = 'insane' order by flash DESC LIMIT 10"
        cursor.execute(sql)
        rowsgods = cursor.fetchall()
        for row in rowsgods:
            sql = "update cars set  category= 'gods' where car_id = %s "
            cursor.execute(sql, row[0])
            connection.commit()
        return 'Repositioning done successfully'   
    else:
        return 'Repositioning not done since car lovers clips are less than 500'
            
        


    
            
    
        
            
            
            
            
            
        
        
    
        
                    

        
    
    
    
    
    
    
    
        
    
    
    
      
    
    



if __name__ == '__main__':
    app.run(debug=True)



  
  