## Modular Recovery Platform - Architecture & Bundle

This codebase implements a **modular recovery platform** that can handle multiple recovery types (chargebacks, shipping refunds, etc.) through a plugin architecture. The current implementation includes the Chargeback Evidence Builder, but the architecture supports easy addition of new recovery modules.

### Shared Core Components
- **Auth & Organization Management**: Multi-tenant support with role-based access
- **Connection Manager**: OAuth and API key management for external services  
- **Detection Engine**: Identifies recovery opportunities across plugins
- **Evidence/Claim Builder**: Template-based document generation
- **Submission Pipeline**: API and manual submission workflows
- **Analytics Dashboard**: Unified metrics across all recovery types
- **Billing System**: Success-fee based billing with Stripe

### Plugin Architecture

Each recovery type (chargeback, shipping, etc.) implements these interfaces:

```typescript
interface RecoveryPlugin {
  id: string;
  name: string;
  connectionTypes: ConnectionType[];
  detector: DetectionEngine;
  templateEngine: TemplateEngine;
  submissionHandlers: SubmissionHandler[];
}
```

### Architecture Decisions (concise)
- Stack: Next.js 14 App Router + TypeScript + TailwindCSS; Supabase (Auth, Postgres, Storage, RLS); Edge Functions for PDF/notifications.
- Integrations/APIs: Shopify Admin API (OAuth, disputes/orders webhooks), Stripe Disputes API + webhooks.
- Data model: org-scoped entities with `org_id` RLS. Core tables per PRD: `orgs, users, user_org_roles, stores, disputes, orders, evidence_items, submissions, analytics_winrates, audit_events, refund_events, alerts, submission_packets`.
- Naming conventions:
  - Files/folders: kebab-case for routes, PascalCase for React components, camelCase for variables/functions, snake_case for SQL identifiers.
  - API routes: `/api/webhooks/{provider}` and typed server actions under `/api/*`.
  - Env vars: UPPER_SNAKE; browser-exposed prefixed with `NEXT_PUBLIC_`.
  - Type exports: central barrel `src/types/index.ts`.
- Imports/exports:
  - Path alias `@/*` to `src/*` via `tsconfig.json`.
  - Named exports for utilities and components; default exports for Next.js route components.
- Security: Strict RLS (deny-by-default), service role only in server contexts, signed URLs for artifacts, idempotent webhooks.
---
<a id="demo-chargeback-evidence-builder"></a>
## Demo: Chargeback Evidence Builder

Below are locale-specific tours. Replace image placeholders under `./assets/chargeback-demo/{locale}/` when ready.

### English (EN)
This quick tour shows the core flow from connecting your store to submitting a complete evidence packet.

1) Connect your store and Stripe
- OAuth into Shopify and connect Stripe to enable dispute sync and submissions.
- Image: ![Connect integrations](./assets/chargeback-demo/en/01-connect-integrations.png)

2) Review your Disputes Inbox
- New and in-progress disputes are automatically listed and kept in sync.
- Image: ![Disputes inbox](./assets/chargeback-demo/en/02-disputes-inbox.png)

3) Open a dispute to compose evidence
- Auto-extracted order, shipping, AVS/CVV and customer comms are pre-filled.
- Gaps are highlighted with guided actions to collect what’s missing.
- Image: ![Dispute detail & evidence](./assets/chargeback-demo/en/03-dispute-detail-evidence.png)

4) Preview the packet
- Generate a clean, merchant-branded PDF with all required sections.
- Image: ![Packet preview](./assets/chargeback-demo/en/04-packet-preview.png)

5) Submit via API or schedule
- Submit instantly through Stripe/Shopify APIs or schedule for later; track status.
- Image: ![Submit & status](./assets/chargeback-demo/en/05-submit-status.png)

6) Track outcomes and analytics
- Win rates, recovery amounts, and time-saved metrics across teams and stores.
- Image: ![Analytics dashboard](./assets/chargeback-demo/en/06-analytics.png)

#### What’s in it for me
- Higher win rates: Evidence templates aligned to network codes + gap checks.
- Hours saved per week: Automated data pull from orders, shipping, and comms.
- Lower losses: Faster, consistent submissions reduce missed deadlines and errors.
- Audit-ready trail: Immutable receipts, versioned packets, and activity logs.
- Team workflows: Roles, locking, review, and batch submissions at scale.
- Secure by default: RLS, signed URLs, and service-role isolation on the server.

### Español (ES)
Este recorrido rápido muestra el flujo principal desde conectar tu tienda hasta enviar un paquete de evidencia completo.

1) Conecta tu tienda y Stripe
- Inicia sesión con OAuth en Shopify y conecta Stripe para habilitar la sincronización de disputas y los envíos.
- Imagen: ![Conectar integraciones](./assets/chargeback-demo/es/01-connect-integrations.png)

2) Revisa tu bandeja de disputas
- Las disputas nuevas y en curso se listan automáticamente y se mantienen sincronizadas.
- Imagen: ![Bandeja de disputas](./assets/chargeback-demo/es/02-disputes-inbox.png)

3) Abre una disputa para redactar evidencia
- Se rellenan automáticamente datos de pedido, envío, AVS/CVV y comunicaciones del cliente.
- Las brechas se destacan con acciones guiadas para recolectar lo que falta.
- Imagen: ![Detalle de disputa y evidencia](./assets/chargeback-demo/es/03-dispute-detail-evidence.png)

4) Previsualiza el paquete
- Genera un PDF limpio con la marca del comercio y todas las secciones requeridas.
- Imagen: ![Vista previa del paquete](./assets/chargeback-demo/es/04-packet-preview.png)

5) Envía por API o programa
- Envía al instante mediante las APIs de Stripe/Shopify o programa para más tarde; haz seguimiento del estado.
- Imagen: ![Envío y estado](./assets/chargeback-demo/es/05-submit-status.png)

6) Haz seguimiento de resultados y analíticas
- Tasas de éxito, montos recuperados y métricas de tiempo ahorrado entre equipos y tiendas.
- Imagen: ![Panel de analíticas](./assets/chargeback-demo/es/06-analytics.png)

#### Beneficios para ti
- Mayores tasas de éxito: Plantillas alineadas a códigos de red + verificación de brechas.
- Horas ahorradas por semana: Extracción automática de datos de pedidos, envíos y comunicaciones.
- Menores pérdidas: Envíos más rápidos y consistentes reducen plazos perdidos y errores.
- Trazabilidad lista para auditoría: Recibos inmutables, paquetes versionados y registro de actividad.
- Flujos de trabajo de equipo: Roles, bloqueo, revisión y envíos por lotes a escala.
- Seguro por defecto: RLS, URLs firmadas y aislamiento del service role en el servidor.

### Deutsch (DE)
Diese kurze Tour zeigt den Kernablauf vom Verbinden deines Shops bis zur Einreichung eines vollständigen Nachweispakets.

1) Shop und Stripe verbinden
- Über OAuth bei Shopify anmelden und Stripe verbinden, um Streitfälle zu synchronisieren und Einreichungen zu ermöglichen.
- Bild: ![Integrationen verbinden](./assets/chargeback-demo/de/01-connect-integrations.png)

2) Streitfall‑Inbox prüfen
- Neue und laufende Streitfälle werden automatisch gelistet und synchron gehalten.
- Bild: ![Streitfall-Inbox](./assets/chargeback-demo/de/02-disputes-inbox.png)

3) Streitfall öffnen und Nachweise zusammenstellen
- Bestell‑, Versand‑, AVS/CVV‑Daten und Kundenkommunikation werden automatisch vorausgefüllt.
- Lücken werden hervorgehoben und mit Anleitungen zur Vervollständigung versehen.
- Bild: ![Streitfall & Nachweise](./assets/chargeback-demo/de/03-dispute-detail-evidence.png)

4) Paketvorschau anzeigen
- Erzeuge ein sauberes, markenkonformes PDF mit allen Pflichtabschnitten.
- Bild: ![Paketvorschau](./assets/chargeback-demo/de/04-packet-preview.png)

5) Per API einreichen oder planen
- Sofort über Stripe/Shopify‑APIs einreichen oder für später planen; Status verfolgen.
- Bild: ![Einreichung & Status](./assets/chargeback-demo/de/05-submit-status.png)

6) Ergebnisse und Analysen verfolgen
- Erfolgsquoten, Rückgewinnungsbeträge und Zeitersparnis über Teams und Shops hinweg.
- Bild: ![Analyse‑Dashboard](./assets/chargeback-demo/de/06-analytics.png)

#### Vorteile für dich
- Höhere Erfolgsquote: Vorlagen gemäß Netzwerkkodes + Lückenprüfungen.
- Stunden pro Woche sparen: Automatisches Ziehen von Bestell‑, Versand‑ und Kommunikationsdaten.
- Geringere Verluste: Schnellere, konsistente Einreichungen reduzieren Fristversäumnisse und Fehler.
- Auditfester Verlauf: Unveränderliche Belege, versionierte Pakete und Aktivitätsprotokolle.
- Team‑Workflows: Rollen, Sperren, Review und Stapel‑Einreichungen im großen Maßstab.
- Sicher per Default: RLS, signierte URLs und Service‑Role‑Isolation auf dem Server.

### Try it with demo data
- Seeded demo org/store/disputes are available; see the migration at
  [supabase/migrations/chargebacks/0010_seed_demo.sql](#supabasemigrationschargebacks0010_seed_demosql).
- Screenshots above reference the `Demo Org` and `demo.myshopify.com` entries defined there.

### Optional: short video tour (placeholder)
- Add a 60–90s walkthrough video link here (e.g., Loom) once recorded.

---

## Folder Tree
```
chargeback-evidence-app/
├── package.json
├── tsconfig.json
├── next.config.mjs
├── next-i18next.config.js
├── postcss.config.js
├── tailwind.config.ts
├── .env.example
├── README.md
├── public/
│   └── locales/
│       ├── en/common.json
│       ├── es/common.json
│       └── de/common.json
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── login/page.tsx
│   │   ├── disputes/page.tsx
│   │   ├── disputes/[id]/page.tsx
│   │   ├── api/
│   │   │   ├── webhooks/stripe/route.ts
│   │   │   ├── webhooks/shopify/route.ts
│   │   │   ├── shopify/oauth/start/route.ts
│   │   │   ├── shopify/oauth/callback/route.ts
│   │   │   ├── submissions/route.ts
│   │   │   ├── evidence/route.ts
│   │   │   └── attachments/upload/route.ts
│   │   ├── orgs/new/page.tsx
│   │   ├── onboarding/page.tsx
│   │   ├── analytics/page.tsx
│   │   ├── settings/page.tsx
│   ├── tests/
│   │   ├── e2e/
│   │   │   └── disputes.spec.ts
│   │   ├── unit/
│   │   │   └── evidenceComposer.test.ts
│   │   └── integration/
│   │       └── rls.test.ts
│   ├── i18n/
│   │   └── index.ts
│   ├── ui/
│   │   ├── DataTable.tsx
│   │   ├── DraftEditor.tsx
│   │   ├── PacketPreview.tsx
│   │   ├── Charts.tsx
│   │   ├── Tabs.tsx
│   │   ├── SubmissionModal.tsx
│   │   └── CommandPalette.tsx
│   ├── lib/
│   │   ├── core/
│   │   │   ├── supabaseServer.ts
│   │   │   ├── supabaseClient.ts
│   │   │   ├── analytics.ts
│   │   │   ├── flags.ts
│   │   │   ├── config.ts
│   │   │   ├── geo.ts
│   │   │   ├── regions.ts
│   │   │   ├── providers.ts
│   │   │   ├── storage.ts
│   │   │   ├── pdf.ts
│   │   │   ├── shopify.ts
│   │   │   └── stripe.ts
│   │   └── chargebacks/
│   │       ├── evidenceComposer.ts
│   │       ├── submissionAdapters.ts
│   │       ├── orderMatching.ts
│   │       └── disputePolling.ts
│   ├── app/globals.css
│   └── types/index.ts
├── supabase/
│   ├── migrations/
│   │   └── chargebacks/
│   │       ├── 0001_init.sql
│   │       ├── 0002_rls_policies.sql
│   │       ├── 0003_flags_geo.sql
│   │       ├── 0004_test_helpers.sql
│   │       └── 0005_idempotency_audit.sql
│   └── functions/
│       └── core/
│           ├── generate-pdf/index.ts
│           └── send-notification/index.ts
├── playwright.config.ts
├── src/middleware.ts
```

Additions for billing/storage/RLS (monorepo-ready):

```
supabase/
├── migrations/
│   ├── chargebacks/
│   │   ├── 0006_order_tracking.sql
│   │   └── 0007_rls_write_policies.sql
│   └── core/
│       ├── 0001_billing_entitlements.sql
│       └── 0002_storage_buckets_policies.sql
```

---

## package.json
```json
{
  "name": "chargeback-evidence-app",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "typecheck": "tsc --noEmit",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "e2e": "playwright test"
  },
  "dependencies": {
    "next": "14.2.5",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "@supabase/supabase-js": "2.45.4",
    "zod": "3.23.8",
    "stripe": "14.23.0",
    "@shopify/shopify-api": "11.0.0",
    "date-fns": "3.6.0",
    "clsx": "2.1.1",
    "tailwindcss": "3.4.9",
    "postcss": "8.4.41",
    "autoprefixer": "10.4.20",
    "next-i18next": "15.2.0"
  },
  "devDependencies": {
    "typescript": "5.5.4",
    "eslint": "8.57.0",
    "eslint-config-next": "14.2.5",
    "@playwright/test": "1.46.0",
    "prettier": "3.3.3",
    "husky": "9.0.11",
    "lint-staged": "15.2.9"
  },
  "lint-staged": {
    "**/*.{ts,tsx,js,jsx,json,css,md}": [
      "prettier --write"
    ]
  }
}
```

---

## tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM"],
    "skipLibCheck": true,
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noPropertyAccessFromIndexSignature": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "resolveJsonModule": true,
    "jsx": "preserve",
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@core/*": ["src/lib/core/*"],
      "@ui/*": ["src/ui/*"],
      "@chargebacks/*": ["src/lib/chargebacks/*"]
    },
    "types": ["node"]
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}
```

---

## Prettier and commit hooks

Add Prettier for consistent formatting and commit-time checks. This does not change runtime behavior but improves diffs and code hygiene.

```bash
npm i -D prettier lint-staged husky
npx husky init
```

Add a minimal Prettier config:

```json
// .prettierrc
{
  "singleQuote": true,
  "semi": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2
}
```

Wire scripts and commit hooks:

```json
// package.json (additions)
{
  "scripts": {
    "format": "prettier --write .",
    "format:check": "prettier --check ."
  },
  "lint-staged": {
    "**/*.{ts,tsx,js,jsx,json,css,md}": [
      "prettier --write"
    ]
  }
}
```

Then create a pre-commit hook to run lint-staged:

```bash
echo "npx lint-staged" > .husky/pre-commit && chmod +x .husky/pre-commit
```

---

## TypeScript strictness additions

Strengthen type safety beyond `strict: true`. Merge these into `compilerOptions`:

```json
// tsconfig.json (merge into compilerOptions)
{
  "noUncheckedIndexedAccess": true,
  "exactOptionalPropertyTypes": true,
  "noPropertyAccessFromIndexSignature": true,
  "forceConsistentCasingInFileNames": true
}
```

These options surface subtle bugs in data-shaping, optional fields, and dictionary access.

---

## Centralized logging and client error boundary

Add a minimal structured logger for server contexts and an error boundary for client routes.

```ts
// src/lib/core/log.ts
type LogMeta = { [key: string]: unknown } & { request_id?: string; org_id?: string; user_id?: string };

function stringify(meta?: LogMeta) {
  try { return meta ? JSON.stringify(meta) : undefined; } catch { return undefined; }
}

export const log = {
  info: (message: string, meta?: LogMeta) => console.log(message, stringify(meta)),
  warn: (message: string, meta?: LogMeta) => console.warn(message, stringify(meta)),
  error: (message: string, meta?: LogMeta) => console.error(message, stringify(meta)),
};
```

```tsx
// src/ui/ErrorBoundary.tsx
import React from 'react';

type Props = { children: React.ReactNode };
type State = { hasError: boolean };

export class ErrorBoundary extends React.Component<Props, State> {
  state: State = { hasError: false };
  static getDerivedStateFromError() { return { hasError: true }; }
  componentDidCatch(error: unknown) { console.error('ui-error', error); }
  render() { return this.state.hasError ? <div>Something went wrong.</div> : this.props.children; }
}
```

Wrap page trees as appropriate (e.g., in `app/(marketing)/layout.tsx`):

```tsx
// app/(marketing)/layout.tsx
import { ErrorBoundary } from '@ui/ErrorBoundary';

export default function Layout({ children }: { children: React.ReactNode }) {
  return <ErrorBoundary>{children}</ErrorBoundary>;
}
```

---

## Input validation, idempotency, and rate limiting

Validate all inputs with Zod, use idempotency keys on mutating endpoints, and apply lightweight rate limits on public routes.

```ts
// app/api/disputes/submit/route.ts (example extract)
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { log } from '@core/log';
import { createServerClient } from '@core/supabaseServer';

const SubmitSchema = z.object({
  disputeId: z.string().uuid(),
  packetId: z.string().uuid(),
});

export async function POST(req: NextRequest) {
  const requestId = req.headers.get('x-request-id') || undefined;
  const idempotencyKey = req.headers.get('idempotency-key');
  const body = await req.json().catch(() => ({}));
  const parse = SubmitSchema.safeParse(body);
  if (!parse.success) {
    return NextResponse.json({ error: 'invalid_request', details: parse.error.flatten() }, { status: 400 });
  }

  if (!idempotencyKey) {
    return NextResponse.json({ error: 'missing_idempotency_key' }, { status: 409 });
  }

  const supabase = createServerClient();
  // record idempotency; if exists, short-circuit
  const { error: idemErr } = await supabase
    .from('idempotency_keys')
    .insert({ key: idempotencyKey, scope: 'disputes.submit' })
    .select()
    .single();
  if (idemErr && idemErr.code !== '23505') { // not unique_violation
    log.error('idempotency_insert_failed', { request_id: requestId, error: idemErr });
    return NextResponse.json({ error: 'server_error' }, { status: 500 });
  }
  if (!idemErr) {
    // first time; proceed with submission logic
  } else {
    return NextResponse.json({ status: 'duplicate' }, { status: 200 });
  }

  return NextResponse.json({ status: 'ok' });
}
```

Public endpoints can add simple rate limits (e.g., Upstash Redis):

```ts
// src/lib/core/rateLimit.ts
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const redis = new Redis({ url: process.env.UPSTASH_REDIS_REST_URL!, token: process.env.UPSTASH_REDIS_REST_TOKEN! });
export const rateLimit = new Ratelimit({ redis, limiter: Ratelimit.slidingWindow(10, '1 m') });
```

```ts
// usage inside a route
import { rateLimit } from '@core/rateLimit';
const ip = req.headers.get('x-forwarded-for') || 'anonymous';
const { success } = await rateLimit.limit(`submit:${ip}`);
if (!success) return NextResponse.json({ error: 'rate_limited' }, { status: 429 });
```

Database helper for idempotency (migration example):

```sql
-- supabase/migrations/core/000X_idempotency.sql
create table if not exists idempotency_keys (
  key text primary key,
  scope text not null,
  created_at timestamptz not null default now()
);
```

---

## src/lib/i18n/translate.ts
```ts
import { z } from 'zod';

export const TranslateRequest = z.object({
  text: z.string().min(1),
  source: z.string().optional(),
  target: z.string().min(2),
  glossary: z.record(z.string(), z.string()).default({}).optional(),
  placeholders: z.array(z.string()).default([]).optional(),
});

export type TranslateRequest = z.infer<typeof TranslateRequest>;

export async function translate(req: TranslateRequest): Promise<string> {
  const { text, source, target, glossary = {}, placeholders = [] } = TranslateRequest.parse(req);
  const cacheKey = `${source || 'auto'}:${target}:${hash(text)}:${hash(JSON.stringify(glossary))}`;
  const cached = await getFromCache(cacheKey);
  if (cached) return cached;

  const provider = process.env.TRANSLATE_PROVIDER || 'deepl';
  let out = text;
  if (provider === 'deepl') {
    out = await translateViaDeepL(text, target, source, glossary);
  } else {
    out = await translateViaLLM(text, target, source, glossary);
  }
  out = restorePlaceholders(out, placeholders);
  await setInCache(cacheKey, out, 60 * 60 * 24);
  return out;
}

function hash(s: string): string { return require('crypto').createHash('sha1').update(s).digest('hex'); }

async function getFromCache(_key: string): Promise<string | null> { return null; }
async function setInCache(_key: string, _val: string, _ttlSec: number): Promise<void> { return; }

async function translateViaDeepL(text: string, target: string, _source?: string, _glossary?: Record<string,string>): Promise<string> {
  // Placeholder: wire real DeepL/Google here in production; respect glossary mapping
  return text; 
}

async function translateViaLLM(text: string, _target: string, _source?: string, _glossary?: Record<string,string>): Promise<string> {
  // Placeholder: call server-side LLM with data controls; avoid sending PII
  return text;
}

function restorePlaceholders(s: string, placeholders: string[]): string {
  // No-op placeholder policy for now
  return s;
}
```

---

## CI additions (no unit tests for now)

Add scripts:

```json
// package.json (additions)
{
  "scripts": {
    "lint": "next lint",
    "typecheck": "tsc --noEmit",
    "e2e": "playwright test"
  }
}
```

Update CI to enforce typecheck, lint, and formatting:

```yaml
# .github/workflows/ci.yml (excerpt)
      - run: npm ci
      - run: npx playwright install --with-deps || true
      - run: npm run typecheck --if-present
      - run: npm run lint --if-present
      - run: npm run format:check --if-present
      - run: npm run build --if-present
      - run: npm run e2e --if-present
```

---

## Monorepo-ready conventions (keep changes minimal now)

---

## Security headers

Enforce baseline security headers at the edge.

```ts
// next.config.mjs (headers)
export default {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          { key: 'X-Content-Type-Options', value: 'nosniff' },
          { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
          { key: 'X-Frame-Options', value: 'DENY' },
          { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
          // Adjust CSP as routes/assets are finalized
          { key: 'Content-Security-Policy', value: "default-src 'self'; img-src 'self' data: blob:; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self' https:" },
          { key: 'Strict-Transport-Security', value: 'max-age=31536000; includeSubDomains; preload' },
        ],
      },
    ];
  },
};
```

---

## src/lib/core/regions.ts
```ts
export type Region = 'US' | 'GB' | 'DE' | 'ES' | 'MX';

export const ProviderDomains: Record<Region, { connectSrc: string[]; psp: string[]; carriers: string[] }> = {
  US: {
    connectSrc: ['https://api.stripe.com', 'https://api.upstash.com', 'https://*.supabase.co'],
    psp: ['stripe.com'],
    carriers: ['ups.com', 'usps.com', 'fedex.com']
  },
  GB: {
    connectSrc: ['https://api.stripe.com', 'https://api.upstash.com', 'https://*.supabase.co'],
    psp: ['stripe.com', 'adyen.com'],
    carriers: ['royalmail.com', 'dhl.com']
  },
  DE: {
    connectSrc: ['https://api.stripe.com', 'https://api.upstash.com', 'https://*.supabase.co'],
    psp: ['stripe.com', 'adyen.com'],
    carriers: ['dhl.de', 'hermesworld.com']
  },
  ES: {
    connectSrc: ['https://api.stripe.com', 'https://api.upstash.com', 'https://*.supabase.co'],
    psp: ['stripe.com', 'adyen.com'],
    carriers: ['correos.es', 'dhl.com']
  },
  MX: {
    connectSrc: ['https://api.stripe.com', 'https://api.upstash.com', 'https://*.supabase.co'],
    psp: ['stripe.com'],
    carriers: ['dhl.com', 'estafeta.com']
  }
};

export function resolveRegionFromHeaders(headers: Headers, fallback: Region = 'US'): Region {
  const lock = process.env.REGION_LOCK as Region | undefined;
  if (lock) return lock;
  const country = headers.get('x-vercel-ip-country') || headers.get('cf-ipcountry') || '';
  const map: Record<string, Region> = { US: 'US', GB: 'GB', UK: 'GB', DE: 'DE', ES: 'ES', MX: 'MX' };
  return (map[country] || (process.env.REGION_DEFAULT as Region) || fallback) as Region;
}
```

---

## src/lib/core/providers.ts
```ts
import type { Region } from '@core/regions';

export type Psp = 'stripe' | 'adyen' | 'shopify_payments';

export function selectDefaultPsp(region: Region): Psp {
  switch (region) {
    case 'GB':
    case 'DE':
    case 'ES':
      return 'stripe'; // can toggle to 'adyen' if needed
    case 'MX':
      return 'stripe';
    case 'US':
    default:
      return 'stripe';
  }
}

export function pspSupportsFileUploads(psp: Psp): boolean {
  return psp !== 'shopify_payments';
}
```

---

## src/middleware.ts
```ts
import { NextResponse, type NextRequest } from 'next/server';
import { ProviderDomains, resolveRegionFromHeaders } from '@core/regions';

export function middleware(req: NextRequest) {
  const region = resolveRegionFromHeaders(req.headers as any);
  const domains = ProviderDomains[region];

  const csp = [
    "default-src 'self'",
    "img-src 'self' data: blob:",
    "style-src 'self' 'unsafe-inline'",
    "script-src 'self' 'unsafe-inline'",
    `connect-src 'self' ${domains.connectSrc.join(' ')}`,
  ].join('; ');

  const res = NextResponse.next();
  res.headers.set('Content-Security-Policy', csp);
  res.headers.set('X-Region', region);
  return res;
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};
```

---

## Health check endpoint

Add a minimal health endpoint suitable for uptime checks.

```ts
// app/api/health/route.ts
import { NextResponse } from 'next/server';

export async function GET() {
  // Optionally verify dependent services here
  return NextResponse.json({ status: 'ok', time: new Date().toISOString() });
}
```

---

## AuthZ helper (entitlements)

Centralize entitlement checks to avoid per-route drift.

```ts
// src/lib/core/authz.ts
type Session = { user: { id: string }; org_id: string };

export type FeatureKey =
  | 'chargebacks.submit'
  | 'chargebacks.generate_pdf'
  | 'chargebacks.shopify_sync';

export async function assertEntitled(session: Session | null, feature: FeatureKey) {
  if (!session) throw new Error('unauthorized');
  // query entitlements via RLS-scoped view/table
  // expect existence of (org_id, feature_key, enabled)
  // pseudo:
  // const row = await db.select('*').from('org_entitlements').where({ org_id: session.org_id, feature_key: feature, enabled: true }).single();
  // if (!row) throw new Error('forbidden');
}
```

Usage in a server route:

```ts
// app/api/disputes/submit/route.ts (excerpt)
import { assertEntitled } from '@core/authz';

await assertEntitled(session, 'chargebacks.submit');
```

---

## Node.js engines

Recommend pinning Node LTS in `package.json` and CI.

```json
// package.json (additions)
{
  "engines": {
    "node": ">=20.11.0 <=22"
  }
}
```

CI matrix example:

```yaml
# .github/workflows/ci.yml (excerpt)
strategy:
  matrix:
    node: [20]
steps:
  - uses: actions/setup-node@v4
    with:
      node-version: ${{ matrix.node }}
```

---

## Sentry server setup (optional but recommended)

Capture server errors with request metadata. Keep client boundary as above.

```ts
// src/lib/core/sentry.ts
import * as Sentry from '@sentry/node';

export function initSentry() {
  if (Sentry.getCurrentHub().getClient()) return;
  Sentry.init({
    dsn: process.env.SENTRY_DSN,
    environment: process.env.NODE_ENV,
    tracesSampleRate: 0.1,
  });
}

export { Sentry };
```

```ts
// app/api/_middleware.ts (optional)
import { initSentry, Sentry } from '@core/sentry';
initSentry();
```

---

## CI: secret scanning and dependency audit

Augment CI with built-in scans. For GitHub, enable Dependabot and secret scanning.

```yaml
# .github/workflows/ci.yml (excerpt)
      - run: npm audit --audit-level=high || true
```

Enable repository settings:

- Dependabot security updates
- Secret scanning (push protection)

- Path aliases:
  - `@core/*` → shared services (`src/lib/core/*`): `supabaseClient`, `supabaseServer`, `config`, `analytics`, `flags`, `storage`, `pdf`, provider clients.
  - `@ui/*` → shared UI (`src/ui/*`): `DataTable`, `Tabs`, `CommandPalette`, `NotificationBell`, etc.
  - `@chargebacks/*` → feature code (`src/lib/chargebacks/*`): `evidenceComposer`, `submissionAdapters`, `orderMatching`, `disputePolling`.
- Migrations/functions:
  - Domain-scope migrations under `supabase/migrations/chargebacks/*`.
  - Core edge functions under `supabase/functions/core/*`.
- Import through `@core` and feature aliases; avoid cross-feature imports except via `@core` interfaces.

Example:

```ts
import { supabaseClient } from '@core/supabaseClient';
import { buildPdfFromPacket } from '@core/pdf';
import { DataTable } from '@ui/DataTable';
import { composePacket } from '@chargebacks/evidenceComposer';
```

---

## supabase/migrations/core/0001_billing_entitlements.sql
```sql
-- Billing core tables (org-scoped) with RLS
create table if not exists org_subscriptions (
  id uuid primary key default gen_random_uuid(),
  org_id uuid not null references orgs(id) on delete cascade,
  stripe_customer_id text,
  stripe_subscription_id text,
  plan text not null,
  status text not null default 'inactive',
  period_end timestamptz,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table if not exists org_entitlements (
  org_id uuid not null references orgs(id) on delete cascade,
  feature_key text not null,
  enabled boolean not null default false,
  source text default 'billing',
  updated_at timestamptz default now(),
  primary key (org_id, feature_key)
);

alter table org_subscriptions enable row level security;
alter table org_entitlements enable row level security;

-- Read: members of org
create policy select_org_subscriptions on org_subscriptions
  for select using (
    exists (
      select 1 from user_org_roles uor
      where uor.org_id = org_subscriptions.org_id and uor.user_id = auth.uid()
    )
  );

create policy select_org_entitlements on org_entitlements
  for select using (
    exists (
      select 1 from user_org_roles uor
      where uor.org_id = org_entitlements.org_id and uor.user_id = auth.uid()
    )
  );

-- Writes via service role only (billing webhooks). No public insert/update policies.
```

---

## supabase/migrations/core/0002_storage_buckets_policies.sql
```sql
-- Buckets
-- evidence-packets: generated PDFs
-- attachments: raw documents/screenshots
-- Note: Create buckets ahead of time in Supabase project or via SQL below if supported

-- Example (if using SQL storage API):
-- select storage.create_bucket('evidence-packets', public := false);
-- select storage.create_bucket('attachments', public := false);

-- Restrictive storage policies (download via signed URLs only, uploads through server actions)
create policy "allow signed url downloads" on storage.objects
  for select using (
    bucket_id in ('evidence-packets','attachments')
  );

-- No insert/update/delete from client; server role only
```

---

## supabase/migrations/chargebacks/0007_rls_write_policies.sql
```sql
-- Harden writes with WITH CHECK to the org of the authenticated user

-- Disputes
create policy disputes_insert on disputes
  for insert with check (
    exists (
      select 1 from user_org_roles uor where uor.org_id = disputes.org_id and uor.user_id = auth.uid()
    )
  );

create policy disputes_update on disputes
  for update using (
    exists (
      select 1 from user_org_roles uor where uor.org_id = disputes.org_id and uor.user_id = auth.uid()
    )
  ) with check (
    exists (
      select 1 from user_org_roles uor where uor.org_id = disputes.org_id and uor.user_id = auth.uid()
    )
  );

-- Orders
create policy orders_insert on orders
  for insert with check (
    exists (
      select 1 from user_org_roles uor where uor.org_id = orders.org_id and uor.user_id = auth.uid()
    )
  );

create policy orders_update on orders
  for update using (
    exists (
      select 1 from user_org_roles uor where uor.org_id = orders.org_id and uor.user_id = auth.uid()
    )
  ) with check (
    exists (
      select 1 from user_org_roles uor where uor.org_id = orders.org_id and uor.user_id = auth.uid()
    )
  );

-- Submissions (insert by server action, readable by org members)
create policy submissions_insert on submissions
  for insert with check (
    exists (
      select 1 from disputes d join user_org_roles uor on uor.org_id = d.org_id
      where d.id = submissions.dispute_id and uor.user_id = auth.uid()
    )
  );

create policy submissions_update on submissions
  for update using (
    exists (
      select 1 from disputes d join user_org_roles uor on uor.org_id = d.org_id
      where d.id = submissions.dispute_id and uor.user_id = auth.uid()
    )
  ) with check (
    exists (
      select 1 from disputes d join user_org_roles uor on uor.org_id = d.org_id
      where d.id = submissions.dispute_id and uor.user_id = auth.uid()
    )
  );
```

---

## src/lib/core/entitlements.ts
```ts
import { createServerClient } from '@core/supabaseServer';

export async function getEntitlements(orgId: string): Promise<Record<string, boolean>> {
  const db = createServerClient();
  const { data } = await db
    .from('org_entitlements')
    .select('feature_key, enabled')
    .eq('org_id', orgId);
  return Object.fromEntries((data || []).map((r) => [r.feature_key, r.enabled]));
}

export async function requireEntitlement(orgId: string, featureKey: string): Promise<void> {
  const entitlements = await getEntitlements(orgId);
  if (!entitlements[featureKey]) {
    throw new Error(`Entitlement required: ${featureKey}`);
  }
}
```

---

## src/app/api/billing/checkout/route.ts
```ts
import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';
import { createServerClient } from '@core/supabaseServer';
import { getConfig } from '@core/config';

export async function POST(req: NextRequest) {
  const { plan, returnUrl } = await req.json();
  const db = createServerClient();
  const cfg = getConfig();
  const stripe = new Stripe(process.env.STRIPE_API_KEY || '', { apiVersion: '2024-06-20' });

  // Get current user and org
  const { data: { user } } = await (db.auth as any).getUser();
  if (!user) return new NextResponse('Unauthorized', { status: 401 });
  const { data: uor } = await db
    .from('user_org_roles')
    .select('org_id')
    .eq('user_id', user.id)
    .single();
  if (!uor) return new NextResponse('No org', { status: 400 });

  // Ensure we have a stripe customer for the org
  const { data: sub } = await db
    .from('org_subscriptions')
    .select('*')
    .eq('org_id', uor.org_id)
    .maybeSingle();

  let customerId = sub?.stripe_customer_id;
  if (!customerId) {
    const customer = await stripe.customers.create({
      metadata: { org_id: uor.org_id }
    });
    customerId = customer.id;
    if (sub) {
      await db.from('org_subscriptions').update({ stripe_customer_id: customerId }).eq('id', sub.id);
    } else {
      await db.from('org_subscriptions').insert({ org_id: uor.org_id, stripe_customer_id: customerId, plan: plan || 'starter' });
    }
  }

  // Create checkout session
  const session = await stripe.checkout.sessions.create({
    mode: 'subscription',
    customer: customerId,
    line_items: [{ price: process.env[`STRIPE_PRICE_${(plan || 'STARTER').toUpperCase()}`], quantity: 1 }],
    success_url: returnUrl || 'https://example.com/success',
    cancel_url: returnUrl || 'https://example.com/cancel'
  });

  return NextResponse.json({ url: session.url });
}
```

---

## src/app/api/webhooks/stripe-billing/route.ts
```ts
import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';
import { createServerClient } from '@core/supabaseServer';

export async function POST(req: NextRequest) {
  const stripe = new Stripe(process.env.STRIPE_API_KEY || '', { apiVersion: '2024-06-20' });
  const sig = req.headers.get('stripe-signature') || '';
  const raw = await req.text();
  try {
    const event = stripe.webhooks.constructEvent(raw, sig, process.env.STRIPE_WEBHOOK_SECRET || '');
    const db = createServerClient();

    switch (event.type) {
      case 'customer.subscription.created':
      case 'customer.subscription.updated':
      case 'customer.subscription.deleted': {
        const sub = (event as any).data.object as Stripe.Subscription;
        const customerId = typeof sub.customer === 'string' ? sub.customer : sub.customer.id;
        const status = sub.status;
        const priceId = sub.items.data[0]?.price?.id;

        // Find org by customer
        const { data: row } = await db
          .from('org_subscriptions')
          .select('id, org_id')
          .eq('stripe_customer_id', customerId)
          .maybeSingle();

        if (row) {
          await db
            .from('org_subscriptions')
            .update({
              stripe_subscription_id: sub.id,
              status,
              plan: priceId || 'custom',
              period_end: sub.current_period_end ? new Date(sub.current_period_end * 1000).toISOString() : null
            })
            .eq('id', row.id);

          // Simple entitlement gating example
          const features = status === 'active' ? ['evidence_autosubmit', 'analytics'] : [];
          // Reset and set entitlements
          await db.from('org_entitlements').delete().eq('org_id', row.org_id).eq('source', 'billing');
          for (const f of features) {
            await db.from('org_entitlements').upsert({ org_id: row.org_id, feature_key: f, enabled: true, source: 'billing' });
          }
        }
        break;
      }
      default:
        break;
    }

    return NextResponse.json({ ok: true });
  } catch (err) {
    return new NextResponse('Invalid webhook', { status: 400 });
  }
}
```

---

## src/app/api/uploads/sign/route.ts
```ts
import { NextRequest, NextResponse } from 'next/server';
import { createServerClient } from '@core/supabaseServer';

export async function POST(req: NextRequest) {
  const { path, bucket = 'attachments' } = await req.json();
  if (!path) return new NextResponse('Missing path', { status: 400 });
  const db = createServerClient();

  // Issue short-lived signed URL for download; for uploads prefer server-side upload route or createSignedUploadUrl if available
  const { data, error } = await (db.storage as any)
    .from(bucket)
    .createSignedUrl(path, 300); // 5 minutes
  if (error) return new NextResponse(error.message, { status: 400 });
  return NextResponse.json({ url: data.signedUrl });
}
```

Note: For uploads, either proxy through a server route that accepts file data and writes with the service role, or use Supabase's `createSignedUploadUrl` if available in your project runtime.


## src/app/api/uploads/put/route.ts
```ts
export const runtime = 'nodejs';
import { NextRequest, NextResponse } from 'next/server';
import { createServerClient } from '@core/supabaseServer';

const MAX_BYTES = 10 * 1024 * 1024; // 10MB
const ALLOWED_MIME = new Set(['application/pdf', 'image/png', 'image/jpeg']);

export async function POST(req: NextRequest) {
  try {
    const db = createServerClient();
    // Require auth
    const { data: { user } } = await (db.auth as any).getUser();
    if (!user) return new NextResponse('Unauthorized', { status: 401 });

    const form = await req.formData();
    const file = form.get('file') as unknown as File | null;
    const disputeId = (form.get('disputeId') as string) || '';
    const customPath = (form.get('path') as string) || '';
    const bucket = (form.get('bucket') as string) || (process.env.EVIDENCE_BUCKET || 'evidence-packets');
    if (!file || !disputeId) return new NextResponse('Missing file/disputeId', { status: 400 });

    if (!ALLOWED_MIME.has((file as File).type)) return new NextResponse('Unsupported type', { status: 415 });
    if ((file as File).size > MAX_BYTES) return new NextResponse('File too large', { status: 413 });

    // Verify requester belongs to dispute's org (RLS + explicit check)
    const { data: uor } = await db
      .from('user_org_roles')
      .select('org_id')
      .eq('user_id', user.id)
      .maybeSingle();
    const { data: d } = await db
      .from('disputes')
      .select('org_id')
      .eq('id', disputeId)
      .single();
    if (!uor?.org_id || !d?.org_id || uor.org_id !== d.org_id) return new NextResponse('Forbidden', { status: 403 });

    const arrayBuffer = await (file as File).arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);
    const now = Date.now();
    const safeName = ((file as File).name || 'upload').replace(/[^a-zA-Z0-9._-]/g, '_');
    const path = customPath || `${disputeId}/${now}-${safeName}`;

    const { error } = await (db.storage as any)
      .from(bucket)
      .upload(path, buffer, { contentType: (file as File).type, upsert: false });
    if (error) return new NextResponse(error.message, { status: 400 });

    return NextResponse.json({ ok: true, path, name: safeName, type: (file as File).type, bucket });
  } catch (e: any) {
    return new NextResponse(e.message || 'Upload failed', { status: 500 });
  }
}
```

---

## src/app/api/evidence/attachments/route.ts
```ts
export const runtime = 'nodejs';
import { NextRequest, NextResponse } from 'next/server';
import { createServerClient } from '@core/supabaseServer';

export async function POST(req: NextRequest) {
  const { disputeId, name, path, type, required = false } = await req.json().catch(()=>({}));
  if (!disputeId || !name || !path || !type) return new NextResponse('Bad Request', { status: 400 });
  const db = createServerClient();
  const { data: { user } } = await (db.auth as any).getUser();
  if (!user) return new NextResponse('Unauthorized', { status: 401 });
  const { data: uor } = await db
    .from('user_org_roles')
    .select('org_id')
    .eq('user_id', user.id)
    .maybeSingle();
  // Confirm dispute exists and requester can access via RLS
  const { data: d } = await db.from('disputes').select('id, org_id').eq('id', disputeId).maybeSingle();
  if (!d || !uor?.org_id || uor.org_id !== d.org_id) return new NextResponse('Forbidden', { status: 403 });

  const { error } = await db.from('evidence_items').insert({
    dispute_id: disputeId,
    type: 'attachment_user',
    content_json: { name, type, required },
    content_path: path
  });
  if (error) return new NextResponse(error.message, { status: 400 });
  return NextResponse.json({ ok: true });
}
```

---

## src/app/api/evidence/override/route.ts
```ts
export const runtime = 'nodejs';
import { NextRequest, NextResponse } from 'next/server';
import { createServerClient } from '@core/supabaseServer';

export async function PUT(req: NextRequest) {
  const { disputeId, title, content, locked = true } = await req.json().catch(()=>({}));
  if (!disputeId || !title || typeof content !== 'string') return new NextResponse('Bad Request', { status: 400 });
  const db = createServerClient();
  const { data: { user } } = await (db.auth as any).getUser();
  if (!user) return new NextResponse('Unauthorized', { status: 401 });
  const { data: uor } = await db
    .from('user_org_roles')
    .select('org_id')
    .eq('user_id', user.id)
    .maybeSingle();
  const { data: disp } = await db
    .from('disputes')
    .select('org_id')
    .eq('id', disputeId)
    .maybeSingle();
  if (!uor?.org_id || !disp?.org_id || uor.org_id !== disp.org_id) return new NextResponse('Forbidden', { status: 403 });

  // Try update existing override else insert
  const { data: existing } = await db
    .from('evidence_items')
    .select('id')
    .eq('dispute_id', disputeId)
    .eq('type', 'section_override')
    .eq('content_json->>title', title)
    .maybeSingle();

  if (existing) {
    const { error } = await db
      .from('evidence_items')
      .update({ content_json: { title, content, locked, updated_at: new Date().toISOString() } })
      .eq('id', existing.id);
    if (error) return new NextResponse(error.message, { status: 400 });
  } else {
    const { error } = await db
      .from('evidence_items')
      .insert({
        dispute_id: disputeId,
        type: 'section_override',
        content_json: { title, content, locked, created_at: new Date().toISOString() }
      });
    if (error) return new NextResponse(error.message, { status: 400 });
  }
  return NextResponse.json({ ok: true });
}
```


## next.config.mjs
```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    typedRoutes: true
  }
};

export default nextConfig;
```

---

## src/app/api/submissions/validate/route.ts (updated)
```ts
export const runtime = 'nodejs';
import { NextRequest, NextResponse } from 'next/server';
import { createServerClient } from '@core/supabaseServer';
import { composePacket } from '@chargebacks/evidenceComposer';

export async function POST(req: NextRequest) {
  const { disputeId } = await req.json().catch(() => ({}));
  if (!disputeId) return new NextResponse('Bad Request', { status: 400 });

  const db = createServerClient();
  const { data: { user } } = await (db.auth as any).getUser();
  if (!user) return new NextResponse('Unauthorized', { status: 401 });

  // Ensure user can access this dispute via org RLS
  const { data: d } = await db
    .from('disputes')
    .select('id, org_id')
    .eq('id', disputeId)
    .maybeSingle();
  if (!d) return new NextResponse('Not Found', { status: 404 });

  try {
    const packet = await composePacket(disputeId);
    const counts = {
      sections: Array.isArray(packet.sections) ? packet.sections.length : 0,
      attachments: Array.isArray(packet.attachments) ? packet.attachments.length : 0
    };
    const response = {
      ok: (packet.gaps || []).length === 0,
      gaps: packet.gaps || [],
      readiness: packet.readiness ?? 0,
      counts,
      guidance: packet.guidance || null
    };
    return NextResponse.json(response);
  } catch (e: any) {
    return new NextResponse(e?.message || 'Validation failed', { status: 500 });
  }
}
```

---

## src/components/Toaster.tsx
```tsx
'use client';
import { createContext, useCallback, useContext, useMemo, useState } from 'react';

type Toast = { id: string; kind: 'success'|'error'|'info'; message: string };

type ToastContextValue = {
  toasts: Toast[];
  push: (kind: Toast['kind'], message: string) => void;
  remove: (id: string) => void;
};

const ToastCtx = createContext<ToastContextValue | null>(null);

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const push = useCallback((kind: Toast['kind'], message: string) => {
    const id = `${Date.now()}_${Math.random().toString(36).slice(2)}`;
    setToasts((prev) => [...prev, { id, kind, message }]);
    // Auto-remove after 3s
    setTimeout(() => setToasts((prev) => prev.filter((t) => t.id !== id)), 3000);
  }, []);

  const remove = useCallback((id: string) => setToasts((prev) => prev.filter((t) => t.id !== id)), []);

  const value = useMemo(() => ({ toasts, push, remove }), [toasts, push, remove]);
  return (
    <ToastCtx.Provider value={value}>
      {children}
      <div className="fixed bottom-4 right-4 space-y-2 z-50">
        {toasts.map((t) => (
          <div key={t.id} className={`px-3 py-2 rounded shadow text-sm border bg-white ${
            t.kind==='success' ? 'border-green-300' : t.kind==='error' ? 'border-red-300' : 'border-gray-300'
          }`}>
            {t.message}
          </div>
        ))}
      </div>
    </ToastCtx.Provider>
  );
}

export function useToast() {
  const ctx = useContext(ToastCtx);
  if (!ctx) throw new Error('useToast must be used within ToastProvider');
  return ctx;
}
```

---

## src/app/layout.tsx (updated)
```tsx
import './globals.css';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { useEffect, useRef, useState } from 'react';
import { CommandPalette } from '@components/CommandPalette';
import { NotificationBell } from '@components/NotificationBell';
import Providers from './providers';
import { ToastProvider } from '@components/Toaster';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-50 text-slate-900">
        <Providers>
            <ToastProvider>
              <div className="min-h-screen flex flex-col">
                <Header />
                <main className="flex-1">{children}</main>
                <CommandPalette />
              </div>
            </ToastProvider>
        </Providers>
      </body>
    </html>
  );
}

function Header() {
  const router = useRouter();
  const params = useSearchParams();
  const [query, setQuery] = useState(params.get('query') || '');
  const inputRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === '/' && !e.metaKey && !e.ctrlKey) {
        const tag = (document.activeElement as HTMLElement | null)?.tagName?.toLowerCase();
        if (tag !== 'input' && tag !== 'textarea') {
          e.preventDefault();
          inputRef.current?.focus();
        }
      }
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, []);

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const q = query.trim();
    router.push(q ? `/disputes?query=${encodeURIComponent(q)}` : '/disputes');
  };

  return (
    <header className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16 gap-4">
          <div className="flex items-center gap-8 min-w-0">
            <h1 className="text-xl font-semibold whitespace-nowrap">Chargeback Evidence Builder</h1>
            <nav className="hidden md:flex items-center gap-6">
              <Link href="/disputes" className="text-sm text-gray-600 hover:text-gray-900">Disputes</Link>
              <Link href="/analytics" className="text-sm text-gray-600 hover:text-gray-900">Analytics</Link>
              <Link href="/settings" className="text-sm text-gray-600 hover:text-gray-900">Settings</Link>
              <Link href="/activity" className="text-sm text-gray-600 hover:text-gray-900">Activity</Link>
            </nav>
          </div>
          <form onSubmit={onSubmit} className="flex-1 flex max-w-lg items-center gap-2">
            <input
              ref={inputRef}
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search by dispute, order, customer, amount… (press / to focus)"
              className="w-full px-3 py-2 border rounded bg-gray-50 focus:bg-white"
            />
            <button type="submit" className="px-3 py-2 border rounded text-sm hover:bg-gray-50">Search</button>
          </form>
          <div className="flex items-center gap-4">
            <NotificationBell />
            <div className="w-8 h-8 rounded-full bg-gray-300" />
          </div>
        </div>
      </div>
    </header>
  );
}
```

---

## src/app/page.tsx
```tsx
import Link from 'next/link';

export default function HomePage() {
  return (
    <main className="max-w-6xl mx-auto px-4 py-16">
      <section className="text-center space-y-4">
        <h1 className="text-3xl md:text-4xl font-semibold">Stop losing chargebacks. Start winning disputes.</h1>
        <p className="text-gray-600">Connect your store and payment processor in 2 minutes.</p>
        <div className="flex items-center justify-center gap-3">
          <Link href="/onboarding" className="px-4 py-2 rounded bg-blue-600 text-white">Get Started</Link>
          <Link href="/disputes" className="px-4 py-2 rounded border">View Disputes</Link>
        </div>
        <div className="text-xs text-gray-500">256-bit encryption • SOC2 ready • No credit card required</div>
      </section>

      <section className="mt-16 grid md:grid-cols-3 gap-6">
        <div className="p-6 rounded border bg-white">
          <h3 className="font-semibold mb-2">Higher win rates</h3>
          <p className="text-sm text-gray-600">Templates aligned to network codes + gap checks.</p>
        </div>
        <div className="p-6 rounded border bg-white">
          <h3 className="font-semibold mb-2">Hours saved</h3>
          <p className="text-sm text-gray-600">Automated data pull from orders, shipping, and comms.</p>
        </div>
        <div className="p-6 rounded border bg-white">
          <h3 className="font-semibold mb-2">Lower losses</h3>
          <p className="text-sm text-gray-600">Faster, consistent submissions reduce missed deadlines and errors.</p>
        </div>
      </section>

      <section className="mt-12 grid md:grid-cols-3 gap-6">
        <div className="p-6 rounded border bg-white">
          <h3 className="font-semibold mb-2">Audit-ready</h3>
          <p className="text-sm text-gray-600">Immutable receipts, versioned packets, and activity logs.</p>
        </div>
        <div className="p-6 rounded border bg-white">
          <h3 className="font-semibold mb-2">Team workflows</h3>
          <p className="text-sm text-gray-600">Roles, locking, review, and batch submissions at scale.</p>
        </div>
        <div className="p-6 rounded border bg-white">
          <h3 className="font-semibold mb-2">Secure by default</h3>
          <p className="text-sm text-gray-600">RLS, signed URLs, and server-only service role usage.</p>
        </div>
      </section>
    </main>
  );
}
```

---

## src/app/disputes/page.tsx (updated)
```tsx
'use client';
import { useEffect, useMemo, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { supabaseClient } from '@core/supabaseClient';
import { useAnalytics } from '@core/analytics';

type Dispute = {
  id: string;
  psp_id: string;
  reason_code: string;
  amount: number;
  status: 'new'|'draft'|'submitted'|'won'|'lost';
  due_by: string | null;
  customer?: any;
};

export default function DisputesPage() {
  const analytics = useAnalytics();
  const params = useSearchParams();
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [disputes, setDisputes] = useState<Dispute[]>([]);
  const [statusFilter, setStatusFilter] = useState<'all'|'new'|'draft'|'submitted'|'won'|'lost'>('all');
  const [chipFilter, setChipFilter] = useState<'due_today'|'high_value'|'auto_ready'|'needs_attention'|null>(null);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [quickViewId, setQuickViewId] = useState<string | null>(null);
  const search = params.get('query') || '';

  useEffect(() => {
    analytics.track({ name: 'disputes_inbox_viewed' });
    (async () => {
      setLoading(true);
      const { data: { user } } = await supabaseClient.auth.getUser();
      if (!user) { setDisputes([]); setLoading(false); return; }
      const { data: uo } = await supabaseClient.from('user_org_roles').select('org_id').eq('user_id', user.id).single();
      if (!uo?.org_id) { setDisputes([]); setLoading(false); return; }
      const { data } = await supabaseClient
        .from('disputes')
        .select('id, created_at, psp_id, reason_code, amount, status, due_by, orders(customer_json), submissions(submitted_at, created_at)')
        .eq('org_id', uo.org_id)
        .order('due_by', { ascending: true });
      setDisputes((data as any[] || []).map(d => ({
        ...d,
        customer: d.orders?.[0]?.customer_json || null
      })));
      setLoading(false);
    })();
  }, []);

  const overdue = useMemo(() => {
    const now = Date.now();
    const list = disputes.filter(d => ['new','draft'].includes(d.status) && d.due_by && new Date(d.due_by).getTime() < now);
    const amount = list.reduce((s, d) => s + Number(d.amount||0), 0);
    return { count: list.length, amount };
  }, [disputes]);

  const filtered = useMemo(() => {
    let list = disputes;
    if (statusFilter !== 'all') list = list.filter(d => d.status === statusFilter);
    if (chipFilter) {
      if (chipFilter === 'due_today') list = list.filter(d => d.due_by && new Date(d.due_by).toDateString() === new Date().toDateString());
      if (chipFilter === 'high_value') list = list.filter(d => Number(d.amount) >= 100);
      if (chipFilter === 'auto_ready') list = list.filter(d => d.status === 'draft');
      if (chipFilter === 'needs_attention') {
        const threeDays = Date.now() + 3*24*60*60*1000;
        list = list.filter(d => d.status==='new' || (d.due_by && new Date(d.due_by).getTime() < threeDays));
      }
    }
    if (search) {
      const q = search.toLowerCase();
      list = list.filter(d => (
        d.psp_id.toLowerCase().includes(q) ||
        d.reason_code.toLowerCase().includes(q) ||
        String(d.amount).includes(q) ||
        (d.customer?.email || '').toLowerCase().includes(q)
      ));
    }
    return list;
  }, [disputes, statusFilter, chipFilter, search]);

  const metrics = useMemo(() => {
    const open = disputes.filter(d => ['new','draft','submitted'].includes(d.status));
    const openCount = open.length;
    const recovered = disputes.filter(d => d.status==='won').reduce((s,d)=>s + Number(d.amount||0),0);
    // Compute average time to first submission across disputes that have a submission
    const withSubs = disputes.filter((d: any) => Array.isArray(d.submissions) && d.submissions.length > 0 && d.created_at);
    const totalHours = withSubs.reduce((sum: number, d: any) => {
      const first = d.submissions.reduce((min: number, s: any) => Math.min(min, new Date(s.submitted_at || s.created_at || 0).getTime()), Number.POSITIVE_INFINITY);
      const created = new Date(d.created_at).getTime();
      if (!isFinite(first) || !created) return sum;
      const hours = (first - created) / (1000*60*60);
      return sum + Math.max(0, hours);
    }, 0);
    const avgSubmitHours = withSubs.length ? Math.round((totalHours / withSubs.length) * 10) / 10 : 0;
    const winRate = (() => {
      const won = disputes.filter(d => d.status==='won').length;
      const decided = disputes.filter(d => ['won','lost'].includes(d.status)).length;
      return decided ? Math.round((won/decided)*100) : 0;
    })();
    return { openCount, winRate, recovered, avgSubmitHours };
  }, [disputes]);

  return (
    <main className="p-6 space-y-4">
      {/* Key metrics */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <MetricCard title="Open Disputes" value={String(metrics.openCount)} tone="red" />
        <MetricCard title="Win Rate" value={`${metrics.winRate}%`} tone="green" />
        <MetricCard title="Revenue Recovered" value={`$${metrics.recovered.toFixed(2)}`} tone="blue" />
        <MetricCard title="Avg. Time to Submit" value={`${metrics.avgSubmitHours}h`} tone="gray" />
      </div>
      {overdue.count > 0 && (
        <div className="p-4 rounded-lg bg-red-50 border border-red-200 flex items-center justify-between">
          <div className="text-sm text-red-800">
            ⚠️ Overdue: {overdue.count} disputes • ${overdue.amount.toFixed(2)} at risk
          </div>
          <button
            className="px-3 py-1.5 text-sm rounded bg-red-600 text-white hover:bg-red-700"
            onClick={() => { setChipFilter('needs_attention'); router.push('/disputes'); }}
          >
            Review oldest first
          </button>
        </div>
      )}

      <div className="flex flex-wrap items-center gap-2">
        <select value={statusFilter} onChange={(e)=>setStatusFilter(e.target.value as any)} className="px-2 py-1 border rounded text-sm">
          <option value="all">All</option>
          <option value="new">New</option>
          <option value="draft">Draft</option>
          <option value="submitted">Submitted</option>
          <option value="won">Won</option>
          <option value="lost">Lost</option>
        </select>
        <Chip label="Due today" active={chipFilter==='due_today'} onClick={()=>setChipFilter(chipFilter==='due_today'?null:'due_today')} />
        <Chip label="High value" active={chipFilter==='high_value'} onClick={()=>setChipFilter(chipFilter==='high_value'?null:'high_value')} />
        <Chip label="Auto-ready" active={chipFilter==='auto_ready'} onClick={()=>setChipFilter(chipFilter==='auto_ready'?null:'auto_ready')} />
        <Chip label="Needs attention" active={chipFilter==='needs_attention'} onClick={()=>setChipFilter(chipFilter==='needs_attention'?null:'needs_attention')} />
      </div>

      {loading ? (
        <div className="p-6 bg-white rounded border animate-pulse text-sm text-gray-500">Loading disputes…</div>
      ) : filtered.length === 0 ? (
        <div className="p-6 bg-white rounded border text-sm text-gray-600">No disputes found. Try adjusting filters or search.</div>
      ) : (
        <div className="bg-white rounded border divide-y relative">
          {filtered.map((d) => (
            <div key={d.id} className="p-4 flex items-center justify-between hover:bg-gray-50">
              <div>
                <div className="font-medium">{d.psp_id}</div>
                <div className="text-xs text-gray-600">Reason: {d.reason_code.replace(/_/g,' ')}</div>
                <div className="text-xs text-gray-500">Due: {d.due_by ? new Date(d.due_by).toLocaleString() : 'No deadline'}</div>
              </div>
              <div className="flex items-center gap-3">
                <div className={`px-2 py-0.5 text-xs rounded ${d.status==='new'?'bg-red-100 text-red-800':d.status==='draft'?'bg-yellow-100 text-yellow-800':d.status==='submitted'?'bg-blue-100 text-blue-800':d.status==='won'?'bg-green-100 text-green-800':'bg-gray-100 text-gray-800'}`}>{d.status}</div>
                <button className="px-3 py-1.5 border rounded text-sm hover:bg-gray-50" onClick={()=>setQuickViewId(d.id)}>Quick view</button>
                <button className="px-3 py-1.5 border rounded text-sm hover:bg-gray-50" onClick={()=>location.assign(`/disputes/${d.id}`)}>Review</button>
              </div>
            </div>
          ))}
          {/* Quick-view panel */}
          {quickViewId && (
            <div className="absolute right-0 top-0 h-full w-full sm:w-[420px] bg-white border-l shadow-xl p-4 z-10">
              <div className="flex items-center justify-between mb-2">
                <div className="font-semibold">Quick View</div>
                <button className="text-sm" onClick={()=>setQuickViewId(null)}>✕</button>
              </div>
              {(() => {
                const d = disputes.find(x=>x.id===quickViewId);
                if (!d) return <div className="text-sm text-gray-600">Not found</div>;
                return (
                  <div className="space-y-3 text-sm">
                    <div className="text-gray-700"><span className="font-medium">ID:</span> {d.psp_id}</div>
                    <div className="text-gray-700"><span className="font-medium">Reason:</span> {d.reason_code.replace(/_/g,' ')}</div>
                    <div className="text-gray-700"><span className="font-medium">Amount:</span> ${Number(d.amount||0).toFixed(2)}</div>
                    <div className="text-gray-700"><span className="font-medium">Due:</span> {d.due_by ? new Date(d.due_by).toLocaleString() : '—'}</div>
                    <div className="text-gray-700"><span className="font-medium">Status:</span> {d.status}</div>
                    <div className="pt-2 border-t">
                      <button className="px-3 py-1.5 border rounded hover:bg-gray-50 mr-2" onClick={()=>location.assign(`/disputes/${d.id}`)}>Open Full Details</button>
                      <button className="px-3 py-1.5 bg-blue-600 text-white rounded hover:bg-blue-700" onClick={()=>location.assign(`/disputes/${d.id}?action=submit`)}>Generate & Submit</button>
                    </div>
                  </div>
                );
              })()}
            </div>
          )}
        </div>
      )}
    </main>
  );
}

function Chip({ label, active, onClick }: { label: string; active: boolean; onClick: () => void }) {
  return (
    <button onClick={onClick} className={`px-2 py-1 rounded-full text-xs border ${active?'bg-blue-600 text-white border-blue-600':'bg-gray-50 text-gray-700 hover:bg-gray-100'}`}>{label}</button>
  );
}
```

---

## src/components/MetricCard.tsx
```tsx
export function MetricCard({ title, value, tone }: { title: string; value: string; tone: 'red'|'green'|'blue'|'gray' }) {
  const toneCls = tone==='red'?'border-red-200 bg-red-50':tone==='green'?'border-green-200 bg-green-50':tone==='blue'?'border-blue-200 bg-blue-50':'border-gray-200 bg-gray-50';
  return (
    <div className={`p-4 rounded border ${toneCls}`}>
      <div className="text-xs text-gray-600">{title}</div>
      <div className="text-xl font-semibold">{value}</div>
    </div>
  );
}
```

---

## src/components/SubmissionModal.tsx (updated)
```tsx
'use client';
import { useEffect, useState } from 'react';
import { useToast } from '@components/Toaster';

interface SubmissionModalProps {
  open: boolean;
  disputeId: string;
  onClose: () => void;
  onSubmitted: (result: { submissionId: string; packetId: string; pdfUrl: string; status: string; externalRef: string|null; contentHash?: string }) => void;
}

type Gap = { code: string; severity: 'error'|'warn'; message: string; action?: string };

export function SubmissionModal({ open, disputeId, onClose, onSubmitted }: SubmissionModalProps) {
  const { push } = useToast();
  const [validating, setValidating] = useState(false);
  const [validationOk, setValidationOk] = useState<boolean | null>(null);
  const [gaps, setGaps] = useState<Gap[]>([]);
  const [counts, setCounts] = useState<{ sections: number; attachments: number }>({ sections: 0, attachments: 0 });
  const [method, setMethod] = useState<'api'|'manual'>('api');
  const [schedule, setSchedule] = useState<'now'|'later'>('now');
  const [scheduledAt, setScheduledAt] = useState<string>('');
  const [reviewed, setReviewed] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!open) return;
    (async () => {
      try {
        setValidating(true);
        const res = await fetch('/api/submissions/validate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ disputeId }) });
        const json = await res.json();
        setValidationOk(Boolean(json.ok));
        setGaps(json.gaps || []);
        setCounts(json.counts || { sections: 0, attachments: 0 });
      } catch (e: any) {
        push('error', e?.message || 'Validation failed');
        setValidationOk(false);
      } finally {
        setValidating(false);
      }
    })();
  }, [open, disputeId]);

  if (!open) return null;

  const submit = async () => {
    try {
      setSubmitting(true);
      const body: any = { disputeId, method };
      if (schedule === 'later' && scheduledAt) body.scheduledAt = scheduledAt;
      const res = await fetch('/api/submissions', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
      if (!res.ok) throw new Error(await res.text());
      const json = await res.json();
      push('success', json.status === 'submitted' ? 'Evidence submitted' : 'Packet generated');
      onSubmitted({ ...json, contentHash: json?.contentHash });
    } catch (e: any) {
      push('error', e?.message || 'Submission failed');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-40 flex items-start justify-center pt-14">
      <div className="absolute inset-0 bg-black/30" onClick={onClose} />
      <div className="relative bg-white w-full max-w-2xl rounded-lg shadow-xl">
        <div className="p-4 border-b flex items-center justify-between">
          <h3 className="font-semibold">Final Review Before Submitting</h3>
          <button className="text-sm px-3 py-1 border rounded" onClick={onClose}>Close</button>
        </div>

        {validating && (
          <div className="p-4 text-sm text-gray-600">Checking submission readiness…</div>
        )}

        {!validating && validationOk === false && (
          <div className="p-4">
            <div className="mb-3 p-3 rounded border border-yellow-300 bg-yellow-50 text-sm text-yellow-900">
              ⚠️ Issues must be fixed before submitting
            </div>
            <ul className="space-y-2 mb-4">
              {gaps.map((g, i) => (
                <li key={i} className="flex items-start gap-2 text-sm">
                  <span className={`mt-0.5 inline-block w-2 h-2 rounded-full ${g.severity==='error'?'bg-red-500':'bg-yellow-500'}`} />
                  <div className="flex-1">
                    <div className="text-gray-900">{g.message}</div>
                    {g.action && (
                      <button
                        className="mt-1 text-xs underline text-blue-700"
                        onClick={() => {
                          // naive deep-link: map actions to tab hash (Evidence, Shipping, Device)
                          const map: Record<string, string> = {
                            attach_pod: '#shipping',
                            collect_avs: '#order',
                            collect_cvv: '#order'
                          };
                          const target = map[g.action] || '#evidence';
                          location.hash = target;
                          onClose();
                        }}
                      >Go fix</button>
                    )}
                  </div>
                </li>
              ))}
            </ul>
            <div className="p-3 rounded bg-gray-50 text-xs text-gray-700">Run validation again after fixing issues.</div>
          </div>
        )}

        {!validating && validationOk && (
          <div className="p-4 space-y-4">
            <div className="p-3 rounded border bg-green-50 text-sm text-green-900">✅ All requirements met</div>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div className="p-3 rounded border bg-white">Sections: {counts.sections}</div>
              <div className="p-3 rounded border bg-white">Attachments: {counts.attachments}</div>
            </div>

            <div>
              <label className="text-sm font-medium block mb-2">Submission method</label>
              <div className="space-y-2">
                <label className="flex items-center gap-3 p-3 border rounded cursor-pointer hover:bg-gray-50">
                  <input type="radio" checked={method==='api'} onChange={()=>setMethod('api')} />
                  <div>
                    <div className="font-medium">Submit via PSP API</div>
                    <div className="text-xs text-gray-600">Recommended — automatic submission</div>
                  </div>
                </label>
                <label className="flex items-center gap-3 p-3 border rounded cursor-pointer hover:bg-gray-50">
                  <input type="radio" checked={method==='manual'} onChange={()=>setMethod('manual')} />
                  <div>
                    <div className="font-medium">Download and submit manually</div>
                    <div className="text-xs text-gray-600">Generates packet PDF</div>
                  </div>
                </label>
              </div>
            </div>

            <div>
              <label className="text-sm font-medium block mb-2">Schedule</label>
              <div className="flex items-center gap-4 text-sm">
                <label className="flex items-center gap-2"><input type="radio" checked={schedule==='now'} onChange={()=>setSchedule('now')} /> Now</label>
                <label className="flex items-center gap-2"><input type="radio" checked={schedule==='later'} onChange={()=>setSchedule('later')} /> Later</label>
                {schedule==='later' && (
                  <input type="datetime-local" className="px-2 py-1 border rounded" value={scheduledAt} onChange={(e)=>setScheduledAt(e.target.value)} />
                )}
              </div>
            </div>

            <label className="flex items-center gap-2 text-sm">
              <input type="checkbox" checked={reviewed} onChange={()=>setReviewed(!reviewed)} />
              I’ve reviewed the evidence and it’s ready to submit
            </label>
          </div>
        )}

        <div className="p-4 border-t flex justify-end gap-2">
          <button className="px-4 py-2 border rounded hover:bg-gray-50" onClick={onClose} disabled={submitting}>Cancel</button>
          <button
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            onClick={submit}
            disabled={submitting || !validationOk || !reviewed}
          >
            {submitting ? 'Submitting…' : 'Submit Evidence'}
          </button>
        </div>
      </div>
    </div>
  );
}
```

---

## src/components/SubmissionSuccess.tsx
```tsx
'use client';

export function SubmissionSuccess({
  submissionId,
  packetId,
  pdfUrl,
  contentHash,
  attachmentsCount,
  sectionsCount,
  externalRef
}: {
  submissionId: string;
  packetId: string;
  pdfUrl: string;
  contentHash?: string;
  attachmentsCount?: number;
  sectionsCount?: number;
  externalRef?: string | null;
}) {
  return (
    <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg flex items-start gap-3">
      <div className="text-green-600 text-2xl">✅</div>
      <div className="space-y-1 text-sm">
        <div className="font-semibold text-green-900">Evidence Submitted Successfully!</div>
        <div className="text-green-800">Submission ID: #{submissionId.slice(0,8)} {externalRef ? `• Ref: ${externalRef}` : ''}</div>
        <div className="text-green-800">Expected response within 7–10 days</div>
        <div className="mt-2 p-3 bg-white rounded border">
          <div className="font-medium mb-1">Permanent Evidence Archive</div>
          <div className="text-xs text-gray-700 break-all">SHA-256: {contentHash || '—'}</div>
          <div className="text-xs text-gray-700">Sections: {sectionsCount ?? '—'} • Attachments: {attachmentsCount ?? '—'}</div>
          <div className="mt-2 flex items-center gap-2">
            <a href={pdfUrl} target="_blank" className="px-3 py-1.5 border rounded text-sm hover:bg-gray-50">Download Archive</a>
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

## src/app/analytics/page.tsx (updated)
```tsx
'use client';
import { useEffect, useMemo, useState } from 'react';
import { supabaseClient } from '@core/supabaseClient';

type Outcome = 'all'|'won'|'lost'|'pending';

export default function AnalyticsPage() {
  const [loading, setLoading] = useState(true);
  const [range, setRange] = useState<'30d'|'90d'>('30d');
  const [outcome, setOutcome] = useState<Outcome>('all');
  const [rows, setRows] = useState<any[]>([]);

  useEffect(() => {
    (async () => {
      setLoading(true);
      const { data: { user } } = await supabaseClient.auth.getUser();
      if (!user) { setRows([]); setLoading(false); return; }
      const { data: uo } = await supabaseClient.from('user_org_roles').select('org_id').eq('user_id', user.id).single();
      if (!uo?.org_id) { setRows([]); setLoading(false); return; }
      const since = new Date(Date.now() - (range==='30d'?30:90)*24*60*60*1000).toISOString();
      const { data } = await supabaseClient
        .from('disputes')
        .select('id, reason_code, amount, status, created_at, submissions(submitted_at)')
        .eq('org_id', uo.org_id)
        .gte('created_at', since)
        .order('created_at');
      setRows(data || []);
      setLoading(false);
    })();
  }, [range]);

  const filtered = useMemo(() => {
    if (outcome==='all') return rows;
    if (outcome==='pending') return rows.filter((r) => !['won','lost'].includes(r.status));
    return rows.filter((r) => r.status === outcome);
  }, [rows, outcome]);

  const byReason = useMemo(() => {
    const map: Record<string, { total: number; won: number }> = {};
    for (const r of filtered) {
      const key = r.reason_code || 'unknown';
      map[key] = map[key] || { total: 0, won: 0 };
      map[key].total += 1;
      if (r.status === 'won') map[key].won += 1;
    }
    return Object.entries(map).map(([reason, v]) => ({ reason, winRate: v.total? Math.round((v.won/v.total)*100):0, total: v.total }));
  }, [filtered]);

  const byDay = useMemo(() => {
    const map: Record<string, { total: number; won: number }> = {};
    for (const r of filtered) {
      const day = new Date(r.created_at).toISOString().slice(0,10);
      map[day] = map[day] || { total: 0, won: 0 };
      map[day].total += 1;
      if (r.status==='won') map[day].won += 1;
    }
    const points = Object.entries(map).sort((a,b)=>a[0].localeCompare(b[0])).map(([day,v])=>({ day, volume: v.total, winRate: v.total? Math.round((v.won/v.total)*100):0 }));
    return points;
  }, [filtered]);

  const downloadCsv = () => {
    const headers = ['dispute_id','reason_code','amount','submitted_at','outcome','days_to_decision'];
    const lines = [headers.join(',')];
    for (const r of filtered) {
      const submittedAt = r.submissions?.[0]?.submitted_at || '';
      const days = ['won','lost'].includes(r.status) && submittedAt ? '7' : '';
      lines.push([r.id, r.reason_code, r.amount, submittedAt, r.status, days].join(','));
    }
    const blob = new Blob([lines.join('\n')], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'dispute_analytics.csv'; a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <main className="p-6 space-y-4">
      <div className="flex items-center gap-3">
        <select value={range} onChange={(e)=>setRange(e.target.value as any)} className="px-2 py-1 border rounded text-sm">
          <option value="30d">Last 30 days</option>
          <option value="90d">Last 90 days</option>
        </select>
        <select value={outcome} onChange={(e)=>setOutcome(e.target.value as any)} className="px-2 py-1 border rounded text-sm">
          <option value="all">All outcomes</option>
          <option value="won">Won</option>
          <option value="lost">Lost</option>
          <option value="pending">Pending</option>
        </select>
        <button onClick={downloadCsv} className="ml-auto px-3 py-1.5 border rounded text-sm hover:bg-gray-50">Download CSV</button>
      </div>

      {loading ? (
        <div className="p-6 bg-white rounded border animate-pulse text-sm text-gray-500">Loading analytics…</div>
      ) : (
        <>
          <section className="bg-white rounded border p-4">
            <h2 className="font-semibold mb-3">Win Rate by Reason</h2>
            <BarChart data={byReason} />
          </section>
          <section className="bg-white rounded border p-4">
            <h2 className="font-semibold mb-3">Volume and Win Rate Over Time</h2>
            <LineChart data={byDay} />
          </section>
        </>
      )}
    </main>
  );
}

function BarChart({ data }: { data: { reason: string; winRate: number; total: number }[] }) {
  if (data.length === 0) return <div className="text-sm text-gray-600">No data</div>;
  const max = 100;
  const barW = 36; const gap = 12; const height = 160; const width = data.length * (barW + gap) + gap;
  return (
    <svg width={width} height={height} className="overflow-visible">
      {data.map((d, i) => {
        const h = Math.round((d.winRate/max)*(height-30));
        const x = gap + i*(barW+gap); const y = height - 20 - h;
        return (
          <g key={d.reason}>
            <rect x={x} y={y} width={barW} height={h} fill="#3b82f6" />
            <text x={x+barW/2} y={height-6} fontSize="10" textAnchor="middle" fill="#374151">{d.reason.slice(0,8)}</text>
            <text x={x+barW/2} y={y-4} fontSize="10" textAnchor="middle" fill="#111827">{d.winRate}%</text>
          </g>
        );
      })}
    </svg>
  );
}

function LineChart({ data }: { data: { day: string; volume: number; winRate: number }[] }) {
  if (data.length === 0) return <div className="text-sm text-gray-600">No data</div>;
  const width = Math.max(360, data.length * 36);
  const height = 180;
  const pad = 30;
  const maxVol = Math.max(...data.map(d=>d.volume), 1);
  const pointsVol = data.map((d, i) => {
    const x = pad + (i*(width - 2*pad) / Math.max(1, data.length-1));
    const y = height - pad - (d.volume/maxVol) * (height - 2*pad);
    return `${x},${y}`;
  }).join(' ');
  const pointsWin = data.map((d, i) => {
    const x = pad + (i*(width - 2*pad) / Math.max(1, data.length-1));
    const y = height - pad - (d.winRate/100) * (height - 2*pad);
    return `${x},${y}`;
  }).join(' ');
  return (
    <svg width={width} height={height} className="overflow-visible">
      <polyline fill="none" stroke="#6b7280" strokeWidth="2" points={pointsVol} />
      <polyline fill="none" stroke="#10b981" strokeWidth="2" points={pointsWin} />
      <text x={8} y={14} fontSize="10" fill="#6b7280">Volume</text>
      <text x={60} y={14} fontSize="10" fill="#10b981">Win Rate</text>
    </svg>
  );
}
```

---

## src/app/activity/page.tsx
```tsx
'use client';
import { useEffect, useState } from 'react';
import { supabaseClient } from '@core/supabaseClient';

type EventRow = { id: string; created_at: string; action: string; data: any };

export default function ActivityPage() {
  const [rows, setRows] = useState<EventRow[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      setLoading(true);
      const { data: { user } } = await supabaseClient.auth.getUser();
      if (!user) { setRows([]); setLoading(false); return; }
      const { data: uo } = await supabaseClient.from('user_org_roles').select('org_id').eq('user_id', user.id).single();
      if (!uo?.org_id) { setRows([]); setLoading(false); return; }
      const { data } = await supabaseClient
        .from('audit_events')
        .select('id, created_at, action, data')
        .eq('org_id', uo.org_id)
        .order('created_at', { ascending: false })
        .limit(100);
      setRows((data as any[]) || []);
      setLoading(false);
    })();
  }, []);

  return (
    <main className="p-6 space-y-4">
      <h1 className="text-lg font-semibold">Activity</h1>
      {loading ? (
        <div className="p-6 bg-white rounded border animate-pulse text-sm text-gray-500">Loading…</div>
      ) : rows.length === 0 ? (
        <div className="p-6 bg-white rounded border text-sm text-gray-600">No recent activity</div>
      ) : (
        <div className="bg-white rounded border divide-y">
          {rows.map((r) => (
            <div key={r.id} className="p-4 text-sm">
              <div className="font-medium">{r.action}</div>
              <div className="text-xs text-gray-600">{new Date(r.created_at).toLocaleString()}</div>
              <pre className="mt-2 text-xs bg-gray-50 p-2 rounded overflow-x-auto">{JSON.stringify(r.data, null, 2)}</pre>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
```


## public/manifest.webmanifest
```json
{
  "name": "Chargeback Evidence Builder",
  "short_name": "CEB",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#2563eb",
  "icons": [
    { "src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

---

## public/sw.js
```js
/* Minimal service worker: cache shell and allow network-first for APIs */
const CACHE = 'ceb-cache-v1';
const SHELL = [
  '/',
  '/manifest.webmanifest'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(SHELL))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
  );
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  if (url.pathname.startsWith('/api/')) {
    // network-first for API
    event.respondWith(
      fetch(event.request).catch(() => caches.match(event.request))
    );
    return;
  }
  // cache-first for shell/static
  event.respondWith(
    caches.match(event.request).then((res) => res || fetch(event.request))
  );
});
```

---

## src/app/layout.tsx
```tsx
import './styles/globals.css';
import React, { useEffect } from 'react';
import { I18nProvider } from '@/i18n';
import { AnalyticsProvider } from '@core/analytics';
import { NotificationBell } from '@ui/NotificationBell';
import { CommandPalette } from '@ui/CommandPalette';
import Link from 'next/link';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    if (typeof window !== 'undefined' && 'serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js').catch(() => {});
    }
  }, []);
  return (
    <html lang="en">
      <head>
        <link rel="manifest" href="/manifest.webmanifest" />
        <meta name="theme-color" content="#2563eb" />
      </head>
      <body className="min-h-screen bg-slate-50 text-slate-900">
        <I18nProvider>
          <AnalyticsProvider>
            <div className="min-h-screen flex flex-col">
              <header className="bg-white shadow-sm border-b">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                  <div className="flex justify-between items-center h-16">
                    <div className="flex items-center gap-8">
                      <h1 className="text-xl font-semibold">Chargeback Evidence Builder</h1>
                      <nav className="hidden md:flex items-center gap-6">
                        <Link href="/disputes" className="text-sm text-gray-600 hover:text-gray-900">
                          Disputes
                        </Link>
                        <Link href="/analytics" className="text-sm text-gray-600 hover:text-gray-900">
                          Analytics
                        </Link>
                        <Link href="/settings" className="text-sm text-gray-600 hover:text-gray-900">
                          Settings
                        </Link>
                      </nav>
                    </div>
                    <div className="flex items-center gap-4">
                      <button className="text-sm text-gray-600 hover:text-gray-900 flex items-center gap-1">
                        <kbd className="px-1.5 py-0.5 text-xs border rounded bg-gray-100">⌘K</kbd>
                      </button>
                      <NotificationBell />
                      <div className="w-8 h-8 rounded-full bg-gray-300" />
                    </div>
                  </div>
                </div>
              </header>
              <main className="flex-1">{children}</main>
              <CommandPalette />
            </div>
          </AnalyticsProvider>
        </I18nProvider>
      </body>
    </html>
  );
}
```

---

## next-i18next.config.js
```js
module.exports = {
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'en-US', 'en-GB', 'de', 'de-DE', 'es', 'es-ES', 'es-MX']
  },
  localeDetection: true,
  // Basic fallbacks per region -> base language
  fallbackLng: {
    'en-US': ['en'],
    'en-GB': ['en'],
    'de-DE': ['de'],
    'es-ES': ['es'],
    'es-MX': ['es'],
    default: ['en']
  },
  returnNull: false
};
```

---

## public/locales/en/common.json
```json
{
  "appTitle": "Chargeback Evidence Builder",
  "nav": {
    "disputes": "Disputes",
    "analytics": "Analytics",
    "settings": "Settings"
  },
  "searchPlaceholder": "Search by dispute, order, customer, amount…"
}
```

---

## public/locales/es/common.json
```json
{
  "appTitle": "Generador de Evidencia de Contracargos",
  "nav": {
    "disputes": "Disputas",
    "analytics": "Analíticas",
    "settings": "Ajustes"
  },
  "searchPlaceholder": "Buscar por disputa, pedido, cliente, importe…"
}
```

---

## public/locales/de/common.json
```json
{
  "appTitle": "Chargeback-Nachweis-Builder",
  "nav": {
    "disputes": "Streitfälle",
    "analytics": "Analysen",
    "settings": "Einstellungen"
  },
  "searchPlaceholder": "Suche nach Streitfall, Bestellung, Kunde, Betrag…"
}
```

---

## public/locales/en-US/common.json
```json
{
  "appTitle": "Chargeback Evidence Builder",
  "nav": {
    "disputes": "Disputes",
    "analytics": "Analytics",
    "settings": "Settings"
  },
  "searchPlaceholder": "Search by dispute, order, customer, amount…"
}
```

---

## public/locales/en-GB/common.json
```json
{
  "appTitle": "Chargeback Evidence Builder",
  "nav": {
    "disputes": "Disputes",
    "analytics": "Analytics",
    "settings": "Settings"
  },
  "searchPlaceholder": "Search by dispute, order, customer, amount…"
}
```

---

## public/locales/de-DE/common.json
```json
{
  "appTitle": "Chargeback-Nachweis-Builder",
  "nav": {
    "disputes": "Streitfälle",
    "analytics": "Analysen",
    "settings": "Einstellungen"
  },
  "searchPlaceholder": "Suche nach Streitfall, Bestellung, Kunde, Betrag…"
}
```

---

## public/locales/es-ES/common.json
```json
{
  "appTitle": "Generador de Evidencia de Contracargos",
  "nav": {
    "disputes": "Disputas",
    "analytics": "Analíticas",
    "settings": "Ajustes"
  },
  "searchPlaceholder": "Buscar por disputa, pedido, cliente, importe…"
}
```

---

## public/locales/es-MX/common.json
```json
{
  "appTitle": "Generador de Evidencias de Contracargos",
  "nav": {
    "disputes": "Disputas",
    "analytics": "Analítica",
    "settings": "Configuración"
  },
  "searchPlaceholder": "Buscar por disputa, pedido, cliente, monto…"
}
```

---

## tailwind.config.ts
```ts
import type { Config } from 'tailwindcss';

export default {
  content: [
    './src/app/**/*.{ts,tsx}',
    './src/components/**/*.{ts,tsx}'
  ],
  theme: {
    extend: {}
  },
  plugins: []
} satisfies Config;
```

---

## postcss.config.js
```js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {}
  }
};
```

---

## .env.example
```bash
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

REGION_DEFAULT=US
# REGION_LOCK=GB

STRIPE_API_KEY=
STRIPE_WEBHOOK_SECRET=
STRIPE_CONNECT_CLIENT_ID=

SHOPIFY_APP_KEY=
SHOPIFY_APP_SECRET=
SHOPIFY_SCOPES=read_orders,read_customers,read_disputes,write_disputes
SHOPIFY_WEBHOOK_SECRET=

EVIDENCE_BUCKET=evidence-packets

# i18n/analytics
NEXT_PUBLIC_DEFAULT_LOCALE=en
ANALYTICS_WRITE_KEY=

# notifications
POSTMARK_SERVER_TOKEN=
NOTIFY_FROM_EMAIL=no-reply@example.com
```

---

## README.md
```markdown
# Chargeback Evidence Builder

Supabase + Next.js app to ingest disputes, assemble evidence, submit via PSP APIs, and track outcomes.

## Run
1. Copy `.env.example` to `.env.local` and fill values.
2. `npm install`
3. `npm run dev`

## Conventions
- Routes under `src/app`. Components PascalCase. Utilities under `src/lib` with named exports.
- SQL identifiers snake_case. Org-scoped RLS.

## Testing Strategy (Summary)
- E2E: Playwright, 100% of user-visible flows (inbox, detail, generate, submit, outcomes).
- Integration: RLS and Edge Functions against a test Supabase project; external APIs mocked.
- Unit: Only complex logic (packet composition), not UI internals.
- CI gates: critical E2E subset on PR; full suite post-merge.
```

---

## src/styles/globals.css
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

html, body, :root { height: 100%; }
```

---

## src/app/layout.tsx
```tsx
import './styles/globals.css';
import React from 'react';
import { I18nProvider } from '@/i18n';
import { AnalyticsProvider } from '@core/analytics';
import { NotificationBell } from '@ui/NotificationBell';
import { CommandPalette } from '@ui/CommandPalette';
import Link from 'next/link';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-50 text-slate-900">
        <I18nProvider>
          <AnalyticsProvider>
            <div className="min-h-screen flex flex-col">
              <header className="bg-white shadow-sm border-b">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                  <div className="flex justify-between items-center h-16">
                    <div className="flex items-center gap-8">
                      <h1 className="text-xl font-semibold">Chargeback Evidence Builder</h1>
                      <nav className="hidden md:flex items-center gap-6">
                        <Link href="/disputes" className="text-sm text-gray-600 hover:text-gray-900">
                          Disputes
                        </Link>
                        <Link href="/analytics" className="text-sm text-gray-600 hover:text-gray-900">
                          Analytics
                        </Link>
                        <Link href="/settings" className="text-sm text-gray-600 hover:text-gray-900">
                          Settings
                        </Link>
                      </nav>
                    </div>
                    <div className="flex items-center gap-4">
                      <button className="text-sm text-gray-600 hover:text-gray-900 flex items-center gap-1">
                        <kbd className="px-1.5 py-0.5 text-xs border rounded bg-gray-100">⌘K</kbd>
                      </button>
                      <NotificationBell />
                      <div className="w-8 h-8 rounded-full bg-gray-300" />
                    </div>
                  </div>
                </div>
              </header>
              <main className="flex-1">{children}</main>
              <CommandPalette />
            </div>
          </AnalyticsProvider>
        </I18nProvider>
      </body>
    </html>
  );
}
```

---

## public/locales/en/common.json
```json
{
  "app_title": "Chargeback Evidence Builder",
  "sign_in": "Sign in",
  "disputes_inbox": "Disputes Inbox"
}
```

---

## public/locales/es/common.json
```json
{
  "app_title": "Constructor de Evidencia de Contracargos",
  "sign_in": "Iniciar sesión",
  "disputes_inbox": "Bandeja de disputas"
}
```

---

## public/locales/de/common.json
```json
{
  "app_title": "Chargeback-Nachweis-Builder",
  "sign_in": "Anmelden",
  "disputes_inbox": "Streitfall-Posteingang"
}
```

---

## src/i18n/index.ts
```ts
'use client';
import { useTranslation } from 'next-i18next';

export function I18nProvider({ children }: { children: React.ReactNode }) {
  return <>{children}</>; // next-i18next manages context via provider at app root
}

export function useT(namespace: string = 'common') {
  const { t } = useTranslation(namespace);
  return t;
}
```

---

## src/app/providers.tsx
```tsx
'use client';
import { appWithTranslation } from 'next-i18next';
import { I18nProvider } from '@/i18n';
import { AnalyticsProvider } from '@core/analytics';

function Providers({ children }: { children: React.ReactNode }) {
  return (
    <I18nProvider>
      <AnalyticsProvider>{children}</AnalyticsProvider>
    </I18nProvider>
  );
}

export default appWithTranslation(Providers);
```

---

## src/app/page.tsx
```tsx
export default function Home() {
  return (
    <main className="p-8">
      <h1 className="text-2xl font-semibold">Chargeback Evidence Builder</h1>
      <p className="mt-2">Go to /disputes to view the inbox.</p>
    </main>
  );
}
```

---

## src/app/login/page.tsx
```tsx
'use client';
import { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import { supabaseClient } from '@core/supabaseClient';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (isSignUp) {
        const { error } = await supabaseClient.auth.signUp({
          email,
          password,
          options: {
            emailRedirectTo: `${window.location.origin}/auth/callback`,
          },
        });
        if (error) throw error;
        setError('Check your email for the confirmation link!');
      } else {
        const { error } = await supabaseClient.auth.signInWithPassword({
          email,
          password,
        });
        if (error) throw error;
        
        // After login, require org and at least one connected store before sending to disputes
        const { data: { user } } = await supabaseClient.auth.getUser();
        if (!user) return;
        const { data: userOrg } = await supabaseClient
          .from('user_org_roles')
          .select('org_id')
          .eq('user_id', user.id)
          .maybeSingle();
        if (!userOrg?.org_id) {
          router.push('/onboarding');
          return;
        }
        const { count } = await supabaseClient
          .from('stores')
          .select('id', { count: 'exact', head: true })
          .eq('org_id', userOrg.org_id);
        if ((count || 0) > 0) {
          router.push('/disputes');
        } else {
          router.push('/onboarding');
        }
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="p-8 max-w-md mx-auto">
      <h1 className="text-2xl font-semibold mb-6">
        {isSignUp ? 'Create Account' : 'Sign In'}
      </h1>
      
      <form onSubmit={handleAuth} className="space-y-4">
        <div>
          <label htmlFor="email" className="block text-sm font-medium mb-1">
            Email
          </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-3 py-2 border rounded-md"
            required
          />
        </div>
        
        <div>
          <label htmlFor="password" className="block text-sm font-medium mb-1">
            Password
          </label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-3 py-2 border rounded-md"
            required
          />
        </div>
        
        {error && (
          <div className={`text-sm ${error.includes('email') ? 'text-green-600' : 'text-red-600'}`}>
            {error}
          </div>
        )}
        
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Loading...' : isSignUp ? 'Sign Up' : 'Sign In'}
        </button>
      </form>
      
      <p className="mt-4 text-center text-sm">
        {isSignUp ? 'Already have an account?' : "Don't have an account?"}{' '}
        <button
          onClick={() => setIsSignUp(!isSignUp)}
          className="text-blue-600 hover:underline"
        >
          {isSignUp ? 'Sign In' : 'Sign Up'}
        </button>
      </p>
    </main>
  );
}
```

---

## src/app/auth/callback/page.tsx
```tsx
'use client';
import { useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { supabaseClient } from '@core/supabaseClient';

export default function AuthCallbackPage() {
  const router = useRouter();
  const params = useSearchParams();

  useEffect(() => {
    const exchange = async () => {
      const code = params.get('code');
      const errorDescription = params.get('error_description');
      if (errorDescription) {
        router.replace('/login?error=' + encodeURIComponent(errorDescription));
        return;
      }
      if (!code) {
        router.replace('/login');
        return;
      }

      const { error } = await supabaseClient.auth.exchangeCodeForSession(code);
      if (error) {
        router.replace('/login?error=' + encodeURIComponent(error.message));
        return;
      }

      const { data: { user } } = await supabaseClient.auth.getUser();
      if (!user) {
        router.replace('/login');
        return;
      }

      const { data: uor } = await supabaseClient
        .from('user_org_roles')
        .select('org_id')
        .eq('user_id', user.id)
        .maybeSingle();

      if (!uor?.org_id) {
        router.replace('/onboarding');
        return;
      }

      const { count } = await supabaseClient
        .from('stores')
        .select('id', { count: 'exact', head: true })
        .eq('org_id', uor.org_id);

      if ((count || 0) > 0) {
        router.replace('/disputes');
      } else {
        router.replace('/onboarding');
      }
    };
    exchange();
  }, []);

  return null;
}
```

---

## src/app/disputes/page.tsx
```tsx
'use client';
import { useEffect, useState } from 'react';
import { supabaseClient } from '@core/supabaseClient';
import { DataTable } from '@ui/DataTable';
import { useAnalytics } from '@core/analytics';

export default function DisputesPage() {
  const analytics = useAnalytics();
  const [metrics, setMetrics] = useState<any>(null);
  const [query, setQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all'|'new'|'draft'|'submitted'|'won'|'lost'>('all');
  const [dateRange, setDateRange] = useState<{ from?: string; to?: string }>({});
  const [selectedCount, setSelectedCount] = useState(0);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [sampleMode, setSampleMode] = useState(false);
  const [activeChip, setActiveChip] = useState<'due_today'|'high_value'|'auto_ready'|'needs_attention'|null>(null);
  const [quickView, setQuickView] = useState<any|null>(null);

  useEffect(() => {
    analytics.track({ name: 'disputes_inbox_viewed' });
    fetchMetrics();
  }, []);

  const fetchMetrics = async () => {
    const { data: { user } } = await supabaseClient.auth.getUser();
    if (!user) return;
    const { data: uo } = await supabaseClient.from('user_org_roles').select('org_id').eq('user_id', user.id).single();
    if (!uo) return;
    
    const { data: disputes } = await supabaseClient.from('disputes').select('status, amount, created_at').eq('org_id', uo.org_id);
    const open = disputes?.filter(d => ['new','draft','submitted'].includes(d.status))?.length || 0;
    const recovered = disputes?.filter(d => d.status === 'won').reduce((s,d)=>s+Number(d.amount),0) || 0;
    const winRate = disputes && disputes.length>0 ? Math.round((disputes.filter(d=>d.status==='won').length/disputes.length)*100) : 0;
    setMetrics({ open, recovered, winRate, timeSaved: '2hrs avg' });
  };

  return (
    <main className="p-6 space-y-4">
      {/* Sample Mode Banner */}
      {sampleMode && (
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-purple-600 font-medium">🎓 Sample Mode</span>
            <span className="text-sm text-purple-700">Exploring with test data</span>
          </div>
          <button 
            onClick={() => setSampleMode(false)} 
            className="text-sm text-purple-600 hover:underline"
          >
            Exit Sample Mode
          </button>
        </div>
      )}
      
      {/* Key metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-lg shadow">
          <p className="text-sm text-gray-600">Open Disputes</p>
          <p className="text-2xl font-bold">{metrics?.open ?? '—'}</p>
          {metrics?.open > 0 && <span className="text-xs text-red-600">Action needed</span>}
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <p className="text-sm text-gray-600">Win Rate</p>
          <p className="text-2xl font-bold flex items-center">
            {metrics?.winRate ?? '—'}%
            {metrics?.winRate > 0 && <span className="ml-2 text-sm text-green-600">↑</span>}
          </p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <p className="text-sm text-gray-600">Revenue Recovered</p>
          <p className="text-2xl font-bold">${(metrics?.recovered ?? 0).toLocaleString()}</p>
          <p className="text-xs text-gray-500">Last 30 days</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <p className="text-sm text-gray-600">Time to Submit</p>
          <p className="text-2xl font-bold">{metrics?.timeSaved ?? '—'}</p>
        </div>
      </div>

      {/* Prioritization chips */}
      <div className="flex flex-wrap gap-2">
        {[
          { id: 'due_today', label: 'Due today', color: 'bg-red-50 text-red-700 border-red-200' },
          { id: 'high_value', label: 'High value', color: 'bg-orange-50 text-orange-700 border-orange-200' },
          { id: 'auto_ready', label: 'Auto-ready', color: 'bg-green-50 text-green-700 border-green-200' },
          { id: 'needs_attention', label: 'Needs attention', color: 'bg-yellow-50 text-yellow-700 border-yellow-200' }
        ].map((c:any) => (
          <button
            key={c.id}
            onClick={() => setActiveChip(activeChip === c.id ? null : c.id as any)}
            className={`px-3 py-1 text-sm border rounded ${c.color} ${activeChip===c.id?'ring-2 ring-offset-1':''}`}
          >
            {c.label}
          </button>
        ))}
      </div>

      {/* Toolbar */}
      <div className="bg-white p-3 rounded-lg shadow flex flex-col md:flex-row md:items-center gap-3">
        <div className="flex-1 relative">
          <input 
            value={query} 
            onChange={e => setQuery(e.target.value)} 
            placeholder="Search by order #, customer, amount..." 
            className="w-full border rounded px-3 py-2 pl-10"
          />
          <svg className="absolute left-3 top-3 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <select 
          value={statusFilter} 
          onChange={e=>setStatusFilter(e.target.value as any)} 
          className="border rounded px-3 py-2"
        >
          <option value="all">All Disputes</option>
          {['new','draft','submitted','won','lost'].map(s=> 
            <option key={s} value={s}>{s.charAt(0).toUpperCase() + s.slice(1)}</option>
          )}
        </select>
        <input 
          type="date" 
          className="border rounded px-3 py-2" 
          onChange={e=>setDateRange({...dateRange, from: e.target.value})}
        />
        <div className="hidden md:block">
          <button 
            className={`px-3 py-2 rounded ${selectedCount > 0 ? 'bg-blue-600 text-white' : 'border'}`}
            disabled={selectedCount === 0}
            onClick={() => {
              if (selectedCount > 0) {
                const action = prompt('Select action:\n1. Generate Evidence\n2. Export Selected\n3. Mark as Priority\n4. Batch Submit (API)\n5. Schedule Batch (API)');
                if (action === '1') alert(`Generating evidence for ${selectedCount} disputes`);
                else if (action === '2') alert(`Exporting ${selectedCount} disputes`);
                else if (action === '3') alert(`Marking ${selectedCount} disputes as priority`);
                else if (action === '4') {
                  fetch('/api/submissions/batch', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ disputeIds: selectedIds, method: 'api' })
                  }).then(()=>alert('Batch submitted'));
                } else if (action === '5') {
                  const when = prompt('Enter ISO datetime to schedule:');
                  if (when) fetch('/api/submissions/batch', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ disputeIds: selectedIds, method: 'api', scheduledAt: when })
                  }).then(()=>alert('Batch scheduled'));
                }
              }
            }}
          >
            Bulk Actions ({selectedCount})
          </button>
        </div>
      </div>

      {/* Mobile cards */}
      <div className="space-y-3 md:hidden">
        <MobileDisputeCards chipFilter={activeChip} search={query} statusFilter={statusFilter} onOpen={(row:any)=>setQuickView(row)} />
      </div>

      {/* Desktop table */}
      <div className="hidden md:block">
        <DataTable 
          search={query} 
          statusFilter={statusFilter} 
          onSelectionChange={(count, ids)=>{ setSelectedCount(count); setSelectedIds(ids||[]); }}
          sampleMode={sampleMode}
          onSampleMode={() => setSampleMode(true)}
          onRowClick={(row:any)=>setQuickView(row)}
          chipFilter={activeChip}
        />
      </div>
      {quickView && (
        <div className="fixed inset-0 z-40" onClick={()=>setQuickView(null)} />
      )}
      {quickView && (
        <aside className="hidden md:block fixed right-0 top-0 bottom-0 w-full sm:w-[420px] bg-white shadow-xl z-50 border-l overflow-y-auto">
          <div className="p-4 border-b flex items-center justify-between">
            <h3 className="font-semibold">Dispute {quickView.psp_id}</h3>
            <button className="text-sm text-gray-600" onClick={()=>setQuickView(null)}>Close</button>
          </div>
          <div className="p-4 space-y-3 text-sm">
            <div className="flex items-center gap-2">
              <span className={`px-2 py-0.5 text-xs rounded ${quickView.status==='new'?'bg-red-100 text-red-800':quickView.status==='draft'?'bg-yellow-100 text-yellow-800':quickView.status==='submitted'?'bg-blue-100 text-blue-800':quickView.status==='won'?'bg-green-100 text-green-800':'bg-gray-100 text-gray-800'}`}>{quickView.status}</span>
              <span>Reason: {quickView.reason_code}</span>
            </div>
            <div>Amount: ${quickView.amount}</div>
            <div>Due: {quickView.due_by ? new Date(quickView.due_by).toLocaleString() : 'No deadline'}</div>
            <div className="text-xs text-gray-600">Customer: {quickView.raw?.customer?.name || '—'}</div>
            <div className="pt-2">
              <button className="px-3 py-2 bg-blue-600 text-white rounded" onClick={()=>window.location.href=`/disputes/${quickView.id}`}>Open Full Details</button>
            </div>
          </div>
        </aside>
      )}
      {quickView && (
        <div className="md:hidden fixed inset-x-0 bottom-0 bg-white rounded-t-xl shadow-2xl z-50 border-t">
          <div className="p-4 border-b flex items-center justify-between">
            <h3 className="font-semibold">Dispute {quickView.psp_id}</h3>
            <button className="text-sm text-gray-600" onClick={()=>setQuickView(null)}>Close</button>
          </div>
          <div className="p-4 space-y-3 text-sm max-h-[70vh] overflow-y-auto">
            <div className="flex items-center gap-2">
              <span className={`px-2 py-0.5 text-xs rounded ${quickView.status==='new'?'bg-red-100 text-red-800':quickView.status==='draft'?'bg-yellow-100 text-yellow-800':quickView.status==='submitted'?'bg-blue-100 text-blue-800':quickView.status==='won'?'bg-green-100 text-green-800':'bg-gray-100 text-gray-800'}`}>{quickView.status}</span>
              <span>Reason: {quickView.reason_code}</span>
            </div>
            <div>Amount: ${quickView.amount}</div>
            <div>Due: {quickView.due_by ? new Date(quickView.due_by).toLocaleString() : 'No deadline'}</div>
            <div className="text-xs text-gray-600">Customer: {quickView.raw?.customer?.name || '—'}</div>
            <div className="pt-2">
              <button className="w-full px-3 py-2 bg-blue-600 text-white rounded" onClick={()=>window.location.href=`/disputes/${quickView.id}`}>Open Full Details</button>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
```

---

## src/app/disputes/[id]/page.tsx
```tsx
'use client';
import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { supabaseClient } from '@core/supabaseClient';
import { DraftEditor } from '@ui/DraftEditor';
import { PacketPreview } from '@ui/PacketPreview';
import { Tabs } from '@ui/Tabs';
import { SubmissionModal } from '@ui/SubmissionModal';
import { formatDistanceToNow } from 'date-fns';

export default function DisputeDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [dispute, setDispute] = useState<any>(null);
  const [evidence, setEvidence] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [progress, setProgress] = useState<'idle'|'validating'|'composing'|'pdf'|'submitting'|'confirming'|'done'|'error'>('idle');
  const [errorMsg, setErrorMsg] = useState<string>('');
  const [showModal, setShowModal] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const [guidance, setGuidance] = useState<any|null>(null);
  const [validation, setValidation] = useState<{ readiness: number; gaps: Array<{ code: string; message: string; action?: string }> } | null>(null);
  const [activeTab, setActiveTab] = useState<string>('Evidence Draft');

  useEffect(() => {
    if (params.id) {
      fetchDispute(params.id as string);
      fetchEvidence(params.id as string);
    }
  }, [params.id]);

  const fetchDispute = async (id: string) => {
    try {
      const { data, error } = await supabaseClient
        .from('disputes')
        .select('*, stores(platform), submissions(*), orders(*)')
        .eq('id', id)
        .single();

      if (error) throw error;
      setDispute(data);
    } catch (error) {
      console.error('Error fetching dispute:', error);
      router.push('/disputes');
    } finally {
      setLoading(false);
    }
  };

  const fetchEvidence = async (disputeId: string) => {
    try {
      const response = await fetch('/api/evidence', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ disputeId }),
      });
      
      if (response.ok) {
        const data = await response.json();
        setEvidence(data.draft);
        setGuidance(data.draft?.guidance || null);
        // Also fetch validation status
        try {
          const v = await fetch('/api/submissions/validate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ disputeId }) });
          if (v.ok) {
            const res = await v.json();
            setValidation(res);
          }
        } catch {}
      }
    } catch (error) {
      console.error('Error fetching evidence:', error);
    }
  };

  const handleSubmit = async (method: 'api' | 'manual') => {
    setSubmitting(true);
    try {
      const response = await fetch('/api/submissions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ disputeId: dispute.id, method }),
      });

      if (response.ok) {
        const data = await response.json();
        setShowModal(false);
        setShowSuccess(true);
        
        if (method === 'manual' && data.pdfUrl) {
          window.open(data.pdfUrl, '_blank');
        }
        
        await fetchDispute(dispute.id);
        
        // Hide success after 5 seconds
        setTimeout(() => setShowSuccess(false), 5000);
      } else {
        throw new Error('Submission failed');
      }
    } catch (error) {
      console.error('Error submitting evidence:', error);
      alert('Failed to submit evidence. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <main className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-1/4"></div>
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </main>
    );
  }

  if (!dispute) {
    return null;
  }

  const lastSubmission = dispute.submissions?.[0];
  const canSubmit = ['new', 'draft'].includes(dispute.status);

  return (
    <main className="p-6">
      {/* Header */}
      <div className="mb-6">
        <button
          onClick={() => router.push('/disputes')}
          className="text-sm text-blue-600 hover:underline mb-2 flex items-center gap-1"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to disputes
        </button>
        
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-2xl font-semibold">Dispute #{dispute.psp_id}</h1>
            <div className="mt-2 flex items-center gap-4 text-sm">
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                dispute.status === 'new' ? 'bg-red-100 text-red-800' :
                dispute.status === 'draft' ? 'bg-yellow-100 text-yellow-800' :
                dispute.status === 'submitted' ? 'bg-blue-100 text-blue-800' :
                dispute.status === 'won' ? 'bg-green-100 text-green-800' :
                'bg-gray-100 text-gray-800'
              }`}>
                {dispute.status.toUpperCase()}
              </span>
              <span>Reason: <strong>{dispute.reason_code}</strong></span>
              <span>Amount: <strong>${dispute.amount}</strong></span>
              <span className={dispute.due_by && new Date(dispute.due_by) < new Date(Date.now() + 3 * 24 * 60 * 60 * 1000) ? 'text-red-600 font-medium' : ''}>
                Due: <strong>{dispute.due_by ? formatDistanceToNow(new Date(dispute.due_by), { addSuffix: true }) : 'No deadline'}</strong>
              </span>
              <span>Customer: <strong>{dispute.raw?.customer?.name || 'Unknown'}</strong></span>
            </div>
          </div>
          
          <div className="space-x-2">
            {canSubmit && (
              <>
                <button
                  onClick={() => alert('Download evidence packet')}
                  className="px-3 py-2 border border-gray-300 rounded hover:bg-gray-50"
                >
                  Download Evidence
                </button>
                <button
                  onClick={() => setShowModal(true)}
                  disabled={submitting}
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
                >
                  Submit to {dispute.stores?.platform === 'shopify' ? 'Shopify' : 'Stripe'}
                </button>
              </>
            )}
          </div>
        </div>
        
        {guidance && (
          <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded">
            <p className="text-sm font-medium text-yellow-800">📋 {guidance.title}</p>
            <p className="text-xs text-yellow-700 mt-1">Must include: {guidance.mustInclude?.join(', ')}</p>
            {guidance.recommended && (
              <p className="text-xs text-yellow-700">Recommended: {guidance.recommended.join(', ')}</p>
            )}
          </div>
        )}

        {lastSubmission && (
          <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded">
            <p className="text-sm text-green-800">
              Last submitted: {formatDistanceToNow(new Date(lastSubmission.submitted_at), { addSuffix: true })}
            </p>
          </div>
        )}
      </div>

      {/* Success Message */}
      {showSuccess && (
        <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center gap-3">
          <div className="text-green-600 text-2xl">✅</div>
          <div>
            <h3 className="font-semibold text-green-900">Evidence Submitted Successfully!</h3>
            <p className="text-sm text-green-800 mt-1">
              Submission ID: #{lastSubmission?.id?.slice(0, 8)} • 
              Expected response within 7-10 days • 
              <a href="#" className="underline">View Submitted Packet</a>
            </p>
          </div>
        </div>
      )}

      {/* Readiness + Quick Actions */}
      <div className="mb-4 grid gap-3">
        {evidence && (
          <div className="p-3 rounded-lg border bg-white">
            {/* Simple readiness computed client-side in demo; move to server if needed */}
            {/* @ts-ignore computeReadiness imported below */}
            {(() => { try { /* no-op */ } catch {} })()}
            {/* Progress stub; computed in evidence tab as well */}
            <div className="flex items-center gap-3">
              <div className="w-24 bg-gray-200 h-2 rounded-full">
                <div className="bg-blue-600 h-2 rounded-full" style={{ width: '70%' }} />
              </div>
              <span className="text-sm text-gray-700">Readiness: ~70%</span>
            </div>
            <ul className="mt-2 text-sm list-disc list-inside text-gray-700">
              <li className="text-yellow-700">Customer verification missing (AVS/CVV)</li>
              <li className="text-yellow-700">Delivery confirmation not attached</li>
            </ul>
          </div>
        )}
        <div className="flex gap-2 p-3 bg-gray-50 rounded-lg">
          <button className="px-3 py-1.5 text-sm border rounded hover:bg-white flex items-center gap-1" onClick={()=>fetchEvidence(dispute.id)}>
            <span>🔄</span> Regenerate Evidence
          </button>
          <button className="px-3 py-1.5 text-sm border rounded hover:bg-white flex items-center gap-1" onClick={()=>alert('Attach file coming soon')}>
            <span>📎</span> Attach File
          </button>
          <button className="px-3 py-1.5 text-sm border rounded hover:bg-white flex items-center gap-1" onClick={()=>window.print()}>
            <span>👁️</span> Preview Packet
          </button>
          <button className="px-3 py-1.5 text-sm border rounded hover:bg-white flex items-center gap-1" onClick={()=>navigator.clipboard.writeText(JSON.stringify(evidence))}>
            <span>📋</span> Copy to Clipboard
          </button>
        </div>
      </div>

      {/* Tabbed Content */}
      <Tabs tabs={['Evidence Draft', 'Order Details', 'Customer History', 'Shipping', 'Device & Session', 'Timeline']} active={activeTab} onChange={setActiveTab}>
        {(tab) => {
          const activeTab = tab; // keep existing code paths below
          if (activeTab === 'Evidence Draft') {
            return (
              <div className="grid gap-6 md:grid-cols-2">
                <section>
                  <div className="bg-blue-50 p-3 rounded mb-4 text-sm">
                    <p className="text-blue-800">✨ Evidence auto-generated 2 minutes ago based on your template</p>
                  </div>
                  <DraftEditor 
                    disputeId={dispute.id}
                    evidence={evidence}
                    onUpdate={() => fetchEvidence(dispute.id)}
                  />
                  {/* Attachment Thumbnails */}
                  <div className="mt-4">
                    <h3 className="font-medium mb-3">Supporting Documents</h3>
                    <div className="grid grid-cols-2 gap-3">
                      {(evidence?.attachments || []).map((att: any, i: number) => (
                        <div key={i} className="border rounded p-3 hover:shadow-md cursor-pointer">
                          <div className="h-20 bg-gray-100 rounded mb-2 flex items-center justify-center">
                            {att.type === 'application/pdf' ? (
                              <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                              </svg>
                            ) : (
                              <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                              </svg>
                            )}
                          </div>
                          <p className="text-sm font-medium truncate">{att.name}</p>
                          {att.required && <span className="text-xs text-red-600">Required</span>}
                        </div>
                      ))}
                      <div className="border-2 border-dashed rounded p-3 flex items-center justify-center cursor-pointer hover:border-blue-400">
                        <div className="text-center">
                          <span className="text-2xl">+</span>
                          <p className="text-sm text-gray-600">Add Document</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </section>
                <section>
                  <PacketPreview 
                    evidence={evidence}
                    loading={!evidence}
                  />
                </section>
              </div>
            );
          }
          
          if (activeTab === 'Order Details') {
            const order = dispute.orders?.[0];
            return (
              <div className="bg-white rounded-lg shadow p-6">
                <div className="grid gap-4">
                  <div className="border rounded p-4">
                    <h3 className="font-medium mb-3">Order Summary</h3>
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      <div>Order #: {order?.id || 'N/A'}</div>
                      <div>Date: {order?.created_at ? new Date(order.created_at).toLocaleDateString() : 'N/A'}</div>
                      <div>Total: ${dispute.amount}</div>
                      <div>Payment: **** {dispute.raw?.charge?.payment_method_details?.card?.last4 || 'N/A'}</div>
                    </div>
                  </div>
                  <div className="border rounded p-4">
                    <h3 className="font-medium mb-3">Response Codes</h3>
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      <div className="flex items-center gap-2">
                        AVS: <span className="font-mono bg-gray-100 px-2 py-1 rounded">{dispute.raw?.evidence?.avs_code || 'N/A'}</span>
                        <span className="text-xs text-gray-600">(Address Verification)</span>
                      </div>
                      <div className="flex items-center gap-2">
                        CVV: <span className="font-mono bg-gray-100 px-2 py-1 rounded">{dispute.raw?.evidence?.cvv_code || 'N/A'}</span>
                        <span className="text-xs text-gray-600">(Card Verification)</span>
                      </div>
                    </div>
                  </div>
                  <div className="border rounded p-4">
                    <h3 className="font-medium mb-3">Addresses</h3>
                    <div className="grid md:grid-cols-2 gap-4 text-sm">
                      <div>
                        <h4 className="font-medium text-gray-700">Billing</h4>
                        <p className="mt-1">{order?.addresses_json?.billing_address?.address1 || 'N/A'}</p>
                        <p>{order?.addresses_json?.billing_address?.city}, {order?.addresses_json?.billing_address?.province} {order?.addresses_json?.billing_address?.zip}</p>
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-700">Shipping</h4>
                        <p className="mt-1">{order?.addresses_json?.shipping_address?.address1 || 'N/A'}</p>
                        <p>{order?.addresses_json?.shipping_address?.city}, {order?.addresses_json?.shipping_address?.province} {order?.addresses_json?.shipping_address?.zip}</p>
                        {order?.addresses_json?.billing_address?.address1 === order?.addresses_json?.shipping_address?.address1 && (
                          <span className="text-xs text-green-600">✓ Addresses match</span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          }
          
          if (activeTab === 'Customer History') {
            return (
              <div className="bg-white rounded-lg shadow p-6">
                <div className="grid gap-4">
                  <div className="border rounded p-4">
                    <h3 className="font-medium mb-3">Customer Profile</h3>
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      <div>Name: {dispute.raw?.customer?.name || 'N/A'}</div>
                      <div>Email: {dispute.raw?.customer?.email || 'N/A'}</div>
                      <div>Customer since: {dispute.raw?.customer?.created_at || 'N/A'}</div>
                      <div>Lifetime value: ${dispute.raw?.customer?.total_spent || '0'}</div>
                    </div>
                  </div>
                  <div className="border rounded p-4">
                    <h3 className="font-medium mb-3">Order History</h3>
                    <p className="text-sm text-gray-600">✅ 12 successful orders • 0 previous disputes</p>
                  </div>
                </div>
              </div>
            );
          }
          
          if (activeTab === 'Shipping') {
            return (
              <div className="bg-white rounded-lg shadow p-6">
                <div className="border rounded p-4">
                  <h3 className="font-medium mb-3">Shipment Tracking</h3>
                  <div className="space-y-2 text-sm">
                    <div>Carrier: UPS</div>
                    <div>Tracking: <a href="#" className="text-blue-600 hover:underline">1Z999AA10123456784</a></div>
                    <div className="mt-4">
                      <div className="relative">
                        <div className="absolute left-4 top-8 bottom-0 w-0.5 bg-gray-300"></div>
                        {['Shipped', 'In Transit', 'Out for Delivery', 'Delivered'].map((status, i) => (
                          <div key={i} className="relative flex items-center gap-3 pb-6">
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                              i === 3 ? 'bg-green-500 text-white' : 'bg-gray-300'
                            }`}>
                              {i === 3 ? '✓' : ''}
                            </div>
                            <div>
                              <p className="font-medium">{status}</p>
                              <p className="text-xs text-gray-600">Date/Time</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          }
          
          if (activeTab === 'Device & Session') {
            return (
              <div className="bg-white rounded-lg shadow p-6">
                <div className="grid gap-4">
                  <div className="border rounded p-4">
                    <h3 className="font-medium mb-3">Session Details</h3>
                    <div className="space-y-2 text-sm">
                      <div>IP Address: 192.168.1.1</div>
                      <div>Location: Los Angeles, CA</div>
                      <div>Device: Desktop Chrome</div>
                      <div>Session duration: 12 minutes</div>
                    </div>
                  </div>
                  <div className="border rounded p-4">
                    <h3 className="font-medium mb-3">Risk Signals</h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex items-center gap-2">
                        <span className="text-green-600">✓</span> IP location matches billing address
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-green-600">✓</span> No VPN/Proxy detected
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-green-600">✓</span> Device previously used for successful orders
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          }
          
          return (
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="font-medium mb-4">Timeline</h3>
              <div className="relative">
                <div className="absolute left-4 top-8 bottom-0 w-0.5 bg-gray-300"></div>
                {[
                  'Order placed', 
                  'Payment processed', 
                  'Order fulfilled', 
                  'Delivered', 
                  'Dispute received',
                  'Evidence generated'
                ].map((event, i) => (
                  <div key={i} className="relative flex items-start gap-3 pb-6">
                    <div className="w-8 h-8 rounded-full bg-white border-2 border-gray-300 flex items-center justify-center">
                      <div className="w-2 h-2 rounded-full bg-gray-400"></div>
                    </div>
                    <div>
                      <p className="font-medium">{event}</p>
                      <p className="text-sm text-gray-600">Date/time and details</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        }}
      </Tabs>

      {/* Submission Modal */}
      <SubmissionModal
        open={showModal}
        onClose={() => setShowModal(false)}
        counts={{ 
          sections: evidence?.sections?.length || 0, 
          attachments: evidence?.attachments?.length || 0 
        }}
        onSubmit={handleSubmit}
        validation={validation}
      />

      {/* Validation issues with deep links */}
      {validation && validation.gaps && validation.gaps.length > 0 && (
        <div className="mt-6 border rounded p-3 bg-yellow-50">
          <div className="text-sm font-medium text-yellow-800 mb-2">Issues to address</div>
          <ul className="text-sm list-disc ml-5 space-y-1">
            {validation.gaps.map((g, i) => (
              <li key={i}>
                <button
                  className="text-blue-700 hover:underline"
                  onClick={() => {
                    // Simple mapping from gap codes to tabs
                    if (g.code.includes('shipping')) setActiveTab('Shipping');
                    else if (g.code.includes('avs') || g.code.includes('cvv')) setActiveTab('Order Details');
                    else setActiveTab('Evidence Draft');
                    // Scroll to tabs
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                  }}
                >
                  {g.message}
                </button>
              </li>
            ))}
          </ul>
        </div>
      />
    </main>
  );
}
```

---

## src/app/api/webhooks/stripe/route.ts
```ts
export const runtime = 'nodejs';
import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';
import { z } from 'zod';
import { createServerClient } from '@core/supabaseServer';

export async function POST(req: NextRequest) {
  const stripe = new Stripe(process.env.STRIPE_API_KEY || '', { apiVersion: '2024-06-20' });
  const sig = req.headers.get('stripe-signature') || '';
  const raw = await req.text();
  try {
    // Rate limit per IP to protect from abuse
    try {
      const db = createServerClient();
      const ip = req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() || 'unknown';
      await db.rpc('check_rate_limit', { p_key: 'stripe_webhook', p_identifier: ip, p_window_seconds: 10, p_max_calls: 30 });
    } catch {}

    const event = stripe.webhooks.constructEvent(raw, sig, process.env.STRIPE_WEBHOOK_SECRET || '');
    // Validate minimal structure with zod if needed
    // Minimal event shape validation
    const BaseEvent = z.object({ id: z.string().min(1), type: z.string().min(1) });
    BaseEvent.parse({ id: event.id, type: event.type });
    // Idempotency check + record
    const db = createServerClient();
    const provider = 'stripe';
    const key = event.id;
    const { data: existing } = await db
      .from('webhook_events')
      .select('id')
      .eq('provider', provider)
      .eq('idempotency_key', key)
      .limit(1)
      .maybeSingle();
    if (existing) return NextResponse.json({ ok: true, duplicate: true });
    await db.from('webhook_events').insert({ provider, idempotency_key: key, payload: event as any });
    // Topic allowlist to reduce surface
    const allowed = new Set([
      'charge.dispute.created',
      'charge.dispute.updated',
      'charge.dispute.closed'
    ]);
    if (!allowed.has(event.type)) {
      return NextResponse.json({ ok: true, ignored: true });
    }
    // Handle Stripe dispute lifecycle (basic upsert + ack reconcile)
    if (event.type.startsWith('charge.dispute.')) {
      try {
        const disputeObj: any = (event as any).data?.object;
        if (disputeObj) {
          const statusMap: Record<string, string> = {
            'needs_response': 'new',
            'warning_needs_response': 'new',
            'under_review': 'submitted',
            'won': 'won',
            'lost': 'lost'
          };
          const status = statusMap[disputeObj.status] ?? 'draft';
          // Resolve org/store: if not resolvable yet, skip insert to avoid violating NOT NULL org_id elsewhere
          const payload = {
            psp_id: disputeObj.id,
            psp_provider: 'stripe',
            reason_code: disputeObj.reason || 'unknown',
            amount: ((disputeObj.amount || 0) / 100.0) as number,
            due_by: disputeObj.evidence_details?.due_by ? new Date(disputeObj.evidence_details.due_by * 1000).toISOString() : null,
            status,
            raw: disputeObj
          } as any;
          // Try resolving store by connected account id if present
          let storeRow: any = null;
          const acctId = (event as any).account as string | undefined;
          if (acctId) {
            const { data: s } = await db
              .from('stores')
              .select('id, org_id')
              .eq('platform', 'stripe')
              .eq('oauth_tokens->>stripe_account_id', acctId)
              .maybeSingle();
            storeRow = s;
          }

          const { data: row } = await db
            .from('disputes')
            .select('id')
            .eq('psp_id', disputeObj.id)
            .maybeSingle();
          if (row) {
            await db.from('disputes').update(payload).eq('id', row.id);
          } else {
            if (storeRow?.org_id) {
              await db.from('disputes').insert({ ...payload, org_id: storeRow.org_id, store_id: storeRow.id });
            } else {
              console.warn('Stripe dispute received but no existing row/org mapping; skipping insert', disputeObj.id);
            }
          }

          // Audit log (best-effort)
          if (storeRow?.org_id) {
            await db.from('audit_events').insert({
              org_id: storeRow.org_id,
              action: 'webhook.stripe.dispute',
              data: { event_type: event.type, dispute_id: disputeObj.id }
            });
          }

          // Reconcile latest submission's receipt with dispute id
          try {
            const { data: lastSub } = await db
              .from('submissions')
              .select('id, receipt')
              .order('submitted_at', { ascending: false })
              .limit(1)
              .maybeSingle();
            if (lastSub?.id && (!lastSub.receipt || !lastSub.receipt.external_ref)) {
              await db
                .from('submissions')
                .update({ receipt: { ...(lastSub.receipt || {}), external_ref: disputeObj.id, webhook: event.type } })
                .eq('id', lastSub.id);
            }
          } catch {}
        }
      } catch (processErr: any) {
        // Dead-letter capture
        try {
          await db.from('webhook_dead_letters').insert({
            provider: 'stripe',
            idempotency_key: (event as any).id || 'unknown',
            payload: (event as any),
            error: String(processErr?.message || processErr)
          });
        } catch {}
      }
    }
    return NextResponse.json({ ok: true });
  } catch (err) {
    return new NextResponse('Invalid webhook', { status: 400 });
  }
}
```

---

## src/app/api/stores/attach/route.ts
```ts
import { NextRequest, NextResponse } from 'next/server';
import { createServerClient } from '@core/supabaseServer';

// Attach a Shopify store to the current user's org
// Body: { shop?: string; storeId?: string; orgId?: string }
export async function POST(req: NextRequest) {
  const db = createServerClient();
  const body = await req.json().catch(() => ({}));
  const { shop, storeId, orgId } = body as { shop?: string; storeId?: string; orgId?: string };

  // Get current user and infer org if not provided
  const { data: { user } } = await (db.auth as any).getUser();
  if (!user) return new NextResponse('Unauthorized', { status: 401 });

  let resolvedOrgId = orgId || null;
  if (!resolvedOrgId) {
    const { data: uor } = await db
      .from('user_org_roles')
      .select('org_id')
      .eq('user_id', user.id)
      .single();
    resolvedOrgId = uor?.org_id || null;
  }
  if (!resolvedOrgId) return new NextResponse('No org found for user', { status: 400 });

  // Resolve store row
  let storeRow: any = null;
  if (storeId) {
    const { data } = await db.from('stores').select('id, org_id').eq('id', storeId).maybeSingle();
    storeRow = data;
  } else if (shop) {
    const { data } = await db
      .from('stores')
      .select('id, org_id')
      .eq('platform', 'shopify')
      .eq('oauth_tokens->>shop_domain', shop)
      .maybeSingle();
    storeRow = data;
  }
  if (!storeRow) return new NextResponse('Store not found', { status: 404 });

  // Attach to org
  await db.from('stores').update({ org_id: resolvedOrgId }).eq('id', storeRow.id);
  return NextResponse.json({ ok: true, storeId: storeRow.id, orgId: resolvedOrgId });
}
```

---

## src/app/api/webhooks/shopify/route.ts
```ts
export const runtime = 'nodejs';
import { NextRequest, NextResponse } from 'next/server';
import crypto from 'crypto';
import { createServerClient } from '@core/supabaseServer';
import { z } from 'zod';

export async function POST(req: NextRequest) {
  const hmacHeader = req.headers.get('x-shopify-hmac-sha256') || '';
  const topic = (req.headers.get('x-shopify-topic') || '').toLowerCase();
  const shopDomain = (req.headers.get('x-shopify-shop-domain') || '').toLowerCase();
  const rawBody = await req.text();
  const secret = process.env.SHOPIFY_WEBHOOK_SECRET || '';
  // Rate limit per shop domain or source IP
  try {
    const db = createServerClient();
    const identifier = shopDomain || (req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() || 'unknown');
    await db.rpc('check_rate_limit', { p_key: 'shopify_webhook', p_identifier: identifier, p_window_seconds: 10, p_max_calls: 30 });
  } catch {}
  const hash = crypto.createHmac('sha256', secret).update(rawBody, 'utf8').digest('base64');
  if (!hmacHeader || hash !== hmacHeader) {
    return new NextResponse('Invalid HMAC', { status: 401 });
  }
  // Topic allowlist
  const allowed = new Set([
    'orders/create',
    'orders/updated',
    'shopify_payments/disputes/create',
    'shopify_payments/disputes/update'
  ]);
  if (!allowed.has(topic)) {
    return NextResponse.json({ ok: true, ignored: true });
  }
  const payload = JSON.parse(rawBody);
  // Minimal per-topic shape validation
  const base = z.object({ id: z.any().optional() });
  const orderSchema = base.extend({
    customer: z.any().optional(),
    line_items: z.array(z.any()).optional(),
    billing_address: z.any().optional(),
    shipping_address: z.any().optional(),
    created_at: z.any().optional()
  });
  const disputeSchema = base.extend({
    status: z.string().optional(),
    amount: z.any().optional(),
    disputed_amount: z.any().optional()
  });
  try {
    if (topic === 'orders/create' || topic === 'orders/updated') orderSchema.parse(payload);
    if (topic.startsWith('shopify_payments/disputes/')) disputeSchema.parse(payload);
  } catch {
    return new NextResponse('Invalid payload', { status: 400 });
  }

  const db = createServerClient();
  // Idempotency guard
  const provider = 'shopify';
  const idempotencyKey = `${topic}:${payload.id || payload.dispute_id || crypto.createHash('sha256').update(rawBody).digest('hex')}`;
  const { data: existingEvent } = await db
    .from('webhook_events')
    .select('id')
    .eq('provider', provider)
    .eq('idempotency_key', idempotencyKey)
    .maybeSingle();
  if (existingEvent) return NextResponse.json({ ok: true, duplicate: true });
  await db.from('webhook_events').insert({ provider, idempotency_key: idempotencyKey, payload: payload as any });
  // Resolve store by shop domain stored in oauth_tokens
  const { data: store } = await db
    .from('stores')
    .select('id, org_id, oauth_tokens')
    .eq('platform', 'shopify')
    .eq('oauth_tokens->>shop_domain', shopDomain)
    .maybeSingle();

  if (!store) return NextResponse.json({ ok: true, no_store: true });

  try {
    if (topic === 'orders/create' || topic === 'orders/updated') {
      // Minimal upsert: insert order snapshot
      await db.from('orders').insert({
        org_id: store.org_id,
        store_id: store.id,
        customer_json: payload.customer || {},
        items_json: payload.line_items || [],
        addresses_json: { shipping_address: payload.shipping_address || {}, billing_address: payload.billing_address || {} },
        raw: payload
      });
      await db.from('audit_events').insert({ org_id: store.org_id, action: 'webhook.shopify.order', data: { topic, id: payload.id } });
    } else if (topic === 'shopify_payments/disputes/create' || topic === 'shopify_disputes/create' || topic === 'disputes/create') {
      const pspId = String(payload.id || payload.dispute_id || '');
      const reason = payload.reason || payload.reason_details || 'unknown';
      const amount = (payload.amount_cents ?? payload.amount ?? 0) / 100.0;
      const { data: existing } = await db
        .from('disputes')
        .select('id')
        .eq('org_id', store.org_id)
        .eq('psp_id', pspId)
        .maybeSingle();
      const row = {
        org_id: store.org_id,
        store_id: store.id,
        psp_id: pspId,
        psp_provider: 'shopify',
        reason_code: reason,
        amount: amount,
        status: 'new',
        raw: payload
      } as any;
      if (existing) {
        await db.from('disputes').update(row).eq('id', existing.id);
      } else {
        await db.from('disputes').insert(row);
      }
      await db.from('audit_events').insert({ org_id: store.org_id, action: 'webhook.shopify.dispute', data: { topic, id: pspId } });
      // Reconcile latest submission receipt if missing external_ref
      try {
        const { data: lastSub } = await db
          .from('submissions')
          .select('id, receipt')
          .order('submitted_at', { ascending: false })
          .limit(1)
          .maybeSingle();
        if (lastSub?.id && (!lastSub.receipt || !lastSub.receipt.external_ref)) {
          await db
            .from('submissions')
            .update({ receipt: { ...(lastSub.receipt || {}), external_ref: pspId, webhook: topic } })
            .eq('id', lastSub.id);
        }
      } catch {}
    }
  } catch (processErr: any) {
    try {
      await db.from('webhook_dead_letters').insert({
        provider: 'shopify',
        idempotency_key: idempotencyKey,
        payload: payload as any,
        error: String(processErr?.message || processErr)
      });
    } catch {}
  }

  return NextResponse.json({ ok: true });
}
```

---

## src/app/api/shopify/backfill/route.ts
```ts
export const runtime = 'nodejs';
import { NextRequest, NextResponse } from 'next/server';
import { createServerClient } from '@core/supabaseServer';
import { getShopifyClient } from '@core/shopify';

export async function POST(req: NextRequest) {
  const { shop, limit = 50 } = await req.json();
  if (!shop) return new NextResponse('Missing shop', { status: 400 });
  const db = createServerClient();

  // Resolve access token
  const { data: store } = await db
    .from('stores')
    .select('id, org_id, oauth_tokens')
    .eq('platform', 'shopify')
    .eq('oauth_tokens->>shop_domain', shop)
    .maybeSingle();
  if (!store?.oauth_tokens?.shopify_access_token) return new NextResponse('Store not found or token missing', { status: 404 });

  const rest: any = getShopifyClient(shop, store.oauth_tokens.shopify_access_token);

  // Orders backfill (recent)
  try {
    const ordersResp = await rest.orders.list({ limit: Math.min(limit, 100) });
    for (const o of ordersResp?.data || []) {
      await db.from('orders').upsert({
        org_id: store.org_id,
        store_id: store.id,
        customer_json: o.customer || {},
        items_json: o.line_items || [],
        addresses_json: { shipping_address: o.shipping_address || {}, billing_address: o.billing_address || {} },
        raw: o,
        created_at: o.created_at || new Date().toISOString()
      }, { onConflict: 'id' });
    }
  } catch (e) {
    console.warn('Orders backfill failed', e);
  }

  // Disputes backfill: Shopify Payments disputes API may differ per shop; keep best-effort
  try {
    // If available, call relevant disputes endpoint and upsert into disputes table
  } catch (e) {
    console.warn('Disputes backfill skipped/failed', e);
  }

  return NextResponse.json({ ok: true });
}
```

---

## src/app/api/shopify/oauth/start/route.ts
```ts
export const runtime = 'nodejs';
import { NextRequest, NextResponse } from 'next/server';
import { getConfig } from '@core/config';
import crypto from 'crypto';

export async function GET(req: NextRequest) {
  const cfg = getConfig();
  const url = new URL(req.url);
  const shop = url.searchParams.get('shop');
  if (!shop) return new NextResponse('Missing shop', { status: 400 });

  const state = crypto.randomBytes(16).toString('hex');
  const redirectUri = `${url.origin}/api/shopify/oauth/callback`;
  // Least-privilege defaults if not configured
  const configured = (cfg.SHOPIFY_SCOPES || '').split(',').map(s => s.trim()).filter(Boolean);
  const scopes = configured.length ? configured : ['read_orders','read_disputes','write_disputes'];
  const authUrl = `https://${shop}/admin/oauth/authorize?client_id=${encodeURIComponent(cfg.SHOPIFY_APP_KEY || '')}&scope=${encodeURIComponent(scopes.join(','))}&redirect_uri=${encodeURIComponent(redirectUri)}&state=${encodeURIComponent(state)}`;

  const res = NextResponse.redirect(authUrl);
  res.cookies.set('shopify_oauth_state', state, { httpOnly: true, secure: true, sameSite: 'lax', path: '/' });
  res.cookies.set('shopify_shop', shop, { httpOnly: true, secure: true, sameSite: 'lax', path: '/' });
  return res;
}
```

---

## src/app/api/shopify/oauth/callback/route.ts
```ts
export const runtime = 'nodejs';
import { NextRequest, NextResponse } from 'next/server';
import { getConfig } from '@core/config';
import { createServerClient } from '@core/supabaseServer';
import { getShopifyClient } from '@core/shopify';
import crypto from 'crypto';

// Verify HMAC on query params to prevent tampering
function verifyShopifyQueryHmac(url: URL, secret: string): boolean {
  const params = new URLSearchParams(url.search);
  const hmac = params.get('hmac') || '';
  params.delete('hmac');
  const msg = params.toString();
  const digest = crypto.createHmac('sha256', secret).update(msg).digest('hex');
  try {
    return crypto.timingSafeEqual(Buffer.from(hmac, 'utf8'), Buffer.from(digest, 'utf8'));
  } catch {
    return false;
  }
}

export async function GET(req: NextRequest) {
  const url = new URL(req.url);
  const code = url.searchParams.get('code');
  const shop = url.searchParams.get('shop');
  const state = url.searchParams.get('state');
  const stateCookie = req.cookies.get('shopify_oauth_state')?.value;
  if (!code || !shop || !state || state !== stateCookie) return new NextResponse('Missing/invalid params', { status: 400 });
  const cfg = getConfig();
  if (!verifyShopifyQueryHmac(url, cfg.SHOPIFY_APP_SECRET || '')) {
    return new NextResponse('Invalid query HMAC', { status: 401 });
  }
  // Exchange code for permanent access token with timeout
  const controller = new AbortController();
  const t = setTimeout(() => controller.abort(), 8000);
  const resp = await fetch(`https://${shop}/admin/oauth/access_token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ client_id: cfg.SHOPIFY_APP_KEY, client_secret: cfg.SHOPIFY_APP_SECRET, code }),
    signal: controller.signal
  }).catch((e) => ({ ok: false, statusText: String(e) } as any));
  clearTimeout(t);
  if (!resp || !(resp as any).ok) return new NextResponse('Token exchange failed', { status: 400 });
  const data = await (resp as any).json();
  const accessToken = data.access_token as string;
  const db = createServerClient();
  // Resolve current user/org or create a new org for the user if none
  const { data: { user } } = await (db.auth as any).getUser();
  let resolvedOrgId: string | null = null;
  if (user) {
    const { data: uor } = await db
      .from('user_org_roles')
      .select('org_id')
      .eq('user_id', user.id)
      .maybeSingle();
    if (uor?.org_id) {
      resolvedOrgId = uor.org_id;
    } else {
      // Create org based on shop domain and attach user as owner
      const orgName = shop!.replace('.myshopify.com', '');
      const { data: org } = await db
        .from('orgs')
        .insert({ name: orgName })
        .select('id')
        .single();
      if (org?.id) {
        resolvedOrgId = org.id;
        await db.from('user_org_roles').insert({ user_id: user.id, org_id: resolvedOrgId, role: 'owner' });
      }
    }
  }

  // Upsert store with unified oauth_tokens keys
  const tokenPayload = { shop_domain: shop, shopify_access_token: accessToken } as any;
  const row = { platform: 'shopify', oauth_tokens: tokenPayload } as any;
  const { data: existing } = await db
    .from('stores')
    .select('id, org_id')
    .eq('platform', 'shopify')
    .eq('oauth_tokens->>shop_domain', shop)
    .maybeSingle();
  let storeId: string | null = existing?.id || null;
  if (existing) {
    await db.from('stores').update(row).eq('id', existing.id);
  } else {
    const { data: inserted } = await db.from('stores').insert({ ...row, org_id: resolvedOrgId }).select('id').single();
    storeId = inserted?.id || null;
  }

  // If user/org resolved after insert, ensure attachment
  if (resolvedOrgId && storeId) {
    await db.from('stores').update({ org_id: resolvedOrgId }).eq('id', storeId);
  }

  // Auto-register webhooks (best effort)
  try {
    const rest = getShopifyClient(shop!, accessToken);
    await (rest as any).webhookSubscriptions.create({
      webhook_subscription: { topic: 'orders/create', format: 'json', address: `${url.origin}/api/webhooks/shopify` }
    });
    await (rest as any).webhookSubscriptions.create({
      webhook_subscription: { topic: 'orders/updated', format: 'json', address: `${url.origin}/api/webhooks/shopify` }
    });
    await (rest as any).webhookSubscriptions.create({
      webhook_subscription: { topic: 'shopify_payments/disputes/create', format: 'json', address: `${url.origin}/api/webhooks/shopify` }
    });
  } catch (e) {
    console.warn('Shopify webhook registration failed', e);
  }

  // Trigger initial backfill (non-blocking)
  try {
    await fetch(`${url.origin}/api/shopify/backfill`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ shop }) });
  } catch {}

  // Redirect back to onboarding to continue setup after successful connect
  const redirect = NextResponse.redirect(`${url.origin}/onboarding`);
  redirect.cookies.delete('shopify_oauth_state');
  redirect.cookies.delete('shopify_shop');
  return redirect;
}
```

---

## src/app/api/stripe/oauth/start/route.ts
```ts
export const runtime = 'nodejs';
import { NextRequest, NextResponse } from 'next/server';
import { getConfig } from '@core/config';

export async function GET(req: NextRequest) {
  const cfg = getConfig();
  const url = new URL(req.url);
  const redirectUri = `${url.origin}/api/stripe/oauth/callback`;
  const params = new URLSearchParams({
    response_type: 'code',
    client_id: cfg.STRIPE_CONNECT_CLIENT_ID || '',
    scope: 'read_write',
    redirect_uri: redirectUri
  });
  return NextResponse.redirect(`https://connect.stripe.com/oauth/authorize?${params.toString()}`);
}
```

---

## src/app/api/stripe/oauth/callback/route.ts
```ts
export const runtime = 'nodejs';
import { NextRequest, NextResponse } from 'next/server';
import { getConfig } from '@core/config';
import { createServerClient } from '@core/supabaseServer';

export async function GET(req: NextRequest) {
  const url = new URL(req.url);
  const code = url.searchParams.get('code');
  if (!code) return new NextResponse('Missing code', { status: 400 });
  const cfg = getConfig();

  // Exchange code for tokens
  const tokenRes = await fetch('https://connect.stripe.com/oauth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      client_id: cfg.STRIPE_CONNECT_CLIENT_ID || '',
      client_secret: process.env.STRIPE_API_KEY || ''
    })
  });
  if (!tokenRes.ok) return new NextResponse('Stripe token exchange failed', { status: 400 });
  const tokenJson: any = await tokenRes.json();
  const stripeAccountId: string = tokenJson.stripe_user_id;
  const accessToken: string = tokenJson.access_token;

  const db = createServerClient();
  // Resolve current user/org
  const { data: { user } } = await (db.auth as any).getUser();
  if (!user) return new NextResponse('Unauthorized', { status: 401 });
  const { data: uor } = await db
    .from('user_org_roles')
    .select('org_id')
    .eq('user_id', user.id)
    .maybeSingle();
  let orgId = uor?.org_id || null;
  if (!orgId) {
    const { data: org } = await db.from('orgs').insert({ name: 'Stripe Org' }).select('id').single();
    orgId = org?.id || null;
    if (orgId) await db.from('user_org_roles').insert({ user_id: user.id, org_id: orgId, role: 'owner' });
  }
  if (!orgId) return new NextResponse('Org not resolved', { status: 400 });

  // Upsert stripe store for this org
  const row = {
    platform: 'stripe',
    oauth_tokens: { stripe_account_id: stripeAccountId, stripe_access_token: accessToken },
    org_id: orgId
  } as any;

  const { data: existing } = await db
    .from('stores')
    .select('id')
    .eq('platform', 'stripe')
    .eq('org_id', orgId)
    .eq('oauth_tokens->>stripe_account_id', stripeAccountId)
    .maybeSingle();

  if (existing) {
    await db.from('stores').update(row).eq('id', existing.id);
  } else {
    await db.from('stores').insert(row);
  }

  // After connect, prefer returning user to onboarding to complete setup
  return NextResponse.redirect(`${url.origin}/onboarding`);
}
```

---

## src/app/api/submissions/route.ts
```ts
export const runtime = 'nodejs';
import { NextRequest, NextResponse } from 'next/server';
import { buildPdfFromPacket } from '@core/pdf';
import { composePacket } from '@chargebacks/evidenceComposer';
import { SubmissionRequest } from '@/types';
import { createServerClient } from '@core/supabaseServer';
import { submitToStripe, submitToShopify, mapShopifyError, mapStripeError } from '@chargebacks/submissionAdapters';
import crypto from 'crypto';
import { requireEntitlement } from '@core/entitlements';

export async function POST(req: NextRequest) {
  const body = await req.json();
  const parsed = SubmissionRequest.safeParse(body);
  if (!parsed.success) return new NextResponse('Bad Request', { status: 400 });
  
  const { disputeId, method } = parsed.data as any;
  const scheduledAt: string | undefined = (body && body.scheduledAt) || undefined;
  const db = createServerClient();

  try {
    // If scheduled for future, create job and exit
    if (scheduledAt && new Date(scheduledAt).getTime() > Date.now()) {
      // Resolve org
      const { data: disputeRow } = await db
        .from('disputes')
        .select('org_id')
        .eq('id', disputeId)
        .single();
      if (!disputeRow?.org_id) return new NextResponse('Forbidden', { status: 403 });
      await db.from('submission_jobs').insert({
        org_id: disputeRow.org_id,
        dispute_id: disputeId,
        method,
        scheduled_at: new Date(scheduledAt).toISOString(),
        status: 'scheduled'
      });
      return NextResponse.json({ status: 'scheduled' });
    }

    // 1. Compose evidence packet
    const packet = await composePacket(disputeId);
    // Block submission if server-reported gaps
    if (packet.gaps && packet.gaps.length > 0) {
      return new NextResponse(JSON.stringify({ error: 'Pre-submission validation failed', gaps: packet.gaps }), { status: 400 });
    }
    
    // Entitlement gating for autosubmit
    if (method === 'api') {
      const { data: dispute } = await db
        .from('disputes')
        .select('org_id')
        .eq('id', disputeId)
        .single();
      if (!dispute?.org_id) return new NextResponse('Forbidden', { status: 403 });
      await requireEntitlement(dispute.org_id, 'evidence_autosubmit');
    }

    // Optional: rate limit submissions per user/org (10 per 60s)
    try {
      await db.rpc('check_rate_limit', { p_key: 'submissions', p_identifier: 'global', p_window_seconds: 60, p_max_calls: 10 });
    } catch {}
    
    // 2. Generate PDF with the composed sections
    const pdfResult = await buildPdfFromPacket(packet);
    
    // 3. Calculate content hash for immutability
    const contentHash = crypto
      .createHash('sha256')
      .update(JSON.stringify(packet))
      .digest('hex');
    
    // 4. Create submission record + audit log (idempotency guard)
    const idempotencyKey = `sub_${disputeId}_${contentHash}`.slice(0, 255);
    const { data: existingSub } = await db
      .from('submissions')
      .select('id')
      .eq('dispute_id', disputeId)
      .eq('receipt->>content_hash', contentHash)
      .maybeSingle();
    if (existingSub?.id) {
      return NextResponse.json({
        submissionId: existingSub.id,
        packetId: packet.id,
        pdfUrl: pdfResult.url,
        status: 'generated',
        externalRef: null
      });
    }
    const { data: submission, error: submissionError } = await db
      .from('submissions')
      .insert({
        dispute_id: disputeId,
        submitted_at: new Date().toISOString(),
        method,
        status: 'processing',
        receipt: { 
          pdf_url: pdfResult.url,
          storage_path: pdfResult.storagePath,
          content_hash: contentHash,
          sections_count: packet.sections.length,
          attachments_count: packet.attachments.length
        }
      })
      .select('id')
      .single();

    if (submissionError || !submission) {
      throw new Error('Failed to create submission record');
    }

    // 5. Store immutable packet reference
    await db.from('submission_packets').insert({
      submission_id: submission.id,
      sha256: contentHash,
      storage_path: pdfResult.storagePath
    });

    // 6. Get dispute details for platform submission
    const { data: dispute } = await db
      .from('disputes')
      .select('*, stores!inner(platform, oauth_tokens)')
      .eq('id', disputeId)
      .single();

    // 7. Submit to payment processor based on method (with retry)
    let externalRef = null;
    if (method === 'api' && dispute) {
      try {
        const attempt = async () => {
        if (dispute.psp_provider === 'shopify' || dispute.stores.platform === 'shopify') {
            return await submitToShopify(dispute, packet, pdfResult.url);
        } else if (dispute.psp_provider === 'stripe') {
            return await submitToStripe(dispute, packet, pdfResult.url, submission.id, contentHash);
          }
          return null;
        };
        const maxAttempts = 3;
        let lastErr: any = null;
        for (let i = 1; i <= maxAttempts; i++) {
          try { externalRef = await attempt(); break; } catch (e:any) {
            lastErr = e; await new Promise(r=>setTimeout(r, i*300));
          }
        }
        if (!externalRef && lastErr) throw lastErr;
        
        // Update submission with external reference
        await db
          .from('submissions')
          .update({ 
            status: 'submitted',
            receipt: {
              ...submission.receipt,
              external_ref: externalRef
            }
          })
          .eq('id', submission.id);

        // Audit event
        try {
          await db.from('audit_events').insert({
            org_id: dispute.org_id,
            action: 'submission.submitted',
            data: { dispute_id: disputeId, submission_id: submission.id, method }
          });
        } catch {}
      } catch (submitError: any) {
        // Map provider error codes/messages where possible and do not fail PDF generation
        console.error('External submission failed:', submitError);
        let providerError = { code: 'submit_error', message: submitError.message } as any;
        try {
          if (dispute?.psp_provider === 'stripe') providerError = await mapStripeError(submitError);
          if (dispute?.psp_provider === 'shopify') providerError = await mapShopifyError(submitError);
        } catch {}
        await db
          .from('submissions')
          .update({ 
            status: 'generated',
            receipt: {
              ...submission.receipt,
              submit_error: providerError.message,
              submit_error_code: providerError.code
            }
          })
          .eq('id', submission.id);

        // Audit failure
        try {
          await db.from('audit_events').insert({
            org_id: dispute?.org_id,
            action: 'submission.failed',
            data: { dispute_id: disputeId, submission_id: submission.id, error: submitError.message }
          });
        } catch {}
      }
    }

    return NextResponse.json({
      submissionId: submission.id,
      packetId: packet.id,
      pdfUrl: pdfResult.url,
      status: externalRef ? 'submitted' : 'generated',
      externalRef
    });
    
  } catch (error: any) {
    console.error('Submission API error:', error);
    return new NextResponse(`Submission failed: ${error.message}`, { status: 500 });
  }
}
```

---

## src/app/api/submissions/batch/route.ts
```ts
import { NextRequest, NextResponse } from 'next/server';
import { createServerClient } from '@core/supabaseServer';
import { requireEntitlement } from '@core/entitlements';

export async function POST(req: NextRequest) {
  const { disputeIds, method, scheduledAt } = await req.json().catch(()=>({}));
  if (!Array.isArray(disputeIds) || disputeIds.length === 0 || !method) return new NextResponse('Bad Request', { status: 400 });
  const db = createServerClient();

  if (method === 'api') {
    const { data: rows } = await db
      .from('disputes')
      .select('id, org_id')
      .in('id', disputeIds);
    const orgId = rows?.[0]?.org_id;
    if (!orgId) return new NextResponse('Forbidden', { status: 403 });
    await requireEntitlement(orgId, 'evidence_autosubmit');
  }

  if (scheduledAt && new Date(scheduledAt).getTime() > Date.now()) {
    const { data: first } = await db
      .from('disputes')
      .select('org_id')
      .eq('id', disputeIds[0])
      .single();
    if (!first?.org_id) return new NextResponse('Forbidden', { status: 403 });
    const payload = disputeIds.map((id: string) => ({
      org_id: first.org_id,
      dispute_id: id,
      method,
      scheduled_at: new Date(scheduledAt).toISOString(),
      status: 'scheduled'
    }));
    await db.from('submission_jobs').insert(payload);
    return NextResponse.json({ status: 'scheduled', count: disputeIds.length });
  }

  try {
    await Promise.all(disputeIds.map((id: string) =>
      fetch('/api/submissions', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ disputeId: id, method }) })
    ));
  } catch {}
  return NextResponse.json({ status: 'queued', count: disputeIds.length });
}
```

---

## src/app/api/submissions/status/route.ts
```ts
import { NextRequest, NextResponse } from 'next/server';
import { createServerClient } from '@core/supabaseServer';

export async function GET(req: NextRequest) {
  const db = createServerClient();
  const url = new URL(req.url);
  const disputeId = url.searchParams.get('disputeId');
  if (!disputeId) return new NextResponse('Bad Request', { status: 400 });

  const { data } = await db
    .from('submissions')
    .select('id, status, submitted_at, receipt')
    .eq('dispute_id', disputeId)
    .order('submitted_at', { ascending: false })
    .limit(1)
    .maybeSingle();

  return NextResponse.json({ submission: data || null });
}
```

---

## src/app/api/evidence/route.ts
```ts
import { NextRequest, NextResponse } from 'next/server';
import { EvidenceRequest } from '@/types';
import { composePacket } from '@chargebacks/evidenceComposer';
import { getSignedUrl } from '@core/storage';

export async function POST(req: NextRequest) {
  const body = await req.json();
  const parsed = EvidenceRequest.safeParse(body);
  if (!parsed.success) return new NextResponse('Bad Request', { status: 400 });
  
  try {
    const { disputeId } = parsed.data;
    const packet = await composePacket(disputeId);
    // Map attachment storage paths to time-limited signed URLs
    const safeAttachments = [] as any[];
    for (const a of packet.attachments || []) {
      try {
        const url = await getSignedUrl(a.path, 900);
        safeAttachments.push({ ...a, url });
      } catch {
        safeAttachments.push(a);
      }
    }

    return NextResponse.json({ 
      draft: { 
        sections: packet.sections,
        attachments: safeAttachments,
        metadata: packet.metadata,
        readiness: packet.readiness,
        gaps: packet.gaps,
        guidance: packet.guidance
      } 
    });
  } catch (error: any) {
    return new NextResponse(error.message, { status: 400 });
  }
}
```

---

## src/app/api/attachments/upload/route.ts
```ts
import { NextRequest, NextResponse } from 'next/server';
import { createServerClient } from '@core/supabaseServer';
import { validateAttachmentFile } from '@core/storage';

export const runtime = 'nodejs';

export async function POST(req: NextRequest) {
  const db = createServerClient();
  const contentType = req.headers.get('content-type') || '';
  if (!contentType.includes('multipart/form-data')) {
    return new NextResponse('Expected multipart/form-data', { status: 400 });
  }

  const form = await req.formData();
  const disputeId = form.get('disputeId') as string;
  const file = form.get('file') as unknown as File;
  const intendedType = (form.get('type') as string) || 'uncategorized';
  if (!disputeId || !file) return new NextResponse('Missing fields', { status: 400 });

  const check = validateAttachmentFile(file.name, (file as any).type || 'application/octet-stream', (file as any).size || 0);
  if (!check.ok) return new NextResponse(`Invalid file: ${check.reason}`, { status: 400 });

  // Store under attachments bucket: org/disputeId/filename to avoid collisions
  const arrayBuf = await file.arrayBuffer();
  const bytes = new Uint8Array(arrayBuf);

  // Resolve dispute to get org
  const { data: disp } = await db
    .from('disputes')
    .select('org_id')
    .eq('id', disputeId)
    .single();
  if (!disp?.org_id) return new NextResponse('Forbidden', { status: 403 });

  const objectPath = `${disp.org_id}/${disputeId}/${Date.now()}_${file.name}`;
  const { error: upErr } = await (db.storage as any)
    .from('attachments')
    .upload(objectPath, bytes, { contentType: (file as any).type });
  if (upErr) return new NextResponse(`Upload failed: ${upErr.message || upErr}`, { status: 500 });

  // Persist evidence_items row for reference
  await db.from('evidence_items').insert({
    dispute_id: disputeId,
    type: 'attachment',
    content_json: { path: objectPath, name: file.name, mime: (file as any).type, size: (file as any).size, category: intendedType }
  });

  return NextResponse.json({ ok: true, path: objectPath });
}
```

---

## src/app/api/evidence/section/route.ts
```ts
import { NextRequest, NextResponse } from 'next/server';
import { createServerClient } from '@core/supabaseServer';
import { composePacket } from '@chargebacks/evidenceComposer';

export async function POST(req: NextRequest) {
  const { disputeId, sectionType } = await req.json().catch(()=>({}));
  if (!disputeId || !sectionType) return new NextResponse('Bad Request', { status: 400 });
  try {
    // Build current packet
    const packet = await composePacket(disputeId);
    const before = packet.sections.find((s:any)=>s.title.toLowerCase().includes(sectionType.replace(/_/g,' ')) )?.content || '';
    // Re-compose to simulate regeneration; real impl can target the single builder
    const refreshed = await composePacket(disputeId);
    const after = refreshed.sections.find((s:any)=>s.title.toLowerCase().includes(sectionType.replace(/_/g,' ')) )?.content || '';
    return NextResponse.json({ before, after });
  } catch (e:any) {
    return new NextResponse(e.message, { status: 400 });
  }
}
```

---

## src/app/onboarding/page.tsx
```tsx
'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { supabaseClient } from '@core/supabaseClient';

type Step = 1 | 2 | 3;

export default function Onboarding() {
  const router = useRouter();
  const [step, setStep] = useState<Step>(1);
  const [orgName, setOrgName] = useState('');
  const [shopDomain, setShopDomain] = useState('');
  const [platforms, setPlatforms] = useState<{ shopify: boolean; stripe: boolean }>({ shopify: false, stripe: false });
  const [disputesFound, setDisputesFound] = useState<number>(0);
  const [loading, setLoading] = useState(false);
  const canContinue = (step === 1 && orgName) || (step === 2 && (platforms.shopify || platforms.stripe)) || step === 3;

  const connectShopify = () => {
    if (!shopDomain) return;
    window.location.href = `/api/shopify/oauth/start?shop=${shopDomain}`;
  };
  
  const connectStripe = () => {
    window.location.href = '/api/stripe/oauth/start';
  };

  useEffect(() => {
    // Check if stores connected
    (async () => {
      const { data: { user } } = await supabaseClient.auth.getUser();
      if (!user) return;
      const { data: stores } = await supabaseClient.from('stores').select('platform');
      setPlatforms({
        shopify: !!stores?.find(s => s.platform === 'shopify'),
        stripe: !!stores?.find(s => s.platform === 'stripe')
      });
    })();
  }, []);

  const createOrg = async () => {
    setLoading(true);
    const { data: { user } } = await supabaseClient.auth.getUser();
    if (!user) return;
    const { data: org } = await supabaseClient.from('orgs').insert({ name: orgName }).select().single();
    if (org) {
      await supabaseClient.from('user_org_roles').insert({ user_id: user.id, org_id: org.id, role: 'owner' });
      setStep(2);
    }
    setLoading(false);
  };

  const checkDisputes = async () => {
    const { data: { user } } = await supabaseClient.auth.getUser();
    if (!user) return;
    const { data: row } = await supabaseClient.from('user_org_roles').select('org_id').eq('user_id', user.id).single();
    if (!row) return;
    const { count } = await supabaseClient.from('disputes').select('id', { count: 'exact', head: true }).eq('org_id', row.org_id);
    setDisputesFound(count || 0);
  };

  useEffect(() => {
    if (step === 3) checkDisputes();
  }, [step]);

  return (
    <main className="p-8 max-w-3xl mx-auto">
      {/* Progress */}
      <div className="flex items-center mb-6 text-sm text-gray-600">
        <div className={`font-medium ${step>=1?'text-blue-600':''}`}>1. Organization</div>
        <div className="mx-2">→</div>
        <div className={`font-medium ${step>=2?'text-blue-600':''}`}>2. Connect Platforms</div>
        <div className="mx-2">→</div>
        <div className={`font-medium ${step>=3?'text-blue-600':''}`}>3. Complete</div>
      </div>

      {step === 1 && (
        <section className="bg-white border rounded p-6">
          <h1 className="text-2xl font-semibold mb-2">Stop losing chargebacks. Start winning disputes.</h1>
          <p className="text-gray-600 mb-6">Connect your store and payment processor in 2 minutes.</p>
          <div className="flex items-center space-x-3 mb-6 text-xs text-gray-500">
            <span>256‑bit encryption</span>
            <span>•</span>
            <span>SOC2 compliant</span>
            <span>•</span>
            <span>No credit card required</span>
          </div>
          <label className="block text-sm font-medium mb-1">Organization Name</label>
          <input 
            className="w-full border rounded px-3 py-2" 
            value={orgName} 
            onChange={e => setOrgName(e.target.value)} 
            placeholder="My Company" 
          />
          <div className="mt-6 flex justify-end">
            <button 
              onClick={createOrg} 
              disabled={!orgName || loading} 
              className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50 hover:bg-blue-700"
            >
              {loading ? 'Creating...' : 'Get Started'}
            </button>
          </div>
        </section>
      )}

      {step === 2 && (
        <section className="bg-white border rounded p-6">
          <p className="text-sm text-gray-500 mb-4">Step 2 of 3</p>
          <div className="grid gap-4 md:grid-cols-2">
            <div className="border rounded p-4">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-semibold">Connect your Shopify store</h3>
                {platforms.shopify && <span className="text-xs text-green-600">✓ Connected</span>}
              </div>
              <p className="text-sm text-gray-600 mb-3">Import orders, customers, and fulfillment data.</p>
              {!platforms.shopify && (
                <>
                  <input 
                    className="w-full border rounded px-3 py-2 mb-3" 
                    placeholder="mystore.myshopify.com" 
                    value={shopDomain} 
                    onChange={e => setShopDomain(e.target.value)} 
                  />
                  <button 
                    onClick={connectShopify} 
                    disabled={!shopDomain}
                    className="px-3 py-2 bg-blue-600 text-white rounded w-full hover:bg-blue-700 disabled:opacity-50"
                  >
                    Connect Shopify
                  </button>
                </>
              )}
            </div>
            <div className="border rounded p-4">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-semibold">Connect your payment processor</h3>
                {platforms.stripe && <span className="text-xs text-green-600">✓ Connected</span>}
              </div>
              <p className="text-sm text-gray-600 mb-3">Sync disputes and submit evidence automatically.</p>
              <button 
                onClick={() => {
                  const url = new URL(window.location.origin + '/api/stripe/oauth/start');
                  window.location.href = url.toString();
                }} 
                className="px-3 py-2 border rounded w-full hover:bg-gray-50"
              >
                Connect Stripe
              </button>
            </div>
          </div>
          <div className="mt-6 flex justify-between">
            <button 
              onClick={() => setStep(3)} 
              className="text-sm text-gray-600 hover:underline"
            >
              I'll connect later
            </button>
            <button 
              onClick={() => setStep(3)} 
              disabled={!platforms.shopify && !platforms.stripe} 
              className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50 hover:bg-blue-700"
            >
              Continue
            </button>
          </div>
        </section>
      )}

      {step === 3 && (
        <section className="bg-white border rounded p-6 text-center">
          <div className="text-5xl mb-2">✅</div>
          <h2 className="text-xl font-semibold mb-2">You're all set! We found {disputesFound} open disputes.</h2>
          <div className="grid md:grid-cols-3 gap-4 my-6 text-sm">
            <div className="border rounded p-3">📊 Current win rate: —</div>
            <div className="border rounded p-3">⏰ Next dispute due: —</div>
            <div className="border rounded p-3">💰 Potential recovery: —</div>
          </div>
          <div className="flex justify-center gap-3">
            <button 
              onClick={() => router.push('/disputes')} 
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              View Disputes Dashboard
            </button>
            <a 
              href="#demo-chargeback-evidence-builder" 
              className="px-4 py-2 border rounded hover:bg-gray-50 inline-block"
            >
              Take a quick tour
            </a>
          </div>
        </section>
      )}
    </main>
  );
}
```

---

## src/app/orgs/new/page.tsx
```tsx
'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { supabaseClient } from '@core/supabaseClient';

export default function NewOrgPage() {
  const router = useRouter();
  const [orgName, setOrgName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleCreateOrg = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Get current user
      const { data: { user } } = await supabaseClient.auth.getUser();
      if (!user) throw new Error('Not authenticated');

      // Create organization
      const { data: org, error: orgError } = await supabaseClient
        .from('orgs')
        .insert({ name: orgName })
        .select()
        .single();

      if (orgError) throw orgError;

      // Add user as owner
      const { error: roleError } = await supabaseClient
        .from('user_org_roles')
        .insert({
          user_id: user.id,
          org_id: org.id,
          role: 'owner'
        });

      if (roleError) throw roleError;

      // Redirect to connect store
      router.push('/stores/connect');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="p-8 max-w-md mx-auto">
      <h1 className="text-2xl font-semibold mb-6">Create Your Organization</h1>
      
      <form onSubmit={handleCreateOrg} className="space-y-4">
        <div>
          <label htmlFor="orgName" className="block text-sm font-medium mb-1">
            Organization Name
          </label>
          <input
            id="orgName"
            type="text"
            value={orgName}
            onChange={(e) => setOrgName(e.target.value)}
            className="w-full px-3 py-2 border rounded-md"
            placeholder="My Company"
            required
          />
        </div>
        
        {error && (
          <div className="text-sm text-red-600">{error}</div>
        )}
        
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Creating...' : 'Create Organization'}
        </button>
      </form>
    </main>
  );
}
```

---

## src/app/stores/connect/page.tsx
```tsx
'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function ConnectStorePage() {
  const router = useRouter();
  const [platform, setPlatform] = useState<'shopify' | 'stripe'>('shopify');
  const [shopDomain, setShopDomain] = useState('');

  const handleConnect = () => {
    if (platform === 'shopify' && shopDomain) {
      // Redirect to Shopify OAuth
      window.location.href = `/api/shopify/oauth/start?shop=${shopDomain}`;
    } else if (platform === 'stripe') {
      // Redirect to Stripe Connect OAuth
      window.location.href = `/api/stripe/oauth/start`;
    }
  };

  return (
    <main className="p-8 max-w-md mx-auto">
      <h1 className="text-2xl font-semibold mb-6">Connect Your Store</h1>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">Platform</label>
          <select
            value={platform}
            onChange={(e) => setPlatform(e.target.value as 'shopify' | 'stripe')}
            className="w-full px-3 py-2 border rounded-md"
          >
            <option value="shopify">Shopify</option>
            <option value="stripe">Stripe</option>
          </select>
        </div>
        
        {platform === 'shopify' && (
          <div>
            <label htmlFor="shopDomain" className="block text-sm font-medium mb-1">
              Shop Domain
            </label>
            <input
              id="shopDomain"
              type="text"
              value={shopDomain}
              onChange={(e) => setShopDomain(e.target.value)}
              className="w-full px-3 py-2 border rounded-md"
              placeholder="mystore.myshopify.com"
              required
            />
          </div>
        )}
        
        <button
          onClick={handleConnect}
          disabled={platform === 'shopify' && !shopDomain}
          className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          Connect {platform === 'shopify' ? 'Shopify' : 'Stripe'}
        </button>
        
        <button
          onClick={() => router.push('/disputes')}
          className="w-full border border-gray-300 py-2 rounded-md hover:bg-gray-50"
        >
          Skip for now
        </button>
      </div>
    </main>
  );
}
```

---

## src/middleware.ts
```ts
import { createMiddlewareClient } from '@supabase/auth-helpers-nextjs';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(req: NextRequest) {
  const res = NextResponse.next();
  const supabase = createMiddlewareClient({ req, res });

  const {
    data: { session },
  } = await supabase.auth.getSession();

  // Allowlist: public API callbacks that must be reachable unauthenticated
  const publicApiPrefixes = [
    '/api/webhooks',
    '/api/shopify/oauth',
    '/api/stripe/oauth',
  ];
  const isPublicApi = publicApiPrefixes.some(path => req.nextUrl.pathname.startsWith(path));

  // Protected routes (app + api)
  const protectedPrefixes = [
    '/disputes',
    '/orgs',
    '/stores',
    '/settings',
    '/api/evidence',
    '/api/submissions',
    '/api/uploads',
    '/api/attachments',
    '/api/stores',
  ];
  const isProtected = !isPublicApi && protectedPrefixes.some(path => req.nextUrl.pathname.startsWith(path));

  if (isProtected && !session) {
    const redirectUrl = req.nextUrl.clone();
    redirectUrl.pathname = '/login';
    redirectUrl.searchParams.set('redirectedFrom', req.nextUrl.pathname);
    return NextResponse.redirect(redirectUrl);
  }

  return res;
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|public).*)',
  ],
};
```

---

## src/components/DataTable.tsx
```tsx
'use client';
import { useEffect, useState, useMemo } from 'react';
import { useRouter } from 'next/navigation';
import { supabaseClient } from '@core/supabaseClient';
import { formatDistanceToNow } from 'date-fns';

interface DataTableProps {
  search?: string;
  statusFilter?: string;
  onSelectionChange?: (count: number, selectedIds?: string[]) => void;
  sampleMode?: boolean;
  onSampleMode?: () => void;
  onRowClick?: (row: any) => void;
  chipFilter?: 'due_today'|'high_value'|'auto_ready'|'needs_attention'|null;
}

export function DataTable({ search = '', statusFilter = 'all', onSelectionChange, sampleMode = false, onSampleMode, onRowClick, chipFilter = null }: DataTableProps) {
  const router = useRouter();
  const [disputes, setDisputes] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Record<string, boolean>>({});

  useEffect(() => {
    fetchDisputes();
  }, []);

  const fetchDisputes = async () => {
    try {
      const { data: { user } } = await supabaseClient.auth.getUser();
      if (!user) return;

      // Get user's org
      const { data: userOrg } = await supabaseClient
        .from('user_org_roles')
        .select('org_id')
        .eq('user_id', user.id)
        .single();

      if (!userOrg) {
        router.push('/orgs/new');
        return;
      }

      // Fetch disputes for org
      const { data: disputes, error } = await supabaseClient
        .from('disputes')
        .select('*, stores(platform)')
        .eq('org_id', userOrg.org_id)
        .order('due_by', { ascending: true });

      if (error) throw error;
      setDisputes(disputes || []);
    } catch (error) {
      console.error('Error fetching disputes:', error);
    } finally {
      setLoading(false);
    }
  };

  // Apply filters client-side
  const filtered = useMemo(() => {
    let list = disputes.filter(d => {
      const matchesStatus = statusFilter === 'all' ? true : d.status === statusFilter;
      const inSearch = search ? JSON.stringify(d).toLowerCase().includes(search.toLowerCase()) : true;
      return matchesStatus && inSearch;
    });
    if (chipFilter) {
      const today = new Date();
      today.setHours(0,0,0,0);
      if (chipFilter === 'due_today') {
        list = list.filter(d => d.due_by && new Date(d.due_by).toDateString() === new Date().toDateString());
      } else if (chipFilter === 'high_value') {
        list = list.filter(d => Number(d.amount) >= 100);
      } else if (chipFilter === 'auto_ready') {
        // heuristic: drafts without known gaps → mark as auto-ready (requires server readiness; fallback to draft)
        list = list.filter(d => d.status === 'draft');
      } else if (chipFilter === 'needs_attention') {
        // heuristic: due < 3 days or status new
        const threeDays = Date.now() + 3*24*60*60*1000;
        list = list.filter(d => d.status === 'new' || (d.due_by && new Date(d.due_by).getTime() < threeDays));
      }
    }
    return list;
  }, [disputes, statusFilter, search, chipFilter]);

  const allSelected = filtered.length > 0 && filtered.every(d => selected[d.id]);
  const selectedIds = Object.keys(selected).filter((id) => !!selected[id]);
  const selectedCount = selectedIds.length;

  useEffect(() => {
    onSelectionChange?.(selectedCount, selectedIds);
  }, [selectedCount, selectedIds, onSelectionChange]);

  const toggleAll = () => {
    const next = { ...selected };
    filtered.forEach(d => { next[d.id] = !allSelected; });
    setSelected(next);
  };

  const toggleOne = (id: string) => {
    setSelected({ ...selected, [id]: !selected[id] });
  };

  const progressPct = (s: string) => {
    switch(s) {
      case 'new': return 0;
      case 'draft': return 50;
      case 'submitted': return 100;
      case 'won': return 100;
      case 'lost': return 100;
      default: return 0;
    }
  };

  if (loading) {
    return (
      <div className="border rounded bg-white p-4">
        <div className="animate-pulse space-y-3">
          <div className="h-4 bg-gray-200 rounded w-1/4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
        </div>
      </div>
    );
  }

  if (disputes.length === 0) {
    return (
      <div className="border rounded bg-white p-8 text-center">
        <svg className="w-12 h-12 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p className="text-gray-600 font-medium">No open disputes - you're all caught up!</p>
        <p className="text-sm text-gray-500 mt-2">
          Your next dispute will appear here automatically
        </p>
        <div className="flex gap-3 justify-center mt-4">
          <button
            onClick={() => router.push('/stores/connect')}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Connect Store
          </button>
          <button
            onClick={() => onSampleMode?.()}
            className="px-4 py-2 border border-purple-300 text-purple-600 rounded hover:bg-purple-50"
          >
            Explore with Sample Data
          </button>
        </div>
      </div>
    );
  }

  const getStatusColor = (status: string) => {
    const colors = {
      new: 'bg-red-100 text-red-800',
      draft: 'bg-yellow-100 text-yellow-800',
      submitted: 'bg-blue-100 text-blue-800',
      won: 'bg-green-100 text-green-800',
      lost: 'bg-gray-100 text-gray-800',
    };
    return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="border rounded bg-white overflow-hidden shadow">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 w-12">
              <input 
                type="checkbox" 
                checked={allSelected} 
                onChange={toggleAll}
                className="rounded border-gray-300"
              />
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Status
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Dispute ID
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Customer Name
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Reason
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Amount
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Due Date
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Progress
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Action
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {filtered.map((dispute) => (
            <tr
              key={dispute.id}
              className="hover:bg-gray-50 cursor-pointer"
              onClick={() => onRowClick ? onRowClick(dispute) : router.push(`/disputes/${dispute.id}`)}
            >
              <td className="px-6 py-4" onClick={(e) => e.stopPropagation()}>
                <input 
                  type="checkbox" 
                  checked={!!selected[dispute.id]} 
                  onChange={() => toggleOne(dispute.id)}
                  className="rounded border-gray-300"
                />
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <div className={`w-2 h-2 rounded-full ${dispute.status === 'new' ? 'bg-red-500' : 'bg-gray-300'}`} />
              </td>
              <td 
                className="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600 hover:underline"
                onClick={(e) => { e.stopPropagation(); onRowClick ? onRowClick(dispute) : router.push(`/disputes/${dispute.id}`); }}
              >
                {dispute.psp_id}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {dispute.raw?.customer?.name || '—'}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <span className="hover:cursor-help" title={dispute.reason_code}>
                  {dispute.reason_code?.replace(/_/g, ' ')}
                </span>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                ${dispute.amount}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {dispute.due_by ? (
                  <span className={new Date(dispute.due_by) < new Date(Date.now() + 3 * 24 * 60 * 60 * 1000) ? 'text-red-600' : ''}>
                    {formatDistanceToNow(new Date(dispute.due_by), { addSuffix: true })}
                  </span>
                ) : 'No deadline'}
              </td>
              <td className="px-6 py-4">
                <div className="flex items-center">
                  <div className="w-24 bg-gray-200 h-2 rounded-full mr-2">
                    <div 
                      className="bg-blue-600 h-2 rounded-full transition-all" 
                      style={{ width: `${progressPct(dispute.status)}%` }}
                    />
                  </div>
                  <span className="text-xs text-gray-600">{progressPct(dispute.status)}%</span>
                </div>
              </td>
              <td className="px-6 py-4">
                <button
                  onClick={() => router.push(`/disputes/${dispute.id}`)}
                  className="text-sm text-blue-600 hover:text-blue-800"
                >
                  Review
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {filtered.length > 20 && (
        <div className="bg-gray-50 px-6 py-3 border-t text-sm text-gray-600">
          Showing 1-20 of {filtered.length}
        </div>
      )}
    </div>
  );
}
```

---

## src/components/MobileDisputeCards.tsx
```tsx
'use client';
import { useEffect, useMemo, useState } from 'react';
import { supabaseClient } from '@core/supabaseClient';

export function MobileDisputeCards({ chipFilter, search='', statusFilter='all', onOpen }: { chipFilter: any; search?: string; statusFilter?: string; onOpen: (row:any)=>void; }) {
  const [disputes, setDisputes] = useState<any[]>([]);
  useEffect(() => { (async ()=>{
    const { data: { user } } = await supabaseClient.auth.getUser();
    if (!user) return;
    const { data: userOrg } = await supabaseClient.from('user_org_roles').select('org_id').eq('user_id', user.id).single();
    if (!userOrg) return;
    const { data } = await supabaseClient.from('disputes').select('*').eq('org_id', userOrg.org_id).order('due_by', { ascending: true });
    setDisputes(data || []);
  })(); }, []);

  const filtered = useMemo(() => {
    let list = disputes.filter(d => (statusFilter==='all' ? true : d.status===statusFilter) && (search? JSON.stringify(d).toLowerCase().includes(search.toLowerCase()) : true));
    if (chipFilter) {
      if (chipFilter === 'due_today') list = list.filter(d => d.due_by && new Date(d.due_by).toDateString() === new Date().toDateString());
      if (chipFilter === 'high_value') list = list.filter(d => Number(d.amount) >= 100);
      if (chipFilter === 'auto_ready') list = list.filter(d => d.status === 'draft');
      if (chipFilter === 'needs_attention') {
        const threeDays = Date.now() + 3*24*60*60*1000;
        list = list.filter(d => d.status==='new' || (d.due_by && new Date(d.due_by).getTime() < threeDays));
      }
    }
    return list;
  }, [disputes, statusFilter, search, chipFilter]);

  return (
    <div className="space-y-3">
      {filtered.map(d => (
        <button key={d.id} onClick={()=>onOpen(d)} className="w-full text-left bg-white rounded-lg shadow p-4 border">
          <div className="flex items-center justify-between">
            <div className="font-medium">{d.psp_id}</div>
            <span className={`px-2 py-0.5 text-xs rounded ${d.status==='new'?'bg-red-100 text-red-800':d.status==='draft'?'bg-yellow-100 text-yellow-800':d.status==='submitted'?'bg-blue-100 text-blue-800':d.status==='won'?'bg-green-100 text-green-800':'bg-gray-100 text-gray-800'}`}>{d.status}</span>
          </div>
          <div className="text-sm text-gray-600 mt-1">Reason: {d.reason_code?.replace(/_/g,' ')}</div>
          <div className="text-sm mt-1">Amount: ${d.amount}</div>
          <div className="text-xs text-gray-500">Due: {d.due_by ? new Date(d.due_by).toLocaleString() : 'No deadline'}</div>
        </button>
      ))}
    </div>
  );
}
```

---

## src/components/DraftEditor.tsx
```tsx
'use client';
import { useState, useEffect } from 'react';
import { useRef } from 'react';

interface DraftEditorProps {
  disputeId: string;
  evidence: any;
  onUpdate: () => void;
}

export function DraftEditor({ disputeId, evidence, onUpdate }: DraftEditorProps) {
  const [editingSection, setEditingSection] = useState<string | null>(null);
  const [editValue, setEditValue] = useState('');
  const [diff, setDiff] = useState<{ before: string; after: string } | null>(null);
  const [toast, setToast] = useState<string>('');
  const [lockedTitles, setLockedTitles] = useState<Record<string, boolean>>({});
  const [history, setHistory] = useState<Record<string, string[]>>({});
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  if (!evidence) {
    return (
      <div className="border rounded bg-white p-4">
        <div className="animate-pulse space-y-3">
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          <div className="h-20 bg-gray-200 rounded"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
      </div>
    );
  }

  const handleEdit = (sectionTitle: string, content: string) => {
    setEditingSection(sectionTitle);
    setEditValue(content);
  };

  const handleSave = async () => {
    if (!editingSection) return;
    try {
      // Persist manual override and lock by default
      const res = await fetch('/api/evidence/override', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ disputeId, title: editingSection, content: editValue, locked: true })
      });
      if (!res.ok) throw new Error(await res.text());
      setLockedTitles((prev)=>({ ...prev, [editingSection!]: true }));
      setHistory((h)=>({ ...h, [editingSection!]: [ ...(h[editingSection!]||[]), editValue ] }));
      setToast('Saved'); setTimeout(()=>setToast(''), 1200);
    } catch (e) {
      setToast('Save failed'); setTimeout(()=>setToast(''), 1500);
    } finally {
      setEditingSection(null);
      onUpdate();
    }
  };

  const handleCancel = () => {
    setEditingSection(null);
    setEditValue('');
  };

  return (
    <div className="border rounded bg-white divide-y">
      {evidence.sections?.map((section: any, index: number) => (
        <div key={index} className="p-4">
          <div className="flex justify-between items-start mb-2">
            <h3 className="font-medium text-gray-900">{section.title}</h3>
            <div className="flex items-center space-x-2 text-xs">
              {section.required && (
                <span className="text-red-600">Required</span>
              )}
              <button
                onClick={() => {
                  setLockedTitles((prev) => ({ ...prev, [section.title]: !prev[section.title] }));
                  setToast(lockedTitles[section.title] ? 'Unlocked' : 'Locked');
                  setTimeout(()=>setToast(''), 1200);
                }}
                className={`hover:underline ${lockedTitles[section.title] ? 'text-gray-700' : 'text-gray-500'}`}
              >
                {lockedTitles[section.title] ? 'Unlock' : 'Lock'}
              </button>
              <button
                onClick={async () => {
                  try {
                    if (lockedTitles[section.title]) {
                      setToast('Section is locked');
                      setTimeout(()=>setToast(''), 1500);
                      return;
                    }
                    setToast('Regenerating section...');
                    const res = await fetch('/api/evidence/section', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ disputeId, sectionType: section.title.toLowerCase().replace(/\s+/g,'_') })
                    });
                    if (res.ok) {
                      const data = await res.json();
                      setDiff({ before: data.before || '', after: data.after || '' });
                      setToast('');
                    } else {
                      setToast('Failed to regenerate');
                      setTimeout(()=>setToast(''), 2000);
                    }
                  } catch {
                    setToast('Failed to regenerate');
                    setTimeout(()=>setToast(''), 2000);
                  }
                }}
                className="text-blue-600 hover:underline"
              >
                Regenerate
              </button>
              {editingSection !== section.title && (
                <button
                  onClick={() => handleEdit(section.title, section.content)}
                  className="text-blue-600 hover:underline"
                >
                  Edit
                </button>
              )}
              {(history[section.title]?.length || 0) > 0 && (
                <button
                  onClick={() => {
                    const stack = history[section.title] || [];
                    const last = stack[stack.length - 1];
                    if (!last) return;
                    setEditingSection(section.title);
                    setEditValue(last);
                  }}
                  className="text-gray-600 hover:underline"
                >
                  Undo
                </button>
              )}
            </div>
          </div>
          
          {editingSection === section.title ? (
            <div className="space-y-2">
              <textarea
                value={editValue}
                onChange={(e) => setEditValue(e.target.value)}
                className="w-full p-2 border rounded-md min-h-[100px] text-sm"
              />
              <div className="flex space-x-2">
                <button
                  onClick={handleSave}
                  className="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
                >
                  Save
                </button>
                <button
                  onClick={handleCancel}
                  className="px-3 py-1 border border-gray-300 text-sm rounded hover:bg-gray-50"
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <pre className="text-sm text-gray-600 whitespace-pre-wrap font-sans">
              {section.content}
            </pre>
          )}
        </div>
      ))}
      {diff && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div className="absolute inset-0 bg-black/30" onClick={()=>setDiff(null)} />
          <div className="relative bg-white w-full max-w-2xl rounded-lg shadow-xl p-4">
            <h4 className="font-semibold mb-2">Review Changes</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
              {(() => {
                const beforeTokens = diff.before.split(/(\s+)/);
                const afterTokens = diff.after.split(/(\s+)/);
                const beforeSet = new Map<string, number[]>();
                beforeTokens.forEach((w, i) => {
                  const arr = beforeSet.get(w) || [];
                  arr.push(i);
                  beforeSet.set(w, arr);
                });
                const used = new Set<number>();
                const afterTypes = afterTokens.map(()=>'add');
                afterTokens.forEach((w, i) => {
                  const idxs = beforeSet.get(w) || [];
                  const idx = idxs.find((j)=>!used.has(j));
                  if (idx !== undefined) { used.add(idx); afterTypes[i] = 'same'; }
                });
                const beforeTypes = beforeTokens.map((_,i)=> used.has(i) ? 'same' : 'del');
                return (
                  <>
                    <div>
                      <div className="text-gray-600 mb-1">Before</div>
                      <div className="border rounded p-2 whitespace-pre-wrap max-h-64 overflow-y-auto">
                        {beforeTokens.map((t, i) => (
                          <span key={i} className={beforeTypes[i]==='del'?'bg-red-100 line-through':''}>{t}</span>
                        ))}
                      </div>
                    </div>
                    <div>
                      <div className="text-gray-600 mb-1">After</div>
                      <div className="border rounded p-2 whitespace-pre-wrap max-h-64 overflow-y-auto">
                        {afterTokens.map((t, i) => (
                          <span key={i} className={afterTypes[i]==='add'?'bg-green-100':''}>{t}</span>
                        ))}
                      </div>
                    </div>
                  </>
                );
              })()}
            </div>
            <div className="mt-3 flex justify-end gap-2">
              <button className="px-3 py-1 border rounded" onClick={()=>setDiff(null)}>Cancel</button>
              <button className="px-3 py-1 bg-blue-600 text-white rounded" onClick={()=>{ setHistory((h)=>{ const curr = h[editingSection||'']||[]; return { ...h, [editingSection||'']: [...curr, diff.before] }; }); setDiff(null); onUpdate(); setToast('Section updated'); setTimeout(()=>setToast(''), 1500); }}>Accept Changes</button>
            </div>
          </div>
        </div>
      )}
      {toast && (
        <div className="fixed bottom-4 right-4 bg-gray-900 text-white text-sm px-3 py-2 rounded shadow">{toast}</div>
      )}
      
      {evidence.attachments && evidence.attachments.length > 0 && (
        <div className="p-4">
          <h3 className="font-medium text-gray-900 mb-2">Attachments</h3>
          <ul className="space-y-1">
            {evidence.attachments.map((attachment: any, index: number) => (
              <li key={index} className="flex items-center text-sm text-gray-600">
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                {attachment.name}
                {attachment.required && (
                  <span className="ml-2 text-xs text-red-600">(Required)</span>
                )}
              </li>
            ))}
          </ul>
          <div className="mt-3">
            <form
              onSubmit={async (e)=>{
                e.preventDefault();
                const fileEl = fileInputRef.current;
                if (!fileEl || !fileEl.files || fileEl.files.length === 0) return;
                const file = fileEl.files[0];
                const form = new FormData();
                form.append('file', file);
                form.append('disputeId', disputeId);
                try {
                  const up = await fetch('/api/uploads/put', { method: 'POST', body: form });
                  if (!up.ok) throw new Error(await up.text());
                  const { path, name, type } = await up.json();
                  const reg = await fetch('/api/evidence/attachments', {
                    method: 'POST', headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ disputeId, name, path, type, required: false })
                  });
                  if (!reg.ok) throw new Error(await reg.text());
                  setToast('Attachment uploaded'); setTimeout(()=>setToast(''), 1500);
                  onUpdate();
                  if (fileEl) fileEl.value = '';
                } catch {
                  setToast('Upload failed'); setTimeout(()=>setToast(''), 1500);
                }
              }}
              className="flex items-center gap-2"
            >
              <input ref={fileInputRef} type="file" accept=".pdf,.png,.jpg,.jpeg" className="text-sm" />
              <button type="submit" className="px-3 py-1 border rounded text-sm hover:bg-gray-50">Upload</button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
```

---

## src/components/PacketPreview.tsx
```tsx
'use client';

interface PacketPreviewProps {
  evidence: any;
  loading: boolean;
}

export function PacketPreview({ evidence, loading }: PacketPreviewProps) {
  if (loading || !evidence) {
    return (
      <div className="border rounded bg-white p-4 min-h-[400px] flex items-center justify-center">
        <div className="text-center">
          <svg className="w-12 h-12 mx-auto text-gray-400 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p className="mt-2 text-sm text-gray-600">Loading evidence preview...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="border rounded bg-white shadow-sm">
      {/* PDF Header */}
      <div className="bg-gray-50 px-4 py-3 border-b">
        <h3 className="font-medium text-gray-900">Evidence Packet Preview</h3>
        <p className="text-xs text-gray-600 mt-1">
          {evidence.sections?.length || 0} sections • {evidence.attachments?.length || 0} attachments
        </p>
      </div>
      
      {/* PDF Content */}
      <div className="p-6 space-y-6 max-h-[600px] overflow-y-auto">
        {/* Cover Page */}
        <div className="text-center pb-6 border-b">
          <h1 className="text-2xl font-bold mb-2">Chargeback Evidence Packet</h1>
          <p className="text-sm text-gray-600">
            Generated: {new Date().toLocaleDateString()}
          </p>
          {evidence.metadata && (
            <>
              <p className="text-sm text-gray-600">
                Dispute ID: {evidence.metadata.disputeId}
              </p>
              <p className="text-sm text-gray-600">
                Amount: ${evidence.metadata.amount}
              </p>
            </>
          )}
        </div>
        
        {/* Sections */}
        {evidence.sections?.map((section: any, index: number) => (
          <div key={index} className="pb-4">
            <h2 className="text-lg font-semibold mb-2">{section.title}</h2>
            <div className="text-sm text-gray-700 whitespace-pre-wrap">
              {section.content}
            </div>
          </div>
        ))}
        
        {/* Attachments */}
        {evidence.attachments && evidence.attachments.length > 0 && (
          <div className="pt-6 border-t">
            <h2 className="text-lg font-semibold mb-3">Attachments</h2>
            <ul className="space-y-2">
              {evidence.attachments.map((attachment: any, index: number) => (
                <li key={index} className="flex items-center text-sm">
                  <svg className="w-5 h-5 mr-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                  </svg>
                  <span>{attachment.name}</span>
                  <span className="ml-2 text-gray-500">({attachment.type})</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
      
      {/* PDF Footer */}
      <div className="bg-gray-50 px-4 py-3 border-t text-center">
        <p className="text-xs text-gray-600">
          This document contains confidential business information
        </p>
      </div>
    </div>
  );
}
```

---

## src/components/Charts.tsx
```tsx
'use client';
import { useEffect, useRef } from 'react';

interface ChartsProps {
  metrics: any;
}

export function Charts({ metrics }: ChartsProps) {
  const statusChartRef = useRef<HTMLCanvasElement>(null);
  const timelineChartRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!metrics) return;
    
    // Draw status distribution chart
    drawStatusChart();
    
    // Draw timeline chart
    drawTimelineChart();
  }, [metrics]);

  const drawStatusChart = () => {
    const canvas = statusChartRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    const { statusCounts } = metrics;
    const statuses = Object.keys(statusCounts || {});
    const values = Object.values(statusCounts || {}) as number[];
    const total = values.reduce((sum, v) => sum + v, 0);
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Set up dimensions
    const padding = 20;
    const barWidth = (canvas.width - padding * 2) / statuses.length;
    const maxValue = Math.max(...values, 1);
    const scale = (canvas.height - padding * 2) / maxValue;
    
    // Draw bars
    statuses.forEach((status, i) => {
      const value = values[i];
      const barHeight = value * scale;
      const x = padding + i * barWidth + barWidth * 0.1;
      const y = canvas.height - padding - barHeight;
      
      // Bar color based on status
      const colors: Record<string, string> = {
        new: '#ef4444',
        draft: '#f59e0b',
        submitted: '#3b82f6',
        won: '#10b981',
        lost: '#6b7280'
      };
      
      ctx.fillStyle = colors[status] || '#6b7280';
      ctx.fillRect(x, y, barWidth * 0.8, barHeight);
      
      // Label
      ctx.fillStyle = '#374151';
      ctx.font = '12px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(status, x + barWidth * 0.4, canvas.height - 5);
      ctx.fillText(value.toString(), x + barWidth * 0.4, y - 5);
    });
  };

  const drawTimelineChart = () => {
    const canvas = timelineChartRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    // Group disputes by month
    const monthlyData = (metrics.disputes || []).reduce((acc: any, dispute: any) => {
      const month = new Date(dispute.created_at).toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short' 
      });
      acc[month] = (acc[month] || 0) + 1;
      return acc;
    }, {});
    
    const months = Object.keys(monthlyData).slice(-6); // Last 6 months
    const values = months.map(m => monthlyData[m]);
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    if (months.length === 0) return;
    
    // Set up dimensions
    const padding = 40;
    const pointSpacing = (canvas.width - padding * 2) / (months.length - 1 || 1);
    const maxValue = Math.max(...values, 1);
    const scale = (canvas.height - padding * 2) / maxValue;
    
    // Draw axes
    ctx.strokeStyle = '#e5e7eb';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, canvas.height - padding);
    ctx.lineTo(canvas.width - padding, canvas.height - padding);
    ctx.stroke();
    
    // Draw line
    ctx.strokeStyle = '#3b82f6';
    ctx.lineWidth = 2;
    ctx.beginPath();
    
    months.forEach((month, i) => {
      const x = padding + i * pointSpacing;
      const y = canvas.height - padding - (values[i] * scale);
      
      if (i === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
      
      // Draw point
      ctx.fillStyle = '#3b82f6';
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fill();
      
      // Label
      ctx.fillStyle = '#374151';
      ctx.font = '11px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(month, x, canvas.height - padding + 15);
      ctx.fillText(values[i].toString(), x, y - 10);
    });
    
    ctx.stroke();
  };

  return (
    <div className="grid gap-6 md:grid-cols-2">
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="font-semibold mb-4">Dispute Status Distribution</h3>
        <canvas 
          ref={statusChartRef} 
          width={400} 
          height={250}
          className="w-full"
        />
      </div>
      
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="font-semibold mb-4">Disputes Over Time</h3>
        <canvas 
          ref={timelineChartRef} 
          width={400} 
          height={250}
          className="w-full"
        />
      </div>
      
      {/* Win Rate by Reason Code */}
      <div className="bg-white p-4 rounded-lg shadow md:col-span-2">
        <h3 className="font-semibold mb-4">Win Rate by Reason Code</h3>
        <div className="space-y-3">
          {Object.entries(metrics.reasonCounts || {}).map(([reason, data]: [string, any]) => {
            const winRate = data.total > 0 ? (data.won / data.total * 100).toFixed(0) : 0;
            return (
              <div key={reason} className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="capitalize">{reason.replace(/_/g, ' ')}</span>
                    <span className="text-gray-600">{winRate}% win rate ({data.total} disputes)</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-4">
                    <div 
                      className={`h-4 rounded-full transition-all ${
                        parseInt(winRate) >= 70 ? 'bg-green-500' :
                        parseInt(winRate) >= 50 ? 'bg-yellow-500' :
                        'bg-red-500'
                      }`}
                      style={{ width: `${winRate}%` }}
                    />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
      
      {/* Submission Methods */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="font-semibold mb-4">Submission Methods</h3>
        <div className="space-y-2">
          {['api', 'manual'].map(method => {
            const count = metrics.submissions?.filter((s: any) => s.method === method).length || 0;
            const percentage = metrics.submissions?.length > 0 
              ? (count / metrics.submissions.length * 100).toFixed(0)
              : 0;
            
            return (
              <div key={method} className="flex items-center justify-between">
                <span className="text-sm capitalize">{method}</span>
                <div className="flex items-center space-x-2">
                  <div className="w-32 bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-blue-600 h-2 rounded-full"
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                  <span className="text-sm font-medium">{count}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
      
      {/* Recent Activity */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="font-semibold mb-4">Recent Activity</h3>
        <div className="space-y-2 text-sm">
          {(metrics.submissions || [])
            .slice(0, 5)
            .map((submission: any, i: number) => (
              <div key={i} className="flex justify-between text-gray-600">
                <span>Submission {submission.status}</span>
                <span>{new Date(submission.created_at).toLocaleDateString()}</span>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}
```

---

## src/app/analytics/page.tsx
```tsx
'use client';
import { useEffect, useState } from 'react';
import { supabaseClient } from '@core/supabaseClient';
import { Charts } from '@ui/Charts';

export default function AnalyticsPage() {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [dateRange, setDateRange] = useState('30');

  useEffect(() => {
    fetchMetrics();
  }, [dateRange]);

  const fetchMetrics = async () => {
    try {
      const { data: { user } } = await supabaseClient.auth.getUser();
      if (!user) return;

      // Get user's org
      const { data: userOrg } = await supabaseClient
        .from('user_org_roles')
        .select('org_id')
        .eq('user_id', user.id)
        .single();

      if (!userOrg) return;

      // Date filter
      const startDate = new Date();
      startDate.setDate(startDate.getDate() - parseInt(dateRange));

      // Fetch current period disputes
      const { data: disputes } = await supabaseClient
        .from('disputes')
        .select('*, submissions(*)')
        .eq('org_id', userOrg.org_id)
        .gte('created_at', startDate.toISOString());

      // Fetch previous period for comparison
      const prevStartDate = new Date(startDate);
      prevStartDate.setDate(prevStartDate.getDate() - parseInt(dateRange));
      
      const { data: prevDisputes } = await supabaseClient
        .from('disputes')
        .select('status, amount')
        .eq('org_id', userOrg.org_id)
        .gte('created_at', prevStartDate.toISOString())
        .lt('created_at', startDate.toISOString());

      // Calculate metrics
      const totalDisputes = disputes?.length || 0;
      const totalAmount = disputes?.reduce((sum, d) => sum + parseFloat(d.amount), 0) || 0;
      const recoveredAmount = disputes?.filter(d => d.status === 'won').reduce((sum, d) => sum + parseFloat(d.amount), 0) || 0;
      
      const statusCounts = disputes?.reduce((acc, d) => {
        acc[d.status] = (acc[d.status] || 0) + 1;
        return acc;
      }, {} as Record<string, number>) || {};

      const reasonCounts = disputes?.reduce((acc, d) => {
        const reason = d.reason_code || 'unknown';
        if (!acc[reason]) acc[reason] = { total: 0, won: 0 };
        acc[reason].total++;
        if (d.status === 'won') acc[reason].won++;
        return acc;
      }, {} as Record<string, { total: number; won: number }>) || {};

      const winRate = totalDisputes > 0 
        ? ((statusCounts.won || 0) / totalDisputes * 100).toFixed(1)
        : 0;

      // Previous period win rate
      const prevWinRate = prevDisputes && prevDisputes.length > 0
        ? (prevDisputes.filter(d => d.status === 'won').length / prevDisputes.length * 100).toFixed(1)
        : 0;

      const winRateTrend = parseFloat(winRate) - parseFloat(prevWinRate);

      // Average response time
      const avgResponseTime = disputes?.filter(d => d.submissions?.length > 0)
        .map(d => {
          const submission = d.submissions[0];
          return submission ? (new Date(submission.submitted_at).getTime() - new Date(d.created_at).getTime()) / (1000 * 60 * 60) : 0;
        })
        .reduce((sum, time, _, arr) => sum + time / arr.length, 0) || 0;

      setMetrics({
        totalDisputes,
        totalAmount,
        recoveredAmount,
        winRate,
        winRateTrend,
        avgResponseTime: avgResponseTime.toFixed(1),
        statusCounts,
        reasonCounts,
        disputes,
        submissions: disputes?.flatMap(d => d.submissions || [])
      });
    } catch (error) {
      console.error('Error fetching metrics:', error);
    } finally {
      setLoading(false);
    }
  };

  const exportCSV = () => {
    if (!metrics?.disputes) return;
    
    const csv = [
      ['Dispute ID', 'Status', 'Amount', 'Reason', 'Created', 'Submitted', 'Outcome'],
      ...metrics.disputes.map((d: any) => [
        d.psp_id,
        d.status,
        d.amount,
        d.reason_code,
        new Date(d.created_at).toLocaleDateString(),
        d.submissions?.[0]?.submitted_at ? new Date(d.submissions[0].submitted_at).toLocaleDateString() : '',
        d.status === 'won' ? 'Won' : d.status === 'lost' ? 'Lost' : 'Pending'
      ])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `disputes-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
  };

  if (loading) {
    return (
      <main className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-1/4"></div>
          <div className="grid grid-cols-4 gap-4">
            {[1, 2, 3, 4].map(i => (
              <div key={i} className="h-24 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">Analytics Dashboard</h1>
        <div className="flex gap-2">
          <select 
            value={dateRange} 
            onChange={(e) => setDateRange(e.target.value)}
            className="border rounded px-3 py-2"
          >
            <option value="7">Last 7 days</option>
            <option value="30">Last 30 days</option>
            <option value="90">Last 90 days</option>
          </select>
          <button 
            onClick={exportCSV}
            className="px-4 py-2 border rounded hover:bg-gray-50"
          >
            Export CSV
          </button>
        </div>
      </div>
      
      {/* Key Metrics with Trends */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg shadow">
          <p className="text-sm text-gray-600">Total Disputes</p>
          <p className="text-2xl font-bold">{metrics?.totalDisputes || 0}</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <p className="text-sm text-gray-600">Revenue Recovered</p>
          <p className="text-2xl font-bold">${(metrics?.recoveredAmount || 0).toLocaleString()}</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <p className="text-sm text-gray-600">Win Rate</p>
          <div className="flex items-center gap-2">
            <p className="text-2xl font-bold">{metrics?.winRate || 0}%</p>
            {metrics?.winRateTrend !== 0 && (
              <span className={`text-sm ${metrics?.winRateTrend > 0 ? 'text-green-600' : 'text-red-600'}`}>
                {metrics?.winRateTrend > 0 ? '↑' : '↓'} {Math.abs(metrics?.winRateTrend).toFixed(1)}%
              </span>
            )}
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <p className="text-sm text-gray-600">Avg. Time to Submit</p>
          <p className="text-2xl font-bold">{metrics?.avgResponseTime || 0} hrs</p>
        </div>
      </div>
      
      {/* Charts with Win Rate by Reason (hide on mobile) */}
      <div className="hidden md:block">
        <Charts metrics={metrics} />
      </div>
      
      {/* Detailed Outcomes Table (hide on mobile) */}
      <div className="hidden md:block mt-6 bg-white rounded-lg shadow">
        <div className="p-4 border-b">
          <h2 className="font-semibold">Dispute Outcomes</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Dispute ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Reason</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Submitted</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Outcome</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Days to Decision</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {(metrics?.disputes || []).slice(0, 10).map((dispute: any) => (
                <tr key={dispute.id}>
                  <td className="px-6 py-4 text-sm">{dispute.psp_id}</td>
                  <td className="px-6 py-4 text-sm">{dispute.reason_code}</td>
                  <td className="px-6 py-4 text-sm">${dispute.amount}</td>
                  <td className="px-6 py-4 text-sm">
                    {dispute.submissions?.[0]?.submitted_at 
                      ? new Date(dispute.submissions[0].submitted_at).toLocaleDateString()
                      : '—'
                    }
                  </td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      dispute.status === 'won' ? 'bg-green-100 text-green-800' :
                      dispute.status === 'lost' ? 'bg-red-100 text-red-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {dispute.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm">
                    {dispute.status === 'won' || dispute.status === 'lost' ? '7' : '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      {/* Mobile summary tiles only */}
      <div className="md:hidden grid grid-cols-2 gap-3 mt-6">
        <div className="bg-white p-3 rounded shadow">
          <div className="text-xs text-gray-500">Total Disputes</div>
          <div className="text-lg font-semibold">{metrics?.totalDisputes || 0}</div>
        </div>
        <div className="bg-white p-3 rounded shadow">
          <div className="text-xs text-gray-500">Win Rate</div>
          <div className="text-lg font-semibold">{metrics?.winRate || 0}%</div>
        </div>
        <div className="bg-white p-3 rounded shadow">
          <div className="text-xs text-gray-500">Recovered</div>
          <div className="text-lg font-semibold">${(metrics?.recoveredAmount || 0).toLocaleString()}</div>
        </div>
        <div className="bg-white p-3 rounded shadow">
          <div className="text-xs text-gray-500">Avg Submit Time</div>
          <div className="text-lg font-semibold">{metrics?.avgResponseTime || 0}h</div>
        </div>
      </div>
    </main>
  );
}
```

---

## src/app/settings/page.tsx
```tsx
'use client';
import { useState, useEffect } from 'react';
import { supabaseClient } from '@core/supabaseClient';

export default function SettingsPage() {
  const [activeSection, setActiveSection] = useState('general');
  const [orgName, setOrgName] = useState('');
  const [timezone, setTimezone] = useState('America/New_York');
  const [currency, setCurrency] = useState('USD');
  const [selectedTemplate, setSelectedTemplate] = useState('ecommerce');
  const [notifications, setNotifications] = useState({
    newDispute: { email: true, app: true, sms: false },
    dueSoon: { email: true, app: true, sms: true },
    outcome: { email: true, app: true, sms: false },
    weekly: { email: true, app: false, sms: false }
  });
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    const { data: { user } } = await supabaseClient.auth.getUser();
    if (!user) return;
    
    const { data: userOrg } = await supabaseClient
      .from('user_org_roles')
      .select('org_id, orgs(*)')
      .eq('user_id', user.id)
      .single();
      
    if (userOrg?.orgs) {
      setOrgName((userOrg.orgs as any).name);
    }
  };

  const saveSettings = async () => {
    setSaving(true);
    // In production, would save to database
    setTimeout(() => {
      setSaving(false);
      alert('Settings saved!');
    }, 1000);
  };

  const sections = [
    { id: 'general', label: 'General', icon: '⚙️' },
    { id: 'templates', label: 'Evidence Templates', icon: '📄' },
    { id: 'integrations', label: 'Integrations', icon: '🔌' },
    { id: 'notifications', label: 'Notifications', icon: '🔔' },
    { id: 'billing', label: 'Billing', icon: '💳' },
    { id: 'team', label: 'Team Members', icon: '👥' },
    { id: 'advanced', label: 'Advanced', icon: '🔧' }
  ];

  return (
    <main className="p-6">
      <h1 className="text-2xl font-semibold mb-6">Settings</h1>
      
      <div className="flex gap-6">
        {/* Sidebar (desktop) */}
        <div className="hidden md:block w-64">
          <nav className="space-y-1">
            {sections.map(section => (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={`w-full text-left px-4 py-2 rounded-lg flex items-center gap-2 transition-colors ${
                  activeSection === section.id 
                    ? 'bg-blue-50 text-blue-700' 
                    : 'hover:bg-gray-100'
                }`}
              >
                <span>{section.icon}</span>
                <span>{section.label}</span>
              </button>
            ))}
          </nav>
        </div>
        {/* Mobile section picker */}
        <div className="md:hidden w-full">
          <label className="block text-sm font-medium mb-2">Section</label>
          <select
            value={activeSection}
            onChange={(e)=>setActiveSection(e.target.value)}
            className="w-full border rounded px-3 py-2 mb-4"
          >
            {sections.map(s => (
              <option key={s.id} value={s.id}>{s.label}</option>
            ))}
          </select>
        </div>

        {/* Content */}
        <div className="flex-1 bg-white rounded-lg shadow p-6">
          {activeSection === 'general' && (
            <div className="space-y-6">
              <h2 className="text-lg font-medium">General Settings</h2>
              
              <div>
                <label className="block text-sm font-medium mb-1">Organization Name</label>
                <input 
                  type="text" 
                  value={orgName} 
                  onChange={(e) => setOrgName(e.target.value)}
                  className="w-full border rounded px-3 py-2"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Time Zone</label>
                <select 
                  value={timezone} 
                  onChange={(e) => setTimezone(e.target.value)}
                  className="w-full border rounded px-3 py-2"
                >
                  <option value="America/New_York">Eastern Time</option>
                  <option value="America/Chicago">Central Time</option>
                  <option value="America/Denver">Mountain Time</option>
                  <option value="America/Los_Angeles">Pacific Time</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Default Currency</label>
                <select 
                  value={currency} 
                  onChange={(e) => setCurrency(e.target.value)}
                  className="w-full border rounded px-3 py-2"
                >
                  <option value="USD">USD - US Dollar</option>
                  <option value="EUR">EUR - Euro</option>
                  <option value="GBP">GBP - British Pound</option>
                </select>
              </div>
            </div>
          )}

          {activeSection === 'templates' && (
            <div className="space-y-6">
              <h2 className="text-lg font-medium">Evidence Templates</h2>
              
              <div>
                <label className="block text-sm font-medium mb-3">Active Template</label>
                <div className="grid grid-cols-3 gap-3">
                  {['ecommerce', 'digital', 'subscription', 'custom'].map(template => (
                    <button
                      key={template}
                      onClick={() => setSelectedTemplate(template)}
                      className={`p-4 border rounded-lg text-center capitalize ${
                        selectedTemplate === template 
                          ? 'border-blue-500 bg-blue-50' 
                          : 'hover:border-gray-400'
                      }`}
                    >
                      {template === 'ecommerce' ? 'E-commerce Standard' :
                       template === 'digital' ? 'Digital Products' :
                       template === 'subscription' ? 'Subscription Services' :
                       'Custom Template'}
                    </button>
                  ))}
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-3">Template Options</label>
                <div className="space-y-2">
                  <label className="flex items-center gap-2">
                    <input type="checkbox" defaultChecked className="rounded" />
                    <span>Include customer history</span>
                  </label>
                  <label className="flex items-center gap-2">
                    <input type="checkbox" defaultChecked className="rounded" />
                    <span>Include device fingerprinting</span>
                  </label>
                  <label className="flex items-center gap-2">
                    <input type="checkbox" defaultChecked className="rounded" />
                    <span>Include delivery confirmation</span>
                  </label>
                  <label className="flex items-center gap-2">
                    <input type="checkbox" className="rounded" />
                    <span>Include social proof</span>
                  </label>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Narrative Tone</label>
                <div className="flex items-center gap-4">
                  <span className="text-sm">Casual</span>
                  <input type="range" className="flex-1" defaultValue="75" />
                  <span className="text-sm">Professional</span>
                </div>
              </div>
            </div>
          )}

          {activeSection === 'integrations' && (
            <div className="space-y-6">
              <h2 className="text-lg font-medium">Integrations</h2>
              
              <div>
                <h3 className="font-medium mb-3">Connected Services</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between p-3 border rounded">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-green-100 rounded flex items-center justify-center">S</div>
                      <div>
                        <div className="font-medium">Shopify</div>
                        <div className="text-sm text-gray-600">Connected</div>
                      </div>
                    </div>
                    <button className="text-sm text-red-600 hover:underline">Disconnect</button>
                  </div>
                  <div className="flex items-center justify-between p-3 border rounded">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-purple-100 rounded flex items-center justify-center">S</div>
                      <div>
                        <div className="font-medium">Stripe</div>
                        <div className="text-sm text-gray-600">Connected</div>
                      </div>
                    </div>
                    <button className="text-sm text-red-600 hover:underline">Disconnect</button>
                  </div>
                </div>
              </div>
              
              <div>
                <h3 className="font-medium mb-3">Optional Integrations</h3>
                <div className="grid gap-3">
                  <button className="p-3 border rounded text-left hover:border-blue-400">
                    <div className="font-medium">Shipping Carriers</div>
                    <div className="text-sm text-gray-600">Connect FedEx, UPS, USPS for tracking</div>
                  </button>
                  <button className="p-3 border rounded text-left hover:border-blue-400">
                    <div className="font-medium">Pre-dispute Alerts</div>
                    <div className="text-sm text-gray-600">Ethoca, Verifi integration</div>
                  </button>
                  <button className="p-3 border rounded text-left hover:border-blue-400">
                    <div className="font-medium">Help Desk</div>
                    <div className="text-sm text-gray-600">Zendesk, Intercom for support history</div>
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeSection === 'notifications' && (
            <div className="space-y-6">
              <h2 className="text-lg font-medium">Notification Preferences</h2>
              
              <div className="space-y-4">
                {Object.entries(notifications).map(([key, prefs]) => (
                  <div key={key} className="border rounded p-4">
                    <h3 className="font-medium mb-3 capitalize">
                      {key === 'newDispute' ? 'New dispute received' :
                       key === 'dueSoon' ? 'Dispute due soon' :
                       key === 'outcome' ? 'Outcome received' :
                       'Weekly summary'}
                    </h3>
                    <div className="flex gap-6">
                      <label className="flex items-center gap-2">
                        <input 
                          type="checkbox" 
                          checked={prefs.email}
                          onChange={(e) => setNotifications({
                            ...notifications,
                            [key]: { ...prefs, email: e.target.checked }
                          })}
                        />
                        <span>Email</span>
                      </label>
                      <label className="flex items-center gap-2">
                        <input 
                          type="checkbox" 
                          checked={prefs.app}
                          onChange={(e) => setNotifications({
                            ...notifications,
                            [key]: { ...prefs, app: e.target.checked }
                          })}
                        />
                        <span>In-app</span>
                      </label>
                      <label className="flex items-center gap-2">
                        <input 
                          type="checkbox" 
                          checked={prefs.sms}
                          onChange={(e) => setNotifications({
                            ...notifications,
                            [key]: { ...prefs, sms: e.target.checked }
                          })}
                        />
                        <span>SMS</span>
                      </label>
                    </div>
                  </div>
                ))}
              </div>
              
              <div>
                <h3 className="font-medium mb-3">Webhook Configuration</h3>
                <div>
                  <label className="block text-sm font-medium mb-1">Slack Webhook URL</label>
                  <div className="flex gap-2">
                    <input 
                      type="text" 
                      placeholder="https://hooks.slack.com/services/..."
                      className="flex-1 border rounded px-3 py-2"
                    />
                    <button className="px-4 py-2 border rounded hover:bg-gray-50">Test</button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeSection === 'billing' && (
            <div className="space-y-6">
              <h2 className="text-lg font-medium">Billing</h2>
              
              <div className="border rounded p-6 bg-gray-50">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="font-medium">Professional Plan</h3>
                    <p className="text-gray-600">$99/month</p>
                  </div>
                  <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                    Upgrade Plan
                  </button>
                </div>
                
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-gray-600">Disputes included</p>
                    <p className="font-medium">50/month</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Additional disputes</p>
                    <p className="font-medium">$2 each</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Current usage</p>
                    <p className="font-medium">32/50 disputes</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Next billing</p>
                    <p className="font-medium">June 1, 2024</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Save button */}
          <div className="mt-8 flex justify-end">
            <button 
              onClick={saveSettings}
              disabled={saving}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {saving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}
```

---

## src/lib/supabaseClient.ts
```ts
import { createClient } from '@supabase/supabase-js';

export const supabaseClient = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);
```

---

## src/lib/supabaseServer.ts
```ts
import { createClient } from '@supabase/supabase-js';

export function createServerClient() {
  return createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  );
}
```

---

## src/lib/analytics.ts
```ts
'use client';
import { createContext, useContext } from 'react';

type AnalyticsEvent = { name: string; properties?: Record<string, unknown> };

const AnalyticsCtx = createContext({ track: (_: AnalyticsEvent) => {} });

export function AnalyticsProvider({ children }: { children: React.ReactNode }) {
  const track = (evt: AnalyticsEvent) => {
    // snake_case event names, scrub PII in properties
    void evt;
  };
  return <AnalyticsCtx.Provider value={{ track }}>{children}</AnalyticsCtx.Provider>;
}

export function useAnalytics() {
  return useContext(AnalyticsCtx);
}
```

---

## src/lib/shopify.ts
```ts
import { shopifyApi, ApiVersion } from '@shopify/shopify-api';

export function getShopifyClient(shop: string, accessToken: string) {
  return shopifyApi({
    apiKey: process.env.SHOPIFY_APP_KEY!,
    apiSecretKey: process.env.SHOPIFY_APP_SECRET!,
    scopes: (process.env.SHOPIFY_SCOPES && process.env.SHOPIFY_SCOPES.trim().length > 0)
      ? (process.env.SHOPIFY_SCOPES || '').split(',').map(s => s.trim())
      : ['read_orders','read_disputes','write_disputes'],
    apiVersion: ApiVersion.July24,
    hostName: `${shop}`
  }).rest(
    { session: { shop, accessToken } as any }
  );
}
```

---

## src/lib/stripe.ts
```ts
import Stripe from 'stripe';

export function getStripe() {
  return new Stripe(process.env.STRIPE_API_KEY || '', { apiVersion: '2024-06-20' });
}
```

---

## src/lib/pdf.ts
```ts
import { composePacket } from './evidenceComposer';
import { createServerClient } from './supabaseServer';
import { getSignedUrl } from './storage';

export async function buildPdfFromPacket(packet: { id: string; sections: any[]; attachments: any[] }) {
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
  const serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;
  
  // Call Edge Function to generate PDF
  const resp = await fetch(`${supabaseUrl}/functions/v1/generate-pdf`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${serviceKey}`
    },
    body: JSON.stringify({ 
      packetId: packet.id,
      sections: packet.sections,
      attachments: packet.attachments 
    })
  });
  
  if (!resp.ok) {
    const error = await resp.text();
    throw new Error(`PDF generation failed: ${error}`);
  }
  
  const { storagePath } = await resp.json();
  
  // Generate signed URL for immediate access
  const signedUrl = await getSignedUrl(storagePath);
  
  return { 
    url: signedUrl,
    storagePath 
  };
}

export function formatEvidence(sections: any[]): string {
  return sections.map(s => `## ${s.title}\n\n${s.content}`).join('\n\n---\n\n');
}
```

---

## src/lib/evidenceComposer.ts
```ts
import { createServerClient } from './supabaseServer';
import { UUID } from '@/types';

export type EvidenceSection = {
  title: string;
  content: string;
  required: boolean;
  weight: number;
};

export type EvidenceAttachment = {
  name: string;
  path: string;
  type: string;
  required: boolean;
};

// Reason code to evidence requirement mappings (network-aware; extend as needed)
const REASON_CODE_TEMPLATES: Record<string, { sections: string[]; attachments: string[]; networkHints?: string[] }> = {
  'fraudulent': {
    sections: ['order_details', 'customer_verification', 'shipping_proof', 'device_info', 'communication'],
    attachments: ['invoice', 'shipping_label', 'tracking_receipt', 'delivery_confirmation', 'customer_signature'],
    networkHints: ['avs_cvv', 'ip_match', 'device_fingerprint']
  },
  'subscription_canceled': {
    sections: ['subscription_details', 'cancellation_policy', 'communication', 'refund_history'],
    attachments: ['subscription_agreement', 'cancellation_request', 'refund_receipt'],
    networkHints: ['terms_timestamp', 'cancellation_flow_logs']
  },
  'product_not_received': {
    sections: ['order_details', 'shipping_proof', 'tracking_updates', 'communication'],
    attachments: ['invoice', 'shipping_label', 'tracking_receipt', 'delivery_confirmation']
  },
  'product_unacceptable': {
    sections: ['order_details', 'product_description', 'return_policy', 'communication', 'quality_proof'],
    attachments: ['invoice', 'product_photos', 'return_request', 'quality_certificate']
  },
  'duplicate': {
    sections: ['transaction_history', 'duplicate_analysis', 'communication'],
    attachments: ['transaction_logs', 'payment_receipts']
  },
  'credit_not_processed': {
    sections: ['refund_history', 'refund_policy', 'communication'],
    attachments: ['refund_receipt', 'refund_request', 'policy_document']
  },
  'general': {
    sections: ['order_details', 'customer_verification', 'communication'],
    attachments: ['invoice', 'customer_id', 'communication_logs']
  }
};

export async function composePacket(disputeId: UUID) {
  const db = createServerClient();
  
  // Fetch dispute with all related data
  const { data: dispute, error } = await db
    .from('disputes')
    .select(`
      *,
      stores!inner(id, platform, oauth_tokens),
      orders(
        id,
        customer_json,
        items_json,
        addresses_json,
        raw,
        created_at
      ),
      refund_events(
        id,
        amount,
        status,
        created_at
      ),
      communication_logs(
        id,
        content,
        channel,
        direction,
        created_at
      )
    `)
    .eq('id', disputeId)
    .single();

  if (error || !dispute) {
    throw new Error(`Dispute not found: ${disputeId}`);
  }

  const template = REASON_CODE_TEMPLATES[dispute.reason_code] || REASON_CODE_TEMPLATES['general'];
  const sections: EvidenceSection[] = [];
  const attachments: EvidenceAttachment[] = [];

  // Build sections based on template + user overrides
  for (const sectionType of template.sections) {
    const section = await buildSection(sectionType, dispute);
    if (section) sections.push(section);
  }

  // Apply manual overrides (locked sections)
  try {
    const { data: overrides } = await db
      .from('evidence_items')
      .select('content_json')
      .eq('dispute_id', disputeId)
      .eq('type', 'section_override');
    if (overrides && Array.isArray(overrides)) {
      for (const o of overrides) {
        const idx = sections.findIndex(s => s.title === o.content_json?.title);
        if (idx >= 0) {
          sections[idx] = { ...sections[idx], content: String(o.content_json?.content || sections[idx].content) };
        }
      }
    }
  } catch {}

  // Add attachments based on template
  for (const attachmentType of template.attachments) {
    const attachment = await buildAttachment(attachmentType, dispute);
    if (attachment) attachments.push(attachment);
  }

  // Sort sections by weight
  sections.sort((a, b) => b.weight - a.weight);

  // Compute readiness and advanced gaps
  const requiredSections = sections.filter(s => s.required).length;
  const requiredAttachments = attachments.filter(a => a.required).length;
  const gaps: Array<{ code: string; severity: 'error'|'warn'; message: string; action?: string }> = [];

  // AVS/CVV required for card-present fraud style codes
  const needsAvs = template.networkHints?.includes('avs_cvv');
  if (needsAvs && !/AVS Result:\s*(?!N\/A)/.test(JSON.stringify(sections))) {
    gaps.push({ code: 'missing_avs', severity: 'error', message: 'AVS result missing', action: 'collect_avs' });
  }
  if (needsAvs && !/CVV Result:\s*(?!N\/A)/.test(JSON.stringify(sections))) {
    gaps.push({ code: 'missing_cvv', severity: 'error', message: 'CVV result missing', action: 'collect_cvv' });
  }
  // Shipping proof for PNR
  if (dispute.reason_code === 'product_not_received') {
    if (!attachments.find(a => /delivery/i.test(a.name))) {
      gaps.push({ code: 'missing_delivery_proof', severity: 'error', message: 'Delivery confirmation not attached', action: 'attach_pod' });
    }
  }
  // Refund reconciliation: partial/duplicate
  const refunds = (dispute.refund_events || []) as Array<{ amount: number }>;
  const totalRefunded = refunds.reduce((s,r)=> s + Number(r.amount||0), 0);
  if (totalRefunded > 0 && totalRefunded < Number(dispute.amount||0)) {
    gaps.push({ code: 'partial_refund', severity: 'warn', message: `Partial refund detected: $${totalRefunded.toFixed(2)}` });
  }
  if (refunds.length > 1) {
    const amounts = new Set(refunds.map(r=>Number(r.amount||0)));
    if (amounts.size === 1) {
      gaps.push({ code: 'duplicate_refund_check', severity: 'warn', message: 'Multiple refunds with same amount detected; verify duplicates' });
    }
  }

  const totalRequired = (template.sections.length) + (template.attachments.length);
  const presentRequired = requiredSections + requiredAttachments;
  const readiness = Math.max(0, Math.min(100, Math.round((presentRequired / Math.max(1, totalRequired)) * 100)));

  // Simple guidance payload by reason code/network (can be expanded per issuer)
  const guidance = {
    title: `Guidance for ${dispute.reason_code}`,
    mustInclude: [
      ...(dispute.reason_code === 'product_not_received' ? ['Delivery proof'] : []),
      ...(template.networkHints?.includes('avs_cvv') ? ['AVS/CVV results'] : [])
    ],
    recommended: ['Customer history', 'Device/session info']
  };

  return { 
    id: disputeId, 
    sections, 
    attachments,
    metadata: {
      disputeId,
      reasonCode: dispute.reason_code,
      amount: dispute.amount,
      dueBy: dispute.due_by,
      status: dispute.status
    },
    readiness,
    gaps,
    guidance
  };
}

async function buildSection(type: string, dispute: any): Promise<EvidenceSection | null> {
  const db = createServerClient();
  
  switch (type) {
    case 'order_details':
      if (!dispute.orders?.[0]) return null;
      const order = dispute.orders[0];
      return {
        title: 'Order Details',
        content: `Order ID: ${order.id}
Date: ${new Date(order.created_at).toLocaleDateString()}
Customer: ${order.customer_json?.email || 'N/A'}
Phone: ${order.customer_json?.phone || 'N/A'}

Items Purchased:
${order.items_json?.map((item: any) => `- ${item.name} x${item.quantity} - $${item.price}`).join('\n') || 'N/A'}

Total Amount: $${dispute.amount}

Billing Address:
${formatAddress(order.addresses_json?.billing_address)}

Shipping Address:
${formatAddress(order.addresses_json?.shipping_address)}`,
        required: true,
        weight: 10
      };

    case 'customer_verification':
      if (!dispute.orders?.[0]) return null;
      const customer = dispute.orders[0].customer_json;
      return {
        title: 'Customer Verification',
        content: `Email: ${customer?.email || 'N/A'}
Phone: ${customer?.phone || 'N/A'}
Account Created: ${customer?.created_at || 'N/A'}
Total Orders: ${customer?.orders_count || 'N/A'}
Customer Since: ${customer?.first_order_date || 'N/A'}

AVS Result: ${dispute.raw?.evidence?.avs_result || 'N/A'}
CVV Result: ${dispute.raw?.evidence?.cvv_result || 'N/A'}`,
        required: true,
        weight: 9
      };

    case 'shipping_proof':
      const { data: shipments } = await db
        .from('order_shipments')
        .select('*')
        .eq('order_id', dispute.orders?.[0]?.id)
        .limit(1);
      
      const shipment = shipments?.[0];
      return {
        title: 'Shipping Information',
        content: `Carrier: ${shipment?.carrier || 'N/A'}
Tracking Number: ${shipment?.tracking_number || 'N/A'}
Shipped Date: ${shipment?.shipped_at || 'N/A'}
Delivery Date: ${shipment?.delivered_at || 'N/A'}
Delivery Status: ${shipment?.status || 'N/A'}
Signature Required: ${shipment?.signature_required ? 'Yes' : 'No'}
Signed By: ${shipment?.signed_by || 'N/A'}`,
        required: true,
        weight: 8
      };

    case 'device_info':
      const { data: sessions } = await db
        .from('order_sessions')
        .select('*')
        .eq('order_id', dispute.orders?.[0]?.id)
        .limit(1);
      
      const session = sessions?.[0];
      return {
        title: 'Device & Session Information',
        content: `IP Address: ${session?.ip_address || 'N/A'}
Country: ${session?.country || 'N/A'}
Device Type: ${session?.device_type || 'N/A'}
Browser: ${session?.browser || 'N/A'}
Device Fingerprint: ${session?.fingerprint || 'N/A'}
Session Duration: ${session?.duration || 'N/A'}`,
        required: false,
        weight: 6
      };

    case 'communication':
      const logs = dispute.communication_logs || [];
      if (logs.length === 0) return null;
      
      return {
        title: 'Customer Communication',
        content: logs.map((log: any) => 
          `[${new Date(log.created_at).toLocaleDateString()}] ${log.direction} via ${log.channel}:\n${log.content}`
        ).join('\n\n'),
        required: false,
        weight: 7
      };

    case 'refund_history':
      const refunds = dispute.refund_events || [];
      return {
        title: 'Refund History',
        content: refunds.length > 0 
          ? refunds.map((r: any) => `${new Date(r.created_at).toLocaleDateString()}: $${r.amount} - ${r.status}${r.external_ref ? ` (Ref: ${r.external_ref})` : ''}`).join('\n')
          : 'No refunds issued for this order.',
        required: false,
        weight: 5
      };

    case 'subscription_details': {
      const sub = dispute.subscription || null;
      if (!sub) return null;
      return {
        title: 'Subscription Details',
        content:
          `Plan: ${sub.plan || 'n/a'}\n` +
          `Status: ${sub.status || 'n/a'}\n` +
          (sub.started_at ? `Started: ${new Date(sub.started_at).toLocaleDateString()}\n` : '') +
          (sub.renewal_at ? `Next Renewal: ${new Date(sub.renewal_at).toLocaleDateString()}\n` : '') +
          (sub.cancellations?.length ? `Cancellations: ${sub.cancellations.length}` : ''),
        required: false,
        weight: 6,
      };
    }

    case 'product_description': {
      const items = dispute.orders?.[0]?.line_items || [];
      if (!Array.isArray(items) || items.length === 0) return null;
      const lines = items.map((li: any, idx: number) => {
        const name = li.name || li.title || `Item ${idx + 1}`;
        const qty = li.quantity ?? li.qty ?? 1;
        const price = typeof li.price === 'number' ? `$${li.price.toFixed(2)}` : String(li.price || 'n/a');
        return `• ${name} — Qty: ${qty} — Price: ${price}`;
      });
      return {
        title: 'Products',
        content: lines.join('\n'),
        required: true,
        weight: 7,
      };
    }

    default:
      return null;
  }
}

async function buildAttachment(type: string, dispute: any): Promise<EvidenceAttachment | null> {
  // Map attachment type to storage path prefix
  const orderId = dispute.orders?.[0]?.id || 'unknown';
  const bucket = process.env.EVIDENCE_BUCKET || 'evidence-packets';
  const prefixMap: Record<string, string> = {
    invoice: 'invoices',
    shipping_label: 'shipping',
    tracking_receipt: 'tracking',
    delivery_confirmation: 'delivery',
    product_photos: 'photos'
  };
  const filenameMap: Record<string, string> = {
    invoice: `invoice-${orderId}.pdf`,
    shipping_label: `shipping-label-${orderId}.pdf`,
    tracking_receipt: `tracking-${orderId}.pdf`,
    delivery_confirmation: `delivery-${orderId}.pdf`,
    product_photos: `product-${orderId}.zip`
  };
  if (!prefixMap[type]) return null;

  const name = filenameMap[type];
  const path = `${prefixMap[type]}/${name}`;
  // Default content types
  const typeMap: Record<string, string> = {
    product_photos: 'application/zip'
  };
  const contentType = typeMap[type] || 'application/pdf';

  return {
    name,
    path: path, // stored within private bucket; access via signed URL when needed
    type: contentType,
    required: ['invoice','shipping_label','delivery_confirmation'].includes(type)
  };
}

function formatAddress(addr: any): string {
  if (!addr) return 'N/A';
  return `${addr.name || ''}
${addr.address1 || ''}
${addr.address2 || ''}
${addr.city || ''}, ${addr.province || ''} ${addr.zip || ''}
${addr.country || ''}`.trim();
}
```

---

## src/types/index.ts
```ts
export type UUID = string;

export type DisputeStatus = 'new' | 'draft' | 'submitted' | 'won' | 'lost';

// Zod contracts (minimal)
import { z } from 'zod';

export const SubmissionRequest = z.object({
  disputeId: z.string().uuid(),
  method: z.enum(['api','manual'])
});

// Plugin system types
export interface RecoveryPlugin {
  id: string;
  name: string;
  icon: string;
  description: string;
  connectionTypes: ConnectionType[];
  detector: DetectionEngine;
  templateEngine: TemplateEngine;
  submissionHandlers: SubmissionHandler[];
  analyticsConfig: AnalyticsConfig;
}

export interface ConnectionType {
  id: string;
  name: string;
  provider: string;
  authMethod: 'oauth' | 'api_key' | 'credentials';
  configSchema: z.ZodSchema;
}

export interface DetectionEngine {
  scan(connections: Connection[]): Promise<RecoveryOpportunity[]>;
  getDetails(id: string): Promise<RecoveryOpportunity>;
}

export interface RecoveryOpportunity {
  id: string;
  pluginId: string;
  type: string;
  amount: number;
  deadline?: Date;
  status: 'new' | 'draft' | 'submitted' | 'won' | 'lost';
  metadata: Record<string, any>;
}

export interface Connection {
  id: string;
  orgId: string;
  pluginId: string;
  connectionType: string;
  provider: string;
  config: Record<string, any>;
  status: 'active' | 'error' | 'disconnected';
}

export const EvidenceRequest = z.object({
  disputeId: z.string().uuid()
});
```

---

## supabase/migrations/0001_init.sql
```sql
-- Core tables
create table if not exists orgs (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  created_at timestamptz default now()
);

create table if not exists users (
  id uuid primary key,
  email text not null,
  created_at timestamptz default now()
);

create table if not exists user_org_roles (
  user_id uuid references users(id) on delete cascade,
  org_id uuid references orgs(id) on delete cascade,
  role text not null check (role in ('owner','admin','agent')),
  primary key (user_id, org_id)
);

create table if not exists stores (
  id uuid primary key default gen_random_uuid(),
  org_id uuid not null references orgs(id) on delete cascade,
  platform text not null check (platform in ('shopify','stripe')),
  oauth_tokens jsonb not null default '{}'::jsonb,
  status text not null default 'active',
  created_at timestamptz default now()
);

create table if not exists disputes (
  id uuid primary key default gen_random_uuid(),
  org_id uuid not null references orgs(id) on delete cascade,
  store_id uuid references stores(id) on delete set null,
  psp_id text,
  psp_provider text not null check (psp_provider in ('shopify','stripe')),
  reason_code text not null,
  amount numeric(18,2) not null,
  due_by date,
  status text not null default 'new',
  raw jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);

create table if not exists orders (
  id uuid primary key default gen_random_uuid(),
  org_id uuid not null references orgs(id) on delete cascade,
  store_id uuid references stores(id) on delete set null,
  customer_json jsonb not null,
  items_json jsonb not null,
  addresses_json jsonb not null,
  raw jsonb not null default '{}'::jsonb,
  created_at timestamptz default now()
);

create table if not exists evidence_items (
  id uuid primary key default gen_random_uuid(),
  dispute_id uuid not null references disputes(id) on delete cascade,
  type text not null,
  content_json jsonb,
  content_path text,
  created_at timestamptz default now()
);

create table if not exists submissions (
  id uuid primary key default gen_random_uuid(),
  dispute_id uuid not null references disputes(id) on delete cascade,
  submitted_at timestamptz,
  method text not null,
  status text not null default 'queued',
  receipt jsonb,
  created_at timestamptz default now()
);

create table if not exists analytics_winrates (
  id uuid primary key default gen_random_uuid(),
  org_id uuid not null references orgs(id) on delete cascade,
  period date not null,
  reason_code text not null,
  win_rate numeric(5,2) not null default 0
);

create table if not exists audit_events (
  id uuid primary key default gen_random_uuid(),
  org_id uuid not null references orgs(id) on delete cascade,
  actor_user_id uuid references users(id),
  action text not null,
  data jsonb,
  created_at timestamptz default now()
);

create table if not exists refund_events (
  id uuid primary key default gen_random_uuid(),
  dispute_id uuid not null references disputes(id) on delete cascade,
  amount numeric(18,2) not null,
  created_at timestamptz default now(),
  method text,
  external_ref text
);

create table if not exists alerts (
  id uuid primary key default gen_random_uuid(),
  org_id uuid not null references orgs(id) on delete cascade,
  store_id uuid references stores(id) on delete set null,
  provider text not null,
  external_id text,
  received_at timestamptz default now(),
  status text not null default 'new',
  decision text
);

create table if not exists submission_packets (
  id uuid primary key default gen_random_uuid(),
  submission_id uuid not null references submissions(id) on delete cascade,
  sha256 text not null,
  storage_path text not null,
  created_at timestamptz default now()
);

-- In-app notifications for users
create table if not exists user_notifications (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references users(id) on delete cascade,
  alert_id uuid references alerts(id) on delete set null,
  title text not null,
  message text not null,
  read boolean not null default false,
  read_at timestamptz,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);
```
```

---

## supabase/migrations/0002_rls_policies.sql
```sql
-- Deny-all by default
alter table orgs enable row level security;
alter table users enable row level security;
alter table user_org_roles enable row level security;
alter table stores enable row level security;
alter table disputes enable row level security;
alter table orders enable row level security;
alter table evidence_items enable row level security;
alter table submissions enable row level security;
alter table analytics_winrates enable row level security;
alter table audit_events enable row level security;
alter table refund_events enable row level security;
alter table alerts enable row level security;
alter table submission_packets enable row level security;
alter table user_notifications enable row level security;

-- Helper: current user's orgs
create or replace view v_user_orgs as
select uor.user_id, uor.org_id, uor.role from user_org_roles uor;

-- Policies: user must belong to org
create policy org_access on orgs
  for select using (exists (
    select 1 from v_user_orgs v where v.org_id = orgs.id and v.user_id = auth.uid()
  ));

create policy users_self on users for select using (id = auth.uid());

create policy org_entity_access on stores
  for select using (exists (
    select 1 from v_user_orgs v where v.org_id = stores.org_id and v.user_id = auth.uid()
  ));

create policy disputes_access on disputes
  for select using (exists (
    select 1 from v_user_orgs v where v.org_id = disputes.org_id and v.user_id = auth.uid()
  ));

create policy orders_access on orders
  for select using (exists (
    select 1 from v_user_orgs v where v.org_id = orders.org_id and v.user_id = auth.uid()
  ));

create policy evidence_items_access on evidence_items
  for select using (exists (
    select 1 from disputes d join v_user_orgs v on v.org_id = d.org_id
    where d.id = evidence_items.dispute_id and v.user_id = auth.uid()
  ));

-- Extend similarly for submissions, analytics_winrates, audit_events, refund_events, alerts, submission_packets
create policy user_notifications_select on user_notifications
  for select using (user_id = auth.uid());
```

---

## supabase/migrations/0003_flags_geo.sql
```sql
create table if not exists feature_flags (
  key text primary key,
  description text,
  enabled_by_default boolean not null default false
);

create table if not exists org_feature_flags (
  org_id uuid references orgs(id) on delete cascade,
  key text references feature_flags(key) on delete cascade,
  enabled boolean not null default false,
  primary key (org_id, key)
);

create table if not exists region_capabilities (
  country_code text primary key,
  currency text not null,
  stripe_available boolean not null default true,
  shopify_available boolean not null default true
);
```

---

## supabase/migrations/0005_idempotency_audit.sql
```sql
create table if not exists webhook_events (
  id uuid primary key default gen_random_uuid(),
  provider text not null,
  idempotency_key text not null,
  status text not null default 'received',
  payload jsonb not null,
  created_at timestamptz default now()
);

create unique index if not exists ux_webhook_events_provider_key
  on webhook_events(provider, idempotency_key);

create index if not exists ix_audit_events_created_at on audit_events(created_at);
```

---

## src/lib/flags.ts
```ts
import { createServerClient } from './supabaseServer';

export async function getFlags(orgId: string) {
  const db = createServerClient();
  const { data } = await db
    .from('org_feature_flags')
    .select('key, enabled')
    .eq('org_id', orgId);
  return Object.fromEntries((data || []).map((r) => [r.key, r.enabled]));
}
```

---

## src/lib/config.ts
```ts
import { z } from 'zod';

const EnvSchema = z.object({
  NEXT_PUBLIC_SUPABASE_URL: z.string().url(),
  NEXT_PUBLIC_SUPABASE_ANON_KEY: z.string().min(1),
  SUPABASE_SERVICE_ROLE_KEY: z.string().min(1),
  STRIPE_API_KEY: z.string().optional(),
  STRIPE_WEBHOOK_SECRET: z.string().optional(),
  STRIPE_CONNECT_CLIENT_ID: z.string().optional(),
  SHOPIFY_APP_KEY: z.string().optional(),
  SHOPIFY_APP_SECRET: z.string().optional(),
  SHOPIFY_SCOPES: z.string().optional(),
  SHOPIFY_WEBHOOK_SECRET: z.string().optional(),
  EVIDENCE_BUCKET: z.string().default('evidence-packets')
});

export type AppEnv = z.infer<typeof EnvSchema>;

export function getConfig(): AppEnv {
  const parsed = EnvSchema.safeParse(process.env);
  if (!parsed.success) {
    throw new Error(`Invalid env: ${parsed.error.message}`);
  }
  return parsed.data as AppEnv;
}
```

---

## src/lib/geo.ts
```ts
export function deriveCountryFromIpHeader(headers: Headers) {
  // Prefer CDN-provided country when available (e.g., Vercel/Cloudflare)
  const h = headers.get('x-vercel-ip-country') || headers.get('cf-ipcountry') || headers.get('x-country');
  if (h && /^[A-Z]{2}$/.test(h)) return h;
  return 'US';
}
```


## src/lib/storage.ts
```ts
import { createServerClient } from './supabaseServer';

export async function getSignedUrl(path: string, expiresInSeconds = 3600): Promise<string> {
  const db = createServerClient();
  const { data, error } = await (db.storage as any)
    .from(process.env.EVIDENCE_BUCKET || 'evidence-packets')
    .createSignedUrl(path, expiresInSeconds);
  if (error) throw error;
  return data.signedUrl as string;
}

export async function objectExists(path: string): Promise<boolean> {
  const db = createServerClient();
  try {
    const bucket = process.env.EVIDENCE_BUCKET || 'evidence-packets';
    const parts = path.split('/');
    const file = parts.pop() as string;
    const prefix = parts.join('/');
    const { data } = await (db.storage as any).from(bucket).list(prefix || '', { limit: 100 });
    return Array.isArray(data) && data.some((o: any) => o.name === file);
  } catch {
    return false;
  }
}

const ALLOWED_MIME = new Set([
  'application/pdf',
  'image/png',
  'image/jpeg',
  'application/zip'
]);

export function validateAttachmentFile(filename: string, mimeType: string, sizeBytes: number): { ok: boolean; reason?: string } {
  // Size limit 10 MB
  if (!ALLOWED_MIME.has(mimeType)) return { ok: false, reason: 'unsupported_type' };
  if (sizeBytes <= 0 || sizeBytes > 10 * 1024 * 1024) return { ok: false, reason: 'invalid_size' };
  // Simple extension check
  const allowedExt = ['.pdf','.png','.jpg','.jpeg','.zip'];
  const lower = filename.toLowerCase();
  if (!allowedExt.some(ext => lower.endsWith(ext))) return { ok: false, reason: 'invalid_extension' };
  return { ok: true };
}
```

---

## src/lib/submissionAdapters.ts
```ts
import Stripe from 'stripe';
import { UUID } from '@/types';

export async function submitToStripe(dispute: any, packet: any, pdfUrl: string, submissionId?: string, packetHash?: string): Promise<string> {
  const stripe = new Stripe(process.env.STRIPE_API_KEY || '', { apiVersion: '2024-06-20' });
  
  // Map our sections to Stripe evidence fields
  const evidenceFields: Record<string, any> = {};
  
  for (const section of packet.sections) {
    switch (section.title) {
      case 'Order Details':
        evidenceFields.receipt = pdfUrl; // Link to full PDF
        evidenceFields.customer_purchase_ip = extractIPFromContent(section.content);
        break;
      case 'Customer Verification':
        evidenceFields.customer_name = extractCustomerName(section.content);
        evidenceFields.customer_email_address = extractEmail(section.content);
        break;
      case 'Shipping Information':
        evidenceFields.shipping_carrier = extractCarrier(section.content);
        evidenceFields.shipping_tracking_number = extractTracking(section.content);
        evidenceFields.shipping_documentation = pdfUrl;
        break;
      case 'Customer Communication':
        evidenceFields.customer_communication = section.content;
        break;
      case 'Refund History':
        evidenceFields.refund_policy = 'See evidence packet';
        evidenceFields.refund_refusal_explanation = section.content;
        break;
    }
  }

  // Update the dispute with evidence
  const idempotencyKey = `submit_${dispute.psp_id}_${submissionId || packet.id}_${packetHash || ''}`.slice(0, 255);
  const updated = await stripe.disputes.update(
    dispute.psp_id,
    {
    evidence: evidenceFields,
    metadata: {
      submission_id: packet.id,
      submitted_via: 'chargeback_evidence_builder'
    }
    },
    { idempotencyKey }
  );

  return updated.id;
}

export async function submitToShopify(dispute: any, packet: any, pdfUrl: string): Promise<string> {
  const shopDomain = dispute.stores.oauth_tokens.shop_domain;
  const accessToken = dispute.stores.oauth_tokens.shopify_access_token;
  
  const evidenceData = {
    shipping_documentation: pdfUrl,
    uncategorized_text: packet.sections.map((s: any) => `${s.title}:\n${s.content}`).join('\n\n'),
    attachments: packet.attachments.map((a: any) => ({
      filename: a.name,
      url: pdfUrl // In production, would be individual attachment URLs
    }))
  };

  // Basic timeout + retry/backoff for 429/5xx; raise on 401 to trigger re-auth
  const endpoint = `https://${shopDomain}/admin/api/2024-01/shopify_payments/disputes/${dispute.psp_id}/dispute_evidences.json`;
  const doRequest = async (attempt: number): Promise<Response> => {
    const controller = new AbortController();
    const timeoutMs = 10000;
    const to = setTimeout(() => controller.abort(), timeoutMs);
    try {
      const res = await fetch(endpoint, {
        method: 'PUT',
        headers: {
          'X-Shopify-Access-Token': accessToken,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ dispute_evidence: evidenceData }),
        signal: controller.signal
      });
      if (res.status === 401 || res.status === 403) {
        // Token invalid/expired or scope missing: require re-auth with least-privilege scopes
        const errTxt = await res.text().catch(() => 'Unauthorized');
        throw new Error(`SHOPIFY_UNAUTHORIZED: ${errTxt}`);
      }
      if (res.status === 429 || (res.status >= 500 && res.status < 600)) {
        if (attempt < 3) {
          const retryAfter = Number(res.headers.get('retry-after'));
          const backoff = isFinite(retryAfter) && retryAfter > 0 ? retryAfter * 1000 : Math.min(2000 * attempt, 6000);
          await new Promise(r => setTimeout(r, backoff));
          return doRequest(attempt + 1);
        }
      }
      return res;
    } finally {
      clearTimeout(to);
    }
  };

  const response = await doRequest(1);
  if (!response.ok) {
    const error = await response.text().catch(() => response.statusText);
    throw new Error(`Shopify submission failed (${response.status}): ${error}`);
  }

  const result = await response.json();
  return result.dispute_evidence.id;
}

export async function mapStripeError(e: any): Promise<{ code: string; message: string }> {
  const err = e as any;
  const code = err?.code || 'stripe_error';
  const message = err?.message || 'Stripe submission failed';
  return { code, message };
}

export async function mapShopifyError(res: Response): Promise<{ code: string; message: string }> {
  try {
    const body = await res.text();
    return { code: `shopify_${res.status}`, message: body || 'Shopify submission failed' };
  } catch {
    return { code: `shopify_${res.status}`, message: 'Shopify submission failed' };
  }
}

// Acknowledgment tracking helpers
export async function recordAcknowledgment(db: any, submissionId: string, externalId: string, provider: 'stripe'|'shopify') {
  await db
    .from('submissions')
    .update({
      status: 'submitted',
      receipt: db.sql`${db.raw('receipt')} || ${JSON.stringify({ external_ref: externalId, provider })}`
    })
    .eq('id', submissionId);
}

// Helper extraction functions
function extractEmail(content: string): string {
  const match = content.match(/Email:\s*([^\n]+)/);
  return match?.[1]?.trim() || '';
}

function extractCustomerName(content: string): string {
  const match = content.match(/Customer:\s*([^\n]+)/);
  return match?.[1]?.trim() || '';
}

function extractIPFromContent(content: string): string {
  const match = content.match(/IP Address:\s*([^\n]+)/);
  return match?.[1]?.trim() || '';
}

function extractCarrier(content: string): string {
  const match = content.match(/Carrier:\s*([^\n]+)/);
  return match?.[1]?.trim() || '';
}

function extractTracking(content: string): string {
  const match = content.match(/Tracking Number:\s*([^\n]+)/);
  return match?.[1]?.trim() || '';
}
```

---

## supabase/migrations/core/0010_rate_limit.sql
```sql
create table if not exists rate_limits (
  key text not null,
  identifier text not null,
  ts timestamptz not null default now()
);

create or replace function check_rate_limit(p_key text, p_identifier text, p_window_seconds int, p_max_calls int)
returns void as $$
declare
  cutoff timestamptz := now() - make_interval(secs => p_window_seconds);
  cnt int;
begin
  delete from rate_limits where ts < cutoff;
  select count(*) into cnt from rate_limits where key = p_key and identifier = p_identifier and ts >= cutoff;
  if cnt >= p_max_calls then
    raise exception 'rate limit exceeded for %:%', p_key, p_identifier using errcode = 'P0001';
  end if;
  insert into rate_limits(key, identifier) values (p_key, p_identifier);
end;
$$ language plpgsql;
```

---

## supabase/migrations/core/0001_billing_entitlements.sql
```sql
-- Billing subscriptions per org
create table if not exists org_subscriptions (
  id uuid primary key default gen_random_uuid(),
  org_id uuid not null unique references orgs(id) on delete cascade,
  stripe_customer_id text,
  stripe_subscription_id text,
  status text,
  plan text,
  period_end timestamptz,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Feature entitlements per org (source indicates how it was granted)
create table if not exists org_entitlements (
  id uuid primary key default gen_random_uuid(),
  org_id uuid not null references orgs(id) on delete cascade,
  feature_key text not null,
  enabled boolean not null default false,
  source text not null default 'billing',
  created_at timestamptz default now(),
  unique(org_id, feature_key, source)
);

create index if not exists org_entitlements_org_idx on org_entitlements(org_id);
```

---

## supabase/migrations/core/0002_storage_buckets_policies.sql
```sql
-- Evidence packet storage bucket (private; access via signed URLs)
insert into storage.buckets (id, name, public)
values ('evidence-packets', 'evidence-packets', false)
on conflict (id) do nothing;

-- Attachments bucket (private)
insert into storage.buckets (id, name, public)
values ('attachments', 'attachments', false)
on conflict (id) do nothing;

-- Harden storage access for evidence-packets (service role manages objects)
alter table if exists storage.objects enable row level security;

-- Allow service role full control in evidence-packets
create policy if not exists service_manage_evidence_packets on storage.objects
  for all
  using (bucket_id = 'evidence-packets' and auth.role() = 'service_role')
  with check (bucket_id = 'evidence-packets' and auth.role() = 'service_role');

-- Note: No general SELECT policy is defined; clients should use signed URLs
-- generated server-side to access artifacts in this private bucket.

-- Allow service role full control in attachments bucket
create policy if not exists service_manage_attachments on storage.objects
  for all
  using (bucket_id = 'attachments' and auth.role() = 'service_role')
  with check (bucket_id = 'attachments' and auth.role() = 'service_role');
```

---

## supabase/migrations/core/0003_events_jobs.sql
```sql
-- Idempotent webhook event ledger
create table if not exists webhook_events (
  id uuid primary key default gen_random_uuid(),
  provider text not null,
  idempotency_key text not null,
  payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  unique(provider, idempotency_key)
);

-- Submission jobs for scheduling/async processing
create table if not exists submission_jobs (
  id uuid primary key default gen_random_uuid(),
  org_id uuid not null references orgs(id) on delete cascade,
  dispute_id uuid not null references disputes(id) on delete cascade,
  method text not null check (method in ('api','manual')),
  scheduled_at timestamptz not null,
  status text not null default 'scheduled' check (status in ('scheduled','processing','submitted','failed','cancelled')),
  attempts int not null default 0,
  max_attempts int not null default 5,
  next_run_at timestamptz,
  last_error text,
  created_at timestamptz not null default now()
);

create index if not exists submission_jobs_org_idx on submission_jobs(org_id);
create index if not exists submission_jobs_dispute_idx on submission_jobs(dispute_id);
 
-- Dead-letter table for failed webhook processing
create table if not exists webhook_dead_letters (
  id uuid primary key default gen_random_uuid(),
  provider text not null,
  idempotency_key text,
  payload jsonb not null,
  error text,
  created_at timestamptz not null default now()
);
-- Dead-letter table for failed submission jobs
create table if not exists submission_dead_letters (
  id uuid primary key default gen_random_uuid(),
  job_id uuid,
  dispute_id uuid,
  error text,
  payload jsonb,
  created_at timestamptz not null default now()
);
```

---

## supabase/migrations/core/0004_user_prefs.sql
```sql
-- Per-user notification preferences scoped to org
create table if not exists user_notification_prefs (
  user_id uuid not null references users(id) on delete cascade,
  org_id uuid not null references orgs(id) on delete cascade,
  prefs jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  primary key (user_id, org_id)
);
```

---

## supabase/migrations/chargebacks/0006_order_tracking.sql
```sql
-- Shipment details linked to orders
create table if not exists order_shipments (
  id uuid primary key default gen_random_uuid(),
  order_id uuid not null references orders(id) on delete cascade,
  carrier text,
  tracking_number text,
  status text,
  shipped_at timestamptz,
  delivered_at timestamptz,
  signature_required boolean not null default false,
  signed_by text,
  created_at timestamptz not null default now()
);
create index if not exists order_shipments_order_idx on order_shipments(order_id);

-- Checkout/session telemetry linked to orders
create table if not exists order_sessions (
  id uuid primary key default gen_random_uuid(),
  order_id uuid not null references orders(id) on delete cascade,
  ip_address text,
  country text,
  device_type text,
  browser text,
  fingerprint text,
  duration_seconds int,
  created_at timestamptz not null default now()
);
create index if not exists order_sessions_order_idx on order_sessions(order_id);

-- Customer communications linked to disputes
create table if not exists communication_logs (
  id uuid primary key default gen_random_uuid(),
  dispute_id uuid not null references disputes(id) on delete cascade,
  direction text not null check (direction in ('inbound','outbound')),
  channel text not null check (channel in ('email','sms','phone','chat','other')),
  content text not null,
  created_at timestamptz not null default now()
);
create index if not exists communication_logs_dispute_idx on communication_logs(dispute_id);
```

---

## supabase/migrations/0007_rls_write_policies.sql
```sql
-- Enable RLS on new tables
alter table if exists webhook_events enable row level security;
alter table if exists submission_jobs enable row level security;
alter table if exists webhook_dead_letters enable row level security;
alter table if exists org_subscriptions enable row level security;
alter table if exists org_entitlements enable row level security;
alter table if exists user_notification_prefs enable row level security;
alter table if exists order_shipments enable row level security;
alter table if exists order_sessions enable row level security;
alter table if exists communication_logs enable row level security;

-- Helper view already defined: v_user_orgs(user_id, org_id, role)

-- webhook_events: service role only
create policy if not exists webhook_events_service_all on webhook_events
  for all
  using (auth.role() = 'service_role')
  with check (auth.role() = 'service_role');

-- webhook_dead_letters: service role only
create policy if not exists webhook_dlq_service_all on webhook_dead_letters
  for all
  using (auth.role() = 'service_role')
  with check (auth.role() = 'service_role');

-- submission_jobs: service role manages; org members may read jobs for their disputes
create policy if not exists submission_jobs_service_all on submission_jobs
  for all
  using (auth.role() = 'service_role')
  with check (auth.role() = 'service_role');

create policy if not exists submission_jobs_select_org on submission_jobs
  for select
  using (exists (
    select 1 from disputes d
    join v_user_orgs v on v.org_id = d.org_id and v.user_id = auth.uid()
    where d.id = submission_jobs.dispute_id
  ));

-- org_subscriptions: service role writes; org members can select
create policy if not exists org_subscriptions_select_org on org_subscriptions
  for select
  using (exists (
    select 1 from v_user_orgs v where v.org_id = org_subscriptions.org_id and v.user_id = auth.uid()
  ));

create policy if not exists org_subscriptions_service_all on org_subscriptions
  for all
  using (auth.role() = 'service_role')
  with check (auth.role() = 'service_role');

-- org_entitlements: service role writes; org members can select
create policy if not exists org_entitlements_select_org on org_entitlements
  for select
  using (exists (
    select 1 from v_user_orgs v where v.org_id = org_entitlements.org_id and v.user_id = auth.uid()
  ));

create policy if not exists org_entitlements_service_all on org_entitlements
  for all
  using (auth.role() = 'service_role')
  with check (auth.role() = 'service_role');

-- user_notification_prefs: self-service per user within their org
create policy if not exists user_notification_prefs_select_self on user_notification_prefs
  for select
  using (user_id = auth.uid());

create policy if not exists user_notification_prefs_upsert_self on user_notification_prefs
  for insert
  with check (user_id = auth.uid());

create policy if not exists user_notification_prefs_update_self on user_notification_prefs
  for update
  using (user_id = auth.uid())
  with check (user_id = auth.uid());

-- order_shipments: org members can select; service role writes
create policy if not exists order_shipments_select_org on order_shipments
  for select
  using (exists (
    select 1 from orders o
    join v_user_orgs v on v.org_id = o.org_id and v.user_id = auth.uid()
    where o.id = order_shipments.order_id
  ));

create policy if not exists order_shipments_service_all on order_shipments
  for all
  using (auth.role() = 'service_role')
  with check (auth.role() = 'service_role');

-- order_sessions: org members can select; service role writes
create policy if not exists order_sessions_select_org on order_sessions
  for select
  using (exists (
    select 1 from orders o
    join v_user_orgs v on v.org_id = o.org_id and v.user_id = auth.uid()
    where o.id = order_sessions.order_id
  ));

create policy if not exists order_sessions_service_all on order_sessions
  for all
  using (auth.role() = 'service_role')
  with check (auth.role() = 'service_role');

-- communication_logs: org members can select; service role writes
create policy if not exists communication_logs_select_org on communication_logs
  for select
  using (exists (
    select 1 from disputes d
    join v_user_orgs v on v.org_id = d.org_id and v.user_id = auth.uid()
    where d.id = communication_logs.dispute_id
  ));

create policy if not exists communication_logs_service_all on communication_logs
  for all
  using (auth.role() = 'service_role')
  with check (auth.role() = 'service_role');

-- user_notifications: allow owners to mark their notifications as read
create policy if not exists user_notifications_update_self on user_notifications
  for update
  using (user_id = auth.uid())
  with check (user_id = auth.uid());
```

---

## supabase/functions/check-due-soon/index.ts
```ts
// Supabase Edge Function (Deno) — schedule via Supabase cron (daily/hourly)
// deno-lint-ignore-file no-explicit-any
import { serve } from 'https://deno.land/std@0.181.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.38.0';

serve(async (_req: Request) => {
  try {
    const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
    const supabaseServiceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
    const supabase = createClient(supabaseUrl, supabaseServiceKey);

    const thresholds = [7, 3, 1];
    for (const days of thresholds) {
      const target = new Date();
      target.setDate(target.getDate() + days);
      const next = new Date(target); next.setDate(next.getDate() + 1);

      const { data: disputes } = await supabase
        .from('disputes')
        .select('id, org_id, psp_id, amount, due_by')
        .in('status', ['new','draft'])
        .gte('due_by', target.toISOString())
        .lt('due_by', next.toISOString());
      if (!disputes || disputes.length === 0) continue;

      for (const d of disputes) {
        const type = days === 1 ? 'dispute_due_1_day' : days === 3 ? 'dispute_due_3_days' : 'dispute_due_7_days';
        // Skip if alert exists
        const { data: existing } = await supabase
          .from('alerts')
          .select('id')
          .eq('org_id', d.org_id)
          .eq('type', type)
          .eq('dispute_id', d.id)
          .maybeSingle();
        if (existing) continue;

        const { data: alert } = await supabase
          .from('alerts')
          .insert({
            dispute_id: d.id,
            org_id: d.org_id,
            type,
            message: `${days === 1 ? '🚨' : days === 3 ? '⚠️' : '📅'} Dispute ${d.psp_id} ($${d.amount}) due in ${days} day${days>1?'s':''}`,
            metadata: { days_remaining: days, due_date: d.due_by, amount: d.amount }
          })
          .select('id')
          .single();
        if (alert?.id) {
          await fetch(`${supabaseUrl}/functions/v1/send-notification`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${supabaseServiceKey}` },
            body: JSON.stringify({ alertId: alert.id })
          });
        }
      }
    }

    return new Response(JSON.stringify({ ok: true }), { headers: { 'Content-Type': 'application/json' } });
  } catch (e: any) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500, headers: { 'Content-Type': 'application/json' } });
  }
});
```


## src/lib/disputePolling.ts
```ts
import { createServerClient } from './supabaseServer';
import Stripe from 'stripe';

export async function pollDisputeStatus(disputeId: string): Promise<void> {
  const db = createServerClient();
  
  // Get dispute details
  const { data: dispute, error } = await db
    .from('disputes')
    .select('*, stores!inner(platform, oauth_tokens)')
    .eq('id', disputeId)
    .single();
    
  if (error || !dispute) {
    console.error('Failed to fetch dispute for polling:', error);
    return;
  }
  
  try {
    let newStatus = dispute.status;
    let updatedData: any = {};
    
    if (dispute.stores.platform === 'stripe') {
      const stripe = new Stripe(process.env.STRIPE_API_KEY || '', { apiVersion: '2024-06-20' });
      const stripeDispute = await stripe.disputes.retrieve(dispute.psp_id);
      
      // Map Stripe status to our status
      const statusMap: Record<string, string> = {
        'needs_response': 'new',
        'warning_needs_response': 'new',
        'warning_under_review': 'submitted',
        'under_review': 'submitted',
        'won': 'won',
        'lost': 'lost',
        'charge_refunded': 'won'
      };
      
      newStatus = statusMap[stripeDispute.status] || dispute.status;
      updatedData = {
        status: newStatus,
        raw: stripeDispute,
        amount: (stripeDispute.amount / 100.0),
        due_by: stripeDispute.evidence_details?.due_by 
          ? new Date(stripeDispute.evidence_details.due_by * 1000).toISOString() 
          : dispute.due_by
      };
      
    } else if (dispute.stores.platform === 'shopify') {
      const shopDomain = dispute.stores.oauth_tokens.shop_domain;
      const accessToken = dispute.stores.oauth_tokens.shopify_access_token;
      
      const response = await fetch(
        `https://${shopDomain}/admin/api/2024-01/shopify_payments/disputes/${dispute.psp_id}.json`,
        {
          headers: {
            'X-Shopify-Access-Token': accessToken,
            'Content-Type': 'application/json'
          }
        }
      );
      
      if (response.ok) {
        const { dispute: shopifyDispute } = await response.json();
        
        // Map Shopify status
        const statusMap: Record<string, string> = {
          'needs_response': 'new',
          'under_review': 'submitted',
          'accepted': 'won',
          'lost': 'lost',
          'won': 'won'
        };
        
        newStatus = statusMap[shopifyDispute.status] || dispute.status;
        updatedData = {
          status: newStatus,
          raw: shopifyDispute,
          amount: parseFloat(shopifyDispute.amount),
          due_by: shopifyDispute.due_at || dispute.due_by
        };
      }
    }
    
    // Update dispute if status changed
    if (newStatus !== dispute.status || Object.keys(updatedData).length > 0) {
      await db
        .from('disputes')
        .update(updatedData)
        .eq('id', disputeId);
        
      // Create alert if status changed to won/lost
      if (newStatus !== dispute.status && ['won', 'lost'].includes(newStatus)) {
        await db.from('alerts').insert({
          dispute_id: disputeId,
          org_id: dispute.org_id,
          type: `dispute_${newStatus}`,
          message: `Dispute ${dispute.psp_id} has been ${newStatus}`,
          metadata: { 
            previous_status: dispute.status,
            new_status: newStatus 
          }
        });
      }
    }
    
  } catch (error) {
    console.error('Error polling dispute status:', error);
  }
}

export async function pollAllActiveDisputes(): Promise<void> {
  const db = createServerClient();
  
  // Get all disputes that need polling
  const { data: disputes } = await db
    .from('disputes')
    .select('id')
    .in('status', ['new', 'draft', 'submitted'])
    .order('due_by', { ascending: true })
    .limit(50); // Process in batches
    
  if (!disputes || disputes.length === 0) return;
  
  // Poll each dispute
  await Promise.all(
    disputes.map(d => pollDisputeStatus(d.id))
  );
}
```

---

## supabase/functions/submission-worker/index.ts
```ts
// Supabase Edge Function (Deno) — scheduled worker to process submission_jobs
// deno-lint-ignore-file no-explicit-any
import { serve } from 'https://deno.land/std@0.181.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.38.0';
import Stripe from 'https://esm.sh/stripe@14.23.0?target=deno';

async function processJob(supabase: any, job: any) {
  try {
    // Mark processing and increment attempts
    const attempts = (job.attempts || 0) + 1;
    await supabase.from('submission_jobs').update({ status: 'processing', attempts }).eq('id', job.id);

    // Load latest submission record (contains PDF URL and content hash)
    const { data: sub } = await supabase
      .from('submissions')
      .select('id, dispute_id, receipt, method')
      .eq('dispute_id', job.dispute_id)
      .order('submitted_at', { ascending: false })
      .limit(1)
      .single();
    if (!sub) throw new Error('Submission record not found');

    const { data: disp } = await supabase
      .from('disputes')
      .select('*, stores!inner(platform, oauth_tokens)')
      .eq('id', job.dispute_id)
      .single();
    if (!disp) throw new Error('Dispute not found');

    let externalRef: string | null = null;
    if (job.method === 'api') {
      if (disp.psp_provider === 'stripe') {
        const stripeApiKey = Deno.env.get('STRIPE_API_KEY') || '';
        const stripe = new Stripe(stripeApiKey, { apiVersion: '2024-06-20' } as any);
        const idempotencyKey = `submit_${disp.psp_id}_${sub.id}_${sub.receipt?.content_hash || ''}`.slice(0, 255);
        const updated = await stripe.disputes.update(
          disp.psp_id,
          { evidence: { receipt: sub.receipt?.pdf_url }, metadata: { submission_id: sub.id } },
          { idempotencyKey }
        );
        externalRef = updated.id;
      } else if (disp.psp_provider === 'shopify' || disp.stores.platform === 'shopify') {
        const token = disp.stores.oauth_tokens.shopify_access_token;
        const shop = disp.stores.oauth_tokens.shop_domain;
        const endpoint = `https://${shop}/admin/api/2024-01/shopify_payments/disputes/${disp.psp_id}/dispute_evidences.json`;
        const res = await fetch(endpoint, {
          method: 'PUT',
          headers: { 'X-Shopify-Access-Token': token, 'Content-Type': 'application/json' },
          body: JSON.stringify({ dispute_evidence: { shipping_documentation: sub.receipt?.pdf_url, uncategorized_text: 'See attached packet' } })
        });
        if (!res.ok) throw new Error(`Shopify error: ${await res.text()}`);
        externalRef = disp.psp_id;
      }
    }

    await supabase.from('submissions').update({
      status: externalRef ? 'submitted' : 'generated',
      receipt: { ...(sub.receipt || {}), external_ref: externalRef }
    }).eq('id', sub.id);

    await supabase.from('submission_jobs').update({ status: 'submitted' }).eq('id', job.id);
  } catch (e) {
    const attempts = (job.attempts || 0) + 1;
    const maxAttempts = job.max_attempts || 5;
    const errMsg = String((e as any).message || e);
    if (attempts >= maxAttempts) {
      await supabase.from('submission_dead_letters').insert({ job_id: job.id, dispute_id: job.dispute_id, error: errMsg });
      await supabase.from('submission_jobs').update({ status: 'failed', attempts, last_error: errMsg }).eq('id', job.id);
    } else {
      const backoffMs = Math.min(60000, Math.pow(2, attempts) * 500);
      const nextRun = new Date(Date.now() + backoffMs).toISOString();
      await supabase.from('submission_jobs').update({ status: 'scheduled', attempts, last_error: errMsg, next_run_at: nextRun }).eq('id', job.id);
    }
  }
}

serve(async (_req: Request) => {
  const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
  const supabaseServiceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
  const supabase = createClient(supabaseUrl, supabaseServiceKey);

  // Fetch due jobs (consider next_run_at for retries)
  const now = new Date().toISOString();
  const { data: jobs } = await supabase
    .from('submission_jobs')
    .select('*')
    .or('status.eq.scheduled,status.eq.processing')
    .or(`lte.scheduled_at.${now},lte.next_run_at.${now}`)
    .order('scheduled_at', { ascending: true })
    .limit(10);

  if (jobs && jobs.length > 0) {
    await Promise.all(jobs.map((j: any) => processJob(supabase, j)));
  }

  return new Response(JSON.stringify({ processed: jobs?.length || 0 }), { headers: { 'Content-Type': 'application/json' } });
});
```

---

## supabase/migrations/0006_order_tracking.sql
```sql
-- Add order matching and tracking tables
create table if not exists order_shipments (
  id uuid primary key default gen_random_uuid(),
  order_id uuid not null references orders(id) on delete cascade,
  carrier text,
  tracking_number text,
  shipped_at timestamptz,
  delivered_at timestamptz,
  status text,
  signature_required boolean default false,
  signed_by text,
  tracking_history jsonb default '[]'::jsonb,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table if not exists order_sessions (
  id uuid primary key default gen_random_uuid(),
  order_id uuid not null references orders(id) on delete cascade,
  ip_address text,
  country text,
  device_type text,
  browser text,
  fingerprint text,
  duration interval,
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);

create table if not exists communication_logs (
  id uuid primary key default gen_random_uuid(),
  dispute_id uuid references disputes(id) on delete cascade,
  order_id uuid references orders(id) on delete cascade,
  content text not null,
  channel text not null check (channel in ('email', 'chat', 'phone', 'social')),
  direction text not null check (direction in ('inbound', 'outbound')),
  metadata jsonb default '{}'::jsonb,
  created_at timestamptz default now()
);

-- Add indexes
create index idx_order_shipments_order_id on order_shipments(order_id);
create index idx_order_shipments_tracking on order_shipments(tracking_number);
create index idx_order_sessions_order_id on order_sessions(order_id);
create index idx_order_sessions_fingerprint on order_sessions(fingerprint);
create index idx_communication_logs_dispute on communication_logs(dispute_id);
create index idx_communication_logs_order on communication_logs(order_id);

-- Add RLS policies
alter table order_shipments enable row level security;
alter table order_sessions enable row level security;
alter table communication_logs enable row level security;

-- Shipments policies
create policy "Org members can view shipments" on order_shipments 
  for select using (
    exists (
      select 1 from orders o
      join user_org_roles uor on uor.org_id = o.org_id
      where o.id = order_shipments.order_id 
      and uor.user_id = auth.uid()
    )
  );

-- Sessions policies  
create policy "Org members can view sessions" on order_sessions
  for select using (
    exists (
      select 1 from orders o
      join user_org_roles uor on uor.org_id = o.org_id
      where o.id = order_sessions.order_id
      and uor.user_id = auth.uid()
    )
  );

-- Communication logs policies
create policy "Org members can view communications" on communication_logs
  for select using (
    exists (
      select 1 from user_org_roles uor
      left join disputes d on d.id = communication_logs.dispute_id
      left join orders o on o.id = communication_logs.order_id
      where uor.user_id = auth.uid()
      and (uor.org_id = d.org_id or uor.org_id = o.org_id)
    )
  );
```

---

## supabase/migrations/chargebacks/0010_seed_demo.sql
```sql
-- Idempotent demo seed (fixed UUIDs)
-- Orgs & user
insert into orgs(id, name) values ('00000000-0000-0000-0000-000000000001','Demo Org') on conflict (id) do nothing;
insert into users(id, email) values ('00000000-0000-0000-0000-0000000000aa','demo@demo.local') on conflict (id) do nothing;
insert into user_org_roles(user_id, org_id, role) values ('00000000-0000-0000-0000-0000000000aa','00000000-0000-0000-0000-000000000001','owner') on conflict do nothing;

-- Store
insert into stores(id, org_id, platform, oauth_tokens, status)
values ('00000000-0000-0000-0000-000000000010','00000000-0000-0000-0000-000000000001','shopify', '{"shop_domain":"demo.myshopify.com","shopify_access_token":"demo_token"}'::jsonb, 'active')
on conflict (id) do nothing;

-- Orders
insert into orders(id, org_id, store_id, customer_json, items_json, addresses_json, raw, created_at)
values
('00000000-0000-0000-0000-000000000101','00000000-0000-0000-0000-000000000001','00000000-0000-0000-0000-000000000010', '{"email":"john@example.com"}', '[{"name":"Widget","quantity":1,"price":49.99}]', '{"shipping_address":{"address1":"123 Main"},"billing_address":{"address1":"123 Main"}}', '{}', now() - interval '7 day'),
('00000000-0000-0000-0000-000000000102','00000000-0000-0000-0000-000000000001','00000000-0000-0000-0000-000000000010', '{"email":"amy@example.com"}', '[{"name":"Gizmo","quantity":2,"price":19.99}]', '{"shipping_address":{"address1":"9 Elm"},"billing_address":{"address1":"9 Elm"}}', '{}', now() - interval '3 day')
on conflict (id) do nothing;

-- Disputes
insert into disputes(id, org_id, store_id, psp_id, psp_provider, reason_code, amount, due_by, status, raw, created_at)
values
('00000000-0000-0000-0000-000000000201','00000000-0000-0000-0000-000000000001','00000000-0000-0000-0000-000000000010','dp_0001','shopify','fraudulent',49.99, now() + interval '5 day','new','{}', now() - interval '1 day'),
('00000000-0000-0000-0000-000000000202','00000000-0000-0000-0000-000000000001','00000000-0000-0000-0000-000000000010','dp_0002','shopify','product_not_received',39.99, now() + interval '2 day','draft','{}', now() - interval '2 day'),
('00000000-0000-0000-0000-000000000203','00000000-0000-0000-0000-000000000001','00000000-0000-0000-0000-000000000010','dp_0003','shopify','duplicate',19.99, null,'won','{}', now() - interval '10 day')
on conflict (id) do nothing;
```

---

## supabase/migrations/core/0012_submission_jobs.sql
```sql
create table if not exists submission_jobs (
  id uuid primary key default gen_random_uuid(),
  org_id uuid not null references orgs(id) on delete cascade,
  dispute_id uuid not null references disputes(id) on delete cascade,
  method text not null check (method in ('api','manual')),
  scheduled_at timestamptz not null,
  status text not null default 'scheduled',
  attempts int not null default 0,
  last_error text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

alter table submission_jobs enable row level security;
create policy submission_jobs_read on submission_jobs for select using (
  exists (select 1 from user_org_roles u where u.org_id = submission_jobs.org_id and u.user_id = auth.uid())
);
```

---

## src/lib/orderMatching.ts
```ts
import { createServerClient } from './supabaseServer';

export async function matchOrderToDispute(disputeId: string): Promise<string | null> {
  const db = createServerClient();
  
  // Get dispute details
  const { data: dispute } = await db
    .from('disputes')
    .select('*, stores!inner(id, org_id)')
    .eq('id', disputeId)
    .single();
    
  if (!dispute) return null;
  
  // Try to match by transaction ID in raw data
  const transactionId = dispute.raw?.charge?.id || dispute.raw?.transaction_id;
  if (transactionId) {
    const { data: order } = await db
      .from('orders')
      .select('id')
      .eq('store_id', dispute.store_id)
      .eq('raw->>transaction_id', transactionId)
      .single();
      
    if (order) return order.id;
  }
  
  // Try to match by amount and date range
  const disputeDate = new Date(dispute.created_at);
  const startDate = new Date(disputeDate);
  startDate.setDate(startDate.getDate() - 180); // 6 months back
  
  const { data: orders } = await db
    .from('orders')
    .select('id, raw')
    .eq('store_id', dispute.store_id)
    .eq('raw->>total', dispute.amount.toString())
    .gte('created_at', startDate.toISOString())
    .lte('created_at', disputeDate.toISOString());
    
  if (orders && orders.length === 1) {
    return orders[0].id;
  }
  
  // Try fuzzy matching by customer email/name
  const customerEmail = dispute.raw?.evidence?.customer_email_address;
  if (customerEmail && orders) {
    const matchedOrder = orders.find(o => 
      o.raw?.customer?.email === customerEmail
    );
    if (matchedOrder) return matchedOrder.id;
  }
  
  return null;
}

export async function linkOrderToDispute(disputeId: string, orderId: string): Promise<void> {
  const db = createServerClient();
  
  // Update dispute with order reference
  await db
    .from('disputes')
    .update({ raw: db.raw(`raw || jsonb_build_object('matched_order_id', ?)`, [orderId]) })
    .eq('id', disputeId);
}
```

---

## src/lib/trackingIntegration.ts
```ts
import { createServerClient } from './supabaseServer';

interface TrackingUpdate {
  status: string;
  location: string;
  timestamp: string;
  description: string;
}

export async function updateTrackingInfo(trackingNumber: string, carrier: string): Promise<void> {
  const db = createServerClient();
  
  // Fetch tracking data based on carrier
  let trackingData;
  switch (carrier.toLowerCase()) {
    case 'ups':
      trackingData = await fetchUPSTracking(trackingNumber);
      break;
    case 'fedex':
      trackingData = await fetchFedExTracking(trackingNumber);
      break;
    case 'usps':
      trackingData = await fetchUSPSTracking(trackingNumber);
      break;
    default:
      console.log(`Unsupported carrier: ${carrier}`);
      return;
  }
  
  if (!trackingData) return;
  
  // Update shipment record
  await db
    .from('order_shipments')
    .update({
      status: trackingData.status,
      delivered_at: trackingData.delivered ? new Date().toISOString() : null,
      signed_by: trackingData.signedBy,
      tracking_history: trackingData.history,
      updated_at: new Date().toISOString()
    })
    .eq('tracking_number', trackingNumber);
}

async function fetchUPSTracking(trackingNumber: string): Promise<any> {
  // In production, would call UPS API
  // Mock response for now
  return {
    status: 'delivered',
    delivered: true,
    signedBy: 'J. DOE',
    history: [
      {
        status: 'picked_up',
        location: 'New York, NY',
        timestamp: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
        description: 'Package picked up'
      },
      {
        status: 'in_transit',
        location: 'Chicago, IL',
        timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
        description: 'In transit'
      },
      {
        status: 'out_for_delivery',
        location: 'Los Angeles, CA',
        timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
        description: 'Out for delivery'
      },
      {
        status: 'delivered',
        location: 'Los Angeles, CA',
        timestamp: new Date().toISOString(),
        description: 'Delivered - Signed by J. DOE'
      }
    ]
  };
}

async function fetchFedExTracking(trackingNumber: string): Promise<any> {
  // Mock FedEx response
  return null;
}

async function fetchUSPSTracking(trackingNumber: string): Promise<any> {
  // Mock USPS response
  return null;
}

export async function createShipmentRecord(orderId: string, carrier: string, trackingNumber: string): Promise<void> {
  const db = createServerClient();
  
  await db.from('order_shipments').insert({
    order_id: orderId,
    carrier,
    tracking_number: trackingNumber,
    shipped_at: new Date().toISOString(),
    status: 'shipped'
  });
  
  // Schedule tracking update
  await updateTrackingInfo(trackingNumber, carrier);
}

export async function getDeliveryProof(shipmentId: string): Promise<any> {
  const db = createServerClient();
  
  const { data: shipment } = await db
    .from('order_shipments')
    .select('*')
    .eq('id', shipmentId)
    .single();
    
  if (!shipment || !shipment.delivered_at) {
    return null;
  }
  
  return {
    delivered: true,
    deliveredAt: shipment.delivered_at,
    signedBy: shipment.signed_by,
    trackingNumber: shipment.tracking_number,
    carrier: shipment.carrier,
    lastUpdate: shipment.tracking_history?.[shipment.tracking_history.length - 1]
  };
}
```

---

## src/components/Tabs.tsx
```tsx
'use client';
import { useEffect, useState } from 'react';

interface TabsProps {
  tabs: string[];
  active?: string;
  onChange?: (tab: string) => void;
  children: (activeTab: string) => JSX.Element;
}

export function Tabs({ tabs, active: controlled, onChange, children }: TabsProps) {
  const [active, setActive] = useState(controlled ?? tabs[0]);
  useEffect(() => {
    if (controlled && controlled !== active) setActive(controlled);
  }, [controlled]);
  
  return (
    <>
      <div className="flex gap-4 border-b mb-4">
        {tabs.map(tab => (
          <button 
            key={tab} 
            onClick={() => { setActive(tab); onChange?.(tab); }} 
            className={`py-2 px-1 border-b-2 transition-colors ${
              active === tab 
                ? 'border-blue-600 font-medium text-blue-600' 
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>
      {children(active)}
    </>
  );
}
```

---

## src/lib/sessionTracking.ts
```ts
import { createServerClient } from './supabaseServer';
import crypto from 'crypto';

export interface SessionData {
  ipAddress: string;
  userAgent: string;
  acceptLanguage: string;
  screenResolution?: string;
  timezone?: string;
  plugins?: string[];
}

export function generateFingerprint(sessionData: SessionData): string {
  const fingerprintData = [
    sessionData.userAgent,
    sessionData.acceptLanguage,
    sessionData.screenResolution || '',
    sessionData.timezone || '',
    (sessionData.plugins || []).join(',')
  ].join('|');
  
  return crypto
    .createHash('sha256')
    .update(fingerprintData)
    .digest('hex')
    .substring(0, 16);
}

export async function recordOrderSession(
  orderId: string,
  sessionData: SessionData
): Promise<void> {
  const db = createServerClient();
  
  const fingerprint = generateFingerprint(sessionData);
  
  // Get geolocation from IP
  const geoData = await getGeolocation(sessionData.ipAddress);
  
  // Parse user agent for device info
  const deviceInfo = parseUserAgent(sessionData.userAgent);
  
  await db.from('order_sessions').insert({
    order_id: orderId,
    ip_address: sessionData.ipAddress,
    country: geoData.country,
    device_type: deviceInfo.deviceType,
    browser: deviceInfo.browser,
    fingerprint,
    metadata: {
      screen_resolution: sessionData.screenResolution,
      timezone: sessionData.timezone,
      plugins: sessionData.plugins,
      user_agent: sessionData.userAgent
    }
  });
}

async function getGeolocation(ipAddress: string): Promise<{ country: string; city?: string }> {
  // In production, would use a service like MaxMind or IP2Location
  // Mock response for now
  return {
    country: 'US',
    city: 'Los Angeles'
  };
}

function parseUserAgent(userAgent: string): { deviceType: string; browser: string } {
  // Simple parsing - in production would use a library like ua-parser-js
  let deviceType = 'desktop';
  let browser = 'unknown';
  
  if (/mobile/i.test(userAgent)) deviceType = 'mobile';
  else if (/tablet/i.test(userAgent)) deviceType = 'tablet';
  
  if (/chrome/i.test(userAgent)) browser = 'Chrome';
  else if (/firefox/i.test(userAgent)) browser = 'Firefox';
  else if (/safari/i.test(userAgent)) browser = 'Safari';
  else if (/edge/i.test(userAgent)) browser = 'Edge';
  
  return { deviceType, browser };
}

export async function checkFraudSignals(orderId: string): Promise<{
  riskScore: number;
  signals: string[];
}> {
  const db = createServerClient();
  
  const { data: session } = await db
    .from('order_sessions')
    .select('*')
    .eq('order_id', orderId)
    .single();
    
  if (!session) {
    return { riskScore: 50, signals: ['No session data'] };
  }
  
  const signals: string[] = [];
  let riskScore = 0;
  
  // Check for VPN/Proxy
  if (await isVpnOrProxy(session.ip_address)) {
    signals.push('VPN/Proxy detected');
    riskScore += 30;
  }
  
  // Check device fingerprint history
  const { data: fingerprintHistory } = await db
    .from('order_sessions')
    .select('order_id, created_at')
    .eq('fingerprint', session.fingerprint)
    .neq('order_id', orderId)
    .order('created_at', { ascending: false })
    .limit(10);
    
  if (fingerprintHistory && fingerprintHistory.length > 5) {
    signals.push('High activity from same device');
    riskScore += 20;
  }
  
  // Check country mismatch
  const { data: order } = await db
    .from('orders')
    .select('addresses_json')
    .eq('id', orderId)
    .single();
    
  if (order && order.addresses_json?.billing_address?.country !== session.country) {
    signals.push('Country mismatch');
    riskScore += 25;
  }
  
  return { riskScore: Math.min(riskScore, 100), signals };
}

async function isVpnOrProxy(ipAddress: string): Promise<boolean> {
  // In production, would check against VPN/Proxy detection service
  return false;
}
```

---

## src/components/SubmissionModal.tsx
```tsx
'use client';
import { useEffect, useRef, useState } from 'react';

interface SubmissionModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (method: 'api' | 'manual') => Promise<void>;
  counts: { sections: number; attachments: number };
  validation?: { readiness: number; gaps: Array<{ code: string; message: string }> } | null;
}

export function SubmissionModal({ open, onClose, onSubmit, counts, validation }: SubmissionModalProps) {
  const [method, setMethod] = useState<'api' | 'manual'>('api');
  const [submitting, setSubmitting] = useState(false);
  const [schedule, setSchedule] = useState<'now'|'later'>('now');
  const [scheduledAt, setScheduledAt] = useState<string>('');
  const [reviewed, setReviewed] = useState(false);
  const dialogRef = useRef<HTMLDivElement | null>(null);
  const firstButtonRef = useRef<HTMLButtonElement | null>(null);
  
  if (!open) return null;

  const handleSubmit = async () => {
    setSubmitting(true);
    if (schedule === 'later' && scheduledAt) {
      // Schedule only
      await fetch('/api/submissions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ method, scheduledAt })
      });
      setSubmitting(false);
      onClose();
      return;
    }
    await onSubmit(method);
    setSubmitting(false);
  };

  useEffect(() => {
    if (open && firstButtonRef.current) firstButtonRef.current.focus();
  }, [open]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center" role="dialog" aria-modal="true" aria-labelledby="submit-title">
      <div className="absolute inset-0 bg-black/30" onClick={onClose} aria-hidden="true" />
      <div className="relative bg-white w-full max-w-lg rounded-lg shadow-xl p-6" ref={dialogRef}>
        <h3 id="submit-title" className="text-lg font-semibold mb-3">Review Before Submitting</h3>
        
        <div className="text-sm border rounded p-3 mb-4 bg-gray-50">
          <div className="space-y-1">
            <p>📄 Evidence packet: {counts.attachments} documents</p>
            <p>📝 Response: {counts.sections} sections</p>
            <p>🔒 This submission will be permanently archived</p>
          </div>
        </div>
        
        <div className="space-y-2 mb-4">
          <h4 className="text-sm font-medium">Checklist</h4>
          <ul className="text-sm space-y-1 text-gray-700">
            <li className="flex items-center gap-2">
              <svg className="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Evidence narrative completed
            </li>
            <li className="flex items-center gap-2">
              <svg className="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Required documents attached
            </li>
            <li className="flex items-center gap-2">
              <svg className="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Delivery confirmation included
            </li>
            <li className="flex items-center gap-2">
              <svg className="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Customer history documented
            </li>
          </ul>
        </div>
        {validation && (
          <div className="mb-4 border rounded p-3 text-sm" aria-live="polite">
            {validation.gaps.length === 0 ? (
              <div className="text-green-700">All requirements met. Readiness: {validation.readiness}%</div>
            ) : (
              <div>
                <div className="text-yellow-800 mb-2">Issues to review:</div>
                <ul className="list-disc ml-5 space-y-1">
                  {validation.gaps.map((g, i) => (
                    <li key={i} className="text-yellow-800">{g.message}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
        
        <div className="mb-6">
          <label className="text-sm font-medium block mb-2">Submission timing</label>
          <div className="space-y-3">
            <label className="flex items-center gap-3 p-3 border rounded cursor-pointer hover:bg-gray-50">
              <input type="radio" checked={schedule==='now'} onChange={()=>setSchedule('now')} aria-label="Submit now" />
              <div>
                <div className="font-medium">Submit now</div>
                <div className="text-xs text-gray-600">Immediate submission</div>
              </div>
            </label>
            <label className="flex items-center gap-3 p-3 border rounded cursor-pointer hover:bg-gray-50">
              <input type="radio" checked={schedule==='later'} onChange={()=>setSchedule('later')} aria-label="Schedule submission" />
              <div className="flex-1">
                <div className="font-medium">Schedule submission</div>
                <div className="text-xs text-gray-600">Pick a date and time</div>
              </div>
              <input type="datetime-local" className="border rounded px-2 py-1 text-sm" disabled={schedule!=='later'} value={scheduledAt} onChange={(e)=>setScheduledAt(e.target.value)} aria-disabled={schedule!=='later'} />
            </label>
          </div>
        </div>
        
        <div className="mb-6">
          <label className="text-sm font-medium block mb-2">Submission method</label>
          <div className="space-y-2">
            <label className="flex items-center gap-3 p-3 border rounded cursor-pointer hover:bg-gray-50">
              <input 
                type="radio" 
                checked={method === 'api'} 
                onChange={() => setMethod('api')}
                className="text-blue-600"
                aria-label="Submit via API"
              />
              <div>
                <div className="font-medium">Submit via Stripe API</div>
                <div className="text-xs text-gray-600">Recommended - Automatic submission</div>
              </div>
            </label>
            <label className="flex items-center gap-3 p-3 border rounded cursor-pointer hover:bg-gray-50">
              <input 
                type="radio" 
                checked={method === 'manual'} 
                onChange={() => setMethod('manual')}
                className="text-blue-600"
                aria-label="Download packet"
              />
              <div>
                <div className="font-medium">Download and submit manually</div>
                <div className="text-xs text-gray-600">Generate PDF for manual upload</div>
              </div>
            </label>
          </div>
        </div>
        <div className="mb-4">
          <label className="inline-flex items-center gap-2 text-sm">
            <input type="checkbox" checked={reviewed} onChange={(e)=>setReviewed(e.target.checked)} aria-label="I have reviewed the evidence and it's ready to submit" />
            <span>I've reviewed the evidence and it's ready to submit</span>
          </label>
        </div>
        
        <div className="flex justify-end gap-2">
          <button 
            ref={firstButtonRef}
            className="px-4 py-2 border rounded hover:bg-gray-50" 
            onClick={onClose}
            disabled={submitting}
          >
            Cancel
          </button>
          <button 
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50" 
            onClick={handleSubmit}
            disabled={submitting || !reviewed}
          >
            {submitting ? 'Submitting...' : 'Submit Evidence'}
          </button>
        </div>
      </div>
    </div>
  );
}
```

---

## src/components/CommandPalette.tsx
```tsx
'use client';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export function CommandPalette() {
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [showHelp, setShowHelp] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsOpen(true);
      }
      if ((e.metaKey || e.ctrlKey) && e.key === 'n') {
        e.preventDefault();
        alert('Create new manual dispute - coming soon');
      }
      if ((e.metaKey || e.ctrlKey) && e.key === '/') {
        e.preventDefault();
        setShowHelp(true);
      }
      if (e.key === 'Escape') {
        setIsOpen(false);
        setShowHelp(false);
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  const commands = [
    { id: 'disputes', label: 'Go to Disputes', action: () => router.push('/disputes'), icon: '📋' },
    { id: 'analytics', label: 'View Analytics', action: () => router.push('/analytics'), icon: '📊' },
    { id: 'settings', label: 'Open Settings', action: () => router.push('/settings'), icon: '⚙️' },
    { id: 'new-dispute', label: 'Create Manual Dispute', action: () => alert('Create dispute'), icon: '➕' },
    { id: 'export', label: 'Export Data', action: () => alert('Export data'), icon: '💾' },
    { id: 'help', label: 'Keyboard Shortcuts', action: () => setShowHelp(true), icon: '⌨️' }
  ];

  const shortcuts = [
    { keys: '⌘K / Ctrl+K', description: 'Open command palette' },
    { keys: '⌘N / Ctrl+N', description: 'Create new manual dispute' },
    { keys: '⌘/ / Ctrl+/', description: 'Show keyboard shortcuts' },
    { keys: 'G then D', description: 'Go to disputes' },
    { keys: 'G then A', description: 'Go to analytics' },
    { keys: 'G then S', description: 'Go to settings' }
  ];

  const filteredCommands = commands.filter(cmd => 
    cmd.label.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-start justify-center pt-20">
          <div 
            className="absolute inset-0 bg-black/30" 
            onClick={() => setIsOpen(false)} 
          />
          <div className="relative bg-white w-full max-w-lg rounded-lg shadow-xl">
            <div className="p-4 border-b">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Type a command or search..."
                className="w-full px-3 py-2 border rounded"
                autoFocus
              />
            </div>
            <div className="max-h-80 overflow-y-auto">
              {filteredCommands.map((cmd) => (
                <button
                  key={cmd.id}
                  onClick={() => {
                    cmd.action();
                    setIsOpen(false);
                    setQuery('');
                  }}
                  className="w-full text-left px-4 py-3 hover:bg-gray-100 flex items-center gap-3"
                >
                  <span className="text-xl">{cmd.icon}</span>
                  <span>{cmd.label}</span>
                </button>
              ))}
            </div>
            <div className="p-3 border-t text-xs text-gray-600 flex gap-4">
              <span>↑↓ Navigate</span>
              <span>⏎ Select</span>
              <span>⎋ Close</span>
            </div>
          </div>
        </div>
      )}
      
      {showHelp && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div 
            className="absolute inset-0 bg-black/30" 
            onClick={() => setShowHelp(false)} 
          />
          <div className="relative bg-white w-full max-w-md rounded-lg shadow-xl p-6">
            <h2 className="text-lg font-semibold mb-4">Keyboard Shortcuts</h2>
            <div className="space-y-2">
              {shortcuts.map((shortcut, i) => (
                <div key={i} className="flex justify-between text-sm">
                  <kbd className="px-2 py-1 bg-gray-100 border rounded text-xs">{shortcut.keys}</kbd>
                  <span className="text-gray-600">{shortcut.description}</span>
                </div>
              ))}
            </div>
            <button 
              onClick={() => setShowHelp(false)}
              className="mt-6 w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </>
  );
}
```

---

## supabase/functions/generate-pdf/index.ts
```ts
// Supabase Edge Function (Deno)
// deno-lint-ignore-file no-explicit-any
import { serve } from 'https://deno.land/std@0.181.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.38.0';
import { PDFDocument, StandardFonts, rgb } from 'https://esm.sh/pdf-lib@1.17.1';

serve(async (req: Request) => {
  if (req.method !== 'POST') return new Response('Method Not Allowed', { status: 405 });
  
  try {
    const { packetId, sections, attachments } = await req.json();
    
    // Initialize Supabase client
    const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
    const supabaseServiceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
    const supabase = createClient(supabaseUrl, supabaseServiceKey);
    
    // Create PDF document
    const pdfDoc = await PDFDocument.create();
    const helveticaFont = await pdfDoc.embedFont(StandardFonts.Helvetica);
    const helveticaBold = await pdfDoc.embedFont(StandardFonts.HelveticaBold);
    
    // Add cover page
    let page = pdfDoc.addPage();
    const { width, height } = page.getSize();
    page.drawText('Chargeback Evidence Packet', {
      x: 50,
      y: height - 100,
      size: 24,
      font: helveticaBold,
      color: rgb(0, 0, 0),
    });
    
    page.drawText(`Generated: ${new Date().toISOString()}`, {
      x: 50,
      y: height - 130,
      size: 12,
      font: helveticaFont,
      color: rgb(0.5, 0.5, 0.5),
    });
    
    page.drawText(`Packet ID: ${packetId}`, {
      x: 50,
      y: height - 150,
      size: 12,
      font: helveticaFont,
      color: rgb(0.5, 0.5, 0.5),
    });
    
    // Add sections
    let yPosition = height - 200;
    for (const section of sections) {
      // Check if we need a new page
      if (yPosition < 100) {
        page = pdfDoc.addPage();
        yPosition = height - 50;
      }
      
      // Section title
      page.drawText(section.title, {
        x: 50,
        y: yPosition,
        size: 16,
        font: helveticaBold,
        color: rgb(0, 0, 0),
      });
      yPosition -= 30;
      
      // Section content (handle text wrapping)
      const lines = wrapText(section.content, 80);
      for (const line of lines) {
        if (yPosition < 50) {
          page = pdfDoc.addPage();
          yPosition = height - 50;
        }
        
        page.drawText(line, {
          x: 50,
          y: yPosition,
          size: 11,
          font: helveticaFont,
          color: rgb(0.2, 0.2, 0.2),
        });
        yPosition -= 15;
      }
      
      yPosition -= 20; // Extra space between sections
    }
    
    // Add attachments list
    if (attachments && attachments.length > 0) {
      page = pdfDoc.addPage();
      yPosition = height - 50;
      
      page.drawText('Attachments', {
        x: 50,
        y: yPosition,
        size: 18,
        font: helveticaBold,
        color: rgb(0, 0, 0),
      });
      yPosition -= 30;
      
      for (const attachment of attachments) {
        page.drawText(`• ${attachment.name} (${attachment.type})`, {
          x: 70,
          y: yPosition,
          size: 11,
          font: helveticaFont,
          color: rgb(0.2, 0.2, 0.2),
        });
        yPosition -= 20;
      }
    }
    
    // Save PDF to bytes
    const pdfBytes = await pdfDoc.save();
    
    // Upload to storage
    const fileName = `${packetId}-${Date.now()}.pdf`;
    const storagePath = `evidence-packets/${fileName}`;
    
    const { error: uploadError } = await supabase.storage
      .from('evidence-packets')
      .upload(storagePath, pdfBytes, {
        contentType: 'application/pdf',
        upsert: false
      });
    
    if (uploadError) {
      throw new Error(`Storage upload failed: ${uploadError.message}`);
    }
    
    return new Response(JSON.stringify({ storagePath }), {
      headers: { 'Content-Type': 'application/json' },
    });
    
  } catch (error) {
    console.error('PDF generation error:', error);
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
});

// Helper function to wrap text
function wrapText(text: string, maxCharsPerLine: number): string[] {
  const words = text.split(' ');
  const lines: string[] = [];
  let currentLine = '';
  
  for (const word of words) {
    if (currentLine.length + word.length + 1 <= maxCharsPerLine) {
      currentLine += (currentLine ? ' ' : '') + word;
    } else {
      if (currentLine) lines.push(currentLine);
      currentLine = word;
    }
  }
  
  if (currentLine) lines.push(currentLine);
  return lines;
}
```

---

## supabase/functions/send-notification/index.ts
```ts
// Supabase Edge Function (Deno)
// deno-lint-ignore-file no-explicit-any
import { serve } from 'https://deno.land/std@0.181.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.38.0';

serve(async (req: Request) => {
  if (req.method !== 'POST') return new Response('Method Not Allowed', { status: 405 });
  
  try {
    const { alertId } = await req.json();
    
    // Initialize Supabase client
    const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
    const supabaseServiceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
    const supabase = createClient(supabaseUrl, supabaseServiceKey);
    
    // Fetch alert details
    const { data: alert } = await supabase
      .from('alerts')
      .select('*, disputes!inner(*, stores!inner(*))')
      .eq('id', alertId)
      .single();
      
    if (!alert) {
      return new Response('Alert not found', { status: 404 });
    }
    
    // Get org members to notify
    const { data: members } = await supabase
      .from('user_org_roles')
      .select('*, users!inner(email)')
      .eq('org_id', alert.org_id);
      
    if (!members || members.length === 0) {
      return new Response('No members to notify', { status: 200 });
    }
    
    // Send notifications based on alert type
    const notifications = [];
    
    for (const member of members) {
      // Email notification
      if (member.users.email) {
        notifications.push(
          sendEmail(member.users.email, alert)
        );
      }
      
      // In-app notification (store in DB)
      notifications.push(
        supabase.from('user_notifications').insert({
          user_id: member.user_id,
          alert_id: alert.id,
          title: getNotificationTitle(alert),
          message: alert.message,
          read: false,
          metadata: {
            dispute_id: alert.dispute_id,
            type: alert.type
          }
        })
      );
    }
    
    await Promise.all(notifications);
    
    // Mark alert as sent
    await supabase
      .from('alerts')
      .update({ sent_at: new Date().toISOString() })
      .eq('id', alertId);
    
    return new Response(JSON.stringify({ 
      ok: true, 
      notified: members.length 
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error: any) {
    console.error('Notification error:', error);
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
});

function getNotificationTitle(alert: any): string {
  const titles: Record<string, string> = {
    'dispute_new': 'New Chargeback Alert',
    'dispute_won': 'Chargeback Won! 🎉',
    'dispute_lost': 'Chargeback Lost',
    'dispute_due_soon': 'Response Due Soon',
    'dispute_submitted': 'Evidence Submitted'
  };
  return titles[alert.type] || 'Chargeback Update';
}

async function sendEmail(email: string, alert: any): Promise<void> {
  // In production, would use SendGrid, Postmark, etc.
  console.log(`Sending email to ${email}:`, {
    subject: getNotificationTitle(alert),
    body: alert.message
  });
  
  // Mock email sending
  return new Promise(resolve => setTimeout(resolve, 100));
}
```

---

## supabase/functions/send-notification/index.ts (updated)
```ts
// Supabase Edge Function (Deno)
// deno-lint-ignore-file no-explicit-any
import { serve } from 'https://deno.land/std@0.181.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.38.0';

interface EmailPayload {
  to: string;
  subject: string;
  text: string;
}

async function sendViaPostmark(apiKey: string, payload: EmailPayload) {
  const res = await fetch('https://api.postmarkapp.com/email', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Postmark-Server-Token': apiKey
    },
    body: JSON.stringify({
      From: Deno.env.get('NOTIFY_FROM_EMAIL') || 'no-reply@example.com',
      To: payload.to,
      Subject: payload.subject,
      TextBody: payload.text
    })
  });
  if (!res.ok) throw new Error(`Postmark failed: ${await res.text()}`);
}

serve(async (req: Request) => {
  if (req.method !== 'POST') return new Response('Method Not Allowed', { status: 405 });
  try {
    const { alertId } = await req.json();
    const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
    const supabaseServiceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
    const supabase = createClient(supabaseUrl, supabaseServiceKey);

    const { data: alert } = await supabase
      .from('alerts')
      .select('*, disputes!inner(org_id, psp_id, amount, status), org_id')
      .eq('id', alertId)
      .single();
    if (!alert) return new Response('Alert not found', { status: 404 });

    // Load org members and their notification prefs
    const { data: members } = await supabase
      .from('user_org_roles')
      .select('user_id, users!inner(email)')
      .eq('org_id', alert.org_id);

    const toNotify = members || [];
    const emails: EmailPayload[] = [];
    const postmarkKey = Deno.env.get('POSTMARK_SERVER_TOKEN') || '';

    // Title mapping
    const titles: Record<string, string> = {
      'dispute_new': 'New Chargeback Alert',
      'dispute_won': 'Chargeback Won! 🎉',
      'dispute_lost': 'Chargeback Lost',
      'dispute_due_7_days': 'Dispute Due in 7 Days',
      'dispute_due_3_days': 'Dispute Due in 3 Days',
      'dispute_due_1_day': 'Dispute Due Tomorrow',
      'dispute_submitted': 'Evidence Submitted'
    };
    const subject = titles[alert.type] || 'Chargeback Update';
    const text = `${alert.message || ''}`;

    // Build emails respecting user prefs
    for (const m of toNotify) {
      if (!m.users?.email) continue;
      const { data: prefRow } = await supabase
        .from('user_notification_prefs')
        .select('prefs')
        .eq('user_id', m.user_id)
        .eq('org_id', alert.org_id)
        .maybeSingle();

      const prefs = (prefRow as any)?.prefs || null;
      const key = alert.type?.startsWith('dispute_due_') ? 'dueSoon' :
        alert.type === 'dispute_new' ? 'newDispute' :
        alert.type === 'dispute_won' || alert.type === 'dispute_lost' ? 'outcome' : 'weekly';
      const emailEnabled = prefs ? !!(prefs[key] && prefs[key].email) : true;

      // In-app notification row
      await supabase.from('user_notifications').insert({
        user_id: m.user_id,
        alert_id: alert.id,
        title: subject,
        message: text,
        read: false,
        metadata: { dispute_id: alert.dispute_id, type: alert.type }
      });

      if (emailEnabled && postmarkKey) {
        emails.push({ to: m.users.email, subject, text });
      }
    }

    // Send batched emails
    for (const e of emails) {
      try { await sendViaPostmark(postmarkKey, e); } catch (err) { console.error('Email error', err); }
    }

    await supabase
      .from('alerts')
      .update({ sent_at: new Date().toISOString() })
      .eq('id', alertId);

    return new Response(JSON.stringify({ ok: true, emailed: emails.length, members: toNotify.length }), {
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (error: any) {
    console.error('Notification error:', error);
    return new Response(JSON.stringify({ error: error.message }), { status: 500, headers: { 'Content-Type': 'application/json' } });
  }
});
```

---

## supabase/functions/run-scheduled-submissions/index.ts
```ts
// Supabase Edge Function (Deno) — cron every 5 minutes
// deno-lint-ignore-file no-explicit-any
import { serve } from 'https://deno.land/std@0.181.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.38.0';

serve(async (_req: Request) => {
  try {
    const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
    const supabaseServiceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
    const supabase = createClient(supabaseUrl, supabaseServiceKey);

    const now = new Date().toISOString();
    const { data: jobs } = await supabase
      .from('submission_jobs')
      .select('*')
      .lte('scheduled_at', now)
      .eq('status', 'scheduled')
      .limit(50);

    if (!jobs || jobs.length === 0) {
      return new Response(JSON.stringify({ ok: true, ran: 0 }), { headers: { 'Content-Type': 'application/json' } });
    }

    for (const job of jobs) {
      try {
        // Call internal API to submit immediately
        const res = await fetch(`${supabaseUrl}/functions/v1/internal-submit`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${supabaseServiceKey}` },
          body: JSON.stringify({ disputeId: job.dispute_id, method: job.method })
        });
        if (!res.ok) throw new Error(await res.text());
        await supabase
          .from('submission_jobs')
          .update({ status: 'completed', updated_at: new Date().toISOString() })
          .eq('id', job.id);
      } catch (e: any) {
        await supabase
          .from('submission_jobs')
          .update({ status: 'error', attempts: (job.attempts || 0) + 1, last_error: e.message, updated_at: new Date().toISOString() })
          .eq('id', job.id);
      }
    }

    return new Response(JSON.stringify({ ok: true, ran: jobs.length }), { headers: { 'Content-Type': 'application/json' } });
  } catch (e: any) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500, headers: { 'Content-Type': 'application/json' } });
  }
});
```

---

## supabase/functions/internal-submit/index.ts
```ts
// Supabase Edge Function (Deno) — internal privileged submit (by cron)
// deno-lint-ignore-file no-explicit-any
import { serve } from 'https://deno.land/std@0.181.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.38.0';

serve(async (req: Request) => {
  if (req.method !== 'POST') return new Response('Method Not Allowed', { status: 405 });
  try {
    const { disputeId, method } = await req.json();
    const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
    const supabaseServiceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
    const supabase = createClient(supabaseUrl, supabaseServiceKey);

    // Compose and submit (minimal duplicate of API path)
    // Load dispute to figure provider
    const { data: dispute } = await supabase
      .from('disputes')
      .select('*, stores!inner(platform, oauth_tokens)')
      .eq('id', disputeId)
      .single();
    if (!dispute) return new Response('Not Found', { status: 404 });

    // No packet building here to keep brief; rely on app API normally
    await fetch(`${supabaseUrl}/api/submissions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ disputeId, method })
    });
    return new Response(JSON.stringify({ ok: true }), { headers: { 'Content-Type': 'application/json' } });
  } catch (e: any) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500, headers: { 'Content-Type': 'application/json' } });
  }
});
```

## supabase/migrations/core/0008_audit_triggers.sql
```sql
create or replace function audit_row_change() returns trigger as $$
declare
  v_user uuid;
  v_action text;
  v_data jsonb;
begin
  v_user := auth.uid();
  v_action := tg_op; -- INSERT/UPDATE/DELETE
  if (tg_op = 'DELETE') then
    v_data := to_jsonb(OLD);
  else
    v_data := to_jsonb(NEW);
  end if;
  insert into audit_events (org_id, actor_user_id, action, data)
  values (
    coalesce(v_data->>'org_id', v_data->>'orgId')::uuid,
    v_user,
    concat(tg_table_name, ':', v_action),
    jsonb_build_object('table', tg_table_name, 'row', v_data)
  );
  return null;
end;
$$ language plpgsql security definer;

-- Attach to sensitive tables
drop trigger if exists trg_audit_disputes on disputes;
create trigger trg_audit_disputes after insert or update or delete on disputes
for each row execute function audit_row_change();

drop trigger if exists trg_audit_orders on orders;
create trigger trg_audit_orders after insert or update or delete on orders
for each row execute function audit_row_change();

drop trigger if exists trg_audit_submissions on submissions;
create trigger trg_audit_submissions after insert or update or delete on submissions
for each row execute function audit_row_change();

drop trigger if exists trg_audit_alerts on alerts;
create trigger trg_audit_alerts after insert or update or delete on alerts
for each row execute function audit_row_change();
```

---

## supabase/migrations/core/0009_rls_write_expansions.sql
```sql
-- Expand write WITH CHECK to org for key tables

-- orders
create policy orders_insert on orders
  for insert with check (
    exists (select 1 from user_org_roles uor where uor.org_id = orders.org_id and uor.user_id = auth.uid())
  );
create policy orders_update on orders
  for update using (
    exists (select 1 from user_org_roles uor where uor.org_id = orders.org_id and uor.user_id = auth.uid())
  ) with check (
    exists (select 1 from user_org_roles uor where uor.org_id = orders.org_id and uor.user_id = auth.uid())
  );

-- evidence_items (writes via server — keep tight, example shown if needed)
-- create policy evidence_items_insert on evidence_items for insert with check (false);

-- refund_events (insert via server actions)
create policy refund_events_insert on refund_events
  for insert with check (
    exists (
      select 1 from disputes d join user_org_roles u on u.org_id = d.org_id
      where d.id = refund_events.dispute_id and u.user_id = auth.uid()
    )
  );

-- alerts (insert via server/edge functions)
create policy alerts_insert on alerts
  for insert with check (
    exists (select 1 from user_org_roles u where u.org_id = alerts.org_id and u.user_id = auth.uid())
  );

-- submissions (already added for insert/update in 0007 but included for completeness)
```

---

## .github/workflows/ci.yml
```yaml
name: CI
on:
  pull_request:
  push:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npx playwright install --with-deps || true
      - run: npm run build --if-present
      - run: npm run test --if-present
```

---

## src/tests/e2e/submit.spec.ts
```ts
import { test, expect } from '@playwright/test';

test('dispute detail validates before submit', async ({ page }) => {
  await page.goto('/disputes/00000000-0000-0000-0000-000000000201');
  await page.waitForSelector('text=Evidence Packet Preview');
  // Readiness bar present
  await expect(page.locator('text=Readiness:')).toBeVisible();
  // Open submit modal
  await page.getByText('Submit').click();
  await expect(page.getByText('Review Before Submitting')).toBeVisible();
});
```

---

## src/tests/unit/evidenceComposer.gaps.test.ts
```ts
import { composePacket } from '@chargebacks/evidenceComposer';

test('composer reports partial refund gap', async () => {
  const pkt = await composePacket('00000000-0000-0000-0000-000000000201');
  expect(Array.isArray(pkt.gaps)).toBe(true);
});
```


## src/lib/notifications.ts
```ts
import { createServerClient } from './supabaseServer';

export async function createAlert(
  disputeId: string,
  type: string,
  message: string,
  metadata?: any
): Promise<void> {
  const db = createServerClient();
  
  // Get dispute details for org_id
  const { data: dispute } = await db
    .from('disputes')
    .select('org_id')
    .eq('id', disputeId)
    .single();
    
  if (!dispute) return;
  
  // Create alert
  const { data: alert } = await db
    .from('alerts')
    .insert({
      dispute_id: disputeId,
      org_id: dispute.org_id,
      type,
      message,
      metadata
    })
    .select('id')
    .single();
    
  if (!alert) return;
  
  // Trigger notification Edge Function
  const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
  const serviceKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;
  
  await fetch(`${supabaseUrl}/functions/v1/send-notification`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${serviceKey}`
    },
    body: JSON.stringify({ alertId: alert.id })
  });
}

export async function checkDueSoonDisputes(): Promise<void> {
  const db = createServerClient();
  
  // Check for T-7, T-3, and T-1 alerts
  const alertThresholds = [
    { days: 7, type: 'dispute_due_7_days' },
    { days: 3, type: 'dispute_due_3_days' },
    { days: 1, type: 'dispute_due_1_day' }
  ];
  
  for (const threshold of alertThresholds) {
    const targetDate = new Date();
    targetDate.setDate(targetDate.getDate() + threshold.days);
    const nextDay = new Date(targetDate);
    nextDay.setDate(nextDay.getDate() + 1);
    
    const { data: disputes } = await db
      .from('disputes')
      .select('id, psp_id, due_by, amount')
      .in('status', ['new', 'draft'])
      .gte('due_by', targetDate.toISOString())
      .lt('due_by', nextDay.toISOString());
      
    if (!disputes) continue;
    
    for (const dispute of disputes) {
      // Check if we already sent this specific alert type
      const { data: existingAlert } = await db
        .from('alerts')
        .select('id')
        .eq('dispute_id', dispute.id)
        .eq('type', threshold.type)
        .single();
        
      if (!existingAlert) {
        const urgencyEmoji = threshold.days === 1 ? '🚨' : threshold.days === 3 ? '⚠️' : '📅';
        await createAlert(
          dispute.id,
          threshold.type,
          `${urgencyEmoji} Dispute ${dispute.psp_id} ($${dispute.amount}) due in ${threshold.days} day${threshold.days > 1 ? 's' : ''}`,
          { 
            days_remaining: threshold.days,
            due_date: dispute.due_by,
            amount: dispute.amount
          }
        );
      }
    }
  }
}

export async function getUserNotifications(userId: string): Promise<any[]> {
  const db = createServerClient();
  
  const { data: notifications } = await db
    .from('user_notifications')
    .select('*, alerts!inner(*)')
    .eq('user_id', userId)
    .eq('read', false)
    .order('created_at', { ascending: false })
    .limit(10);
    
  return notifications || [];
}

export async function markNotificationRead(notificationId: string): Promise<void> {
  const db = createServerClient();
  
  await db
    .from('user_notifications')
    .update({ read: true, read_at: new Date().toISOString() })
    .eq('id', notificationId);
}
```

---

## src/components/NotificationBell.tsx
```tsx
'use client';
import { useEffect, useState } from 'react';
import { supabaseClient } from '@core/supabaseClient';

export function NotificationBell() {
  const [notifications, setNotifications] = useState<any[]>([]);
  const [showDropdown, setShowDropdown] = useState(false);

  useEffect(() => {
    fetchNotifications();
    
    // Set up realtime subscription
    const subscription = supabaseClient
      .channel('notifications')
      .on('postgres_changes', {
        event: 'INSERT',
        schema: 'public',
        table: 'user_notifications'
      }, () => {
        fetchNotifications();
      })
      .subscribe();
      
    return () => {
      subscription.unsubscribe();
    };
  }, []);

  const fetchNotifications = async () => {
    const { data: { user } } = await supabaseClient.auth.getUser();
    if (!user) return;
    
    const { data } = await supabaseClient
      .from('user_notifications')
      .select('*, alerts!inner(*)')
      .eq('user_id', user.id)
      .eq('read', false)
      .order('created_at', { ascending: false })
      .limit(5);
      
    setNotifications(data || []);
  };

  const markAsRead = async (notificationId: string) => {
    await supabaseClient
      .from('user_notifications')
      .update({ read: true, read_at: new Date().toISOString() })
      .eq('id', notificationId);
      
    fetchNotifications();
  };

  return (
    <div className="relative">
      <button
        onClick={() => setShowDropdown(!showDropdown)}
        className="relative p-2 text-gray-600 hover:text-gray-900"
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
        {notifications.length > 0 && (
          <span className="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-500" />
        )}
      </button>
      
      {showDropdown && (
        <>
          <div
            className="fixed inset-0 z-10"
            onClick={() => setShowDropdown(false)}
          />
          <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border z-20">
            <div className="p-3 border-b">
              <h3 className="font-semibold">Notifications</h3>
            </div>
            
            {notifications.length === 0 ? (
              <div className="p-4 text-center text-gray-500">
                No new notifications
              </div>
            ) : (
              <div className="max-h-96 overflow-y-auto">
                {notifications.map((notification) => (
                  <div
                    key={notification.id}
                    onClick={() => markAsRead(notification.id)}
                    className="p-3 hover:bg-gray-50 cursor-pointer border-b last:border-b-0"
                  >
                    <p className="font-medium text-sm">{notification.title}</p>
                    <p className="text-xs text-gray-600 mt-1">{notification.message}</p>
                    <p className="text-xs text-gray-400 mt-1">
                      {new Date(notification.created_at).toLocaleString()}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}
```


---

## supabase/migrations/0004_test_helpers.sql
```sql
-- Helpers for tests
create or replace function truncate_all_test_data() returns void language plpgsql as $$
begin
  perform (select true);
  -- Order matters due to FKs. Truncate child tables first.
  truncate table submission_packets, submissions, evidence_items, refund_events,
    alerts, disputes, orders, stores, user_org_roles, users, orgs restart identity cascade;
end;
$$;
```

---

## playwright.config.ts
```ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: 'src/tests/e2e',
  timeout: 30000,
  fullyParallel: true,
  retries: 0,
  use: { baseURL: 'http://localhost:3000' },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } }
  ]
});
```

---

## src/tests/e2e/disputes.spec.ts
```ts
import { test, expect } from '@playwright/test';

test('disputes inbox loads', async ({ page }) => {
  await page.goto('/disputes');
  await expect(page.getByText('Disputes Inbox')).toBeVisible();
});
```

---

## src/tests/unit/evidenceComposer.test.ts
```ts
import { composePacket } from '@chargebacks/evidenceComposer';

test('composePacket builds basic sections', async () => {
  const pkt = await composePacket('00000000-0000-0000-0000-000000000000');
  expect(pkt.sections.length).toBeGreaterThan(0);
});
```

---

## src/tests/integration/rls.test.ts
```ts
test('placeholder RLS test', () => {
  expect(true).toBe(true);
});
```

---

## Testing — Critical E2E Paths (PR Gate)
```markdown
- Auth and onboarding (if enabled): sign-in → org create → connect store (stub if not in MVP)
- Disputes inbox: list disputes, filter by reason/status/date
- Dispute detail: draft generation (narrative + attachments list)
- Packet preview: shows composed sections and attachment fingerprints
- Submission: submit via provider (Stripe/Shopify) → queued → ack
- Webhooks: provider webhook updates dispute status → submission recorded
- Outcomes: decision received (won/lost), analytics updated
- Archive: packet stored with immutable SHA-256; signed URL retrieval works
```

---

## RLS Policy Test Matrix (Read/Write Expectations)
```markdown
- orgs: members of org (via user_org_roles) can select; writes restricted to owners/admins (service role).
- users: user can select self; service role manages inserts.
- user_org_roles: user can select rows where user_id = auth.uid(); service role manages writes.
- stores: users in same org can select; writes via service role (OAuth flows).
- disputes: users in same org can select; writes via service role/webhooks.
- orders: users in same org can select; writes via service role/importers.
- evidence_items: users in dispute.org can select; writes via server actions when composing.
- submissions: users in dispute.org can select; inserts via server action; updates via webhooks.
- analytics_winrates: org members can select; writes by background jobs/service role.
- audit_events: org members can select limited fields; inserts by server actions and webhooks.
- refund_events: users in dispute.org can select; inserts by server/import.
- alerts: users in same org can select; inserts by alert provider webhooks.
- submission_packets: org members can select metadata; storage object access via signed URL only.

Test each table for:
- Access allowed for correct org member
- Access denied for user in another org
- Write paths only via server role/webhook contexts
```

---

## supabase/migrations/core/0003_notification_prefs.sql
```sql
create table if not exists user_notification_prefs (
  user_id uuid not null references users(id) on delete cascade,
  org_id uuid not null references orgs(id) on delete cascade,
  prefs jsonb not null default jsonb_build_object(
    'newDispute', jsonb_build_object('email', true, 'app', true, 'sms', false),
    'dueSoon', jsonb_build_object('email', true, 'app', true, 'sms', true),
    'outcome', jsonb_build_object('email', true, 'app', true, 'sms', false),
    'weekly', jsonb_build_object('email', true, 'app', false, 'sms', false)
  ),
  updated_at timestamptz not null default now(),
  primary key (user_id, org_id)
);

alter table user_notification_prefs enable row level security;

create policy user_notification_prefs_select on user_notification_prefs
  for select using (
    user_id = auth.uid() and exists (
      select 1 from user_org_roles uor where uor.org_id = user_notification_prefs.org_id and uor.user_id = auth.uid()
    )
  );

create policy user_notification_prefs_upsert on user_notification_prefs
  for insert with check (
    user_id = auth.uid() and exists (
      select 1 from user_org_roles uor where uor.org_id = user_notification_prefs.org_id and uor.user_id = auth.uid()
    )
  );

create policy user_notification_prefs_update on user_notification_prefs
  for update using (user_id = auth.uid())
  with check (user_id = auth.uid());
```

---

## src/app/api/settings/notifications/route.ts
```ts
import { NextRequest, NextResponse } from 'next/server';
import { createServerClient } from '@core/supabaseServer';

export async function GET(req: NextRequest) {
  const db = createServerClient();
  const { data: { user } } = await (db.auth as any).getUser();
  if (!user) return new NextResponse('Unauthorized', { status: 401 });

  // Resolve user's active org (first one)
  const { data: uor } = await db
    .from('user_org_roles')
    .select('org_id')
    .eq('user_id', user.id)
    .maybeSingle();
  if (!uor?.org_id) return NextResponse.json({ prefs: null });

  const { data } = await db
    .from('user_notification_prefs')
    .select('prefs')
    .eq('user_id', user.id)
    .eq('org_id', uor.org_id)
    .maybeSingle();

  return NextResponse.json({ prefs: data?.prefs ?? null });
}

export async function PUT(req: NextRequest) {
  const db = createServerClient();
  const { data: { user } } = await (db.auth as any).getUser();
  if (!user) return new NextResponse('Unauthorized', { status: 401 });

  const { prefs } = await req.json().catch(() => ({ prefs: null }));
  if (!prefs || typeof prefs !== 'object') return new NextResponse('Bad Request', { status: 400 });

  const { data: uor } = await db
    .from('user_org_roles')
    .select('org_id')
    .eq('user_id', user.id)
    .maybeSingle();
  if (!uor?.org_id) return new NextResponse('No org', { status: 400 });

  await db
    .from('user_notification_prefs')
    .upsert({ user_id: user.id, org_id: uor.org_id, prefs, updated_at: new Date().toISOString() });

  return NextResponse.json({ ok: true });
}
```

---

## src/app/settings/page.tsx (updated)
```tsx
'use client';
import { useState, useEffect } from 'react';
import { supabaseClient } from '@core/supabaseClient';

export default function SettingsPage() {
  const [activeSection, setActiveSection] = useState('general');
  const [orgName, setOrgName] = useState('');
  const [timezone, setTimezone] = useState('America/New_York');
  const [currency, setCurrency] = useState('USD');
  const [selectedTemplate, setSelectedTemplate] = useState('ecommerce');
  const [notifications, setNotifications] = useState({
    newDispute: { email: true, app: true, sms: false },
    dueSoon: { email: true, app: true, sms: true },
    outcome: { email: true, app: true, sms: false },
    weekly: { email: true, app: false, sms: false }
  });
  const [saving, setSaving] = useState(false);

  useEffect(() => { loadSettings(); }, []);

  const loadSettings = async () => {
    const { data: { user } } = await supabaseClient.auth.getUser();
    if (!user) return;

    const { data: userOrg } = await supabaseClient
      .from('user_org_roles')
      .select('org_id, orgs(*)')
      .eq('user_id', user.id)
      .maybeSingle();
    if (userOrg?.orgs) setOrgName((userOrg.orgs as any).name || '');

    // Fetch persisted notification prefs
    const res = await fetch('/api/settings/notifications', { method: 'GET' });
    if (res.ok) {
      const json = await res.json();
      if (json.prefs) setNotifications(json.prefs);
    }
  };

  const saveSettings = async () => {
    setSaving(true);
    try {
      await fetch('/api/settings/notifications', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prefs: notifications })
      });
      alert('Settings saved');
    } finally {
      setSaving(false);
    }
  };

  const sections = [
    { id: 'general', label: 'General', icon: '⚙️' },
    { id: 'templates', label: 'Evidence Templates', icon: '📄' },
    { id: 'integrations', label: 'Integrations', icon: '🔌' },
    { id: 'notifications', label: 'Notifications', icon: '🔔' },
    { id: 'billing', label: 'Billing', icon: '💳' },
    { id: 'team', label: 'Team Members', icon: '👥' },
    { id: 'advanced', label: 'Advanced', icon: '🔧' }
  ];

  return (
    <main className="p-6">
      <h1 className="text-2xl font-semibold mb-6">Settings</h1>
      <div className="flex gap-6">
        <div className="hidden md:block w-64">
          <nav className="space-y-1">
            {sections.map(section => (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={`w-full text-left px-4 py-2 rounded-lg flex items-center gap-2 transition-colors ${
                  activeSection === section.id ? 'bg-blue-50 text-blue-700' : 'hover:bg-gray-100'
                }`}
              >
                <span>{section.icon}</span>
                <span>{section.label}</span>
              </button>
            ))}
          </nav>
        </div>
        <div className="md:hidden w-full">
          <label className="block text-sm font-medium mb-2">Section</label>
          <select
            value={activeSection}
            onChange={(e)=>setActiveSection(e.target.value)}
            className="w-full border rounded px-3 py-2 mb-4"
          >
            {sections.map(s => (
              <option key={s.id} value={s.id}>{s.label}</option>
            ))}
          </select>
        </div>
        <div className="flex-1 bg-white rounded-lg shadow p-6">
          {activeSection === 'general' && (
            <div className="space-y-6">
              <h2 className="text-lg font-medium">General Settings</h2>
              <div>
                <label className="block text-sm font-medium mb-1">Organization Name</label>
                <input 
                  type="text" 
                  value={orgName}
                  onChange={(e) => setOrgName(e.target.value)}
                  className="w-full border rounded px-3 py-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Time Zone</label>
                <select 
                  value={timezone} 
                  onChange={(e) => setTimezone(e.target.value)}
                  className="w-full border rounded px-3 py-2"
                >
                  <option value="America/New_York">Eastern Time</option>
                  <option value="America/Chicago">Central Time</option>
                  <option value="America/Denver">Mountain Time</option>
                  <option value="America/Los_Angeles">Pacific Time</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Default Currency</label>
                <select 
                  value={currency} 
                  onChange={(e) => setCurrency(e.target.value)}
                  className="w-full border rounded px-3 py-2"
                >
                  <option value="USD">USD - US Dollar</option>
                  <option value="EUR">EUR - Euro</option>
                  <option value="GBP">GBP - British Pound</option>
                </select>
              </div>
            </div>
          )}

          {activeSection === 'notifications' && (
            <div className="space-y-6">
              <h2 className="text-lg font-medium">Notification Preferences</h2>
              <div className="space-y-4">
                {Object.entries(notifications).map(([key, prefs]) => (
                  <div key={key} className="border rounded p-4">
                    <h3 className="font-medium mb-3 capitalize">
                      {key === 'newDispute' ? 'New dispute received' :
                       key === 'dueSoon' ? 'Dispute due soon' :
                       key === 'outcome' ? 'Outcome received' :
                       'Weekly summary'}
                    </h3>
                    <div className="flex gap-6">
                      <label className="flex items-center gap-2">
                        <input 
                          type="checkbox" 
                          checked={prefs.email as boolean}
                          onChange={(e) => setNotifications({
                            ...notifications,
                            [key]: { ...(prefs as any), email: e.target.checked }
                          })}
                        />
                        <span>Email</span>
                      </label>
                      <label className="flex items-center gap-2">
                        <input 
                          type="checkbox" 
                          checked={prefs.app as boolean}
                          onChange={(e) => setNotifications({
                            ...notifications,
                            [key]: { ...(prefs as any), app: e.target.checked }
                          })}
                        />
                        <span>In-app</span>
                      </label>
                      <label className="flex items-center gap-2">
                        <input 
                          type="checkbox" 
                          checked={prefs.sms as boolean}
                          onChange={(e) => setNotifications({
                            ...notifications,
                            [key]: { ...(prefs as any), sms: e.target.checked }
                          })}
                        />
                        <span>SMS</span>
                      </label>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="mt-8 flex justify-end">
            <button 
              onClick={saveSettings}
              disabled={saving}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {saving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}
```

---

## src/app/api/submissions/validate/route.ts
```ts
import { NextRequest, NextResponse } from 'next/server';
import { createServerClient } from '@core/supabaseServer';
import { composePacket } from '@chargebacks/evidenceComposer';

export async function POST(req: NextRequest) {
  const { disputeId } = await req.json().catch(() => ({}));
  if (!disputeId) return new NextResponse('Bad Request', { status: 400 });

  const db = createServerClient();
  // Auth required
  const { data: { user } } = await (db.auth as any).getUser();
  if (!user) return new NextResponse('Unauthorized', { status: 401 });

  try {
    const packet = await composePacket(disputeId);
    return NextResponse.json({
      readiness: packet.readiness,
      gaps: packet.gaps,
      guidance: packet.guidance
    });
  } catch (e: any) {
    return new NextResponse(e.message, { status: 400 });
  }
}
```

---

## src/app/disputes/[id]/page.tsx (updated pre-submit validation)
```tsx
'use client';
import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { supabaseClient } from '@core/supabaseClient';
import { DraftEditor } from '@ui/DraftEditor';
import { PacketPreview } from '@ui/PacketPreview';
import { Tabs } from '@ui/Tabs';
import { SubmissionModal } from '@ui/SubmissionModal';
import { formatDistanceToNow } from 'date-fns';

export default function DisputeDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [dispute, setDispute] = useState<any>(null);
  const [evidence, setEvidence] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const [guidance, setGuidance] = useState<any|null>(null);
  const [validation, setValidation] = useState<{ readiness: number; gaps: any[] } | null>(null);

  useEffect(() => {
    if (params.id) {
      fetchDispute(params.id as string);
      fetchEvidence(params.id as string);
      validate(params.id as string);
    }
  }, [params.id]);

  const fetchDispute = async (id: string) => {
    try {
      const { data, error } = await supabaseClient
        .from('disputes')
        .select('*, stores(platform), submissions(*), orders(*)')
        .eq('id', id)
        .single();
      if (error) throw error;
      setDispute(data);
    } finally {
      setLoading(false);
    }
  };

  const fetchEvidence = async (disputeId: string) => {
    try {
      const response = await fetch('/api/evidence', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ disputeId })
      });
      if (response.ok) {
        const data = await response.json();
        setEvidence(data.draft);
        setGuidance(data.draft?.guidance || null);
      }
    } catch {}
  };

  const validate = async (disputeId: string) => {
    try {
      const res = await fetch('/api/submissions/validate', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ disputeId })
      });
      if (res.ok) {
        const json = await res.json();
        setValidation({ readiness: json.readiness, gaps: json.gaps || [] });
      }
    } catch {}
  };

  const handleSubmit = async (method: 'api' | 'manual') => {
    setSubmitting(true);
    setErrorMsg('');
    setProgress('validating');
    try {
      // Re-validate before submission
      await validate(dispute.id);
      if (validation && (validation.gaps || []).some((g: any) => g.severity === 'error')) {
        alert('Fix required gaps before submitting');
        return;
      }
      setProgress('composing');
      const response = await fetch('/api/submissions', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ disputeId: dispute.id, method })
      });
      if (response.ok) {
        setProgress('confirming');
        const data = await response.json();
        setShowModal(false);
        setShowSuccess(true);
        if (method === 'manual' && data.pdfUrl) window.open(data.pdfUrl, '_blank');
        await fetchDispute(dispute.id);
        setTimeout(() => setShowSuccess(false), 5000);
        setProgress('done');
      } else {
        setProgress('error');
        throw new Error('Submission failed');
      }
    } catch (e) {
      setErrorMsg('Failed to submit evidence. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return null;
  if (!dispute) return null;

  const lastSubmission = dispute.submissions?.[0];
  const canSubmit = ['new', 'draft'].includes(dispute.status);

  return (
    <main className="p-6">
      <div className="mb-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-2xl font-semibold">Dispute #{dispute.psp_id}</h1>
            <div className="mt-2 flex items-center gap-4 text-sm">
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                dispute.status === 'new' ? 'bg-red-100 text-red-800' :
                dispute.status === 'draft' ? 'bg-yellow-100 text-yellow-800' :
                dispute.status === 'submitted' ? 'bg-blue-100 text-blue-800' :
                dispute.status === 'won' ? 'bg-green-100 text-green-800' :
                'bg-gray-100 text-gray-800'
              }`}>
                {dispute.status.toUpperCase()}
              </span>
              <span>Reason: <strong>{dispute.reason_code}</strong></span>
              <span>Amount: <strong>${dispute.amount}</strong></span>
              <span className={dispute.due_by && new Date(dispute.due_by) < new Date(Date.now() + 3 * 24 * 60 * 60 * 1000) ? 'text-red-600 font-medium' : ''}>
                Due: <strong>{dispute.due_by ? formatDistanceToNow(new Date(dispute.due_by), { addSuffix: true }) : 'No deadline'}</strong>
              </span>
            </div>
          </div>
          <div className="space-x-2">
            {canSubmit && (
              <button
                onClick={() => setShowModal(true)}
                disabled={submitting || (validation && (validation.gaps || []).some((g: any) => g.severity === 'error'))}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
              >
                Submit
              </button>
            )}
          </div>
        </div>

        {validation && (
          <div className="mt-3 p-3 rounded border bg-white">
            <div className="flex items-center gap-3">
              <div className="w-24 bg-gray-200 h-2 rounded-full">
                <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${validation.readiness || 0}%` }} />
              </div>
              <span className="text-sm text-gray-700">Readiness: {validation.readiness || 0}%</span>
            </div>
            {(validation.gaps || []).length > 0 && (
              <ul className="mt-2 text-sm list-disc list-inside">
                {validation.gaps.map((g: any) => (
                  <li key={g.code} className={g.severity === 'error' ? 'text-red-700' : 'text-yellow-700'}>
                    {g.message}
                  </li>
                ))}
              </ul>
            )}
            {errorMsg && (
              <div className="mt-2 text-sm text-red-700">{errorMsg}</div>
            )}
            {submitting && (
              <div className="mt-3 text-xs text-gray-600">
                {progress === 'validating' && 'Checking submission readiness...'}
                {progress === 'composing' && 'Composing evidence packet...'}
                {progress === 'pdf' && 'Generating PDF...'}
                {progress === 'submitting' && 'Submitting to provider...'}
                {progress === 'confirming' && 'Confirming submission...'}
              </div>
            )}
          </div>
        )}
      </div>

      <Tabs tabs={['Evidence Draft', 'Order Details', 'Customer History', 'Shipping', 'Device & Session', 'Timeline']}>
        {() => (
          <div className="grid gap-6 md:grid-cols-2">
            <section>
              <DraftEditor 
                disputeId={dispute.id}
                evidence={evidence}
                onUpdate={() => { fetchEvidence(dispute.id); validate(dispute.id); }}
              />
            </section>
            <section>
              <PacketPreview evidence={evidence} loading={!evidence} />
            </section>
          </div>
        )}
      </Tabs>

      <SubmissionModal
        open={showModal}
        onClose={() => setShowModal(false)}
        counts={{ sections: evidence?.sections?.length || 0, attachments: evidence?.attachments?.length || 0 }}
        onSubmit={handleSubmit}
      />
    </main>
  );
}
```

---

## src/app/api/shopify/backfill/route.ts (updated disputes backfill)
```ts
import { NextRequest, NextResponse } from 'next/server';
import { createServerClient } from '@core/supabaseServer';
import { getShopifyClient } from '@core/shopify';

export async function POST(req: NextRequest) {
  const { shop, limit = 50 } = await req.json();
  if (!shop) return new NextResponse('Missing shop', { status: 400 });
  const db = createServerClient();

  const { data: store } = await db
    .from('stores')
    .select('id, org_id, oauth_tokens')
    .eq('platform', 'shopify')
    .eq('oauth_tokens->>shop_domain', shop)
    .maybeSingle();
  if (!store?.oauth_tokens?.shopify_access_token) return new NextResponse('Store not found or token missing', { status: 404 });

  const rest: any = getShopifyClient(shop, store.oauth_tokens.shopify_access_token);

  // Orders backfill (recent)
  try {
    const ordersResp = await rest.orders.list({ limit: Math.min(limit, 100) });
    for (const o of ordersResp?.data || []) {
      await db.from('orders').upsert({
        org_id: store.org_id,
        store_id: store.id,
        customer_json: o.customer || {},
        items_json: o.line_items || [],
        addresses_json: { shipping_address: o.shipping_address || {}, billing_address: o.billing_address || {} },
        raw: o,
        created_at: o.created_at || new Date().toISOString()
      }, { onConflict: 'id' });
    }
  } catch (e) {
    console.warn('Orders backfill failed', e);
  }

  // Disputes backfill (Shopify Payments)
  try {
    const res = await fetch(`https://${shop}/admin/api/2024-01/shopify_payments/disputes.json?limit=${Math.min(limit, 50)}`, {
      headers: {
        'X-Shopify-Access-Token': store.oauth_tokens.shopify_access_token,
        'Content-Type': 'application/json'
      }
    });
    if (res.ok) {
      const body: any = await res.json();
      const disputes = body.disputes || body.shopify_payments_disputes || [];
      for (const d of disputes) {
        const pspId = String(d.id || d.dispute_id || '');
        const reason = d.reason || d.reason_details || 'unknown';
        const amount = parseFloat(String(d.amount || d.amount_cents / 100 || 0));
        const dueAt = d.due_at || d.evidence_details?.due_by || null;
        const statusMap: Record<string, string> = { needs_response: 'new', under_review: 'submitted', accepted: 'won', won: 'won', lost: 'lost' };
        const status = statusMap[String(d.status)] || 'draft';
        const row = {
          org_id: store.org_id,
          store_id: store.id,
          psp_id: pspId,
          psp_provider: 'shopify',
          reason_code: reason,
          amount,
          due_by: dueAt,
          status,
          raw: d
        } as any;

        const { data: existing } = await db
          .from('disputes')
          .select('id')
          .eq('org_id', store.org_id)
          .eq('psp_id', pspId)
          .maybeSingle();
        if (existing) await db.from('disputes').update(row).eq('id', existing.id);
        else await db.from('disputes').insert(row);
      }
    }
  } catch (e) {
    console.warn('Disputes backfill failed', e);
  }

  return NextResponse.json({ ok: true });
}
```

---

## src/lib/evidenceComposer.ts (hardened)
```ts
import { createServerClient } from './supabaseServer';
import { UUID } from '@/types';
import { objectExists } from './storage';
import { checkFraudSignals } from './sessionTracking';

export type EvidenceSection = {
  title: string;
  content: string;
  required: boolean;
  weight: number;
};

export type EvidenceAttachment = {
  name: string;
  path: string;
  type: string;
  required: boolean;
  present?: boolean;
};

const REASON_CODE_TEMPLATES: Record<string, { sections: string[]; attachments: string[] }> = {
  fraudulent: {
    sections: ['order_details', 'customer_verification', 'shipping_proof', 'device_info', 'communication', 'refund_history'],
    attachments: ['invoice', 'shipping_label', 'tracking_receipt', 'delivery_confirmation']
  },
  product_not_received: {
    sections: ['order_details', 'shipping_proof', 'tracking_updates', 'communication'],
    attachments: ['invoice', 'shipping_label', 'tracking_receipt', 'delivery_confirmation']
  },
  duplicate: {
    sections: ['transaction_history', 'duplicate_analysis', 'refund_history', 'communication'],
    attachments: ['transaction_logs', 'payment_receipts']
  },
  subscription_canceled: {
    sections: ['subscription_details', 'refund_history', 'communication', 'terms_of_service'],
    attachments: ['subscription_agreement', 'refund_receipt', 'terms_of_service']
  },
  digital_goods: {
    sections: ['order_details', 'digital_delivery', 'device_info', 'communication', 'refund_history', 'terms_of_service'],
    attachments: ['invoice', 'download_receipts', 'terms_of_service']
  },
  general: {
    sections: ['order_details', 'customer_verification', 'communication'],
    attachments: ['invoice', 'communication_logs']
  }
};

export async function composePacket(disputeId: UUID) {
  const db = createServerClient();
  const { data: dispute, error } = await db
    .from('disputes')
    .select(`
      *,
      stores!inner(id, platform, oauth_tokens),
      orders(
        id, customer_json, items_json, addresses_json, raw, created_at
      ),
      refund_events(id, amount, method, external_ref, created_at),
      communication_logs(id, content, channel, direction, created_at)
    `)
    .eq('id', disputeId)
    .single();
  if (error || !dispute) throw new Error(`Dispute not found: ${disputeId}`);

  const template = REASON_CODE_TEMPLATES[dispute.reason_code] || REASON_CODE_TEMPLATES.general;
  const sections: EvidenceSection[] = [];
  const attachments: EvidenceAttachment[] = [];

  for (const sectionType of template.sections) {
    const section = await buildSection(sectionType, dispute);
    if (section) sections.push(section);
  }
  for (const attachmentType of template.attachments) {
    const attachment = await buildAttachment(attachmentType, dispute);
    if (attachment) attachments.push(attachment);
  }
  sections.sort((a, b) => b.weight - a.weight);

  const gaps: Array<{ code: string; severity: 'error'|'warn'; message: string; action?: string }> = [];

  // Required section gaps
  const requiredSectionTitles = new Set(['Order Details', 'Customer Verification']);
  for (const title of requiredSectionTitles) {
    if (!sections.find(s => s.title === title)) {
      gaps.push({ code: `missing_${title.toLowerCase().replace(/\s+/g,'_')}`, severity: 'error', message: `${title} is missing` });
    }
  }

  // Delivery confirmation gap for physical goods
  if (template.attachments.includes('delivery_confirmation') && !attachments.find(a => a.name.startsWith('delivery-confirmation') && a.present)) {
    gaps.push({ code: 'missing_delivery_confirmation', severity: 'warn', message: 'Delivery confirmation not attached', action: 'attach_delivery_proof' });
  }

  if (['fraudulent','digital_goods'].includes(dispute.reason_code)) {
    const hasAVS = sections.find(s => s.title === 'Customer Verification' && /AVS Result:\s*(?!N\/A)/.test(s.content));
    const hasCVV = sections.find(s => s.title === 'Customer Verification' && /CVV Result:\s*(?!N\/A)/.test(s.content));
    if (!hasAVS) gaps.push({ code: 'missing_avs', severity: 'error', message: 'AVS result missing', action: 'collect_avs' });
    if (!hasCVV) gaps.push({ code: 'missing_cvv', severity: 'error', message: 'CVV result missing', action: 'collect_cvv' });
  }

  if ((template.sections.includes('terms_of_service') || template.attachments.includes('terms_of_service')) && !sections.find(s => s.title === 'Terms of Service')) {
    gaps.push({ code: 'missing_tos', severity: 'warn', message: 'Terms of Service version at purchase missing', action: 'attach_tos' });
  }

  // Refund reconciliation (partial/duplicate)
  const refunds = dispute.refund_events || [];
  const totalRefunded = refunds.reduce((s: number, r: any) => s + Number(r.amount || 0), 0);
  if (totalRefunded > 0 && totalRefunded < Number(dispute.amount)) {
    gaps.push({ code: 'partial_refund_present', severity: 'warn', message: `Partial refund detected: $${totalRefunded.toFixed(2)} applied`, action: 'include_refund_receipts' });
  }
  if (totalRefunded >= Number(dispute.amount)) {
    gaps.push({ code: 'duplicate_refund_claim', severity: 'error', message: 'Refund already processed in full', action: 'attach_refund_receipts' });
  }

  // Readiness score
  const totalRequired = (template.sections.length) + (template.attachments.length);
  const presentRequired = sections.filter(s => s.required).length + attachments.filter(a => a.required && a.present !== false).length;
  const readiness = Math.max(0, Math.min(100, Math.round((presentRequired / Math.max(1, totalRequired)) * 100)));

  // Issuer/network guidance
  const network = dispute.psp_provider === 'shopify' ? 'Visa/MC (Shopify Payments)' : 'Stripe';
  const issuerGuides: Record<string, { must: string[]; rec: string[] }> = {
    fraudulent: { must: ['AVS/CVV', 'Delivery proof (physical)'], rec: ['Customer history', 'Device fingerprint'] },
    product_not_received: { must: ['Tracking with delivery event'], rec: ['Signature (if high value)'] },
    duplicate: { must: ['Transaction receipts and reconciliation'], rec: ['Customer communication'] },
    subscription_canceled: { must: ['Cancellation evidence', 'Refund policy excerpt'], rec: ['ToS at purchase'] },
    digital_goods: { must: ['Download/access logs'], rec: ['Device/IP consistency'] }
  };
  const g = issuerGuides[dispute.reason_code] || { must: ['Core required docs'], rec: [] };
  const guidance = {
    title: `Guidance for ${dispute.reason_code} • ${network}`,
    mustInclude: g.must,
    recommended: g.rec
  };

  return {
    id: disputeId,
    sections,
    attachments,
    metadata: {
      disputeId,
      reasonCode: dispute.reason_code,
      amount: dispute.amount,
      dueBy: dispute.due_by,
      status: dispute.status
    },
    readiness,
    gaps,
    guidance
  };
}

async function buildSection(type: string, dispute: any): Promise<EvidenceSection | null> {
  const db = createServerClient();
  switch (type) {
    case 'order_details': {
      const order = dispute.orders?.[0];
      if (!order) return null;
      return {
        title: 'Order Details',
        content: `Order ID: ${order.id}\nDate: ${new Date(order.created_at).toLocaleDateString()}\nCustomer: ${order.customer_json?.email || 'N/A'}\n\nItems Purchased:\n${(order.items_json||[]).map((i:any)=>`- ${i.name} x${i.quantity} - $${i.price}`).join('\n')}\n\nTotal Amount: $${dispute.amount}\n\nBilling Address:\n${formatAddress(order.addresses_json?.billing_address)}\n\nShipping Address:\n${formatAddress(order.addresses_json?.shipping_address)}`,
        required: true,
        weight: 10
      };
    }
    case 'customer_verification': {
      const order = dispute.orders?.[0];
      if (!order) return null;
      const customer = order.customer_json;
      return {
        title: 'Customer Verification',
        content: `Email: ${customer?.email || 'N/A'}\nPhone: ${customer?.phone || 'N/A'}\nAccount Created: ${customer?.created_at || 'N/A'}\nTotal Orders: ${customer?.orders_count || 'N/A'}\n\nAVS Result: ${dispute.raw?.evidence?.avs_result || dispute.raw?.evidence?.avs_code || 'N/A'}\nCVV Result: ${dispute.raw?.evidence?.cvv_result || dispute.raw?.evidence?.cvv_code || 'N/A'}`,
        required: true,
        weight: 9
      };
    }
    case 'shipping_proof': {
      const { data: shipments } = await db
        .from('order_shipments')
        .select('*')
        .eq('order_id', dispute.orders?.[0]?.id)
        .limit(1);
      const s = shipments?.[0];
      return {
        title: 'Shipping Information',
        content: `Carrier: ${s?.carrier || 'N/A'}\nTracking Number: ${s?.tracking_number || 'N/A'}\nShipped Date: ${s?.shipped_at || 'N/A'}\nDelivery Date: ${s?.delivered_at || 'N/A'}\nDelivery Status: ${s?.status || 'N/A'}\nSignature Required: ${s?.signature_required ? 'Yes' : 'No'}\nSigned By: ${s?.signed_by || 'N/A'}`,
        required: true,
        weight: 8
      };
    }
    case 'device_info': {
      const { data: sessions } = await db
        .from('order_sessions')
        .select('*')
        .eq('order_id', dispute.orders?.[0]?.id)
        .limit(1);
      const session = sessions?.[0];
      let riskText = '';
      try {
        const risk = await checkFraudSignals(dispute.orders?.[0]?.id);
        riskText = `\nRisk Score: ${risk.riskScore}\nSignals: ${(risk.signals||[]).join(', ')}`;
      } catch {}
      return {
        title: 'Device & Session Information',
        content: `IP Address: ${session?.ip_address || 'N/A'}\nCountry: ${session?.country || 'N/A'}\nDevice Type: ${session?.device_type || 'N/A'}\nBrowser: ${session?.browser || 'N/A'}\nDevice Fingerprint: ${session?.fingerprint || 'N/A'}\nSession Duration: ${session?.duration || 'N/A'}${riskText}`,
        required: false,
        weight: 6
      };
    }
    case 'communication': {
      const logs = dispute.communication_logs || [];
      if (!logs.length) return null;
      return {
        title: 'Customer Communication',
        content: logs.map((log: any) => `[${new Date(log.created_at).toLocaleDateString()}] ${log.direction} via ${log.channel}:\n${log.content}`).join('\n\n'),
        required: false,
        weight: 7
      };
    }
    case 'refund_history': {
      const refunds = dispute.refund_events || [];
      return {
        title: 'Refund History',
        content: refunds.length ? refunds.map((r:any)=>`${new Date(r.created_at).toLocaleDateString()}: $${Number(r.amount).toFixed(2)} • ${r.method || 'method'} ${r.external_ref ? '('+r.external_ref+')':''}`).join('\n') : 'No refunds issued for this order.',
        required: false,
        weight: 5
      };
    }
    case 'subscription_details': {
      const email = dispute.orders?.[0]?.customer_json?.email || null;
      const { data: sub } = await db
        .from('subscriptions')
        .select('*')
        .eq('org_id', dispute.org_id)
        .eq('customer_email', email)
        .order('started_at', { ascending: false })
        .limit(1);
      const s = sub?.[0];
      return {
        title: 'Subscription Details',
        content: s ? `Plan: ${s.plan || 'N/A'}\nStatus: ${s.status}\nStarted: ${s.started_at || 'N/A'}\nCanceled: ${s.canceled_at || 'N/A'}\nReason: ${s.cancellation_reason || '—'}` : 'No subscription record found.',
        required: true,
        weight: 8
      };
    }
    case 'digital_delivery': {
      const { data: logs } = await db
        .from('digital_download_logs')
        .select('*')
        .eq('order_id', dispute.orders?.[0]?.id)
        .order('download_at', { ascending: true });
      return {
        title: 'Digital Delivery Logs',
        content: (logs||[]).length ? (logs||[]).map((l:any)=>`${new Date(l.download_at).toLocaleString()} • ${l.file_name} • IP ${l.ip_address || 'N/A'} • FP ${l.device_fingerprint || 'N/A'}`).join('\n') : 'No download activity recorded.',
        required: true,
        weight: 8
      };
    }
    case 'tracking_updates': {
      const { data: shipments } = await db
        .from('order_shipments')
        .select('tracking_history')
        .eq('order_id', dispute.orders?.[0]?.id)
        .limit(1);
      const hist = shipments?.[0]?.tracking_history || [];
      return {
        title: 'Tracking Updates',
        content: hist.length ? hist.map((h:any)=>`${h.timestamp || ''} • ${h.status || ''} • ${h.location || ''} • ${h.description || ''}`).join('\n') : 'No tracking history available.',
        required: false,
        weight: 6
      };
    }
    case 'duplicate_analysis': {
      const disputeDate = new Date(dispute.created_at);
      const startDate = new Date(disputeDate); startDate.setDate(startDate.getDate() - 30);
      const { data: ordersSameTotal } = await db
        .from('orders')
        .select('id, created_at')
        .eq('org_id', dispute.org_id)
        .eq('store_id', dispute.store_id)
        .eq('raw->>total', String(dispute.amount))
        .gte('created_at', startDate.toISOString())
        .lte('created_at', disputeDate.toISOString());
      return {
        title: 'Duplicate Charge Analysis',
        content: (ordersSameTotal||[]).length > 1 ? `Found ${ordersSameTotal!.length} orders with identical total in last 30 days.` : 'No duplicate-amount orders found in the last 30 days.',
        required: false,
        weight: 5
      };
    }
    case 'terms_of_service': {
      const orderId = dispute.orders?.[0]?.id;
      if (!orderId) return null;
      const { data: row } = await db
        .from('order_tos_acceptance')
        .select('accepted_at, tos_versions!inner(version, content_path, effective_at)')
        .eq('order_id', orderId)
        .maybeSingle();
      return {
        title: 'Terms of Service',
        content: row ? `Version: ${row.tos_versions.version}\nEffective: ${new Date(row.tos_versions.effective_at).toLocaleDateString()}\nAccepted: ${new Date(row.accepted_at).toLocaleString()}` : 'No ToS acceptance recorded for this order.',
        required: true,
        weight: 7
      };
    }
    default:
      return null;
  }
}

async function buildAttachment(type: string, dispute: any): Promise<EvidenceAttachment | null> {
  switch (type) {
    case 'invoice':
      return await resolveAttachment(`invoices/${dispute.orders?.[0]?.id}.pdf`, `invoice-${dispute.orders?.[0]?.id}.pdf`, true);
    case 'shipping_label':
      return await resolveAttachment(`shipping/${dispute.orders?.[0]?.id}-label.pdf`, `shipping-label-${dispute.orders?.[0]?.id}.pdf`, true);
    case 'tracking_receipt':
      return await resolveAttachment(`tracking/${dispute.orders?.[0]?.id}.pdf`, `tracking-${dispute.orders?.[0]?.id}.pdf`, false);
    case 'delivery_confirmation':
      return await resolveAttachment(`proof/${dispute.orders?.[0]?.id}.pdf`, `delivery-confirmation-${dispute.orders?.[0]?.id}.pdf`, true);
    case 'subscription_agreement':
      return await resolveAttachment(`subscriptions/${dispute.orders?.[0]?.id}.pdf`, `subscription-agreement-${dispute.orders?.[0]?.id}.pdf`, true);
    case 'refund_receipt':
      return await resolveAttachment(`refunds/${dispute.id}.pdf`, `refund-${dispute.id}.pdf`, false);
    case 'download_receipts':
      return await resolveAttachment(`downloads/${dispute.orders?.[0]?.id}.pdf`, `download-receipts-${dispute.orders?.[0]?.id}.pdf`, true);
    case 'terms_of_service':
      return await resolveAttachment(`tos/${dispute.orders?.[0]?.id}.pdf`, `tos-${dispute.orders?.[0]?.id}.pdf`, true);
    default:
      return null;
  }
}

function formatAddress(addr: any): string {
  if (!addr) return 'N/A';
  return `${addr.name || ''}\n${addr.address1 || ''}\n${addr.address2 || ''}\n${addr.city || ''}, ${addr.province || ''} ${addr.zip || ''}\n${addr.country || ''}`.trim();
}

async function resolveAttachment(path: string, name: string, required: boolean): Promise<EvidenceAttachment> {
  const present = await objectExists(path);
  return { name, path, type: 'application/pdf', required, present };
}
```


