# Ejercicios

__1. Descarga de los datos__

Arrancar la maquina virtual. Abrir una consola de comando y desde la home descarga la carpeta que contiene los datos que se van a utilizar con el siguiente comando:

`wget path`

__2. Registro de los datos en el HDFS__

Una vez que los ficheros estén guardados en la maquina virtual, hay que registrar los ficheros *.csv en el sistema de ficheros con el siguiente comando:

`hdfs fs copy`

Para comprobar que se haya registrado correctamente, ejecuta este comando y comprueba que en la lista de ficheros que devuelve están los ficheros que has registrado previamente:

`hdfs ls`

__3. Exploración de los datos__

La exploración de datos en formato csv se puede llevar al cabo muy facilmente cargandolos en un dataframe.
Abrir el notebook Spark con el comando:
`spark notebook command` 

* Ejecutar el siguiente codigo para explorar las primeras lineas del fichero a:

`pd.head(5)`

__Pregunta__ Cuantas columnas tiene el fichero a?

* Exlorar el fichero b: cargarlo en un dataframe (como con el fichero a) y explorar las primeras lineas del dataframe
Para saber cuantas filas contiene se pueden usar distintos metodos: haver una consulta en Hive o utilizando pandas.
Selecciona el metodo que mejor conoces para contestar a la siguiente pregunta.

__Pregunta__ Cuantas filas contiene el fichero b?

__Pregunta__ Cuantos valores validos (no NaNs) contiene la columna x del fichero b? (ejemplo:usar la función numpy.isfinite())

__Pregunta__ Que columna del fichero a contiene valores también contenidos en el fichero b? Como se llama la columna del fichero b? Que representa?

* Exploración de las imagenes de galaxias
En la carpeta imagenes/ se encuentran ficheros con la imagenes de las galaxias que hay que clasificar. Las imagenes se pueden ver ejecutando el comando por consola
`command jpg`
Mirar las imagenes para ver si es posible reconocer los distintos tipos (elípticas, espirales), así como explicado en la introducción.

__Pregunta__ Abre la imagen correspondiente a la entrada numero 2 del fichero a. De que tipo es?









