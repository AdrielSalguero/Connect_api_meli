# Conexion API MercadoLibre Argentina


## Objetivo !🎯

_Realizar un análisis sobre la oferta/vidriera de las opciones de productos que responden a distintas búsquedas en el sitio Mercadolibre.com.ar_

## Consignas 🖥️

```
1) Barrer una lista de más de 150 ítems ids en el servicio público:
https://api.mercadolibre.com/sites/MLA/search?q=chromecast&limit=50#json
En este caso particular y solo a modo de ejemplo, son resultados para la búsqueda “chromecast”, 
pero deberás elegir otros términos para el experimento que permitan enriquecer el análisis en 
un hipotético dashboard (ejemplo Google Home, Apple TV, Amazon Fire TV, o afines para poder comparar 
dispositivos portátiles, o bien elegir otros 3 que te interesen para comparar)

2) Por cada resultado, realizar el correspondiente GET por Item_Id al recurso público:
https://api.mercadolibre.com/items/{Item_Id}

3) Escribir los resultados en un archivo plano delimitado por comas, desnormalizando el JSON obtenido 
en el paso anterior, en tantos campos como sea necesario para guardar las variables que te interesen modelar .

```


Saludos, Adriel
