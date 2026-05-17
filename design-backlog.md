# ramblin.dev — Design Backlog

Living list of design/content work for the site. Order is rough priority, not commitment. Check off or delete items as they ship; add new ones freely.

## Site structure (decided)

- **`/` (landing)** — what ramblin.dev *is today*: founded and solely run by Ivan, a home for his independent software projects. Also hosts the mailing-list signup and the projects list. Plain-spoken, scannable, no manifesto vibes.
- **`/vision`** (working title; could also be `/vision-and-principles`) — the long-term plans: equitable profit-sharing model, priority stack, core-company pay-ratio cap, anything aspirational about ramblin.dev as a multi-creator framework. Lives off the landing page so it doesn't set the tone for every visit, but is linked from it.

Both pages use the plain-spoken tone decided earlier.

## 1. Landing page (`/`) — what ramblin.dev is now

The current `content/pages/index.md` is a two-sentence stub. Replace with copy describing ramblin.dev as it exists today, plus the signup form and projects list.

**Must cover:**
- Founded and solely run (today) by Ivan VenOsdel; a home for his independent software ideas.
- **The name.** Short version of what "ramblin'" means here — the old American sense of freedom-through-community-exchange (Depression-era / folk-tradition connotation), applied to creative work. One or two sentences; the longer treatment lives on `/vision`.
- The intent that these projects cross-promote each other and collectively fund ongoing development.
- Default funding model: premium subscriptions/licenses and voluntary support (GitHub Sponsors, Patreon, etc.) of a specific product or of ramblin.dev itself.
- The kinds of apps and sites Ivan personally likes to build — **pro-social**: things that foster human connection, support mental health, lean FOSS/transparent, and treat the user as the customer rather than the product (i.e., avoiding ad targeting, data resale, attention farming). Framed here as a description of Ivan's taste, *not* a company-wide rule a future creator would be bound to — the broader policy framing belongs on `/vision`.
- A one-line pointer to `/vision` for readers who want the longer-term picture.
- **Mailing-list signup, prominently placed.** This is the most visible call-to-action on the landing page — not tucked into the footer, not on a separate `/subscribe` page. Details in section 3.
- Projects list or pointer to `/projects` (see section 4).

**Decided:**
- **Tone: plain-spoken.** Person-introducing-themselves voice, not flag-planting. Hedges age better than declarations.
- **Pay-ratio cap does *not* appear on the landing page** — it lives on `/vision`.

## 2. `/vision` page — long-term plans and principles

A dedicated page for the aspirational picture of ramblin.dev as a multi-creator framework. The landing page links to it; it isn't the first thing a visitor reads.

**Must cover:**
- **The name, full treatment.** The "ramblin'" origin — old American sense of freedom-through-community-exchange (Depression-era ramblers, the Guthrie/folk tradition of trading work, songs, and shelter). ramblin.dev as the same spirit applied to creative work: freedom to make what we wish for others and receive in kind. This is the load-bearing metaphor; everything else on the page is an expression of it.
- Equitable profit-sharing plan, organized around the canonical short framing: **creators first, ramblin.dev second, individual upside third.**
- Core-company pay-ratio cap: no core-company employee earns more than 4x the lowest-paid core-company employee, measured across pay + benefits + equity. No loopholes. Scoped to the company itself — does not bound what a creator earns from their own project.
- Pro-social bias as the company-level project-selection preference (the version of the pro-social paragraph that's about *what kinds of projects ramblin.dev as a whole takes on*, not just Ivan's personal taste). Strong preference for the user-is-the-customer model; framed as a bias, not an absolute bar, so an edge-case creator isn't excluded.
- Honest framing that this is the plan, not the current state — ramblin.dev is solo today.
- **Epigraph (approved):** the Woody Guthrie quote from his 1942 notebook — *"all a human being is, anyway, is just a hoping machine, a working machine."* Primary-source verified (held by the Woody Guthrie Center; reproduced on the official Woody Guthrie site). Place at the top of `/vision`, attributed to Guthrie with the year (1942).

**Decided:**
- **Foreground the aspirational plan, with specifics framed as examples.** Pattern: state the principle plainly, illustrate with hedged examples ("might," "for example," "to give a concrete picture"), then explicitly separate the layers — *mechanics illustrative, principle settled*. This way the numbers can change later without breaking a promise.
- **Canonical short framing:** *creators first, ramblin.dev second, individual upside third.* Use this exact phrasing wherever the priority stack is stated.

**Open questions:**
- Final page slug: `/vision` vs. `/vision-and-principles` vs. something else. `/vision` is shorter and link-friendlier; the longer one is more descriptive.

**Approved draft copy — profit-sharing / priorities section** (drop into `/vision`):

> Right now ramblin.dev is just me, but the longer-term plan is to bring in other creators and share the upside. The principle, short version: **creators first, ramblin.dev second, individual upside third.**
>
> In a little more detail, that's an order of priorities for where a successful project's profits go:
>
> 1. **Creators first.** Every ramblin.dev creator can make a comfortable living doing what they love. Until that's true for everyone under the roof, that's where the money goes.
> 2. **ramblin.dev second.** The shared resources that make it easier for the next creator to launch and find an audience.
> 3. **Individual upside third.** Once the people and the platform are taken care of, the creator who brought the success in keeps the rest. Getting rich is fine — it just comes after the first two.
>
> To give a concrete picture of the kind of mechanics I mean: a "comfortable living" threshold might be defined per creator (cost of living varies a lot), and a runaway hit might route some portion of its profits into the shared creator pool and into ramblin.dev itself before the rest flows back to the originating creator. The core company would be structured along the same lines — for example, a 4x cap between the highest- and lowest-paid core-company employee, across pay, benefits, and equity — so the same priority order is built into how ramblin.dev itself runs.

## 3. Email signup for updates

Collect emails for periodic updates. Socials can come later; email is enough for v1.

**To decide:**
- **Provider.** Should not monetize subscribers' data — this is the ramblin.dev marketing surface, where we hold the pro-social line tight. Candidates to evaluate: Buttondown, Listmonk (self-hosted), Mailchimp (probably no, due to data practices — verify), ConvertKit/Kit, EmailOctopus. Pick one and document the choice in `CLAUDE.md`.
- **Form integration.** Static-site-friendly options: Netlify Forms (since we're already on Netlify) posting to a webhook into the chosen provider, or the provider's own embeddable form. Avoid heavy JS widgets.
- **What we promise subscribers.** Cadence (monthly? on-launch only?), content (new projects, behind-the-scenes, etc.), and an explicit "your email won't be sold or used for ad targeting" line near the form.
- **Confirmation flow.** Double opt-in by default.
- ~~**Where the form lives.**~~ **Decided:** prominently on the landing page itself — the most visible CTA, not a footer afterthought, not on a separate `/subscribe` page.

**Out of scope for v1:** segmenting lists, transactional email, drip sequences.

## 4. Projects list

A page (or landing-page section) listing published ramblin.dev projects. Many will live on subdomains (e.g. `something.ramblin.dev`).

**Per-project entry should include:**
- Name + one-line description
- Link (subdomain or external)
- Status (live / beta / in-development / archived)
- How to support it (subscription link, sponsor link, repo link)

**To decide:**
- Data source: hand-written Markdown per project (`content/pages/projects/*.md` or a Pelican custom generator), or a single `projects.yaml` rendered by a template? Lean: per-project Markdown files — low ceremony, fits Pelican's grain.
- Where to surface: dedicated `/projects` page, plus a "featured" subset on the landing page.
- Visual treatment: simple list vs. cards. Lean: simple list to start; revisit when there are 3+ projects.

**Blocked on:** having actual projects to list. Until then, this can be a placeholder or omitted.

## Cross-cutting / smaller items

- **Favicon + open-graph metadata.** Currently neither is set in `themes/ramblin-simple/templates/base.html`. Add a favicon and OG/Twitter tags so shared links render decently.
- **Page `<title>`.** `base.html` currently uses `{{ SITENAME }}` for every page; should include the page title when on a sub-page.
- **Accessibility pass.** Verify contrast in `style.css`, ensure semantic landmarks, alt text discipline once images appear.
- **Mobile check.** Theme has a viewport tag but no responsive review has been done.
- **License / footer.** Footer currently shows copyright + email. Add a link to the repo and to `/vision` once that page exists.
- **Retire `uv-shim.sh`.** Delete it and simplify `netlify.toml` once Netlify's build image ships `uv` natively.
- **Analytics.** If we ever want traffic numbers, pick a privacy-respecting option (Plausible, GoatCounter, server-log-based). No Google Analytics on the ramblin.dev marketing site.

## Explicitly out of scope (for now)

- Blog/article publishing pipeline (no posts planned yet; `content/content/` stays empty).
- User accounts on ramblin.dev itself (accounts belong to individual products).
- Social media presence beyond email.
- Multi-creator onboarding flows / profit-sharing tooling (aspirational; revisit when a second creator is actually joining).
