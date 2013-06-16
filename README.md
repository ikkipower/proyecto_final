Proyecto final
==============

Entrega del Proyecto Final del Curso Programación Avanzada en Python, 2ª edición

Arbol del proyecto

proyecto_final
---Mysql : contiene script para generar la base de datos
---rssReader : directorio raiz del proyecto scrapy
-----rssReader
---------spiders # Directorio donde almacenar los Spiders.


1) Abrir el Web Browser desde python
  "http://docs.python.org/2/library/webbrowser.html"
   
2) Scrapy para leer el RSS de ""
Pruebas de lectura de ficheros XML del RSS 

   "http://www.elperiodico.com/es/rss/rss_portada.xml"
   
A continuación los 3 campos obligatorios para el RSS, puede haber más
pero solamente tenemos en cuenta estos tres:
   
    titulorss = xxs.select("//channel/title/text()").extract()[0]
    descrss = xxs.select("//channel/description/text()").extract()[0]
    url = xxs.select("//channel/link/text()").extract()[0]
   
Para cada ítem al igual que en el caso del título de RSS solamente 
tenemos 3 elementos obligatorios que son los siguientes:
   
    titItem = xxs.select("//channel/item/title/text()").extract()
    linkItem = xxs.select("//channel/item/link/text()").extract()
    descItem = xxs.select("//channel/item/description/text()").extract()


3) Generación Base de Datos Mysql (dentro de la carpeta Mysql fichero 
database.sql)

Base de datos que contendrá una tabla donde se guarde por cada entrada
del feed rss los 3 datos genéricos a todos y los específicos de cada
entrada.

-- Borra la base de datos si existe
DROP DATABASE IF EXISTS RSSdata;

-- Crea la base de datos
CREATE DATABASE RSSdata;

-- Usuario para la conexión
GRANT ALL ON RSSdata.* TO 'rssuser'@'localhost' IDENTIFIED BY 'rss';

-- Creación de la tabla
USE RSSdata;
CREATE TABLE entrada (id INT NOT NULL AUTO_INCREMENT,
                      TitRss VARCHAR(200), DescRss VARCHAR(200),
                      LinkRss VARCHAR(200), TitItem VARCHAR(200), 
                      DescItem VARCHAR(200), LinkItem VARCHAR(200), 
                      PRIMARY KEY (id));

4) Pipeline para guardar los datos seleccionados en un base de Datos Myql


5) 

Programa ejecutado desde una interface Gráfica Gtk+
