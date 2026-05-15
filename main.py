from sqlalchemy import create_engine,text
from dotenv import load_dotenv
import os

# Cargar .env
load_dotenv()

# Leer URL completa que se encuentra en el .env
database_url = os.getenv("DATABASE_URL")

try:
    # Crear conexión con DBeaver 
    engine = create_engine(database_url)

    # Probar la conexión, si no hay error, se muestra el mensaje de conexión exitosa
    with engine.connect() as conn:
        print("Conexión exitosa")

# Si hay un error, se muestra el mensaje de error.
except Exception as e:
    print("Error")
    print(e)
