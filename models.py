from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class Venta(db.Model):
    __tablename__ = 'venta'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(50))
    fecha_pedido = db.Column(db.Date)
    total = db.Column(db.Float)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

class User(db.Model, UserMixin):  # Asegúrate de heredar de db.Model
    __tablename__ = 'user'  # (si lo deseas) Definir el nombre de la tabla

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.email}>'

# Función para obtener el usuario desde la base de datos
def get_user(email):
    return User.query.filter_by(email=email).first()