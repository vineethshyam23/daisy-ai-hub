# Business Case

## Problem

In early 2025, the data platform team at a SaaS company started getting requests to explore Gemini's capabilities for internal productivity. The options were:

- Use the raw Vertex AI API directly (no UI, requires coding)
- Wait for Google Workspace AI to roll out (timeline unknown)
- Buy an external tool (approval process, budget, vendor risk)

None of these worked for the goal: let non-engineers across four companies experiment with AI against real work tasks, today.

## What DAISY solved

DAISY gave 129 employees a sandboxed, authenticated UI to use Vertex AI Gemini without needing a GCP account, API key, or any coding knowledge. Tools were task-specific rather than generic chat, which meant lower prompt-engineering overhead for end users.

Specific gaps it filled:

| Gap | DAISY solution |
|---|---|
| No UI for Gemini | Nuxt 3 frontend with per-tool input forms |
| Email drafting eating time | Email Assistant with tone, length, and reply-type controls |
| Meeting notes inconsistent | Meeting Summarizer with structured output templates |
| PDF/invoice processing manual | Document Analyzer and Invoice Validator with multi-modal input |
| No internal job description tooling | JD Generator pulled from HR system by job ID |

## Impact

- **129 authenticated users** across 4 companies (3 month active period)
- **Zero incidents** in production
- **Decommissioned cleanly** in October 2026 when Anthropic Claude rolled out org-wide

## Why it was decommissioned

Not a failure — planned obsolescence. When a company adopts Claude or Google Workspace AI at the org level, a home-grown sandbox loses its reason to exist. The goal was always to prove the concept and generate usage data to inform the enterprise AI rollout, not to run indefinitely.

## What this demonstrates

- Full-stack ownership from infrastructure to UI: GCP project setup, Cloud Run deployment, Firebase Auth, Vertex AI integration
- Production discipline on a small team: auth, error handling, CORS, Secret Manager, logging, health checks
- Multi-modal AI patterns: text, image generation, document analysis (PDF + image input to Gemini)
- Real user adoption — not a demo, not a proof-of-concept with fake data
