from wtforms import Form, validators, BooleanField, StringField, DateField, SelectField, IntegerField, RadioField, SubmitField
from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms.validators import DataRequired
from wtforms.validators import DataRequired, Email, Length


class PizzaForm(Form):

    tamano = SelectField("Tamaño", choices=[('Chica', 'Chica ($50)'), ('Mediana', 'Mediana ($70)'), ('Grande', 'Grande ($120)')], 
                         validators=[validators.DataRequired(message='Selecciona un tamaño')])
    jamon = BooleanField("Jamón")
    pina = BooleanField("Piña")
    champi = BooleanField("Champiñones")
    numero_pizzas = IntegerField("Cantidad", validators=[
        validators.DataRequired(message='Campo requerido'),
        validators.NumberRange(min=1, max=20)
    ])

    nombre = StringField("Nombre Completo", [
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=4, max=100)
    ])
    direccion = StringField("Dirección", [
        validators.DataRequired(message='Campo requerido')
    ])
    telefono = StringField("Teléfono", [
        validators.DataRequired(message='Campo requerido'),
        validators.Length(min=10, max=15)
    ])
    fecha = DateField("Fecha", format='%Y-%m-%d',
        validators=[ validators.DataRequired(message='Selecciona una fecha') ])

    btn_agregar = SubmitField("Agregar")
    btn_quitar = SubmitField("Quitar")
    btn_terminar = SubmitField("Terminar")

class ConsultaVentasForm(FlaskForm):
    tipo_busqueda = RadioField("Tipo de reporte", choices=[('dia', 'Día'), ('mes', 'Mes')], 
                                 validators=[validators.DataRequired(message='Selecciona un tipo')])
    fecha_busqueda = DateField("Fecha", format='%Y-%m-%d', validators=[
        validators.DataRequired(message='Selecciona una fecha')
    ])
    btn_buscar = SubmitField("Buscar")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')
    
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Sign Up')