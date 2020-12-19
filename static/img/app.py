
import os 
import time
from datetime import datetime
from flask import Flask, request,render_template,redirect,url_for,session,flash,jsonify,send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.datastructures import  FileStorage
from werkzeug.utils import secure_filename
import yagmail
app = Flask(__name__)
app.secret_key = 'dsadwe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
app.config['UPLOAD_FOLDER'] = './static/imagenes'
db = SQLAlchemy(app)
from modelos import Usuarios,Imagenes



#-------------------------------------------------------------------- 

@app.route('/')
def index():
    """Funcion principal muestra index.html

       Contiene los formularios de registro y login.
    """ 
    if 'nombreUsuario' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html')

#-------------------------------------------------------------------- 

@app.route('/crearusuario',methods=['POST'] )
def create():
    
    """ Se encarga de crear la sessiones si existe el usuario.

        .Verfica que el correo y la contraseña coincidan,
        si coinciden envia un mensaje de 'correcto', si no
        envia un mensaje de error.
    """
    
  
    u = Usuarios.query.filter_by(nombreUsuario=request.form["nombreUsuario"]).first()
    if u != None:
        return jsonify({'error': '1'}) 
    else:
        u = Usuarios.query.filter_by(correo=request.form["correo"]).first()
        if u != None:
            return jsonify({'error': '2'})
        else:
            contraseña_cifrada = generate_password_hash(request.form['contraseña'])
            usuarios = Usuarios(nombre=request.form['nombre'],apellido=request.form['apellido'],correo=request.form['correo'],contraseña=contraseña_cifrada,fecha=request.form['fecha'],nombreUsuario=request.form['nombreUsuario'])
            db.session.add(usuarios)
            db.session.commit() 
            return jsonify({'creado': 'usuario creado'})
    
#-------------------------------------------------------------------- 

@app.route('/login',methods=['POST'])
def login():  
    """ Se encarga de crear la sessiones si existe el usuario.

        .Verfica que el correo y la contraseña coincidan,
        si coinciden envia un mensaje de 'correcto', si no
        envia un mensaje de error.
    """
    
    usuario = Usuarios.query.filter_by(correo=request.form["correo"]).first()
    print(usuario.correo)
    print(usuario != None)
    if usuario != None:
        if  check_password_hash(usuario.contraseña,request.form['contraseña']):
            session['id'] = usuario.id
            session['nombreUsuario'] = usuario.nombreUsuario
            session['correo'] = usuario.correo
            
            print('usuario correcto')
            return jsonify({'correcto': 'correcto'})
        else:
            return jsonify({'error': '2'})
    else:  
        print('error')        
        return jsonify({'error': '1'})
   
#-------------------------------------------------------------------- 

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    """
         muestra el dashboard cuando el usuario esta logeado

    """
    busqueda = request.args.get("buscar")

    if 'nombreUsuario' in session:         
        if busqueda == None or busqueda == "" :
            imagenes = Imagenes.query.filter_by(id_usuario=session["id"]).filter_by(publico=1)
            return render_template('dashboard.html',imagenes = imagenes)
        else:
            imagenes = BuscarImagenesDashboard(busqueda)

                
            return render_template('dashboard.html',imagenes = imagenes)
            
            
        
    else:
        return redirect(url_for('index'))

#-------------------------------------------------------------------- 

@app.route('/exit',methods=['GET'])
def exit():
    """ 
        Elimina la Session y redireciona a 'index'

    """
    session.clear()
    return redirect(url_for('index'))

#-------------------------------------------------------------------- 

@app.route('/uploadImg',methods=['POST'] )
def uploadImg():
    """ 
        Sube imagenes del usuario
    """
    if request.method == 'POST':
        # obtenemos el archivo del input "archivo"
        f = request.files['imagen']
        filename = secure_filename(f.filename)
        filename = "ejemploe2.jpg"
        lista = filename.split(".")
        extension = lista[1]
                
        segundos = time.time();
        milisegundos = str(segundos * 1000 )
        filename =  milisegundos + '.' + extension
        
        
        
        # Guardamos el archivo en el directorio "Archivos PDF"
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        
        #Obteniendo datos del formulario
        
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        estado = request.form['estado']
        id_usuario = session['id']
        url = "imagenes/"+ filename
        publico = True
        now = datetime.now()
        
        fecha = str(now.year )+ "-" + str(now.month) + "-" + str(now.day)
        
        
        if estado == 'publica':
            publico = True
        else :
            publico = False
            
        print(id_usuario, nombre,  descripcion, url,  publico, fecha)
        
        
        imagenes = Imagenes(id_usuario=id_usuario, nombre = nombre, descripcion = descripcion, url = url, publico = publico, fecha = fecha)
        
        db.session.add(imagenes)
        db.session.commit()
       
        
        # Retornamos una respuesta satisfactoria
        return redirect(url_for('perfil'))
     
#-------------------------------------------------------------------- 


@app.route('/updateImage',methods=['POST'] )
def updateImage():
    
    """ 
        Actualiza imagenes del usuario
    """
    if request.method == 'POST':
        fl = request.files['nuevaImagen']
        filename = secure_filename(fl.filename)
        lista = filename.split(".")
        extension = lista[1]
        
        segundos = time.time();
        milisegundos = str(segundos * 1000 )
        filename =  milisegundos + '.' + extension
        
        
        # Guardamos el archivo en el directorio "Archivos PDF"
        fl.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        estado = request.form['estado']
        idImagen = request.form['idImagen']
        direccion = request.form['direccion']
        url = "imagenes/"+ filename
        publico = True
        now = datetime.now()
        image_eliminar = "./static/"+direccion;
        
        if estado == 'publica':
                publico = True
        else :
            publico = False
        
        imagen = db.session.query(Imagenes).filter_by(id = idImagen).first()
        imagen.nombre = nombre
        imagen.descripcion = descripcion
        imagen.publico = publico
        imagen.url = url
        
        #eliminado imagen antigua del directorio
        os.remove(image_eliminar)
        
        db.session.commit()
    
    return redirect(url_for('perfil'))


#-------------------------------------------------------------------- 



def BuscarImagenesDashboard(busqueda):
     
    
    imagenes = []
            #imagenes = Imagenes.query.filter_by(nombre=busqueda).filter_by(publico=1)
    img = Imagenes.query.filter_by(publico=1)
    claves = busqueda.split()
    for i in img:   
        encontrado = False            
        clavesNombre = i.nombre.split()
        for clave in claves: 
            if encontrado:
                continue 
            if clave in clavesNombre:
                imagenes.append(i)
                encontrado = True


    return imagenes

#-------------------------------------------------------------------- 


@app.route('/perfil/')
def perfil():
    """ 
        Muestra perfil del usuario

    """
    usuario = Usuarios.query.filter_by(nombreUsuario=session["nombreUsuario"]).first()
    if 'nombreUsuario' in session: 
        imagenes = Imagenes.query.filter_by(id_usuario=session["id"])
        npublicaciones = 0
        for i in imagenes:
            npublicaciones +=1
        return render_template('perfil.html',imagenes = imagenes,usuario=usuario,npublicaciones = npublicaciones)

    else:
        return redirect(url_for('index'))

#-------------------------------------------------------------------- 

@app.route('/configuracion/')
def configuracion():
    if 'correo' in session: 
        return render_template('configuracion.html')

    else:
        return redirect(url_for('index'))
#--------------------------------------------------------------------
@app.route('/deleteImage',methods=['POST'] )
def deleteImage():
    
    """ 
        Delete imagenes del usuario
    """
    if request.method == 'POST':
        print("entro")
        id = request.form["id"]
        id_usuario = session["id"]
        imagen = Imagenes.query.filter_by(id=id).first()
        print("elimino " + id)
        if imagen.id_usuario == id_usuario:
            db.session.delete(imagen)
            db.session.commit()
            os.remove("./static/" + imagen.url)
            print("elimino " + id)
            return jsonify({'mensaje':'correcto'})

        
    else:
        return redirect(url_for('index'))
#-------------------------------------------------------------------- 

@app.route('/CorreoRecuperar',methods=['POST'])
def correoRecuperacion():
    """ 
        Envia Correo de recuperacion
    """
    email=request.form["recuperarcorreo"]
    yag = yagmail.SMTP('redvisionmisiontic@gmail.com', 'Grupo11B') 
    yag.send(to=email, subject="Recuperar contraseña",contents="Usa este link para recuperar la constraseña")
    return redirect(url_for('index'))

#-------------------------------------------------------------------- 

@app.route('/CorreoValidar/',methods=['POST'])
def correoValidacion():
    """ 
        Envia Correo de validacion del usuario

    """
    return ''

#-------------------------------------------------------------------- 

@app.route('/recuperar/')
def cambiarContraseña():
    """ 
        Muestra template para cambiar contraseña

    """
    return render_template('configuracion.html')

#-------------------------------------------------------------------- 

@app.route('/cambiocontraseña/')
def envioContraseña():
    """ 
        Guarda la nueva contraseña

    """
    return ''











