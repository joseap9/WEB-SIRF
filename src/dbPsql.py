import psycopg2
import requests
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name = "ddaykte02",
    api_key = "872276631135446",
    api_secret= "NI9-RTc2xPqBnZHoCRnFbW26MUk"
)

conn = psycopg2.connect(
  host="localhost",
  database="face_detector_system",
  user="postgres",
  password="Japa1998")

# Automatically commit transactions
conn.set_session(autocommit=True)

# Create a cursor object
cur = conn.cursor()

#retorna la longitud de una tabla
def lenn():
    cur.execute('SELECT count(*) FROM alumnos;')

    len = str(cur.fetchone())
    len = len.replace("(","").replace(",","").replace(")","")


    return int(len)


#retorna diccionario de columna de una tabla
def get_nombres():
    # Run a query
    cur.execute("SELECT nombre |" "| apellido,imagen FROM alumnos;")

    # Get all the rows for that query
    items = cur.fetchall()
    # Convert the result into a list of dictionaries (useful later)
    return [
    {'nombre_completo': item[0], 'imagen': item[1]}
    for item in items
    ]

#esta funcion sube una imagen local a claudinary y retorna el url de la misma, necesita como parametro la imagen local
#y el id el cual debe ser unico por ende se selecciona la longitud de la tabla de la base de datos y se le suma 1
def subir_imagen_clodinary(imagen, id):

    public_id = id + 1
    cloudinary.uploader.upload(imagen,public_id = public_id)

    data = cloudinary.api.resource(str(public_id))

    url = data['secure_url']

    return url

#metodo para crear usuario y registrarlo en postgres
def crear_usuario(usuario):

    imagen = subir_imagen_clodinary(usuario[-1],lenn())

    sql = f"""INSERT INTO alumnos (id_alumno,nombre,apellido,imagen) VALUES('{usuario[0]}','{usuario[1]}','{usuario[2]}','{imagen}')  """

    cur.execute(sql)

user = (lenn()+1,'Silvia','Gonzalez','silvia.jpg')

#crear_usuario(user)





