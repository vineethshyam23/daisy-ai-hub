# Business Case

## The problem

Early 2025. The data team started getting requests to explore what Gemini could actually do for internal work. The options were rough: use the raw Vertex AI API (requires coding, no one outside the team can use it), wait for Google Workspace AI to roll out (timeline unknown, almost certainly months), or buy something external (approval process, procurement, vendor risk, three months minimum).

None of that worked. The ask was simple: let people try AI against real tasks, now.

## What we built

DAISY gave 129 employees a sandboxed, authenticated UI to use Vertex AI Gemini without needing a GCP account or any coding knowledge. Tools were task-specific — email drafting, meeting minutes, document analysis — not a generic chat box. That was deliberate. A blank chat window makes people feel like they need to know what to ask. A tool with an input form for "tone" and "reply type" removes that friction entirely.

The tools that actually got used were not the ones I expected. Email Assistant and Meeting Summarizer were the top two by a wide margin. Image Generator had the most sessions but the shortest. Document Analyzer had the best user feedback, mostly because it replaced a genuinely painful manual process — uploading a PDF to find a specific clause.

The Invoice Validator wasn't in the original plan at all. A team member was spending two hours every Friday cross-referencing Excel invoices against a Jira export. They built the tool in a day. It became one of the most used things in the whole product.

## Why it was decommissioned

Not a failure. Anthropic Claude rolled out org-wide in October 2026, alongside native Google Workspace AI. At that point a home-grown sandbox has no reason to exist — you decommission it and move the energy somewhere else.

The goal from the start was to generate real usage data to inform the enterprise AI rollout, not to run something in production forever. By that measure it did exactly what it was supposed to do.

## What this demonstrates

Building and running this end-to-end: GCP project setup, Cloud Run deployment, Firebase Auth integration, Vertex AI multi-modal inference, production monitoring. A 2-person team, 129 real users, 3 months in production without an incident. The architecture decisions in this repo reflect what was actually built and what we learned running it, not a cleaned-up post-hoc version.
