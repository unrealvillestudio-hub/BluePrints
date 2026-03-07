# UNRLVL — BluePrints

Repositorio de custodia de todos los Blueprints exportados desde **BlueprintLab**.

Los blueprints son **datos de entrada** del ecosistema UNRLVL Studio — no son outputs ni están atados a ninguna plataforma de destino (Shopify, WordPress, etc.). Son consumidos por cualquier Lab que los necesite: ImageLab para generación de avatares y escenas, VideoLab para storyboards, VoiceLab para calibración de voz, CopyLab para voz de marca, WebLab para contexto de producto, AgentLab para orchestración local.

---

## Estructura

```
BluePrints/
├── persons/          ← BP_PERSON: voz, tono, compliance, humanize overrides
│   └── [id].blueprint.json
├── locations/        ← BP_LOCATION: atributos visuales de locaciones
│   └── [id].blueprint.json
└── products/         ← BP_PRODUCT: catálogo por categoría y marca
    └── [id].blueprint.json
```

---

## Schemas activos

| Schema | Versión | Compatible con |
|--------|---------|----------------|
| BP_PERSON | 1.0 | ImageLab, VideoLab, VoiceLab, AgentLab |
| BP_LOCATION | 1.0 | ImageLab (SceneGenerator), VideoLab |
| BP_PRODUCT | 1.0 | ImageLab (E-Commerce / UGC), WebLab |

---

## Flujo de trabajo

```
BlueprintLab (AI Studio)
    ↓ crea, edita, valida
    ↓ Export tab → JSON
    ↓
BluePrints/ (este repo) ← custodia y versioning
    ↓
Labs consumen el blueprint pegando el JSON
manualmente en el panel de cada Lab (fase AI Studio)

FUTURO (VPS + MySQL):
Labs hacen query directo → BlueprintLab es la UI admin
Este repo desaparece como necesidad operativa
```

---

## Convención de nombres

```
BP_{TIPO}_{Identificador}_{versión}.json

Ejemplos:
  persons/BP_PERSON_PO_Patricia_1.0.json
  locations/BP_LOCATION_MiamiBeach_1.0.json
  products/BP_PRODUCT_Neurone_Colorimetria_1.0.json
```

---

## Marcas activas

| Marca | BrandId | Blueprints disponibles |
|-------|---------|----------------------|
| D7Herbal | `D7Herbal` | products (pendiente) |
| Vivosé Mask | `VivoseMask` | products (pendiente) |
| Diamond Details | `DiamondDetails` | — |
| Vizos Cosmetics | `VizosCosmetics` | — |
| PO Personal | `PatriciaOsorioPersonal` | persons (pendiente export desde BlueprintLab) |
| PO Comunidad | `PatriciaOsorioComunidad` | persons (pendiente export) |
| PO Vizos Salón | `PatriciaOsorioVizosSalon` | persons (pendiente export) |
| Neurone Cosmética | `NeuroneCosmetics` | products (pendiente — llega en fase e-commerce) |

**Locations activas:** Miami Beach, Miami Streets (ver `/locations`)

---

*Fuente de verdad en runtime: BlueprintLab (AI Studio) / MySQL (futuro VPS)*
*Este repo es custodia y versioning — no CDN de datos en runtime*
