# Usamos una imagen ligera de Python
FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia todo el proyecto al contenedor
COPY . /app/

# Instala paquetes del sistema necesarios para generar PDFs, Pillow, etc.
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
    cairo \
    pango \
    && rm -rf /var/lib/apt/lists/*

# Crea un entorno virtual e instala dependencias
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Archivos estáticos (si es necesario)
RUN python manage.py collectstatic --noinput || true

# Expone el puerto que usará el contenedor
EXPOSE 8000

# Comando para ejecutar la app con Gunicorn
CMD ["gunicorn", "matematicas.wsgi:application", "--bind", "0.0.0.0:8000"]
