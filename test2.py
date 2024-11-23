#import psycopg2
#from psycopg2 import sql

# Configuración de conexión
#host = "dbpostgres.ciqouinz0rvh.us-east-1.rds.amazonaws.com"
#port = "5432"  # El puerto predeterminado para PostgreSQL
#database = "postgres"  # Sustituye con el nombre de tu base de datos si es diferente
#user = "root"
#password = "root1234"

#try:
    # Crear la conexión
 #   connection = psycopg2.connect(
  #      host=host,
   #     port=port,
    #    database=database,
     #   user=user,
      #  password=password
    #)
    #print("Conexión exitosa a PostgreSQL")

    # Crear un cursor para ejecutar consultas
    #cursor = connection.cursor()

    # Ejecutar una consulta de prueba
  #  cursor.execute("SELECT version();")
   # db_version = cursor.fetchone()
    #print("Versión de la base de datos:", db_version)

    # Cerrar el cursor
 #   cursor.close()

#except Exception as error:
 #   print("Error al conectar a la base de datos:", error)

#finally:
    # Cerrar la conexión
 #   if connection:
  #      connection.close()
   #     print("Conexión cerrada")
