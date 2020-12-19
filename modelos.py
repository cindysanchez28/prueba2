from app import db
#-------------------------------------------------------------------- 
class Usuarios(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    nombre = db.Column(db.String())
    apellido = db.Column(db.String())
    nombreUsuario = db.Column(db.String())
    correo = db.Column(db.String())
    contraseña = db.Column(db.String())
    fecha = db.Column(db.String())
    activo = db.Column(db.Boolean())


class Imagenes(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    id_usuario = db.Column(db.Integer())
    nombre = db.Column(db.String())
    descripcion = db.Column(db.String())
    url = db.Column(db.String())
    publico = db.Column(db.Boolean())
    fecha = db.Column(db.String())