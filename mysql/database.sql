-- Borra la base de datos si existe
DROP DATABASE IF EXISTS RSSdata;

-- Crea la base de datos
CREATE DATABASE RSSdata;

-- Usuario para la conexión
GRANT ALL ON RSSdata.* TO 'rssuser'@'localhost' IDENTIFIED BY 'rss';

-- Creación de la tabla
USE RSSdata;
CREATE TABLE entrada (id INT NOT NULL AUTO_INCREMENT,TitRss VARCHAR(200),DescRss VARCHAR(200),
                      LinkRss VARCHAR(200), TitItem VARCHAR(200), DescItem VARCHAR(200),
                      LinkItem VARCHAR(200), PRIMARY KEY (id));



