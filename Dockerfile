# Usar una imagen base de Python
FROM python:3.9-slim

# Instalar dependencias necesarias
USER root
RUN apt-get update && \
    apt-get install -y curl gnupg2 unixodbc-dev gcc g++ build-essential && \
    apt-get install -y apt-transport-https && \
    apt-get clean

# Instalar los drivers ODBC de Microsoft para SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Instalar Dask, SQLAlchemy, pyodbc y otras dependencias
RUN pip install dask[distributed] sqlalchemy pyodbc pandas

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el script de Dask en el contenedor
COPY script.py /app/

# Comando para ejecutar el script
CMD ["python", "/app/script.py"]
