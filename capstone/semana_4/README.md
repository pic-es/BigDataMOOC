# Semana 4. Análisis de datos y Machine Learning

## Introducción

**En semanas anteriores:**

* Diseñamos el modelo de datos de nuestra aplicación
* Analizamos los datos científicos del proyecto
* Recogimos los votos de los participantes
* Descartamos los votos erróneos o sospechosos
* Utilizamos los datos de votos para clasificar los objetos en tres clases:
    * espiral
    * elíptica
    * indefinido
    
**Esta semana:**

* Introduciremos el dataset de imágenes de galaxias
* A partir de las imágenes y la clasificación de las galaxias: 
diseñaremos, entrenaremos y validaremos un algoritmo
de Inteligencia Artificial para la clasificación automática de galaxias a partir de una imagen.
* Aplicaremos este algoritmo sobre galaxias no clasificadas.


## ¿Qué es un algoritmo de clasificación?

Explicar ...

## Dataset de imágenes de galaxias

Las imágenes de galaxias tomadas por nuestro telescopio son procesadas y almacenadas como 
imágenes JPEG de 64x64 píxeles en color como éstas:

<table style="width:50%; margin-left:auto; margin-right:auto;" >
<tr>
<td align="center"><img src="../../_static/images/587726032770498738.jpg"/></td>
<td align="center"><img src="../../_static/images/587733397567176814.jpg"/></td>
<td align="center"><img src="../../_static/images/588018252689178934.jpg"/></td>
<td align="center"><img src="../../_static/images/587727179520409692.jpg"/></td>
</tr>
<tr>
<td align="center"><img src="../../_static/images/587733412053844080.jpg"/></td>
<td align="center"><img src="../../_static/images/588297864176599167.jpg"/></td>
<td align="center"><img src="../../_static/images/587731513691930797.jpg"/></td>
<td align="center"><img src="../../_static/images/587733604804067664.jpg"/></td>
</tr>
<tr>
<td align="center"><img src="../../_static/images/588848899381788857.jpg"/></td>
<td align="center"><img src="../../_static/images/587731872851820676.jpg"/></td>
<td align="center"><img src="../../_static/images/587735743156191523.jpg"/></td>
<td align="center"><img src="../../_static/images/588848899905028344.jpg"/></td>
</tr>
<tr>
<td align="center"><img src="../../_static/images/587732051093815414.jpg"/></td>
<td align="center"><img src="../../_static/images/587739406262337752.jpg"/></td>
<td align="center"><img src="../../_static/images/587732053234876853.jpg"/></td>
<td align="center"><img src="../../_static/images/587742774567043199.jpg"/></td>
</tr>
</table>

La mayoría de algoritmos de Machine Learning necesitan que los datos esten 
organizados de forma tabular, con las observaciones (imágenes en nuestro caso) distribuidas por filas
y los parámetros (píxeles) de cada observación en columnas.

Así pues, hemos convertido cada una de las imágenes en un vector de 64*64=4096 posiciones,
con los siguientes pasos:

* **Convertir la imagen en color en una imagen en blanco y negro.** Cada uno de los píxeles de la 
imagen contiene 3 valores entre 0 y 255 correspondientes a los 3 canales RGB (R=Rojo, G=Verde, 
B=Azul). Podríamos decir que cada imagen está compuesta por tres matrices 64x64: `MR`, `MG` y `MB`,
correspondientes a los canales R, G y B respectivamente. Aplicamos la siguiete fórmula para
fusionar las tres matrices en una sola matriz (`M`) en tonos de gris.

  ``` M = 0.2989 * MR + 0.5870 * MG + 0.1140 * MB```

* **"Aplanar" la matriz a un vector** Reorganizamos los valores de la matriz `M` de dimensiones 64x64

<table style="border-collapse: collapse; margin-left:auto; margin-right:auto;">
<tr><td style="border: 1px solid black;">1_1</td><td style="border: 1px solid black;">1_2</td><td style="border: 1px solid black;">1_3</td><td style="border: 1px solid black;">1_4</td><td style="border: 1px solid black;">...</td><td style="border: 1px solid black;">1_64</td></tr>
<tr><td style="border: 1px solid black;">2_1</td><td style="border: 1px solid black;">2_2</td><td style="border: 1px solid black;">2_3</td><td style="border: 1px solid black;">2_4</td><td style="border: 1px solid black;">...</td><td style="border: 1px solid black;">2_64</td></tr>
<tr><td style="border: 1px solid black;">3_1</td><td style="border: 1px solid black;">3_2</td><td style="border: 1px solid black;">3_3</td><td style="border: 1px solid black;">3_4</td><td style="border: 1px solid black;">...</td><td style="border: 1px solid black;">3_64</td></tr>
<tr><td style="border: 1px solid black;">4_1</td><td style="border: 1px solid black;">4_2</td><td style="border: 1px solid black;">4_3</td><td style="border: 1px solid black;">4_4</td><td style="border: 1px solid black;">...</td><td style="border: 1px solid black;">4_64</td></tr>
<tr><td style="border: 1px solid black;">...</td><td style="border: 1px solid black;">...</td><td style="border: 1px solid black;">...</td><td style="border: 1px solid black;">...</td><td style="border: 1px solid black;">...</td><td style="border: 1px solid black;">...</td></tr>
<tr><td style="border: 1px solid black;">64_1</td><td style="border: 1px solid black;">64_2</td><td style="border: 1px solid black;">64_3</td><td style="border: 1px solid black;">64_4</td><td style="border: 1px solid black;">...</td><td style="border: 1px solid black;">64_64</td></tr>
</table>

> A una tupla de longitud 4096 como sigue:

<table style="border-collapse: collapse; margin-left:auto; margin-right:auto;">
<tr>
<td style="border: 1px solid black;">1_1</td>
<td style="border: 1px solid black;">1_2</td><td style="border: 1px solid black;">...</td><td style="border: 1px solid black;">1_64</td><td style="border: 1px solid black;">2_1</td><td style="border: 1px solid black;">2_2</td><td style="border: 1px solid black;">...</td><td style="border: 1px solid black;">2_64</td><td style="border: 1px solid black;">...</td>
<td style="border: 1px solid black;">64_64</td>
</tr>
</table>

* **Normalización** Algunos algoritmos funcionan mejor si todas las variables se encuentran dentro del mismo
rango de valores, típicamente [-1, 1] o [0, 1], por este motivo, dividimos los valores por 255.

Este procedimiento ya ha sido llevado a cabo para todas las imágenes y el resultado 
lo podéis encontrar en: `/nfs/astro/torradeflot/MOOC/GalaxyZoo1/F_DR14_ZooSpec_10000.csv`


## Target

Para poder entrenar un algoritmo de clasificación también necesitamos los "targets" de las observaciones.
En nuestro caso, el fichero que creamos en la semana anterior, dónde se identifica el tipo de cada una
de las galaxias: `/nfs/astro/torradeflot/MOOC/GalaxyZoo1/T_DR14_ZooSpec_10000.csv`

<table style="margin-left:auto; margin-right:auto;">
<tr><th>target</th><th>clase</th></tr>
<tr><td>0</td><td>incierto</td></tr>
<tr><td>1</td><td>elíptica</td></tr>
<tr><td>2</td><td>espiral</td></tr>
</table>

## Datos completos

Juntamos los dos sets de datos en un solo fichero que contiene tanto los features como el target: `T_F_DR14_ZooSpec_10000.csv`

Este conjunto de datos tiene los campos:

* dr7objid: identificador del objeto
* target: clase del objeto según definición anterior
* F0 a F4095: correspondientes a la tupla de 4096 atributos anteriormente descrita


## Ingestión de los datos en HDFS

