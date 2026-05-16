from sqlalchemy import create_engine,text
from dotenv import load_dotenv
from faker import Faker
import os

#Función para crear la tabla personas_elizabeth 
# en la base de datos de DBeaver.

def crear_tabla(conn):

    query = """
    CREATE TABLE IF NOT EXISTS personas_elizabeth (

        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre_completo VARCHAR(100),
        fecha_nacimiento DATE,
        correo_electronico VARCHAR(100) UNIQUE,
        telefono VARCHAR(50) UNIQUE,
        ciudad VARCHAR(100),
        direccion VARCHAR(200),
        estado_civil VARCHAR(100),
        ocupacion VARCHAR(100)
        

    );
    """
    # Ejecutar la consulta SQL para crear la tabla.
    conn.execute(text(query))
    # Guardar los cambios en la base de datos.
    conn.commit()

# Función para insertar los datos falsos
# generados con Faker en la tabla.

def insertar_datos(conn, rows):

    query = text("""

        INSERT INTO personas_elizabeth (

            nombre_completo,
            fecha_nacimiento,
            correo_electronico,
            telefono,
            ciudad,
            direccion,
            estado_civil,
            ocupacion

        )

        VALUES (

            :nombre_completo,
            :fecha_nacimiento,
            :correo_electronico,
            :telefono,
            :ciudad,
            :direccion,
            :estado_civil,
            :ocupacion

        )

    """)

    # Insertar todos los registros de manera masiva.
    conn.execute(query, rows)
    
     # Guardar los cambios en la base de datos.
    conn.commit()

def main():
   # Cargar .env
    load_dotenv()

   # Leer URL completa que se encuentra en el .env
    database_url = os.getenv("DATABASE_URL")

    try:
       # Crear conexión con DBeaver 
       engine = create_engine(database_url)

       # Crear instancia de Faker
       fake = Faker("es_ES")

       # Generar datos falsos 
       rows =[
           {
                "nombre_completo": fake.name(),
                "fecha_nacimiento": fake.date_of_birth(),
                "correo_electronico": fake.unique.email(),
                "telefono": fake.unique.phone_number(),
                "ciudad": fake.city(),
                "direccion": fake.address(),
                "estado_civil": fake.random_element(elements=["Soltero", "Casado", "Divorciado", "Viudo"]),
                "ocupacion": fake.job()
           }

           for _ in range(100000)

       ]

       # Probar la conexión, si no hay error, se muestra el mensaje de conexión exitosa
       with engine.connect() as conn:
          
          print("Conexión exitosa")

           # Llamar la función para crear la tabla
          crear_tabla(conn)
          print("Tabla creada correctamente")

          # insertar datos
          insertar_datos(conn, rows)
          print("100000 registros insertados correctamente")

      # Por si hay un error en la conexión. 
    except Exception as e:
       print("Error")
       print(e)

# Ejecutar la función principal
if __name__ == "__main__":
    main()
