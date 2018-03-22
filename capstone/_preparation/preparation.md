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


## Imágenes de muestra

Algunas imágenes de muestra se han descargado en `images`: