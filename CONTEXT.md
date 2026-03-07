# UNRLVL STUDIO — CONTEXT.md
**Archivo de recuperación de contexto entre chats**
**Última actualización:** 2026-03-07
**Instrucción de uso:** Pega este archivo completo como PRIMER MENSAJE de cada nuevo chat.
Claude responderá "contexto cargado" y el trabajo puede empezar sin recuperación adicional.
**Cuándo actualizar:** Al cierre de sesión, pide: "Actualiza el CONTEXT.md con lo de hoy"
Claude genera el bloque Markdown completo. Commítalo con: `chore: context update YYYY-MM-DD`

---

## 1. QUIÉN SOY Y CÓMO TRABAJAMOS

Marketer, publicista y administrador de negocios, +20 años experiencia independiente.
Operando desde España (próximamente Panamá). Negocios en Miami, Florida. Sin residencia en EEUU.

**Unreal>ille** — agencia inhouse. Propietaria de e-commerce, proveedora de marketing/publicidad/estrategia para mis negocios y los de mi familia. No es agencia pública en esta fase.

**Líneas de negocio:**
- Laboratorio dropshipping (Florida) → detector de productos ganadores → alimenta Marcas Propias
- Marcas Propias: productos validados + importados de Colombia (incluye gel bebible Asaí/Espirulina/Monje)
- Gestión de tiendas e-commerce de asociados y familia
- Joint venture con distribuidora local Miami (Patricia Osorio, PO) — ella infraestructura local, Unreal>ille marketing y estrategia

**Cómo quiero que trabajes:**
- Análisis directo y honesto. No me des la razón si no la tengo.
- Opciones con pros/contras reales cuando haya decisiones importantes.
- Avísame proactivamente de riesgos con probabilidades estimadas.
- Siempre en español. Documentos formales en español salvo indicación.
- Outputs listos para usar, no borradores genéricos.

---

## 2. ECOSISTEMA UNRLVL STUDIO LABS

### Principio fundamental: SIEMPRE MULTIMARCA
Ningún archivo del stack puede ser exclusivo de una sola marca. Compliance, contextos de producto, reglas de copy — todo va en archivos multimarca bajo la key del brandId. Ejemplo: el compliance de Neurone no es un archivo separado, vive en brandContexts.tsx bajo NeuroneCosmetics.

### Labs y estado actual

| Lab | Función | Estado | Output |
|-----|---------|--------|--------|
| WebLab | Copy web: hero, features, FAQ, testimonials, blog, e-commerce | v2.1 activo | MD / HTML / Liquid |
| BlogLab | Posts de blog (módulo dentro de WebLab) | v1.0 activo | MD / HTML / Liquid |
| CopyLab | Copy ads, emails, captions, scripts | v1.2 activo | Texto |
| SocialLab | Copy + scheduling redes sociales | v1.2 activo | Texto + mock publish |
| VideoLab | Storyboards y guiones visuales | v1.1 activo | Texto estructurado |
| VoiceLab | Scripts y calibración de voz | v1.2 activo | Texto / audio |
| ImageLab | Prompts para generación de imagen (SceneGenerator + E-Commerce/UGC) | v1.2 activo | Prompts estructurados |
| BlueprintLab | CRUD + Export de blueprints (Person, Location, Product, Copy) | v1.0 activo | JSON |
| Orchestrator | Planner de flujos multi-Lab | v1.2 activo | Plan de stages |
| AgentLab | Agentes conversacionales por marca | v1.0 en Vercel | Desplegado |

### Stack técnico
- AI Studio Labs (todos excepto AgentLab): React 18 + TypeScript, Gemini 2.0 Flash, Zustand, Vite
- AgentLab: React 18 + TypeScript, Zustand, Vercel
- Cambios en AI Studio Labs → vía prompts en Gemini AI Studio
- Cambios en AgentLab → Claude modifica código directamente

### Fases de implementación
| Fase | Nombre | Estado |
|------|--------|--------|
| F2 | Blueprints | Completo |
| F2.5 | Humanize Layer (transversal) | Completo — BLOQUEANTE para F6 |
| F6 | Testing formal | En curso (WebLab E-Commerce probado) |

F2.5 es hard-blocker de F6. Testing formal no puede considerarse completo hasta que Humanize esté verificado en todos los engines.

---

## 3. FUENTES DE VERDAD

### DB_VARIABLES v6.4
Archivo Excel en Google Drive. Cerebro central. Hojas: Marcas (44 cols), CONTEXTOS, DD_DATOS (buyer personas), CTAs, KEYWORDS, PersonBlueprints, LocationBlueprints, HUMANIZE.

Visión a futuro: migrará a MySQL en VPS propio. Los Labs pasarán de AI Studio a apps propias. Arquitectura diseñada para migración no-destructiva.

### BlueprintLab = Fuente de verdad de blueprints en runtime
UNRLVL-Core fue propuesto y DESCARTADO. BlueprintLab ya es la fuente de verdad. No existe repo separado para runtime.

Schemas activos:
| Schema | Versión | Compatible con |
|--------|---------|----------------|
| BP_PERSON | 1.0 | ImageLab (avatares), VideoLab, VoiceLab, AgentLab |
| BP_LOCATION | 1.0 | ImageLab (SceneGenerator), VideoLab |
| BP_PRODUCT | 1.0 | ImageLab (E-Commerce/UGC), WebLab |
| BP_COPY | 1.0 | CopyLab (disponible pero NO flujo primario — copys desde DB_VARIABLES) |

Flujo de consumo (fase AI Studio):
BlueprintLab Export tab → JSON → copy-paste manual en el Lab destino

### Repo BluePrints (custodia y versioning — NO runtime)
github.com/unrealvillestudio-hub/BluePrints

Los blueprints son datos de ENTRADA del ecosistema. Son consumidos por cualquier Lab, independientemente del destino final (Shopify, WordPress, avatar generado, scene para video, UGC con producto, etc.). NO están atados a ninguna plataforma de output.

Estructura actual:
```
BluePrints/
├── README.md
├── persons/      ← pendiente: exportar blueprints PO desde BlueprintLab
├── locations/
│   ├── BP_LOCATION_MiamiBeach_1.0.json    (activo)
│   └── BP_LOCATION_MiamiStreets_1.0.json  (activo)
└── products/     ← pendiente: Neurone, D7H, Vivosé en fase e-commerce
```

---

## 4. MARCAS ACTIVAS

| Marca | BrandId | Mercado | Estado blueprints |
|-------|---------|---------|------------------|
| D7Herbal | D7Herbal | España | products pendiente |
| Vivosé Mask | VivoseMask | España | products pendiente |
| Diamond Details | DiamondDetails | Miami | sin blueprints aún |
| Vizos Cosmetics | VizosCosmetics | Miami + España | sin blueprints aún |
| PO Personal | PatriciaOsorioPersonal | Miami | persons: pendiente export |
| PO Comunidad | PatriciaOsorioComunidad | Miami | persons: pendiente export |
| PO Vizos Salón | PatriciaOsorioVizosSalon | Miami | persons: pendiente export |
| Neurone Cosmética | NeuroneCosmetics | Miami B2C+B2B | products pendiente (fase e-commerce) |

### Neurone Cosmética — detalles críticos

PO tiene distribución exclusiva South & Central Miami. NO es dueña de la marca.
FLAG PENDIENTE: Confirmar con PO autorización formal de marca Neurone para operar en US antes de lanzar dominio.

Arquitectura de dominios (decidida):
- vizoscosmetics.com — institucional + marcas propias (bajo riesgo ban RRSS)
- neuronescmiami.com — e-commerce B2C
- pro.neuronescmiami.com — Portal Pro B2B (Locksmith, fase inicial)

Plataforma: Shopify (por modelo B2B OAuth/Locksmith). NO WordPress.

Catálogo (7 categorías, ~38 líneas, ~142 SKUs):
1. Scalp — compliance ALTO, claims médicos prohibidos
2. Moisture
3. Color Rescue
4. Restore
5. Styling — la más grande (~11 productos)
6. Pro Salon — b2bOnly: true, shopifyVisibility: pending (confirmar arquitectura Locksmith)
7. Hair Color — Neurone Color 70+ tonos + Fanzi Mix 11 tonos fantasía
Outlier: Hyaloneurine — único producto cara+cabello, lógica de copy propia.

Compliance Neurone (guardarraíl NO negociable — FDA/FTC):
- Usar: "ayuda a", "favorece", "contribuye a", "potencia", "nutre", "fortalece"
- Prohibido: "trata", "cura", "elimina enfermedades", claims médicos
- Implementado en brandContexts.tsx campo productCompliance (multimarca)
- Se inyecta en webEngine.ts ANTES del bloque AGGRO

### Relación PO con marcas
PO (Miami) y MO (España) co-operan Vizos Cosmetics. PO da expertise técnico y es la cara. D7Herbal y Vivosé Mask solo en España. Los blueprints de PO son consumibles por estas marcas cuando ella genera contenido para ellas.

---

## 5. CAPA HUMANIZE (F2.5)

Transversal — no es un Lab ni un toggle. Inyección automática en todos los prompts.

Cadena de resolución:
DB_VARIABLES [hoja HUMANIZE por marca] → override opcional
    ↓
BP_PERSON.humanize.[medio] → override por persona
    ↓
humanizeConfig.ts defaults → fallback
    ↓
Engine prompt → Output

Bloques por medio: COPY, IMAGE/AVATAR, VIDEO, VOICE, WEB

---

## 6. MODO AGGRO

Filosofía: warnings + responsabilidad del operador. Nunca bloqueo. El profesional advierte, el cliente decide.
- AGGRO actúa SIEMPRE después del compliance de marca
- Neurone compliance → AGGRO → output

---

## 7. WEBLAB v2.1 — ESTADO POST-TESTING

11 fixes aplicados en webEngine.ts, WebGeneratorModule.tsx y packs.ts. Output modes: markdown, html, liquid.

Testing E-Commerce Neurone completado:
| Pack | Estado |
|------|--------|
| Product Listing | Aprobado |
| Collection Page | Aprobado |
| Homepage Tienda | Aprobado — CTA Final mejor headline generado |
| About/Historia | Aprobado |
| Product Page | Pendiente — próxima acción |
| AGGRO en Liquid | Pendiente prueba |

---

## 8. PENDIENTES — ORDEN DE PRIORIDAD

### Inmediatos (próxima sesión)
1. Integrar productCompliance de Neurone en webEngine.ts — inyección antes del bloque AGGRO. Traer webEngine.ts actual.
2. Integrar buildNeuroneProductContext() en brandContexts.tsx — cuando usuario selecciona Neurone + categoría + producto en WebLab.
3. Test Product Page + AGGRO — cierre del módulo E-Commerce.

### Siguiente bloque
4. Testing Landings.
5. Exportar blueprints de PO desde BlueprintLab y subir a BluePrints/persons/.
6. Confirmar Pro Salon shopifyVisibility — Locksmith acceso restringido o solo Portal Pro.
7. Fotos Miami Beach y Downtown Miami para BP_LOCATION (pendiente sesión fotográfica).
8. Audio PO nuevo — el existente no es suficientemente representativo para VoiceLab (3 min modo profesional activo).
9. Confirmar autorización formal de marca Neurone para operar en US.

### Pendientes de arquitectura (no urgentes)
10. VideoLab rebuild (en agenda, sin fecha).
11. Assets Library architecture.
12. DB_VARIABLES auto-fill en generators (checklist WebLab).
13. SUPER AGGRO mode (checklist WebLab).
14. Shopify vs WordPress selector (checklist WebLab).

---

## 9. REPOS Y ACCESO

| Recurso | URL |
|---------|-----|
| AgentLab (producción) | https://unrlvl-agent-lab.vercel.app |
| AgentLab (repo) | github.com/unrealvillestudio-hub/UNRLVL-AgentLab |
| UNRLVL-Shopify (outputs web Liquid/HTML) | github.com/unrealvillestudio-hub/UNRLVL-Shopify |
| BluePrints (custodia blueprints) | github.com/unrealvillestudio-hub/BluePrints |
| GitHub org principal | github.com/unrealvillestudio-hub |
| GitHub org anterior (migración en curso) | github.com/blackoutbusiness-hub |
| DB_VARIABLES v6.4 | Google Drive — UnrealVille_Studio/ |

Token GitHub: se pasa al inicio de cada sesión que requiera push. No persiste entre sesiones.
Medidas de control: scope limitado a repo, caducidad 30-90 días.

---

## 10. DECISIONES ARQUITECTÓNICAS CERRADAS

| Decisión | Resultado |
|----------|-----------|
| Neurone plataforma | Shopify (B2B OAuth/Locksmith) |
| UNRLVL-Core | DESCARTADO — BlueprintLab es fuente de verdad |
| BP_COPY flujo primario | DESCARTADO — copys desde DB_VARIABLES en CopyLab |
| Custodia blueprints | Repo BluePrints (transversal, NO en UNRLVL-Shopify) |
| Humanize | Transversal, no siloed, inyección automática |
| Reset Button en UI | Solo form-level — no toca Assets Library ni pipeline outputs |
| AGGRO mode | Warnings + responsabilidad operador, nunca bloqueo |
| Arquitectura multimarca | Todo en archivos multimarca bajo brandId, ningún archivo exclusivo por marca |

---

*Generado: 2026-03-07 | Próxima actualización: al cierre de sesión siguiente*
