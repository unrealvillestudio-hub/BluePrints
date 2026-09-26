# Fichas técnicas del fabricante: Neurone Cosmética (neuronecosmetica.com)

**Qué es.** Las 45 fichas técnicas públicas que el fabricante enlaza en cada producto de su web
(«Descargar ficha técnica»), descargadas el 2026-09-26. Es la **fuente primaria** de los hechos
de producto de NeuroneSCF: descripción, activos, modo de uso, pH, precauciones y presentaciones.

| Ruta | Contenido |
|---|---|
| `urls.txt` | Las 45 URL, medidas desde la API pública de productos del fabricante (`/wp-json/wc/store/v1/products`). |
| `pdf/` | Los PDF tal como los publica el fabricante. |
| `txt/` | Texto extraído con `pdftotext -layout` (dos columnas: español a la izquierda, inglés a la derecha). |
| `descarga.log` | Código HTTP y tamaño de cada descarga. Las 45 respondieron 200. |
| `fichas.json` | Secciones por idioma, separadas por `parse.py`. |

## Cómo se usa, y cómo no

- **Es evidencia, no texto publicable.** El fabricante es mexicano y su redacción tiene
  regionalismos («tiempo de pose», «alaciado», «cano», «brocha»…). Nada de aquí se copia a un
  canal.
- **La ficha canónica vive en Supabase**, `public.product_blueprints` (descripción, modo de uso,
  activos, problemas, beneficios, afirmaciones prohibidas), redactada en ES/EN neutro a partir de
  estas fichas. Su columna `supplier_ref` apunta al PDF y al texto de esta carpeta.
- **Precios: nunca.** Ni aquí ni en la ficha. El precio vive en la tienda y se lee en vivo.

## Regenerar `fichas.json`

```
python3 parse.py
```

Sin dependencias. Si el fabricante publica fichas nuevas, se actualiza `urls.txt`, se descargan
los PDF y se vuelve a correr `pdftotext -layout` y `parse.py`.
