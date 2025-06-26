# Imagen base oficial de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para PDF, Pillow, PostgreSQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libpq-dev \
    python3-cairocffi \
    fonts-liberation \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar el código del proyecto
COPY . /app/

# Instalar dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput

# Expone el puerto (si usas gunicorn)
EXPOSE 8000

# Comando para iniciar la app en producción
CMD ["gunicorn", "matematicas.wsgi:application", "--bind", "0.0.0.0:8000"]
