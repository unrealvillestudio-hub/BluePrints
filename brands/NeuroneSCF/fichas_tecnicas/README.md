# Fichas técnicas NeuroneSCF

Una ficha por producto y por kit (51 en total), más `fichas.json` con los mismos datos en formato
legible por máquina.

## De dónde salen

La fuente única es la **ficha de producto en Supabase**, en las tablas
`public.product_blueprints` y `public.product_presentations`. Estos archivos son su versión legible
y **no se editan a mano**: si algo cambia, cambia en la tabla y la ficha se regenera.

- **Hechos:** activos, modo de uso, pH, precauciones y tamaños, verificados el 2026-09-26.
- **Redacción:** propia de NeuroneSCF, en ES y EN neutros, sin voseo.
- **Originalidad:** la redacción no comparte ninguna secuencia de 5 palabras con material de
  terceros (medido el 2026-09-26). Solo coinciden los rangos de pH, que son cifras.

## El ADN de la marca: tu cabello en diferentes climas

Cada ficha dice **por qué** el producto sirve en un clima concreto. Hoy el único clima es el calor
húmedo de Florida.

Cada clima nuevo de EE. UU. entra como una entrada más de `use_contexts` en la tabla, sin cambiar
el esquema, y su catálogo está en `fichas.json → climas`.

**Regla:** nunca se afirma que un producto fue formulado para un clima; se explica por qué funciona
en él.

## Lo que nunca va aquí

- **Precios.** El precio vive en la tienda y se lee en vivo. Cada presentación apunta a su variante
  de la tienda desde `product_presentations.commerce_listings`.
- **Material de marketing de terceros.**
