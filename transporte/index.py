from flask import Flask, request, session, redirect, url_for, render_template, flash
import psycopg2 #pip install psycopg2 
import psycopg2.extras
import re 
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'
 
DB_HOST = "localhost"
DB_NAME = "bdLogin"
DB_USER = "postgres"
DB_PASS = "password"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
"""
@app.route('/')
def principal():
    return "xDDDD"

@app.route('/contacto')   
def contacto():
    return "Holiiiiiiiii"
"""

@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/base')   
def base():
    return render_template('base.html')


@app.route('/welcome', methods=['GET', 'POST'])   
def welcome():
    if request.method == 'POST' and 'codigo':
        codigo = request.form['codigo']
        if 'loggedin' in session:
            codValidacion=session['codigoValidacion']
            if (str(codigo) == str(codValidacion)):                    
                return redirect(url_for('newpassword'))
            else:
                return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # cursor2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if "username" and "password" POST requests exist (user submitted form)
    # if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    if request.method == 'POST' and 'username' and 'password' :
        username = request.form['username']
        password = request.form['password']
        print(password)
 
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM cuenta WHERE id_cuenta = %s', (username,))
        # Fetch one record and return result
        account = cursor.fetchone()

 
        if account:
            password_rs = account['des_contraseña']
            estadoUsu = account['ind_estado']
            print(estadoUsu)
            # If account exists in users table in out database
            #check_password_hash
            if (password_rs == password):
                codigoV=random.randint(500, 1000)
                # codigoV=10
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id_cuenta']
                session['codigoValidacion']=codigoV
                # session['username'] = account['username']
                # Redirect to home page
                if (str(estadoUsu) in '0'):                    

                    # username = "transporteucss@gmail.com"
                    # password = "cfvotdoormuiubun"
                    # mail_from = "transporteucss@gmail.com"
                    # mail_to = account['id_cuenta']
                    # mail_subject = "Código de validación"
                    # mail_body = ("Este es el código de validación "+str(codigoV))

                    # mimemsg = MIMEMultipart()
                    # mimemsg['From']=mail_from
                    # mimemsg['To']=mail_to
                    # mimemsg['Subject']=mail_subject
                    # mimemsg.attach(MIMEText(mail_body, 'plain'))
                    # connection = smtplib.SMTP(host='smtp.gmail.com', port=587)
                    # connection.starttls()
                    # connection.login(username,password)
                    # connection.send_message(mimemsg)
                    # connection.quit()
                    return render_template('welcome.html', account=account, codigoV=codigoV)
                else:
                    return redirect(url_for('menu'))
                                # return redirect(url_for('menu'))

            else:
                # flash.success(request, "Error")
                # flash(f'Bought {messages} items successfully!', 'success')
                # Account doesnt exist or username/password incorrect
                flash('Incorrect username/password')
                # alertify.error("El usuario no existe")

        else:
            # flash(f'Bought {messages} items successfully!', 'success')
            # flash.success(request, "Error")
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password')
                            # alertify.error("El usuario no existe")
 
    return render_template('index.html')


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('codigoValidacion', None)
   return redirect(url_for('login'))

@app.route('/menu') 
def menu(): 
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if user is loggedin
    if 'loggedin' in session:
        # cursor.execute('SELECT * FROM cuenta WHERE id_cuenta = %s', [session['id']])
        # cursor.execute('SELECT * FROM "rolTrabajador" WHERE "id_rolTrabajador"=701')
        cursor.execute('select t.id_dni as DNI,des_nombre,des_apepat,des_apemat, c.id_cuenta,c.des_contraseña,c.ind_estado,r.des_rol from trabajador t, "ctaTrabajador" ctaT, cuenta c, "rolTrabajador" rolT, rol r where t.id_dni=ctaT.id_dni and ctaT.id_cuenta=c.id_cuenta and rolT.id_trabajador=t.id_dni and r.id_rol=rolT.id_rol and c.id_cuenta = %s', [session['id']])
        account = cursor.fetchone()
        cursor2.execute('select t.id_dni,c.id_cuenta, o.des_opcion from trabajador t, "ctaTrabajador" ctaT, cuenta c, "rolTrabajador" rolT, rol r, opcion o where t.id_dni=ctaT.id_dni and ctaT.id_cuenta=c.id_cuenta and rolT.id_trabajador=t.id_dni and r.id_rol=rolT.id_rol and o.id_rol=r.id_rol and c.id_cuenta = %s', [session['id']])
        account2 = cursor2.fetchall()

        # Show the profile page with account info
        return render_template('menu.html', account=account, account2=account2)
    # User is not loggedin redirect to login page
    return redirect(url_for('menu'))


@app.route('/questions', methods=['GET', 'POST'])   
def questions():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM pregunta')
    account = cursor.fetchall()
 
    if request.method == 'POST' and 'rsp10' in request.form and 'rsp11' in request.form and 'rsp12' in request.form and 'rsp13' in request.form and 'rsp14' in request.form:
    # if request.method == 'POST' and 'rsp10':
        # Create variables for easy access
        rsp10 = request.form['rsp10']
        rsp11 = request.form['rsp11']
        rsp12 = request.form['rsp12']
        rsp13 = request.form['rsp13']
        rsp14 = request.form['rsp14']
     

            # Account doesnt exists and the form data is valid, now insert new account into users table
        if 'loggedin' in session:
            id_cuenta=session['id']
            cursor2.execute('INSERT INTO "pregCuenta" (id_cuenta, id_pregunta, res_pregunta) VALUES (%s,%s,%s)', (id_cuenta, 10, rsp10))
            cursor2.execute('INSERT INTO "pregCuenta" (id_cuenta, id_pregunta, res_pregunta) VALUES (%s,%s,%s)', (id_cuenta, 11, rsp11))
            cursor2.execute('INSERT INTO "pregCuenta" (id_cuenta, id_pregunta, res_pregunta) VALUES (%s,%s,%s)', (id_cuenta, 12, rsp12))
            cursor2.execute('INSERT INTO "pregCuenta" (id_cuenta, id_pregunta, res_pregunta) VALUES (%s,%s,%s)', (id_cuenta, 13, rsp13))
            cursor2.execute('INSERT INTO "pregCuenta" (id_cuenta, id_pregunta, res_pregunta) VALUES (%s,%s,%s)', (id_cuenta, 14, rsp14))
            cursor2.execute('UPDATE cuenta set ind_estado=%s where id_cuenta=%s', (1,id_cuenta))
            conn.commit()
            flash('You have successfully registered!')
            return redirect(url_for('login'))

        # cursor2.execute('INSERT INTO "pregCuenta" (id_cuenta, id_pregunta, res_pregunta) VALUES (%s,%s,%s)', ('jadrianzenrojas@hotmail.com', 10, rsp10))
        # conn.commit()
        # flash('You have successfully registered!')
        # return redirect(url_for('login'))


    return render_template('questions.html', account=account)

@app.route('/newpassword', methods=['GET', 'POST'])   
def newpassword():
    
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST' and 'password' and 'password2':
        password = request.form['password']
        password2 = request.form['password2']

        if 'loggedin' in session:
            id_cuenta=session['id']
            cursor2.execute('SELECT * FROM cuenta WHERE id_cuenta = %s', (id_cuenta,))            
            account2 = cursor2.fetchone()
            estadoUsu = account2['ind_estado']
            
            if (password == password2):       
                cursor.execute('UPDATE cuenta set "des_contraseña"=%s where id_cuenta=%s', (password,id_cuenta))
                conn.commit()  

                if (str(estadoUsu) in '0'):              
                    return redirect(url_for('questions'))
                else:
                    return redirect(url_for('login'))
            else:
                return redirect(url_for('newpassword'))


            # return render_template('newpassword.html')

    return render_template('newpassword.html')

@app.route('/answer', methods=['GET', 'POST'])   
def answer():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor2 = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    buscarRsp= conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    buscarRsp2= conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    usuario= conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    numpregunta=(random.randint(10, 14))
    numpregunta2=(random.randint(10, 14))
    # numpregunta=11
    # numpregunta2=10

    if numpregunta == numpregunta2:

        return render_template('index.html')
                
    else:
        cursor.execute("SELECT * FROM pregunta where id_pregunta=%s",[numpregunta])
        cursor2.execute("SELECT * FROM pregunta where id_pregunta=%s",[numpregunta2])

        account = cursor.fetchone()
        account2 = cursor2.fetchone()


        if request.method == 'POST' and 'rspPregunta1' and 'rspPregunta2' and 'cuenta':
            cuenta = request.form['cuenta']
            rspPregunta1 = request.form['rspPregunta1']
            rspPregunta2 = request.form['rspPregunta2']
            session['loggedin'] = True
            session['id'] = cuenta
            # usuario.execute('SELECT * FROM cuenta WHERE id_cuenta = %s', (cuenta,))
            # usuario = usuario.fetchone()


            buscarRsp.execute('select pc."id_pregCuenta",pc.id_cuenta,p.id_pregunta,pc.res_pregunta from "pregCuenta" pc,pregunta p where p.id_pregunta=pc.id_pregunta and pc.id_cuenta=%s and p.id_pregunta=%s',(cuenta,account['id_pregunta']))
            accountBus = buscarRsp.fetchone()
            buscarRsp2.execute('select pc."id_pregCuenta",pc.id_cuenta,p.id_pregunta,pc.res_pregunta from "pregCuenta" pc,pregunta p where p.id_pregunta=pc.id_pregunta and pc.id_cuenta=%s and p.id_pregunta=%s',(cuenta,account2['id_pregunta']))
            accountBus2 = buscarRsp2.fetchone()

            if accountBus:
                if ((accountBus['res_pregunta'])==rspPregunta1 and (accountBus2['res_pregunta'])==rspPregunta2 and (accountBus2['id_cuenta'])==cuenta):
                    return render_template('newpassword.html')
                else:
                    return render_template('answer.html',account=account,account2=account2)
            else:
                return render_template('index.html')
        else:
            return render_template('answer.html',account=account,account2=account2)


        return render_template('answer.html',account=account,account2=account2)









    # return render_template('answer.html')


if __name__=='__main__':
    app.run(debug=True, port=2000)