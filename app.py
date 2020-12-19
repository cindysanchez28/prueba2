
import os 
import time
from datetime import datetime
from flask import Flask, request,render_template,redirect,url_for,session,flash,jsonify,send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.datastructures import  FileStorage
from werkzeug.utils import secure_filename
import yagmail
from OpenSSL.crypto import FILETYPE_PEM
app = Flask(__name__)
app.secret_key = 'dsadwe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
app.config['UPLOAD_FOLDER'] = './static/imagenes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from modelos import Usuarios,Imagenes
import utils


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
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    nombreUsuario = request.form['nombreUsuario']
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    fecha = request.form['fecha']
    
    
    if not utils.formValid( nombre ):
        return jsonify({'error': '3'})
    if not utils.formValid( apellido ):
        return jsonify({'error': '4'})
    if not utils.formValid( nombreUsuario ):
        return jsonify({'error': '5'})
    if not utils.isEmailValid( correo ):
        return jsonify({'error': '6'})
    if not utils.formValid( contraseña ):
        return jsonify({'error': '7'})
    if not utils.formValid( fecha ):
        return jsonify({'error': '8'})


        
    u = Usuarios.query.filter_by(nombreUsuario=request.form["nombreUsuario"]).first()
    if u != None:
        return jsonify({'error': '1'}) 
    else:
        u = Usuarios.query.filter_by(correo=request.form["correo"]).first()
        if u != None:
            return jsonify({'error': '2'})
        else:
            contraseña_cifrada = generate_password_hash(request.form['contraseña'])
            usuarios = Usuarios(nombre=request.form['nombre'],apellido=request.form['apellido'],correo=request.form['correo'],contraseña=contraseña_cifrada,fecha=request.form['fecha'],nombreUsuario=request.form['nombreUsuario'], imgPerfil="img/perfil_defecto.jpg")
            db.session.add(usuarios)
            db.session.commit() 
            #correoValidacion(usuarios.correo)

            return jsonify({'creado': 'usuario creado'})

#-------------------------------------------------------------------- 

@app.route('/login',methods=['POST'])
def login():  
    """ Se encarga de crear la sessiones si existe el usuario.

        .Verfica que el correo y la contraseña coincidan,
        si coinciden envia un mensaje de 'correcto', si no
        envia un mensaje de error.
    """
    
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    
    if not utils.isEmailValid( correo ):
        return jsonify({'error': '3'})
    else :
        usuario = Usuarios.query.filter_by(correo=request.form["correo"]).first()
    
        if usuario != None:
            if  check_password_hash(usuario.contraseña,request.form['contraseña']):
                session['id'] = usuario.id
                session['nombreUsuario'] = usuario.nombreUsuario
                session['correo'] = usuario.correo
                return jsonify({'correcto': 'correcto'})
            else:
                return jsonify({'error': '2'})
        else:  
        
            return jsonify({'error': '1'})
   
#-------------------------------------------------------------------- 

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    """
         muestra el dashboard cuando el usuario esta logeado

    """
    busqueda = request.args.get("buscar")

    if 'nombreUsuario' in session:         
        usuario = Usuarios.query.filter_by(nombreUsuario=session["nombreUsuario"]).first()
        print(usuario)
        if busqueda == None or busqueda == "" :
            print("entro")
            imagenes = Imagenes.query.filter_by(publico=True)
            return render_template('dashboard.html',imagenes = imagenes,  usuario = usuario)
        else:
            imagenes = BuscarImagenesDashboard(busqueda)               
            return render_template('dashboard.html',imagenes = imagenes, usuario = usuario)
            
            
        
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
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        estado = request.form['estado']
        idImagen = request.form['idImagen']
        direccion = request.form['direccion']
       
        
        publico = True
        now = datetime.now()

    
        if estado == 'publica':
                publico = True
        else :
            publico = False
        
        imagen = db.session.query(Imagenes).filter_by(id = idImagen).first()
        imagen.nombre = nombre
        imagen.descripcion = descripcion
        imagen.publico = publico
        
        if filename != "":

            lista = filename.split(".")
            extension = lista[1]
            segundos = time.time();
            milisegundos = str(segundos * 1000 )
            filename =  milisegundos + '.' + extension
            url = "imagenes/"+ filename
            imagen.url = url
            # Guardamos el archivo en el directorio "Archivos PDF"
            fl.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_eliminar = "./static/" +  direccion;
            
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

@app.route('/configuracion')
def configuracion():
    usuario = Usuarios.query.filter_by(nombreUsuario=session["nombreUsuario"]).first()
    print(usuario)
    if 'correo' in session: 
        return render_template('configuracion.html', usuario=usuario)

    else:
        return redirect(url_for('index'))
 #-------------------------------------------------------------------- 
    
@app.route('/updateConfiguracion', methods=['POST'] )
def updateConfiguracion():
    usuario = Usuarios.query.filter_by(nombreUsuario=session["nombreUsuario"]).first()
    if 'correo' in session: 
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha = request.form['fecha']
        usuario.nombre = nombre
        usuario.apellido = apellido
        usuario.fecha = fecha
        
        db.session.commit()
        
        return redirect(url_for('configuracion'))
   
    else:
        return redirect(url_for('index'))    
    
    

#--------------------------------------------------------------------

@app.route('/uploadImagePerfil',methods=['POST'] )
def uploadImagePerfil():
    
    """ 
        Actualiza imagen de perfil del usuario
    """
    if request.method == 'POST':
        
        usuario = Usuarios.query.filter_by(nombreUsuario=session["nombreUsuario"]).first()
        
        fl = request.files['imagenPerfil']
        filename = secure_filename(fl.filename)
        lista = filename.split(".")
        extension = lista[1]
        
        segundos = time.time();
        milisegundos = str(segundos * 1000 )
        filename =  milisegundos + '.' + extension
        url = "imagenes/"+ filename
        
        fl.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        if usuario.imgPerfil == "img/perfil_defecto.jpg" :
            pass
        else :
            image_eliminar = "./static/"+usuario.imgPerfil;
            os.remove(image_eliminar)
        

        usuario.imgPerfil = url
 
        
        #eliminado imagen antigua del directorio
        
        
        db.session.commit()
    
    return redirect(url_for('configuracion'))   
    
#--------------------------------------------------------------------
@app.route('/deleteImage',methods=['POST'] )
def deleteImage():
    
    """ 
        Delete imagenes del usuario
    """
    if request.method == 'POST':
 
        id = request.form["id"]
        id_usuario = session["id"]
        imagen = Imagenes.query.filter_by(id=id).first()

        if imagen.id_usuario == id_usuario:
            db.session.delete(imagen)
            db.session.commit()
            os.remove("./static/" + imagen.url)

            return jsonify({'mensaje':'correcto'})

        
    else:
        return redirect(url_for('index'))
#-------------------------------------------------------------------- 

@app.route('/CorreoRecuperar',methods=['POST'])
def correoRecuperacion():
    """ 
        Envia Correo de recuperacion
    """
    usuario = Usuarios.query.filter_by(correo=request.form["recuperarcorreo"]).first()
    if usuario != None:
        email=request.form["recuperarcorreo"]
        token = usuario.get_reset_token()
        contenido = render_template('emailRecuperar.html', nombre = usuario.nombreUsuario, token=token )
        yag = yagmail.SMTP('redvisionmisiontic@gmail.com', 'Grupo11B') 
        yag.send(to=email, subject="Recuperar contraseña",contents=contenido)
        return redirect(url_for('index'))
    else:  
        print('error')        
        return jsonify({'error': '1'})

#-------------------------------------------------------------------- 

@app.route('/CorreoValidar/',methods=['POST'])
def correoValidacion():
    """ 
        Envia Correo de validacion del usuario

    """
    usuario = Usuarios.query.filter_by(correo=email).first()
    contenido = render_template('correoActivacion.html', nombre = usuario.nombreUsuario )
    yag = yagmail.SMTP('redvisionmisiontic@gmail.com', 'Grupo11B') 
    yag.send(to=email, subject='Confirmación de activación de cuenta',contents=contenido)
    usuario.activo = True
    db.session.commit()

#-------------------------------------------------------------------- 

@app.route('/recuperar/<token>', methods=['GET','POST'])
def cambiarContraseña():
    """ 
        Muestra template para cambiar contraseña

    """
    return render_template('recuperacion.html')

#-------------------------------------------------------------------- 

@app.route('/cambiocontraseña/')
def envioContraseña():
    """ 
        Guarda la nueva contraseña

    """
    return ''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80  )










