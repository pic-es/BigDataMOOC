# Frequently asked questions (FAQs)

## Error al importar `numpy` en un notebook

Si al ejecutar una celda de un notebook, nos sale un error de este estilo:

```
AttributeError: module 'numpy' has no attribute 'core'
```

Lo más probable es que no tengamos pyspark instalado y configurado correctamente.

Consulta el apartado de instalación y configuración de pyspark para más información.

En caso que la carpeta `/home/cloudera/anaconda3` ya existiera, borrala antes de 
ejecutar los pasos de instalación de pyspark de nuevo:
```
> rm -rf /home/cloudera/anaconda3
```

## Al ejecutar `pyspark` en la consola se abre un shell de python

Esto se debe a que la variable de entorno para encontrar el ejecutable de PySpark no está configurada.

Debemos abrir un terminal y ejecutar:
```
> source ~/.bashrc
```
