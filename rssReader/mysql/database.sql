-- Borra la base de datos si existe
DROP DATABASE IF EXISTS RSSdata;

-- Crea la base de datos CHARACTER SET utf8 COLLATE utf8_bin;
CREATE DATABASE RSSdata CHARACTER SET latin1 COLLATE latin1_spanish_ci;

-- Usuario para la conexión
GRANT ALL ON RSSdata.* TO 'rssuser'@'localhost' IDENTIFIED BY 'rss';

-- Creación de la tabla
USE RSSdata;
CREATE TABLE entrada (id INT NOT NULL AUTO_INCREMENT,TitRss VARCHAR(300),DescRss VARCHAR(300),
                      LinkRss VARCHAR(300), TitItem VARCHAR(300), DescItem VARCHAR(300),
                      LinkItem VARCHAR(300), PRIMARY KEY (id));



