
## Descripción

Este repositorio contiene una spyder de scrapy que permite identificar y descargar todos los archivos que se encuentren en una página web, estos se guardan en una colección de mongo con los detalles de donde se obtuvieron. o si se desea, se pueden guardar en una ubicación del disco duro.

## Requerimientos:

* Python v3.6 o superior

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
|url|Dirección principal desde donde se comenzarán a buscar archivos, los links que se encuentren que no sean archivos se visitarán para buscar archivos dentro de los mismos, hasta llegar a la profundidad indicada|`-a url=https://imgur.com/`|`None`|
|depth|Profundiad máxima en la que se buscarán links| `-a profundidad=5` | `3`
|files|Extensiones permitidad para los archivos, separadas por coma y sin espacios| `-a files=pdf,txt,png,jpg,jpeg`|`pdf`|


------
Ajustar:

Path lleva un arreglo
cambiar UUID por MD5
Recorrer scripts hasta llegar a la ultima fecha que se encuentre
