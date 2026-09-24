# Django

## Crear un proyecto

    mkdir src
    cd src
    django-admin startproject config .

## Comprobar posibles problemas en el proyecto

    python manage.py check

## Ejecutar el servidor

    python manage.py runserver

## Crear una aplicación

    python manage.py startapp core

## Preparar archivos de migración

    python manage.py makemigrations

## Aplicar migraciones a la base de datos

    python manage.py migrate

## Crear superusuario

    python manage.py createsuperuser

## Shell interactivo con las configuraciones de Django

    python manage.py shell

## Ejecutar pruebas automáticas

    python manage.py test

## Recopilar archivos estáticos

    python manage.py collectstatic
