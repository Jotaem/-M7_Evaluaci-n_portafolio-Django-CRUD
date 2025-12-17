# Portafolio Módulo 7 – Django CRUD con Base de Datos

## 📌 Descripción General
Este proyecto corresponde a la **Evaluación de Portafolio del Módulo 7**, cuyo objetivo es demostrar, de forma práctica y progresiva, el dominio de las competencias técnicas adquiridas durante el curso, especialmente aquellas relacionadas con la **integración del framework Django con bases de datos**.

El repositorio forma parte del **registro de evidencia del portafolio académico**, y presenta una aplicación web desarrollada con Django que implementa operaciones **CRUD completas**, uso del **ORM**, manejo de **migraciones**, y modelado de datos tanto **simples como relacionados**, cumpliendo con los requerimientos funcionales mínimos solicitados.

---

## 🎯 Objetivo del Proyecto
Implementar clase a clase las distintas tecnologías vistas en el curso, aplicándolas en un proyecto Django funcional que permita:

- Integrar Django con una base de datos relacional.
- Modelar entidades de datos simples y relacionadas.
- Persistir y consultar información utilizando el ORM de Django.
- Desarrollar una aplicación web bajo el patrón **MVC (Model–View–Controller)**, siguiendo las buenas prácticas del framework.

---

## 🧩 Integración de Django con Bases de Datos
Django permite integrarse de forma nativa con distintos motores de bases de datos, entre ellos:

- **SQLite** (utilizado por defecto en este proyecto para facilitar el desarrollo).
- **PostgreSQL**
- **MySQL / MariaDB**
- **Oracle**

La configuración de la base de datos se realiza a través del archivo `settings.py`, específicamente en la sección `DATABASES`, donde se definen el motor, nombre de la base de datos, credenciales y parámetros de conexión.

Django gestiona automáticamente las conexiones y operaciones mediante su **ORM (Object Relational Mapper)**, permitiendo interactuar con la base de datos usando objetos Python sin necesidad de escribir SQL de forma explícita en la mayoría de los casos.

---

## 🗃️ Capa de Modelo – Entidades sin Relaciones
El proyecto incluye modelos simples que representan entidades independientes, las cuales se traducen directamente en tablas dentro de la base de datos.

Características:
- Modelos sin relaciones entre sí.
- Campos básicos como texto, números y fechas.
- Persistencia automática mediante migraciones.

Este enfoque permite resolver problemáticas simples y comprender el funcionamiento básico del ORM y del mapeo objeto-relacional.

---

## 🔗 Capa de Modelo – Entidades con Relaciones
Además de entidades simples, el proyecto implementa modelos relacionados utilizando los tipos de relaciones que ofrece Django:

- **OneToOneField** (uno a uno)
- **ForeignKey** (uno a muchos)
- **ManyToManyField** (muchos a muchos)

Estas relaciones permiten modelar escenarios más complejos, como asociaciones entre usuarios, registros y categorías, resolviendo una problemática real mediante datos interconectados.

---

## 🔄 Migraciones de Base de Datos
El esquema de la base de datos se gestiona mediante el sistema de **migraciones de Django**, lo que permite:

- Crear tablas automáticamente a partir de los modelos.
- Propagar cambios cuando se agregan o modifican campos.
- Mantener sincronizado el código con la estructura de la base de datos.

Durante el desarrollo se ejecutaron comandos como:

- `python manage.py makemigrations`
- `python manage.py migrate`

para asegurar la correcta evolución del esquema de datos.

---

## 🔍 Consultas y Recuperación de Información
El proyecto hace uso del **ORM de Django** para realizar consultas sobre la base de datos, tales como:

- Filtrado de registros (`filter()`)
- Exclusión de datos (`exclude()`)
- Obtención de registros únicos (`get()`)
- Consultas personalizadas y optimizadas

Estas consultas permiten resolver necesidades específicas de información dentro de la aplicación, manteniendo el código legible y desacoplado del SQL directo.

---

## 🧱 Aplicación Web CRUD (MVC)
La aplicación implementa el patrón **MVC**, donde:

- **Model**: define la estructura y lógica de los datos.
- **View**: gestiona la lógica de negocio y las respuestas HTTP.
- **Template**: presenta la información al usuario.

Se desarrollaron funcionalidades completas de:

- **Crear** registros
- **Leer** y listar información
- **Actualizar** datos existentes
- **Eliminar** registros

permitiendo una gestión completa de la información almacenada en la base de datos.

---

## 🛠️ Aplicaciones Preinstaladas de Django
El proyecto utiliza y reconoce la utilidad de diversas aplicaciones preinstaladas del ecosistema Django, entre ellas:

- `django.contrib.admin`: administración de modelos mediante un panel web.
- `django.contrib.auth`: gestión de usuarios, autenticación y permisos.
- `django.contrib.sessions`: manejo de sesiones de usuario.
- `django.contrib.messages`: sistema de mensajes para feedback al usuario.

Estas aplicaciones facilitan el desarrollo y permiten centrarse en la lógica del negocio sin reinventar funcionalidades comunes.

---

## ✅ Conclusión
Este proyecto evidencia la correcta aplicación de los conceptos fundamentales del framework Django en relación con bases de datos, demostrando competencias técnicas en:

- Modelado de datos
- Uso del ORM
- Migraciones
- Consultas
- Desarrollo de aplicaciones web CRUD

Cumpliendo así con los **requerimientos funcionales mínimos esperados del Portafolio del Módulo 7**.
