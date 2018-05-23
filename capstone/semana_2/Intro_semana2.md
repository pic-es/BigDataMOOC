## Presentación de la semana 2

Como ya se comentó la semana pasada, el proyecto [GalaxyZoo](https://www.zooniverse.org/projects/zookeeper/galaxy-zoo/) consiste en recolectar datos sobre la forma de los objetos celestes fotografiados por unos telescopios ópticos.

El objetivo fundamental de esta segunda semana es definir un modelo de datos que sirva por un lado para almacenar correctamente esa información, y por otro para poder analizarla plenamente y de manera eficiente.

## Modelado de los datos

Lo primero que tenemos que hacer para crear un correcto modelo de datos es conocer los datos en sí mismo.

Nosotros partimos de los siguientes conjuntos de datos:

- Un catálogo de galaxias caracterízadas por un conjunto de propiedades

- Una serie de imágenes que corresponden a cada una de las galaxias del catálogo de galaxias

- Un conjunto de usuarios que nos han ayudado a clasificar las galaxias usando las imágenes

- Un conjunto de votos generados por los usuarios que clasifican morfológicamente las galaxias

### Modelo de datos relacional

En nuestro caso vamos a usar un modelo de datos relacional ya que vamos a almacenar nuestros datos en una base de datos relacional. En un modelo de datos relacional la información está organizada en tablas. Éstas tablas están compuestas por registros (cada fila de la tabla sería un registro) y columnas (también llamadas campos). El modelo de datos relacional es el más utilizado en la actualidad para modelar problemas reales y administrar datos dinámicamente.

Como ejemplo sencillo y claro podemos coger el fichero que contiene la información del catálogo de galaxias.
Aunque ya se hizo la semana pasada podemos explorar rápidamente el catálogo usando la terminal:
1) Dirigirse al directorio donde se encuentra el fichero:
> cd /path
2) Mostrar la cabecera del fichero con el comando head ya que se trata de un fichero con formato [CSV](https://es.wikipedia.org/wiki/Valores_separados_por_comas):
> head fichero

Habéis podido ver que el fichero tiene en primer lugar una serie de comentarios, a continuación una cabecera que define los campos (o columnas) de cada registro, y finalmente una lista de registro (o galaxias) con distintos valores en los campos.

Como ya hemos dicho, en un modelo de datos relacional la información está organizada en tablas. El fichero en formato CSV del catálogo de galaxias es una tabla en sí mismo, y de esta manera podemos definir nuestra primera tabla dentro de nuestro modelo de datos:

IMAGEN DE UNA TABLA CON LOS DATOS DEL FICHERO QUE ACABAMOS DE VER (excell por ejemplo).

### Normalización y clave principal
Aunque no vamos a entrar en detalles es importante saber que existe toda una teoría sobre la definición de un correcto modelo de datos (https://es.wikipedia.org/wiki/Normalizaci%C3%B3n_de_bases_de_datos). Se podrían presentar muchos casos prácticos en los que un modelo de datos incorrecto suele conllevar una deuda técnica que provoca retrasos en los tiempos de ejecución o incluso la imposibilidad de realizar algún tipo de análisis en particular. Este no va a ser nuestro caso ya que vamos a conseguir un perfecto modelado de nuestros datos.

Y antes de pasar a los primeros ejercicios vamos a introducir otro concepto muy común en el diseño de bases de datos relacionales, se trata de la clave principal. La clave principal es un campo o una combinación de campos que identifica de forma única a cada fila de una tabla.
Por ejemplo, en el caso anterior, los científicos que han creado el catálogo se han asegurado de que cada registro del catálogo sea único y por ello han creado el campo galaxy_id que se trataría de la clave principal de la tabla galaxy_catalog.



## Ejercicios
A continuación vais a ser vosotros a través de una serie de ejercicios los que continueis con el modelado de los datos.

Ejercicios:

1) En este caso vamos a definir la tabla en la que se van a almacenar los datos de los usuarios. El fichero con los datos de todos los usuarios se encuentra en /path
	a) Cuántos campos definen a cada usuario
	b) 

1) La tabla de usuarios la podéis encontrar
1) La siguiente tabla que vamos a definir es la del conjunto de usuarios. En la imagen siguiente se muestra la tabla pero es necesario rellenar algunos campos