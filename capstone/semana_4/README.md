# Semana 4. Análisis de datos y Machine Learning

## Introducción

En semanas anteriores:
* Diseñamos el modelo de datos de nuestra aplicación
* Analizamos los datos científicos del proyecto
* Recogimos los votos de los participantes
* Descartamos los votos erróneos o sospechosos
* Utilizamos los datos de votos para clasificar los objetos en tres clases:
    * espiral
    * elíptica
    * indefinido
    
Esta semana:
* Introduciremos el dataset de imágenes de galaxias
* A partir de las imágenes y la clasificación de las galaxias: 
diseñaremos, entrenaremos y validaremos un algoritmo
de Inteligencia Artificial para la clasificación automática de galaxias a partir de una imagen.
* Aplicaremos este algoritmo sobre galaxias no clasificadas.

## Dataset de imágenes de galaxias

Las imágenes de galaxias tomadas por nuestro telescopio son procesadas y almacenadas como 
imágenes JPEG de 64*64 píxeles en color como éstas:

<table style="width:50%; margin-left:auto" >
<tr>
<td><img src="../../_static/images/587726032770498738.jpg"/></td>
<td><img src="../../_static/images/587733397567176814.jpg"/></td>
<td><img src="../../_static/images/588018252689178934.jpg"/></td>
<td><img src="../../_static/images/587727179520409692.jpg"/></td>
</tr>
<tr>
<td><img src="../../_static/images/587733412053844080.jpg"/></td>
<td><img src="../../_static/images/588297864176599167.jpg"/></td>
<td><img src="../../_static/images/587731513691930797.jpg"/></td>
<td><img src="../../_static/images/587733604804067664.jpg"/></td>
</tr>
<tr>
<td><img src="../../_static/images/588848899381788857.jpg"/></td>
<td><img src="../../_static/images/587731872851820676.jpg"/></td>
<td><img src="../../_static/images/587735743156191523.jpg"/></td>
<td><img src="../../_static/images/588848899905028344.jpg"/></td>
</tr>
<tr>
<td><img src="../../_static/images/587732051093815414.jpg"/></td>
<td><img src="../../_static/images/587739406262337752.jpg"/></td>
<td><img src="../../_static/images/587732053234876853.jpg"/></td>
<td><img src="../../_static/images/587742774567043199.jpg"/></td>
</tr>
</table>


