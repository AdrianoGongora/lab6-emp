import dask.dataframe as dd
import pandas as pd
from sqlalchemy import create_engine

# Configuración de conexión
server = 'host.docker.internal'
database = 'MovieLens'  # Cambia según tu base de datos
username = 'SA'
password = 'mssql1Ipw'
connection_string = (
    f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
)

# Crear el motor de SQLAlchemy
engine = create_engine(connection_string)

# Establecer la conexión
try:
    with engine.connect() as conn:
        print("Conexión exitosa a la base de datos")

        # Leer los datos de la tabla 'ratings' de SQL Server a un DataFrame de Pandas
        query = "SELECT * FROM ratings"
        ratings_df = pd.read_sql(query, conn)

        # Convertir el DataFrame de Pandas a un DataFrame de Dask
        ratings_ddf = dd.from_pandas(ratings_df, npartitions=4)

        # Realizar alguna operación de Dask: Promedio de calificaciones por película
        average_ratings = ratings_ddf.groupby("MovieID").Rating.mean().compute()

        # Mostrar el resultado
        print(average_ratings)

except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
