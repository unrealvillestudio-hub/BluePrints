# BluePrints — Unreal>ille Studio

Repositorio de custodia de todos los Blueprints y assets del ecosistema Unreal>ille Studio.

**Contexto completo del ecosistema:** [`CoreProject/CONTEXT.md`](https://github.com/unrealvillestudio-hub/CoreProject/blob/main/CONTEXT.md)

---

## Rol en el ecosistema

BluePrints es la **fuente de verdad de assets y datos maestros** del ecosistema. No produce outputs — almacena y versiona los inputs que todos los Labs consumen. Cuando el ecosistema migre a VPS + MySQL, este repo pasará a ser exclusivo de assets binarios (imágenes, logos).

```
BlueprintLab (crea BPs) ──→ BluePrints/ (custodia) ──→ Todos los Labs
```

---

## Estructura

```
brands/
  BP_BRAND_ForumPHs_v1.0.json       ← Identidad Amatista Carbon
  BP_BRAND_NeuroneSCF_v1.0.json     ← Identidad Neurone
  assets/
    ForumPHs/                        ← FPHS_logo_wt.png · FPHS_logo_deep.png
    NeuroneSCF/
      brand/                         ← logos (blue/dark/white, aro)
      products/                      ← 44 product images + dark_versions/ + alpha_dark/
    VizosCosmetics/                  ← vizos_logo_*.png
locations/
  BP_LOCATION_MiamiBeach_1.0.json
  BP_LOCATION_MiamiStreets_1.0.json
  BP_LOCATION_VizosSalon_1.0.json
  assets/[Location]/                 ← fotos de locación
persons/
  BP_PERSON_PO_*.json               ← Patricia Osorio (Personal/Comunidad/Salón)
  assets/PO/                         ← fotos con alpha channel
products/
  BP_PRODUCT_Neurone_*.json         ← 39 productos Neurone SCF
assets/
  MANIFEST.json                      ← índice de assets con paths canónicos
```

**Regla:** Para buscar assets nunca usar paths hardcodeados — consultar `assets/MANIFEST.json`.

---

## Schemas activos

| Schema | Versión | Compatible con |
|--------|---------|----------------|
| BP_BRAND | 1.1 | BlueprintLab, WebLab, CoreProject |
| BP_PERSON | 1.0 | ImageLab, VideoLab, VoiceLab, AgentLab |
| BP_LOCATION | 1.0 | ImageLab, VideoLab |
| BP_PRODUCT | 1.0 | ImageLab, WebLab, AgentLab |

---

## Marcas con BPs activos

| Marca | BP_BRAND | BP_PRODUCT | Assets |
|-------|----------|------------|--------|
| ForumPHs | ✅ v1.0 | — | ✅ logos |
| Neurone SCF | ✅ v1.0 | ✅ 39 productos | ✅ completo |
| Vizos Cosmetics | — | — | ✅ logos |
| Patricia Osorio | — | — | ✅ fotos completas |

---

## Pendiente

- BP_BRAND para Vizos Cosmetics
- BP_BRAND para D7Herbal
- Logos PNG en curvas + alpha para Unreal>ille Studio (Sam pendiente)

---

## Changelog

| Fecha | Cambio |
|---|---|
| 2026-03-20 | Assets reorganizados bajo `brands/assets/[Brand]/` · MANIFEST v1.1 · README actualizado |
| 2026-03-09 | BP_BRAND_ForumPHs_v1.0 añadido |
