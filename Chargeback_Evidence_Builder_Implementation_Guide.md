# Chargeback Evidence Builder — Implementation Guide (Unbundling → First Run)

## 1) Prerequisites
- Node.js 18+ and npm
- Supabase account and a new project (Org → New Project)
- Optional now: Stripe account (test mode) and Shopify Partner account
- Optional: Supabase CLI installed (`npm i -g supabase`)

## 2) Unbundle the App
1. Run your unbundling script against `docs/chargeback-evidence-app.md` to materialize the tree into a local folder, e.g. `chargeback-evidence-app/`.
2. Open the project folder in your editor.

## 3) Supabase Project Setup
1. Create a Supabase project.
2. Copy these values from Project Settings → API:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY` (server-side only)
3. Apply SQL migrations (in order):
   - Chargebacks (domain):
     - `supabase/migrations/chargebacks/0001_init.sql`
     - `supabase/migrations/chargebacks/0002_rls_policies.sql`
     - `supabase/migrations/chargebacks/0003_flags_geo.sql`
     - `supabase/migrations/chargebacks/0004_test_helpers.sql`
     - `supabase/migrations/chargebacks/0005_idempotency_audit.sql`
     - `supabase/migrations/chargebacks/0006_order_tracking.sql`
     - `supabase/migrations/chargebacks/0007_rls_write_policies.sql`
     - `supabase/migrations/chargebacks/0010_seed_demo.sql` (optional demo data)
   - Core (shared):
     - `supabase/migrations/core/0001_billing_entitlements.sql`
     - `supabase/migrations/core/0002_storage_buckets_policies.sql`

Options to apply:
- Using SQL editor: paste each file content and run in the order above.
- Using Supabase CLI (from the project root):
  - `supabase db execute --file <path-to-sql>`

4. Storage buckets (private):
   - Create buckets `evidence-packets` and `attachments`.
   - Access pattern: read via signed URLs only (no public read).

## 4) Environment Configuration
1. In the app root, copy `.env.example` to `.env.local`.
2. Fill values:
   - `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`
   - `EVIDENCE_BUCKET=evidence-packets`
   - Stripe (single account): `STRIPE_API_KEY`, `STRIPE_WEBHOOK_SECRET`. Optional: `STRIPE_PRICE_STARTER`, `STRIPE_PRICE_PRO`
   - Shopify: `SHOPIFY_APP_KEY`, `SHOPIFY_APP_SECRET`, `SHOPIFY_SCOPES`, `SHOPIFY_WEBHOOK_SECRET`
3. Save.

## 5) Install and Run
```bash
cd chargeback-evidence-app
npm install
npm run dev
# visit http://localhost:3000
```

Notes:
- The app will boot and render basic pages (Inbox/Detail) with placeholders.
- API routes are stubs; DB-backed logic requires your Supabase env + migrations applied.

## 6) Edge Functions
- Provided: `supabase/functions/generate-pdf`, `supabase/functions/send-notification`.
- Deploy with Supabase CLI:
```bash
supabase functions deploy generate-pdf
supabase functions deploy send-notification
```
- Ensure `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are available to functions.

## 7) Provider Setup (Stripe & Shopify)
Stripe
- Set `STRIPE_API_KEY`, `STRIPE_WEBHOOK_SECRET` in `.env.local`.
- Local dev (Stripe CLI):
```bash
stripe login
stripe listen --events charge.dispute.created,charge.dispute.updated,charge.dispute.closed \
  --forward-to http://localhost:3000/api/webhooks/stripe
```
- Dashboard: add a webhook endpoint to `https://<your-host>/api/webhooks/stripe` with the same events.
- Optional billing: set price IDs in env and use `/api/billing/checkout`.

Shopify
- Set `SHOPIFY_APP_KEY`, `SHOPIFY_APP_SECRET`, `SHOPIFY_SCOPES`, `SHOPIFY_WEBHOOK_SECRET`.
- In Shopify Partners, create a public app with redirect URL:
  `https://<your-host>/api/shopify/oauth/callback`
- Webhooks: Orders Create/Update and Disputes Create → `https://<your-host>/api/webhooks/shopify`.
- After OAuth via `/api/shopify/oauth/start?shop=<shop-domain>`, link the store to an org:
  - API (recommended): send POST to `/api/stores/attach` with `{ shop: '<shop-domain>' }` from the onboarding flow. The route will attach the store to the current user's org.
  - Or manual SQL (fallback):
    ```sql
    update stores set org_id = '<ORG_UUID>' where id = '<STORE_UUID>';
    ```

- To reduce manual setup, webhooks are auto-registered during OAuth, and a best-effort backfill is triggered via `POST /api/shopify/backfill`.

## 8) Testing
Playwright E2E (optional now)
```bash
npm i -D @playwright/test
npx playwright install
npx playwright test
```
- The provided example verifies the Disputes page renders. As features land, extend critical paths under `src/tests/e2e`.

## 9) Common Issues
- 401/403 on DB calls:
  - Ensure migrations are applied and keys are correct.
  - Use `createServerClient` (service role) only on the server.
- Storage access denied:
  - Ensure the `evidence-packets` bucket exists and you’re using signed URLs for download.
- Webhook 400/verification failures:
  - Confirm secrets, raw body handling, and provider configuration.

## 10) What Works Now vs Later
Works now
- App boots; pages render; DB schema + RLS applied; evidence compose and PDF (with function deployed) work.
- Webhook endpoints exist; ingestion scaffolding for Stripe/Shopify is in place.

To be implemented next
- Automate store↔org link post-OAuth (or keep manual SQL).
- Stripe Connect (multi-merchant) if needed.
- Upload flow for attachments (signed URLs) and UI.
- Billing portal and entitlement checks in routes.
- E2E tests for draft→submit→webhook→outcome.

## 11) Minimal Validation Checklist
- [ ] Migrations applied without errors (chargebacks/* then core/*)
- [ ] Buckets `evidence-packets` and `attachments` created (private)
- [ ] Edge functions deployed: `generate-pdf`, `send-notification`
- [ ] `.env.local` filled and app boots on `localhost:3000`
- [ ] Stripe CLI webhook forwards reach `/api/webhooks/stripe`
- [ ] Shopify OAuth works; store linked to an org

