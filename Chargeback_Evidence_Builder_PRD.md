# Chargeback Evidence Builder — PRD (v1)

## 1. Problem
Merchants lose revenue to chargebacks, spending hours assembling inconsistent evidence. Built‑ins are basic; managed recovery often demands high rev‑share.

## 2. Solution
Connect store and PSP, ingest disputes, auto‑assemble bank‑ready evidence from orders, shipment and session/device data, submit via APIs, and track outcomes with win‑rate analytics.

- Additions (v1.1):
  - Issuer/network‑specific briefs, with explicit mapping to reason codes.
  - Partial‑ and duplicate‑refund detection with supporting receipts/ARNs included in packets.
  - Optional pre‑dispute alert integrations to deflect (auto‑refund thresholds) before chargeback.
  - Transparent “What we submit” packet preview and immutable archive for every submission.

## 3. Users & Roles
- Merchant Owner/Admin: billing, configuration
- Ops/Support Agent: reviews evidence drafts, submits/edits
- Agency Partner Admin (optional): manages multiple stores (white‑label)

## 4. Web Stack
- Frontend: Next.js 14 + TypeScript + Tailwind
- Backend: Supabase (Auth, Postgres + RLS, Storage, Edge Functions/workers)
- Integrations: Shopify Admin API, Stripe Disputes/Webhooks; carriers (UPS/USPS) optional; pre‑dispute alert providers (optional)
- Billing: Shopify App Billing (if Shopify), Stripe Billing (non‑Shopify)

## 5. Auth & User Management
- Supabase Auth for app sign‑in; Shopify OAuth for store connection; Stripe OAuth for PSP.
- Role table per org; RLS on disputes by org.

## 6. Data Model (core)
- `orgs`, `users`, `user_org_roles`
- `stores(id, org_id, platform, oauth_tokens, status)`
- `disputes(id, org_id, store_id, psp_id, reason_code, amount, due_by, status)`
- `orders(id, org_id, store_id, customer_json, items_json, addresses_json)`
- `evidence_items(id, dispute_id, type, content_path|json)`
- `submissions(id, dispute_id, submitted_at, method, status, receipt)`
- `analytics_winrates(id, org_id, period, reason_code, win_rate)`
- `audit_events(...)`
- `refund_events(id, dispute_id, amount, created_at, method, external_ref)`
- `alerts(id, org_id, store_id, provider, external_id, received_at, status, decision)`
- `submission_packets(id, submission_id, sha256, storage_path)`

## 7. Payments
- Shopify App Billing (recurring + usage tiers) when installed via Shopify.
- Stripe Billing otherwise (monthly plan + per‑dispute add‑on).

## 8. Screen-by-Screen UX

### 8.1 Onboarding Flow (3 steps max)

#### Screen 1: Welcome & Organization Setup
**What user sees:**
- Clean hero section: "Stop losing chargebacks. Start winning disputes."
- Subheading: "Connect your store and payment processor in 2 minutes"
- Single input field: "Organization Name" (pre-filled if coming from Shopify)
- Primary button: "Get Started" (large, centered)
- Trust badges: "256-bit encryption" | "SOC2 compliant" | "No credit card required"

**User expects:** Quick start without complex forms
**User actions:** Enter org name → Click "Get Started"

#### Screen 2: Connect Your Platforms
**What user sees:**
- Progress indicator: Step 2 of 3
- Two connection cards side-by-side:
  
  **Store Connection Card:**
  - Shopify logo
  - "Connect your Shopify store"
  - Subtext: "Import orders, customers, and fulfillment data"
  - Button: "Connect Shopify" (OAuth flow)
  - Status: ✓ Connected (green) once complete
  
  **Payment Processor Card:**
  - Stripe logo (expandable to show PayPal, Square later)
  - "Connect your payment processor"
  - Subtext: "Sync disputes and submit evidence automatically"
  - Button: "Connect Stripe"
  - Status: ✓ Connected (green) once complete

- Skip link: "I'll connect later" (bottom right, de-emphasized)
- Continue button: Disabled until at least one connection made

**User expects:** Standard OAuth flows they're familiar with
**User actions:** Click connection buttons → Authorize in popup → Return to see green checkmarks

#### Screen 3: Quick Setup Complete
**What user sees:**
- Success animation (checkmark)
- "You're all set! We found X open disputes."
- Three info cards:
  - "📊 Current win rate: X%" (or "No dispute history yet")
  - "⏰ Next dispute due: [date]" (or "No open disputes")
  - "💰 Potential recovery: $X"
- Primary button: "View Disputes Dashboard"
- Secondary link: "Take a quick tour" (3-step interactive overlay)

**User expects:** Immediate value/insights
**User actions:** Click to dashboard or tour

### 8.2 Disputes Dashboard (Home Screen)

**What user sees above the fold:**
- Header bar:
  - Logo/Org name (left) with org switcher dropdown for agencies
  - Global search: "Search by order #, customer, amount..."
  - Notification bell (badge if new)
  - User menu (avatar → dropdown)

- Alert banner (when applicable):
  - Red background: "⚠️ Overdue: 2 disputes • $1,240 at risk" 
  - Button: "Review oldest first"

- Key metrics cards (horizontal row):
  - **Open Disputes:** Large number, red badge if any overdue
  - **Win Rate:** Percentage with trend arrow
  - **Revenue Recovered:** Dollar amount (last 30 days)
  - **Time to Submit:** Average hours saved

- Prioritization chips (above table):
  - "Due today (3)" - red
  - "High value (5)" - orange  
  - "Auto-ready (8)" - green
  - "Needs attention (4)" - yellow
  - Click chip to filter table

- Action toolbar:
  - Primary button: "Generate Evidence" (bulk action, disabled until selection)
  - Filter dropdown: "All Disputes" (default)
  - Date range picker: "Last 30 days"
  - View toggle: Table / Cards

**Main disputes table:**
- Columns: 
  - Checkbox (for bulk actions)
  - Status indicator (color-coded dot)
  - Dispute ID (clickable)
  - Customer Name
  - Reason (simplified, hover for code)
  - Amount
  - Due Date (red if < 3 days)
  - **Readiness:** Visual indicator (0% = Missing docs, 50% = Needs review, 100% = Ready)
  - Progress (visual bar: 0% = New, 50% = Draft ready, 100% = Submitted)
  - Action: "Review" button (or "Fix" if readiness < 100%)

- Row click behavior: Opens quick-view panel on right side
- Row hover: Highlights entire row, shows quick actions
- Sorting: Clickable headers (default: Due date ascending, then amount descending)
- Pagination: "Showing 1-20 of X" with page numbers

**Quick-view panel (slides in from right):**
- Header: Dispute ID, amount, X to close
- Readiness summary:
  - ✅ Evidence generated
  - ⚠️ Missing delivery proof
  - ✅ Customer history included
- Key facts: Order date, customer, reason
- Action buttons:
  - "Open Full Details" 
  - "Generate & Submit" (if 100% ready)
- Mini timeline of events

**Empty state:**
- Illustration of shield with checkmark
- "No open disputes - you're all caught up!"
- "Your next dispute will appear here automatically"
- Buttons: 
  - "View Past Disputes" (primary)
  - "Explore with Sample Data" (secondary, purple)

**Sample mode banner (when active):**
- Purple background: "🎓 Sample Mode - Exploring with test data"
- "Exit Sample Mode" button

**User expects:** 
- See urgent items first
- Quick understanding of what needs attention
- Fast triage without opening each dispute
- One-click access to dispute details

**User actions:**
- Click dispute row → Quick-view panel
- Click prioritization chip → Filter table
- Select multiple → "Generate Evidence" for bulk processing
- Click "Fix" → Jump to specific issue in detail view

### 8.3 Dispute Detail Screen

**What user sees:**

**Sticky header section (always visible):**
- Back arrow: "← Back to disputes"
- Dispute title: "Dispute #CHB-2024-001"
- Status pill: "Draft Ready" (yellow)
- Key info bar:
  - Reason: "Fraudulent Transaction" 
  - Amount: "$127.43"
  - Due: "3 days left" (countdown timer if < 72 hours)
  - Customer: "John Smith"

**Readiness bar (below header):**
- Progress: "2 of 3 steps complete" with visual progress bar
- Current step highlighted: "Step 2: Review Evidence"
- Steps: ✅ Generate → 🔄 Review → ⏸️ Submit

**Action buttons (sticky in header, right):**
- Secondary: "Download Evidence"  
- Primary: "Submit to Stripe" (green when ready, gray if gaps exist)

**Reason-code guidance banner:**
- Yellow background: "📋 Visa Code 10.4 Requirements"
- "Must include: ✓ Delivery proof ✓ AVS/CVV match ⚠️ Customer communication"
- Link: "View full requirements" (expands inline)

**Tab navigation with completion indicators:**
```
[Evidence Draft ✓] [Order Details ✓] [Customer History ✓] [Shipping ⚠️] [Device & Session ✓] [Timeline]
```

#### Evidence Draft Tab (Default)
**Gaps detector panel (if issues exist):**
- Red banner: "2 gaps found - Fix these to improve win rate"
- Gap cards:
  - "⚠️ Missing delivery signature for high-value order"
    - Button: "Upload proof" or "Request from carrier"
  - "⚠️ Terms of Service not timestamped"
    - Button: "Attach dated version"

**Auto-generated evidence section:**
- Blue info box: "✨ Evidence auto-generated 2 minutes ago • E-commerce template v2.1"
- Narrative sections (each with header):
  
  **Transaction Overview** (🔒 locked)
  - Pre-filled text with inline citations: "The customer placed order #1234 on May 1, 2024 [1]"
  - Hover [1] to highlight linked Order Invoice
  - Section menu (⋮): "Regenerate this section" | "Unlock"
  
  **Customer Verification**
  - "AVS and CVV matched successfully [2]. The billing address..."
  - Character count per section: "245/500"
  
  **Fulfillment & Delivery**
  - "Package delivered on May 3, 2024 at 2:47 PM [3]"
  - If gap exists: Highlighted yellow with "Add delivery proof to strengthen"

  **Total narrative:** "1,847 / 4,000 characters recommended"

**Supporting documents with citations:**
- Grid of attachment cards showing citation numbers:
  - [1] Order Invoice (PDF preview)
  - [2] Payment Verification (Auto-attached)
  - [3] Proof of Delivery (Image) - ⚠️ if missing
  - [4] Terms of Service (PDF, dated)
  - [5] Customer History Report
  - + Add Document (dashed border)

**Quick actions bar:**
- "🔄 Regenerate All" (dropdown: "Regenerate Section")
- "📎 Attach File" 
- "👁️ Preview Packet" (shows compiled evidence)
- "🔗 Copy Share Link"

**Section regeneration (when clicking ⋮ menu):**
- Mini modal: "Regenerating Customer Verification section..."
- Shows diff view: removed text in red, new text in green
- Buttons: "Accept Changes" | "Undo" | "Edit Manually"

#### Order Details Tab
**What user sees:**
- Order summary card:
  - Order #, Date, Total
  - Payment method (last 4 digits)
  - Billing/Shipping addresses (with match indicator)
  - IP address & location
  - AVS/CVV response codes (with explanations on hover)

- Line items table:
  - Product, SKU, Quantity, Price
  - Digital/Physical indicator
  - Fulfillment status per item

- Transaction timeline:
  - Order placed → Payment captured → Fulfilled → Delivered
  - Each with timestamp and details

#### Customer History Tab  
**What user sees:**
- Customer profile card:
  - Name, email, phone
  - Account age: "Customer since [date]"
  - Lifetime value: "$X across Y orders"
  - Previous disputes: "None" (or list)

- Order history table:
  - Past successful orders (proves legitimate history)
  - No disputes indicator: "✅ 12 orders, 0 disputes"

#### Shipping Tab
**What user sees:**
- Shipment tracking card:
  - Carrier logo & tracking number (clickable)
  - Visual progress bar of delivery
  - Key events: Shipped → In Transit → Out for Delivery → Delivered
  - Delivery confirmation: Signature/Photo if available
  - Download proof button

- Delivery address verification:
  - ✅ "Shipping address matches billing address"
  - Map preview (if available)

#### Device & Session Tab
**What user sees:**
- Session details card:
  - Device type, OS, Browser
  - IP address & geolocation
  - Session duration
  - Pages viewed before purchase

- Risk signals:
  - ✅ "IP location matches billing address"
  - ✅ "No VPN/Proxy detected"  
  - ✅ "Device previously used for successful orders"

#### Timeline Tab
**What user sees:**
- Vertical timeline of all events:
  - Order placed
  - Payment processed
  - Order fulfilled
  - Shipment events
  - Delivery confirmed
  - Dispute received
  - Evidence generated
  - Each with timestamp, description, and relevant data

**User expects:**
- Everything needed in one place
- Confidence that evidence is complete
- Clear next steps

**User actions:**
- Review/edit evidence narrative
- Add additional documents if needed
- Click "Submit to Stripe" when ready

### 8.4 Evidence Submission Flow

#### Pre-submission Validation
**What happens when clicking "Submit" (before modal):**
- Quick validation spinner: "Checking submission readiness..."
- If issues found, inline alert appears:
  - "⚠️ 2 issues must be fixed before submitting"
  - Issue list with jump links:
    - "Missing required delivery proof" → [Go to Shipping tab]
    - "Narrative missing customer verification section" → [Go to Evidence]
  - Submit button remains disabled

#### Pre-submission Modal (opens only when validation passes)
**What user sees:**
- Modal title: "Final Review Before Submitting"
- Green banner: "✅ All requirements met for Visa Code 10.4"

- Validation summary:
  - "✅ Evidence narrative complete (1,847 chars)"
  - "✅ All required documents attached (6 total)"
  - "✅ Delivery confirmation included with signature"
  - "✅ Customer history shows 12 successful orders"
  - "✅ AVS/CVV verification documented"

- Evidence packet preview:
  - "📄 Your submission packet (2.3 MB)"
  - Expandable sections showing narrative preview
  - Document thumbnails in order of attachment
  - "🔒 SHA-256: abc123..." (will be permanently archived)

- Submission options:
  - (•) Submit via Stripe API (recommended)
    - "Automatic submission in 1 click"
  - ( ) Schedule submission
    - Time picker: "Submit at: [dropdown]"
    - "Auto-submit 1 hour before deadline if not already sent"
  - ( ) Download packet only
    - "Manual submission required"

- Final confirmation:
  - Checkbox: "I've reviewed the evidence and it's ready to submit"
  - Buttons:
    - "Back to Edit" (left)
    - "Submit Evidence" (right, primary, disabled until checkbox)

#### Submission Progress Screen
**What user sees during submission:**
- Progress indicator with steps:
  - ✅ Compiling evidence packet
  - 🔄 Generating PDF (animated)
  - ⏸️ Submitting to Stripe
  - ⏸️ Confirming submission
- "This usually takes 10-15 seconds..."
- Cancel button (warns about interruption)

#### Post-submission Success Screen
**What user sees:**
- Success animation (checkmark)
- "Evidence Submitted Successfully!"
- 
- Submission confirmation card:
  - Submission ID: #SUB-2024-001
  - Submitted to: Stripe (via API)
  - Time: Just now (May 15, 2024 2:47 PM)
  - Method: Automated API submission
  - Expected response: Within 7-10 days
  
- Evidence archive card:
  - "📦 Permanent Evidence Archive"
  - SHA-256: abc123def456...
  - Size: 2.3 MB (6 documents)
  - Buttons: "Download Archive" | "View in Browser"

- What happens next:
  - "✉️ Stripe will review your evidence"
  - "📱 We'll notify you when they respond"
  - "📊 Track outcome in your analytics"

- Actions:
  - "Back to Dashboard" (primary)
  - "Submit Another Dispute" (secondary)
  - "Share Submission" (link icon)

### 8.5 Analytics & Insights Screen

**What user sees:**
- Page title: "Dispute Analytics"
- Date range picker: Last 30 days (default)

**Key metrics dashboard:**
- Large metric cards:
  - Win Rate: 68% (↑ 5% from last period)
  - Revenue Recovered: $12,847
  - Disputes Handled: 47
  - Avg. Time to Submit: 8 minutes (↓ from 2 hours manual)

**Win rate by reason code (bar chart):**
- Fraudulent: 72% win rate (25 disputes)
- Product Not Received: 81% (12 disputes)  
- Not as Described: 54% (10 disputes)
- Duplicate Processing: 90% (5 disputes)

**Trends over time (line graph):**
- Win rate trend line
- Dispute volume line
- Toggle: Weekly/Monthly view

**Dispute outcomes table:**
- Columns: Dispute ID, Reason, Amount, Submitted, Outcome, Days to Decision
- Filters: Won/Lost/Pending
- Export button: "Download CSV"

**User expects:**
- Clear ROI demonstration
- Actionable insights
- Easy reporting for stakeholders

### 8.6 Settings Screen

**What user sees:**
- Settings navigation sidebar:
  - General
  - Evidence Templates
  - Integrations
  - Notifications
  - Billing
  - Team Members
  - Advanced

#### General Settings
- Organization name (editable)
- Time zone selector
- Default currency

#### Evidence Templates
**Template selector:**
- Dropdown: "Active template: E-commerce Standard"
- Template cards:
  - E-commerce Standard (selected)
  - Digital Products
  - Subscription Services
  - Custom Template (+)

- Template editor:
  - Section toggles:
    - ☑ Include customer history
    - ☑ Include device fingerprinting
    - ☑ Include delivery confirmation
    - ☐ Include social proof
  - Narrative tone: Professional (slider)

#### Integrations
**Connected services:**
- Shopify: ✅ Connected (Disconnect link)
- Stripe: ✅ Connected (Disconnect link)  
- Add integration: PayPal, Square, etc.

**Optional integrations:**
- Shipping carriers (FedEx, UPS, USPS)
- Pre-dispute alerts (Ethoca, Verifi)
- Help desk (Zendesk, Intercom)

#### Notifications
**Notification preferences:**
- New dispute received: ☑ Email ☑ In-app
- Dispute due soon: ☑ Email ☑ In-app ☑ SMS
- Outcome received: ☑ Email ☑ In-app
- Weekly summary: ☑ Email

**Webhook configuration:**
- Slack webhook URL: [input field]
- Test webhook button

#### Billing
**Current plan card:**
- Plan: Professional ($99/month)
- Disputes included: 50/month
- Additional disputes: $2 each
- Current usage: 32/50 disputes
- Next billing: June 1, 2024
- Button: "Upgrade Plan"

### 8.7 Quick Actions & Shortcuts

**Global quick actions (accessible everywhere):**
- Keyboard shortcuts:
  - Cmd/Ctrl + K: Global search
  - Cmd/Ctrl + N: New manual dispute
  - Cmd/Ctrl + /: Keyboard shortcuts help

**Bulk operations:**
- Select all checkbox in header
- Bulk actions menu appears:
  - Generate evidence for selected
  - Export selected
  - Mark as priority

**Smart notifications:**
- In-app toast notifications:
  - "New dispute received for Order #1234"
  - "Dispute #CHB-001 due in 24 hours"
  - "You won dispute #CHB-999! $127 recovered"

**User expects:**
- Efficient workflows
- Timely alerts
- Keyboard-friendly interface for power users

## 9. Evidence Generation
- Narrative composer fills required sections per network guidelines.
- Attachments auto‑selected: receipt, ToS at purchase time, delivery confirmation, device fingerprint summary.
- Manual edits preserved on regenerate (field‑level lock).
- Partial/duplicate refund handling: auto‑detect prior refunds, include proof (refund receipts/ARNs) and reconcile against claimed amount.
- Issuer‑specific briefs: adjust structure/sections and evidence emphasis per reason code and network guidance.

## 10. Emails/Notifications
- New dispute digest; approaching deadline alerts (T‑7/T‑3/T‑1).
- Decision received; win/loss summary weekly.
- Pre‑dispute alert received; auto‑refund actioned/not‑actioned notifications.

## 11. Non-Functional
- Reliability: idempotent webhooks; background jobs for PDF build.
- Security: secrets vaulted; RLS; signed URLs for artifacts.
- Performance: P95 page < 1.5s; evidence build < 10s typical.
- Transparency: every submission packet stored with immutable hash; full audit trail of generated narratives and attachments.

## 12. Out of Scope (v1)
- Network appeals automation; chargeback representment beyond first cycle.

## 13. Rollout
- Pilot with 10 stores via 3 Shopify agencies; success = +10% absolute win‑rate uplift; NPS ≥ 40.
- Provide agency white‑label kit (branding, multi‑store management) and sample win‑packet templates for co‑selling.

## 14. Optional Pre‑Dispute Alerts (v1.1)
- Support ingesting alert events from selected providers.
- Rules: auto‑refund under configurable thresholds and/or high loss‑probability reason codes.
- Dashboard: alert inbox with disposition (refund/contest) and downstream dispute linkage for tracking.

## 15. Future Enhancements (Post-v1)

### 15.1 Enhanced Empty States with Sample Data
- Toggle to populate realistic sample disputes for training/exploration
- Purple badges to distinguish sample from real data
- Interactive tutorials using sample disputes

### 15.2 Digital Product Optimizations
- Automatic template switching based on product type
- Digital delivery confirmation (license keys, download logs)
- IP/session matching for digital goods

### 15.3 Advanced Submission Features
- Submission scheduling with SLA guardrails
- Batch submission workflows
- Auto-submit rules based on readiness score

### 15.4 Analytics Intelligence
- "What to improve" recommendations based on loss patterns
- A/B testing of evidence templates
- Win rate predictions before submission

### 15.5 Power User Features
- Full keyboard navigation (G=generate, S=submit, L=lock)
- Command palette (Cmd+K)
- Bulk operations with smart filters
- API access for automation

### 15.6 Enhanced Agency Features
- White-label customization per merchant
- Cross-merchant analytics
- Template sharing marketplace
- Commission tracking on recovered revenue

### 15.7 Performance Optimizations
- Background PDF generation with progress toasts
- Optimistic UI updates
- Intelligent prefetching of related data
- Offline mode for evidence drafting

### 15.8 Advanced Integrations
- Multi-PSP support (PayPal, Square, Adyen)
- Shipping carrier APIs for automatic proof retrieval
- Customer service platform integration (Zendesk, Intercom)
- Fraud detection service connections

### 15.9 Compliance & Security
- SOC2 Type II certification
- PCI DSS compliance for payment data
- GDPR-compliant data retention policies
- Audit trail export for compliance reporting

### 15.10 AI Enhancements
- Smart evidence suggestions based on win/loss patterns
- Automated customer communication summarization
- Anomaly detection for unusual dispute patterns
- Natural language search across all disputes