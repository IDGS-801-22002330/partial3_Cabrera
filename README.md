Este proyecto es una aplicación web desarrollada con Flask para gestionar pedidos de pizzas y consultar ventas. Utiliza Flask-Login para la autenticación y manejo de sesiones, Flask-SQLAlchemy para la persistencia de datos en la base de datos, y Tailwind CSS junto con Flowbite para un mejor diseño.

*===========!! REQUISITOS !!===========*

blinker==1.7.0
click==8.1.7
colorama==0.4.6
dnspython==2.5.0
email-validator==2.1.0.post1
Flask==3.0.1
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.1
greenlet==3.0.3
idna==3.6
itsdangerous==2.1.2
Jinja2==3.1.3
MarkupSafe==2.1.4
PyMySQL==1.1.0
SQLAlchemy==2.0.27
typing_extensions==4.9.0
Werkzeug==3.0.1
WTForms==3.1.2

*===========!! INSTALACION !!===========*

1. Clonar el repositorio: git clone https://github.com/IDGS-801-22002330/partial3_Cabrera cd *tu_proyecto*

Crear y activar un entorno virtual (opcional, pero recomendado) en Windows: python -m venv venv venv\Scripts\activate

Instalar las dependencias: pip install -r requirements.txt

Configurar la base de datos: El proyecto utiliza mySQL. La URI de la base de datos se puede configurar en el archivo de configuración (config.py o directamente en app.py).

Ejecutar la aplicación: python app.py La aplicación se ejecutará en http://localhost:3000 (o el puerto configurado).

*===========!! TAILWIND Y FLOWBITE !!===========*

El proyecto utiliza Tailwind CSS y Flowbite vía CDN para estilizar la interfaz. En el archivo layout.html se incluyen los siguientes enlaces:

En la sección <head>:

Tailwind CSS: https://cdn.jsdelivr.net/npm/tailwindcss@2.0.3/dist/tailwind.min.css

Flowbite CSS: https://cdn.jsdelivr.net/npm/flowbite@1.4.4/dist/flowbite.min.css

Antes del cierre de la etiqueta </body>:

Flowbite JS: https://cdn.jsdelivr.net/npm/flowbite@1.4.4/dist/flowbite.min.js

