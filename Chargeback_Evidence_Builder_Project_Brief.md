# Chargeback Evidence Builder — Project Brief

## Summary
- Purpose: Increase chargeback win rates by auto-assembling bank-ready evidence and submitting via Shopify/Stripe.
- Killer feature: 1-click Shopify/Stripe connect, verticalized templates (e.g., supplements, fashion), and measurable win-rate uplift dashboard.

## Problem
- Merchants lose revenue to chargebacks and spend hours assembling inconsistent evidence. Built-ins are basic; managed services take a painful rev-share.

## Solution
- Pull orders, delivery proof, and session/device data; generate network-specific evidence packets; submit via PSP APIs; track outcomes and win-rate uplift.

## Target Users
- DTC brands on Shopify/Stripe; ops teams handling 5–100 disputes/month.

## Goals/KPIs (first 90 days)
- +10% absolute win-rate uplift vs. baseline.
- <10 minutes from connect to first auto-submission.
- 80% disputes auto-drafted without manual edits.

## Scope (MVP)
- Shopify app + Stripe OAuth connection.
- Dispute inbox, evidence generator, PDF assembly, API submission.
- Outcome tracking and basic analytics by reason code/vertical.

## Out of Scope (MVP)
- Deep fraud scoring; network appeals automation (phase 2).

## Suggested Stack & Integrations
- Web: Next.js 14 + TypeScript; UI: Tailwind.
- Backend: Supabase (Postgres + RLS, Auth, Storage, Edge Functions/workers).
- PSPs: Shopify Admin API, Stripe Disputes/Webhooks.
- Billing: Shopify App Billing (Shopify), Stripe Billing (non-Shopify).

## Security & Privacy
- Store-scoped tokens; signed URLs for artifacts; role-based access; audit logs.

## Risks & Mitigations
- Proving uplift → benchmark mode + A/B holdout; transparent reports.
- PSP/network changes → abstraction layer and versioned templates.

## Timeline (team of 3)
- Week 1–2: OAuth/connectors, dispute ingest, evidence templates.
- Week 3: Submission pipeline, outcomes, basic analytics.
- Week 4: Shopify listing prep, agency pilot (3 partners).

---

## Account Integration Details

### Shopify Connection
- Flow:
  - Merchant installs app from Shopify App Store → OAuth redirect to our app → exchange code for access token scoped to the store.
  - We store store-scoped token (encrypted) linked to org.
- Minimum scopes (principle of least privilege; final list validated during app review):
  - Orders (read), Customers (read), Fulfillments/Shipping (read), Disputes/Payments (read/submit where supported), Shop (read_basic).
- Webhooks we subscribe to:
  - Orders updated/fulfilled (to attach delivery proof), Disputes/Chargebacks created/updated (Shopify Payments), App uninstalled (revoke token), GDPR webhooks (customers/data requests/deletions).
- Billing:
  - Shopify App Billing for merchants connected via Shopify (recurring + usage if needed). Cancel on app uninstall.

### Stripe Connection
- Flow:
  - Merchant clicks "Connect Stripe" → Stripe OAuth (Connect) → we receive account-scoped access token for Disputes API and read-only resources.
  - Alternative: API keys entered manually (not preferred). OAuth strongly recommended.
- Events/Webhooks we handle:
  - `charge.dispute.created`, `charge.dispute.closed`, `balance.transaction.updated` (as applicable), idempotent processing with signing secret verification.
- Permissions:
  - Read disputes/charges/refunds/checkout sessions; submit evidence for disputes on behalf of the connected account.

### Data Ingestion Summary
- Orders/line items, timestamps, AVS/CVV (if available), customer contact/shipping address.
- Shipment tracking (carrier, delivered_at, proof URL/images when available).
- Optional session/device metadata (from store scripts or existing tools) if merchant opts in.

---

## GDPR & Data Protection Plan
- Roles:
  - Merchant = Data Controller; Our app = Data Processor.
- Lawful basis:
  - Performance of contract with the merchant; legitimate interest in fraud/chargeback prevention and evidence preparation.
- Data minimization:
  - Ingest only fields required for dispute evidence; no card PAN; no sensitive categories beyond what the merchant already processes.
- Data residency:
  - Supabase project provisioned in EU region for EU merchants; US region for others. Configure per-org at onboarding.
- International transfers:
  - Standard Contractual Clauses (SCCs) with US subprocessors (e.g., Stripe, Shopify if applicable). Maintain subprocessor list.
- Retention:
  - Default: retain dispute-related artifacts until case closure + 180 days (configurable per org); automatic purge thereafter.
- Data Subject Rights (DSAR):
  - Admin UI export tool for per-customer evidence data (search by email/order). Deletion requests cascade artifacts unless required for legal defense.
- DPA & Policies:
  - Provide Data Processing Addendum; list of subprocessors; incident response policy; breach notification within statutory timelines.
- Security:
  - RLS row-level isolation; encryption at rest; signed URLs with short TTL; webhook signature verification; audit logs for access and submissions.
- Shopify GDPR webhooks:
  - Implement required endpoints for customer data erasure/access and shop redaction. Honor within timelines; log all actions.
  
Why isnt this build yet? 
  Versions exist, but the “last mile” is hard and misaligned with how incumbents make money. That leaves gaps a small, vertical team can fill.
Vendor compliance tracker
Why incumbents haven’t won: Enterprise-first (myCOI/TrustLayer) are heavy/expensive; SMB PMs/GCs avoid change. Parsing COIs reliably is messy; nobody wants liability for a wrong “approved.” Broker coordination is operational, not just software.
What changed: Better doc tooling, email-native SMB workflows are acceptable, and “invoice gating” plus broker-handoff is a clear ROI wedge that enterprises don’t prioritize for SMBs.
Chargeback evidence builder (Shopify/Stripe-first)
Why incumbents haven’t won: Rev-share vendors (Chargeflow/Justt) favor their pricing over merchant transparency; maintaining network-specific evidence rules is unglamorous; proving uplift requires data breadth and holdouts. Built-ins are “good enough” for low-volume stores.
What changed: Easier PSP/app integrations, agencies want fixed-fee, white-label options, and merchants are pushing back on rev-share. A verticalized, transparent tool can carve share if it shows +win-rate clearly.
Missed-call text-back + AI triage (HVAC)
Why incumbents haven’t won: Generic voice/SMS tools (CallRail/CallFire/Podium) stop at replies; vertical scripts, A2P compliance, calendar booking, and bilingual flows are services-heavy. SMBs resist DIY setup; margins on “DFY onboarding” don’t scale for big players.
What changed: A2P 10DLC is standardized, calendar APIs are trivial, and DFY + outcome-based pricing works at small scale per niche (HVAC, plumbing).
Net: These aren’t “not built”; they’re not packaged for SMBs with the right wedge (vertical scripts, DFY onboarding, transparent pricing, accountable outcomes). That’s the opening.

Why this could fail: 
Data access gaps: Stores can’t/won’t grant scopes (AVS/CVV, session data, carrier proof), weakening evidence quality.
Uplift hard to prove: Small dispute volumes and noisy cohorts make +win-rate claims statistically weak.
Policy whiplash: Shopify/Stripe/network evidence rules change; templates go stale and lose effectiveness.
“Good enough” incumbents: Built-ins + rev-share vendors (Chargeflow/Justt) bundle aggressively, undercuting fixed-fee value.
Merchant fit: Many merchants have too few disputes to justify another app; ARPU too low for support burden.
Integration fragility: Webhooks fail, rate limits hit, or app gets delisted during review; trust evaporates.
Evidence sources missing: No delivery confirmation/photos for digital goods or international carriers; packets look thin.
Compliance drag: GDPR/DSAR and DPA demands from agencies slow sales and create ongoing ops load.
Agency channel churn: Agencies want white-label + SLAs; high support expectations crush margins.
Appeals phase gap: If you don’t handle representment/second cycle, merchants blame you for losses anyway.

## Ideal Customer Profile (ICP) for Pilot
- Shopify brands handling ~10–100 disputes/month (supplements, fashion, electronics).
- Teams with ops capacity to connect Shopify/Stripe and provide delivery/source data.
- Agencies managing multiple Shopify brands (white-label friendly).

## Pilot KPIs & Kill Gates (4–6 weeks)
- Targets:
  - +10% absolute win-rate uplift vs baseline (with holdout cohort).
  - <10 minutes from connect → first auto-draft submission.
  - ≥70% disputes receive “strong packet” (order + delivery + policy + device/session where available).
  - 80% auto-drafts require ≤2 edits before submit.
- Kill/adjust if:
  - Uplift <5% after 6 weeks with sufficient volume.
  - App review/integration issues block merchant installs.
  - Merchants consistently lack delivery/session data and won’t add it.

## Scope Constraints (Pilot)
- First-cycle representment only (no appeals/second cycle initially).
- Shopify/Stripe first; carriers (UPS/USPS) and session script are optional add-ons.
- Evidence templates for top reason codes; weekly template updates.

## Pricing & Channel (Pilot)
- Pricing: fixed + light usage (avoid heavy rev-share). Agency white-label available.
- Channel: 3–5 Shopify agencies (portfolio entry) + 10–15 brands with clear chargeback pain.

## Risk Mitigations (Operational)
- Data gaps: optional client script for device/session; carrier lookup fallback; per-vertical checklists.
- Proof: benchmark mode + store-level holdout; reason-code analytics.
- Fragility: idempotent webhooks, retry queues, health checks; versioned templates.
- GDPR/Compliance: EU residency toggle, 180-day retention, DSAR tools, DPA/subprocessors published.