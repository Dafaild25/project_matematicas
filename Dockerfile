# Imagen base ligera de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema para WeasyPrint, PostgreSQL, Pillow, etc.
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
    libcairo2 \
    pango1.0-tools \
    fonts-liberation \
    fonts-dejavu \
    libfreetype6 \
    libharfbuzz-dev \
    libfribidi-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos del proyecto
COPY . /app/

# Instalar dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Recopilar archivos estáticos de Django
RUN python manage.py collectstatic --noinput

# Exponer el puerto en Railway
EXPOSE 8000

# Comando para ejecutar Gunicorn como servidor de producción
CMD ["gunicorn", "matematicas.wsgi:application", "--bind", "0.0.0.0:8000"]
