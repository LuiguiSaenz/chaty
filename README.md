# chaty
# CREAR ENTORNO VIRTUAL
virtualenv env

# ACTIVAMOS EL ENTORNO VIRTUAL
env\Scripts\activate

# INSTALAMOS DEPENDENCIAS
cd pruebaluigui
pip install -r requirements.txt

# LEVANTAMOS EL PROYECTO
python manage.py runserver 8080
