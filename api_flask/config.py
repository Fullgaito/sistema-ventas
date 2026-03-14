import firebase_admin #importamos la libreria de firebase_admin para poder inicializar la conexion con firebase
from firebase_admin import credentials, firestore #importamos credentials para autenticar la conexion y firestore para interactuar con la base de datos de firebase

def init_firebase():
    cred = credentials.Certificate("serviceAccountKey.json") #creamos una variable cred que contiene las credenciales de autenticacion para conectar con firebase, estas credenciales se encuentran en un archivo json llamado serviceAccountKey.json
    firebase_admin.initialize_app(cred) #inicializamos la aplicacion de firebase con las credenciales proporcionadas
    return firestore.client() #retornamos un cliente de firestore que nos permite interactuar con la base de datos de firebase

db = init_firebase()