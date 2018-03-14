
## Descripción

Este repositorio contiene una spyder de scrapy que permite identificar y descargar todos los archivos que se encuentren en una página web, estos se guardan en una colección de mongo con los detalles de donde se obtuvieron. o si se desea, se pueden guardar en una ubicación del disco duro.

## Requerimientos:

* Python v3.6 o superior
* 
---
## Instalación

Para instalar todas las dependencias basta con ejecutar:

```shell
pip3 install -r requirements.txt
```

en caso de que no se tenga python2 basta con ejecutar `pip` en vez de `pip3`

---
## Ejecución

Para ejecutar basta con escribir en la terminal:

```
scrapy crawl docs <params>
```

los parámetros disponibles son:

|parámetro|descripcion|ejemplo|default|
|---:|:---|:---|:---:|
|url|Dirección principal desde donde se comenzarán a buscar archivos, los links que se encuentren que no sean archivos se visitarán para buscar archivos dentro de los mismos, hasta llegar a la profundidad indicada|`-url https://imgur.com/`|`None`|
|depth|Profundiad máxima en la que se buscarán links| `-depth 5` | `3`
|files|Extensiones permitidad para los archivos, separadas por coma y sin espacios| `-files pdf,txt,png,jpg,jpeg`|`pdf`|
|saveOnMongo|Indica si el archivo se guardará en mongo como blob, de lo contrario se tiene que indicar la dirección donde se guardarán los archivos|`-saveOnMongo true`|`true`|
|dest|Dirección destino en donde se guardarán los archivos descargados.|`-dest ./files`|`./descargas`|
