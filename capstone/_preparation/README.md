# Preparación del Capstone Project

Todos los datos están almacenados en `/nfs/astro/torradeflot/MOOC/GalaxyZoo1`.
Las rutas a los datos hacen referencia a ubicaciones dentro de esta carpeta.

## Datos GalaxyZoo

Extracción de datos del DR14 de [SkyServer](http://skyserver.sdss.org/dr14/en/tools/search/sql.aspx)

```SQL
Select * from Zoospec
```

* Total de 667944 registros `DR14_ZooSpec.csv`
* Muestra aleatoria de 10.000 registros `DR14_ZooSpec_10000.csv`
* De la anterior muestra, los que están clasificados: `DR14_ZooSpec_10000_classified.csv`

Especificación de los campos en [Sky Server Schema Browser](http://skyserver.sdss.org/dr14/en/help/browser/browser.aspx#&&history=description+zooSpec+U)

---
<h3 color="red">Alerta!!!</h3>
En algunos casos, los valores de los campos `elliptical` y `spiral`  no se corresponden con su definición. Teóricamente:

<table>
<tr><td>elliptical</td><td>flag for elliptical - 1 if debiased elliptical fraction > 0.8, 0 otherwise</td></tr>
<tr><td>spiral</td><td>flag for combined spiral - 1 if debiased spiral fraction > 0.8, 0 otherwise</td></tr>
</table>

En la tabla a continuación se puede ver la correspondencia entre la definición y el valor de los campos.

<table border="1" bgcolor="cornsilk">
<tbody><tr align="center"><td><font size="-1">p_cs_debiased > 0.8</font></td><td><font size="-1">spiral</font></td><td><font size="-1">p_el_debiased > 0.8</font></td><td><font size="-1">elliptical</font></td><td><font size="-1">recuento</font></td></tr>	
<tr align="center" bgcolor="#eeeeff"><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">373,719</font></td></tr>
<tr align="center" bgcolor="#eeeeff"><td nowrap=""><font size="-1">1</font></td><td nowrap=""><font size="-1">1</font></td><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">147,138</font></td></tr>
<tr align="center" bgcolor="#eeeeff"><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">1</font></td><td nowrap=""><font size="-1">1</font></td><td nowrap=""><font size="-1">57,755</font></td></tr>
<tr align="center" bgcolor="#eeeeff"><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">1</font></td><td nowrap=""><font size="-1">1</font></td><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">165</font></td></tr>
<tr align="center" bgcolor="#eeeeff"><td nowrap=""><font size="-1">1</font></td><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">13,628</font></td></tr>
<tr align="center" bgcolor="#eeeeff"><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">1</font></td><td nowrap=""><font size="-1">4,435</font></td></tr>
<tr align="center" bgcolor="#eeeeff"><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">1</font></td><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">28,182</font></td></tr>
<tr align="center" bgcolor="#eeeeff"><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">1</font></td><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">0</font></td><td nowrap=""><font size="-1">42,922</font></td></tr>
</tbody></table>

Sugiero ignorar los campos `elliptical` y `spiral` y utilizar únicamente los campos `p_cs_debiased` y `p_el_debiased`
---

## Imágenes de muestra

Algunas imágenes jpeg de muestra se han descargado en `images`:
```
images
└── 0.4
    ├── 16x16
    ├── 32x32
    └── 64x64
```
Corresponden a objetos seleccionados aleatoriamente de entre los del Galaxy Zoo, con pixel scale=0.4 y tamaño 16x16, 32x32 o 64x64 píxeles.

```
# /image_script.py get_jpegs -o /nfs/astro/torradeflot/MOOC/GalaxyZoo1/DR14_ZooSpec.csv -n 100 -f /nfs/astro/torradeflot/MOOC/GalaxyZoo1
# /image_script.py get_jpegs -o /nfs/astro/torradeflot/MOOC/GalaxyZoo1/DR14_ZooSpec.csv -n 100 -f /nfs/astro/torradeflot/MOOC/GalaxyZoo1 -d 32
# /image_script.py get_jpegs -o /nfs/astro/torradeflot/MOOC/GalaxyZoo1/DR14_ZooSpec.csv -n 100 -f /nfs/astro/torradeflot/MOOC/GalaxyZoo1 -d 16
```

## Imágenes como arrays

1. Dividir el csv con datos del Galaxy Zoo en chunks:

    `./image_script.py split_csvs -o /nfs/astro/torradeflot/MOOC/GalaxyZoo1/DR14_ZooSpec_10000.csv -c 100 -d /tmp`

2. Para cada fichero recoger las imágenes de todos los objetos y guardarlo en un csv

    `./image_script.py get_features -o /tmp/{file_name}`
    
    Este csv tendrá 64*64 + 1 = 4097 campos.

3. Hacer merge de todos los ficheros de features:

    `./image_script.py merge_csvs -o /tmp/{f1},...,/tmp/{fn} -d /nfs/astro/torradeflot/MOOC/GalaxyZoo1/F_DR14_ZooSpec_10000.csv`

4. Filtrar solamente las imágenes clasificadas. El fichero de salida tiene un tamaño de 600MiB e incluye también imágenes que no han
sido satisfactoriamente clasificadas. Esto quiere decir que no tienen almenos un 80% de votos en uno de los sentidos. Éstas imágenes
no van a ser utilizadas para la clasificación, así que para el entreno y validación del modelo las podemos filtrar.

    Seleccionamos aquellos objetos de `ZooSpec` con `spiral==1` o `elliptical==1` y nos quedan 3788 registros y el fichero de features se "reduce" a 200MiB.

    Los datos filtrados son: `DR14_ZooSpec_10000_classified.csv` i `F_DR14_ZooSpec_10000_classified.csv`


## Generación de imágenes a partir de csv

1. Generación de un sample aleatorio de imágenes
    `./image_script.py plot_sample_images -o /nfs/astro/torradeflot/MOOC/GalaxyZoo1/F_DR14_ZooSpec_10000.csv -s 3,3`

    <img src="../../_static/galaxy_3x3_sample.png" style="width: 50%;"/>

2. Generación de la imagen de una galaxia por su id:

    `./image_script.py plot_sample_images -o /nfs/astro/torradeflot/MOOC/GalaxyZoo1/F_DR14_ZooSpec_10000.csv -i 587741726583292117`

	<table>
		<tr>
			<td><img src="../../_static/galaxy_spiral_sample.png"/></td>
			<td><img src="../../_static/galaxy_elliptic_sample.png"/></td>	
		</tr>
	</table>
