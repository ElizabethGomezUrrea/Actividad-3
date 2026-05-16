# Proyecto Faker + SQLAlchemy + DBeaver

## Descripción

Este proyecto tiene como finalidad crear una tabla en una base de datos MySQL utilizando el SQLAlchemy para, posteriormente, insertar 100,000 registros falsos generados automáticamente con la librería Faker.

Para el desarrollo del proyecto se utilizó:
- **Python**: Como lenguaje de programación base.
- **SQLAlchemy**: Para la gestión y conexión con la base de datos mediante código Python.
- **Faker**: Para la creación de datos ficticios realistas.
- **MySQL**: Como el sistema de gestión de bases de datos relacionales.
- **DBeaver**: Como herramienta de interfaz gráfica para administrar y verificar la base de datos.
- **Git y GitHub**: Para el control de versiones y el trabajo colaborativo.

---

# 1. Configuración Inicial y Conexión a GitHub

En una primera instancia, iniciamos el repositorio local con Git y nos conectamos con el repositorio remoto en GitHub. Tras esto, se crean los archivos principales y se realiza el primer commit denominado 'Configuración inicial', el cual contiene la estructura base del proyecto:

```text
.env
.env.example
main.py
.gitignore
```
En el archivo .env se almacena la información personal y las credenciales necesarias para crear la conexión con MySQL desde Python. Por razones de seguridad, este archivo no se debe subir a GitHub.

Para solucionar esto, se crea el archivo .env.example. El objetivo de este archivo es mostrar únicamente la estructura de la cadena de conexión sin exponer las contraseñas reales. La estructura configurada es:
```text
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/database_name
```
Por otro lado, configuramos el archivo .gitignore para indicarle a Git de forma explícita qué archivos y carpetas debe ignorar por completo, evitando subir basura al repositorio o filtrar datos privados.

Los archivos ignorados fueron:

```text
.env
venv/
.venv/
__pycache__/
*.pyc
node_modules/
*.pptx
```
# 2. Conexión con DBeaver
Con la estructura base lista, comenzamos la construcción del archivo main.py, el cual tendrá toda la lógica de ejecución del proyecto.

Primero, importamos las librerías necesarias para interactuar con el sistema operativo, manejar las variables de entorno y establecer la comunicación con la base de datos:
```text 
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
```
Posteriormente, cargamos las variables del archivo .env utilizando:
```text 
load_dotenv()
```
Después de esto, recuperamos de forma segura la URL de conexión que guardamos previamente en el entorno a través de:
```text 
database_url = os.getenv("DATABASE_URL")
```
La conexión técnica con MySQL se gestiona mediante SQLAlchemy utilizando el "engine" (motor de conexión):
```text
engine = create_engine(database_url)
```
Finalmente, abrimos un bloque de conexión seguro para probar que DBeaver y MySQL estén conectando correctamente nuestro script:
```text 
with engine.connect() as conn:
```
Si la conexión es exitosa, la consola nos mostrará el mensaje Conexión exitosa. En caso de que surja algún problema (como credenciales erróneas o el servidor apagado), controlamos la situación capturando el error mediante un bloque try y except.

# 3. Creación de Tabla
Para asegurar la integridad de la rama principal (main) creamos una rama secundaria llamada Tabla. Dentro de esta rama, definimos la función que se encargará de estructurar la base de datos:
```text 
def crear_tabla(conn):
```
Esta función recibe la conexión activa con MySQL para poder ejecutar comandos directamente desde Python.

Dentro de la función se define la variable query, la cual contiene toda la sentencia SQL pura necesaria para crear la tabla:
```text
CREATE TABLE IF NOT EXISTS personas_elizabeth
```
La tabla se diseñó con los siguientes campos para cubrir un perfil de usuario completo:

- id (Clave primaria auto_incremental)
- nombre_completo
- fecha_nacimiento
- correo_electronico
- telefono
- ciudad
- direccion
- estado_civil
- ocupacion

Para pasar esta consulta de Python a la base de datos, ejecutamos:
```text 
conn.execute(text(query))
```
La función text() nos permite escribir consultas SQL tal y como lo haríamos en DBeaver, pero de forma segura dentro del código.

Después, utilizamos:
```text 
conn.commit()
```
Esto para aplicar y guardar cambios realizados en el estado de la base de datos. Una vez declarada la función, la llamamos dentro de nuestra función principal main:
```text 
crear_tabla(conn)
```
- Flujo de Git para esta sección:
Al terminar la funcionalidad, guardamos los cambios localmente con un commit. Subimos la rama Tabla a GitHub y, para unificar el código, primero realizamos el merge de forma visual dentro de la plataforma de GitHub. Una vez combinado a la rama principal en la nube, regresamos a nuestra terminal local, nos cambiamos a la rama main y ejecutamos un git pull para actualizar nuestro entorno de trabajo local con los cambios ya unificados.

# 4. Generación de Datos Falsos
Para avanzar con la simulación de datos, creamos una nueva rama llamada Datos_falsos. Aquí instalamos la librería Faker, la cual es la pieza central que ayudará a generar de manera automatizada los 100,000 registros falsos.

Primero, creamos una instancia de Faker configurada específicamente en idioma español para que las ciudades, nombres y direcciones tengan sentido en nuestro contexto:
```text 
fake = Faker("es_ES")
```
Luego, definimos una variable llamada rows. Esta variable es una lista que utiliza un ciclo de comprensión (for _ in range(100000)) para generar en segundos los 100,000 diccionarios con datos únicos y variados gracias a las funciones internas de Faker:
```text 
rows = [
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
```
Para asegurar que cualquier otra persona pueda replicar este entorno virtual exactamente, se exporta todas las dependencias del proyecto ejecutando en la consola:
```text 
pip freeze > requirements.txt
```
El archivo requirements.txt resultante quedó de la siguiente manera:
```text 
dotenv==0.9.9
Faker==40.18.0
greenlet==3.5.0
PyMySQL==1.1.3
python-dotenv==1.2.2
SQLAlchemy==2.0.49
typing_extensions==4.15.0
tzdata==2026.2
```
- Flujo de Git para esta sección:
Al verificar que todo funcionaba bien, guardamos con un commit y subimos la rama Datos_falsos a GitHub. Repitiendo las buenas prácticas, primero entramos a GitHub para realizar el merge hacia la rama principal. Acto seguido, en nuestra terminal local nos posicionamos en la rama principal y ejecutamos:
```text 
git pull origin main
```
Con esto, traemos los nuevos cambios de la nube.

# 5. Inserción Masiva de Datos
Para la última etapa, creamos la rama llamada Inserción. Aquí definimos la siguiente función:
```text 
def insertar_datos(conn, rows):
```
Esta función se encarga de recibir la conexión activa de MySQL y la lista de 100,000 registros que creamos en el paso anterior.

Dentro de la función preparamos la estructura de inserción:
```text 
INSERT INTO personas_elizabeth
```
Para este proceso utilizamos SQLAlchemy para realizar una inserción masiva pasando la consulta y la lista completa de golpe mediante:
```text 
conn.execute(query, rows)
```
Esto hace que SQLAlchemy procese todos los registros de forma interna optimizando la comunicación con el servidor de bases de datos.

Luego, confirmamos la transacción: 
```text 
conn.commit()
```
Para ejecutar esto, simplemente llamamos a la función dentro del bloque main:
```text 
insertar_datos(conn, rows)
```
Por último, abrimos DBeaver y ejecutamos una consulta de control para verificar que, en efecto, los datos estuvieran completos en la tabla
```text 
SELECT COUNT(*) FROM personas_elizabeth;
```
La consulta nos retornó exitosamente el número 100000, confirmando que la inserción masiva fue un éxito total.

- Flujo de Git para esta sección:
Hicimos el último commit local de la funcionalidad, subimos la rama Inserción a GitHub, realizamos el merge final desde la interfaz web de GitHub y concluimos haciendo un git pull origin main en nuestra terminal local en la rama main para dar por cerrado el ciclo de desarrollo.

# Resultado Final
- Al concluir el proyecto, logramos un sistema automatizado capaz de:

- Conectarse de forma segura y encriptada a bases de datos a través de variables de entorno.

- Crear automáticamente la estructura de tablas necesarias en MySQL desde Python.

- Generar masivamente 100,000 registros únicos, realistas y adaptados al idioma español utilizando Faker.

- Insertar grandes volúmenes de información eficientemente en pocos segundos.

- Llevar una gestión organizada del proyecto utilizando un flujo limpio de Git basado en ramas, commits descriptivos, integraciones en GitHub (merges) y sincronizaciones locales (pulls).




