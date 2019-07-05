# chaty
# CREAR ENTORNO VIRTUAL
virtualenv env

# ACTIVAMOS EL ENTORNO VIRTUAL
En windows:
env\Scripts\activate

En ubuntu:
source env/bin/activate

# INSTALAMOS DEPENDENCIAS
cd pruebaluigui
pip install -r requirements.txt

# LEVANTAMOS EL PROYECTO
python manage.py runserver 8080

# LINK DEL DEMO


http://18.218.14.83/
