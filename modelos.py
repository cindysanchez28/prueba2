from app import db, app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
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
    imgPerfil = db.Column(db.String())

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.secret_key, expires_sec)
        return s.dumps({'usuario_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.secret_key)
        try:
            usuario_id = s.loads(token)['usuario_id']
        except:
            return None
        return Usuarios.query.get(usuario_id)


class Imagenes(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    id_usuario = db.Column(db.Integer())
    nombre = db.Column(db.String())
    descripcion = db.Column(db.String())
    url = db.Column(db.String())
    publico = db.Column(db.Boolean())
    fecha = db.Column(db.String())