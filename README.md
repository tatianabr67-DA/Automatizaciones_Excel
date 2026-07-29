# 🐍 Automatización y Limpieza de Reportes de Nómina con Python

## 📌 Descripción del Proyecto
Herramienta de automatización desarrollada con **Python** que incluye una interfaz gráfica de usuario (**Tkinter**) para transformar reportes de nómina desestructurados (provenientes de sistemas como Nominax) en bases de datos limpias y listas para análisis operativo.

## 💡 El Reto de Negocio
Los reportes exportados de sistemas de recursos humanos y nómina suelen venir en formatos con celdas combinadas, encabezados dispersos, múltiples saltos de sección y sin normalización geográfica. Procesar esto manualmente consume horas de trabajo operativo y es propenso a errores humanos.

## 🛠️ Solución Implementada
* **Lectura Defensiva:** Implementación de manejo de excepciones para asegurar la compatibilidad con diferentes extensiones de Excel (`.xls` y `.xlsx`).
* **Procesamiento Condicional:** Uso de iteraciones lógicas con `Pandas` para capturar dinámicamente los departamentos y asociarlos geográficamente mediante un diccionario de mapeo (`MAPA_CIUDADES`).
* **Tratamiento de Fechas y Nulos:** Funciones de seguridad para estandarizar formatos temporales (`AAAA-MM-DD`) y filtrar filas vacías o registros de ruido.
* **Interfaz Gráfica Amigable:** Creación de una ventana interactiva (`Tkinter`) que permite al usuario seleccionar archivos locales sin necesidad de modificar código fuente.

## 🛠️ Tecnologías y Librerías
* **Python**
* **Pandas** (Manipulación y transformación de datos)
* **Tkinter** (Interfaz gráfica de usuario)
* **Re / Os** (Expresiones regulares y manejo de rutas)

---
*Desarrollado como parte del portafolio práctico de automatización de procesos y análisis de datos.*
