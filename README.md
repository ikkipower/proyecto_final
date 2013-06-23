Proyecto final
==============

Entrega del Proyecto Final del Curso Programación Avanzada en Python, 2ª edición

Arbol del proyecto

proyecto_final

--Readme.md

---rssReader : directorio raiz del proyecto scrapy

-----log : contiene los logs creados por el spider

-----Mysql : contiene script para generar la base de datos

-----src   : contiene todas las imageness del proyecto

-----glade : contiene la interfaz gráfica del proyecto

-----rssReader

---------spiders # Directorio donde almacenar los Spiders.


1) Scrapy para leer el RSS de "http://www.elperiodico.com/es/rss/rss_portada.xml"
   
A continuación los 3 campos obligatorios para el RSS, puede haber más
pero solamente tenemos en cuenta estos tres:
   
    Titulo del Rss
    Descripcion Rss
    Link Rss
   
Para cada ítem al igual que en el caso del título de RSS solamente 
tenemos 3 elementos obligatorios que son los siguientes:
   
    Titulo del Item
    Descripcion Item
    Link Item

2) Generación Base de Datos Mysql (dentro de la carpeta Mysql fichero 
database.sql)

Base de datos que contendrá una tabla donde se guarde por cada entrada
del feed rss los 3 datos genéricos a todos y los específicos de cada
entrada.

4)Pipeline para guardar los datos seleccionados en un base de Datos Myql

-MySqlPipeline(object) es el pipeline que coge los datos recogidos por 
el spider y los inserta en la base de datos, siempre y cuando no existan
previamente en ella.

5) Ejecución del fichero principal del programa (rssReader.py) que 
ejecuta la interfaz gráfica (gtk3) generada con glade.

-Siempre que la base de datos no contenga ninguna entrada o se queira 
actualizar se ha de ir al menú Archivo --> Actualizar base de datos, 
para insertar las noticias del rss del periodico (mediante scrapy).

-Posteriormente se puede interactuar con los diferentes elementos del 
menu (es decir, ver/eliminar las entradas y abrir un web browser para 
leer la noticia completa)
