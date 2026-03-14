import firebase_admin #importar firebase_admin para usar la base de datos de firebase
from firebase_admin import credentials, db #importar credentials y db para autenticar y acceder a la base de datos de firebase
from dotenv import load_dotenv #importar load_dotenv para cargar las variables de entorno desde un archivo .env
import os #importar os para acceder a las variables de entorno del sistema operativo

load_dotenv()

def init_firebase():
    cred = credentials.Certificate("serviceAccountKey.json") #cargar las credenciales de firebase desde un archivo JSON que contiene la clave de servicio
    firebase_admin.initialize_app(cred, { #inicializar la aplicación de firebase con las credenciales y la URL de la base de datos
        'databaseURL': os.getenv('DATABASE_URL')
    })
    return db.reference('/') #devolver una referencia a la raíz de la base de datos para poder acceder a los datos

database = init_firebase() #inicializar la conexión a la base de datos de firebase y almacenar la referencia en la variable database para usarla en otras partes del código