# Imagen base ligera de Python
FROM python:3.11-slim

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=matematicas.settings

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
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

# Copiar requirements primero para aprovechar el cache de Docker
COPY requirements.txt /app/

# Instalar dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar el resto del código
COPY . /app/

# Crear directorio para archivos estáticos
RUN mkdir -p /app/staticfiles

# Recopilar archivos estáticos de Django
RUN python manage.py collectstatic --noinput

# NO ejecutar migrate en el Dockerfile - hazlo en Railway como comando separado

# Crear un usuario no-root para seguridad
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Railway asigna el puerto dinámicamente
EXPOSE $PORT

# Comando para ejecutar Gunicorn con puerto dinámico
CMD ["sh", "-c", "gunicorn matematicas.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120"]