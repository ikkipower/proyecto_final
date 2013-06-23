Proyecto final
==============

Entrega del Proyecto Final del Curso Programación Avanzada en Python, 2ª edición

Arbol del proyecto


<pre><code>
Proyecto_final
|--Readme.md
|--rssReader : directorio raiz del proyecto scrapy
|   |--log : contiene los logs creados por el spider
|   |-Mysql : contiene script para generar la base de datos
|   |-src   : contiene todas las imageness del proyecto
|   |-glade : contiene la interfaz gráfica del proyecto
|   |-rssReader
|       |- spiders # Directorio donde almacenar los Spiders.
</code></pre>




Pasos del Proyecto
------------------

<ol>
<li><b>Scrapy</b> Lectura del <a href="http://www.elperiodico.com/es/rss/rss_portada.xml/">RSS de portada del periódico</a> mediante scrapy

   
<p>A continuación los 3 campos obligatorios para el RSS, puede haber más pero solamente tenemos en cuenta estos tres:</p>

<ul>
<li>Titulo del Rss</li>
<li>Descripcion Rss</li>
<li>Link Rss</li>
</ul>    
    
<p>Para cada ítem al igual que en el caso del título de RSS solamente tenemos 3 elementos obligatorios que son los siguientes:</p>

<ul>
<li>Titulo del Item</li>
<li>Descripcion Item</li>
<li>Link Item</li>
</ul>
   
</li>
<li><b>Generación Base de Datos Mysql</b>

<ul>
<li>Base de datos (fichero database.sql dentro de la carpeta Mysql) que contendrá una tabla donde se guarde por cada entrada del feed rss los 3 datos genéricos a todos y los específicos de cada entrada.</li>
</ul>
</li>
<li><b>Pipeline para guardar los datos seleccionados en un base de Datos Mysql</b>

<ul>
<li>MySqlPipeline(object) es el pipeline que coge los datos recogidos por el spider y los inserta en la base de datos, siempre y cuando no existan previamente en ella.</li>
</ul>




</li>

<li> <b>Ejecutar el programa</b>

<ul>
   <li>Ejecución del fichero principal del programa (rssReader.py) que ejecuta la interfaz gráfica (gtk3) generada con glade.

   Siempre que la base de datos no contenga ninguna entrada o se queira actualizar se ha de ir al menú Archivo --> Actualizar base de datos, 
   para insertar las noticias del rss del periodico (mediante scrapy).

   Posteriormente se puede interactuar con los diferentes elementos del menu (es decir, ver/eliminar las entradas y abrir un web browser para leer la noticia completa)</li>
</ul>
</li>

</ol>


