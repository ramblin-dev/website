# ramblin.dev — Design Backlog

Living list of design/content work for the site. Order is rough priority, not commitment. Check off or delete items as they ship; add new ones freely.

## Site structure

- **`/` (landing)** — what ramblin.dev *is today*: founded and solely run by Ivan, a home for his independent software projects. Also hosts the mailing-list signup and the "Out so far" projects list. Plain-spoken, scannable, no manifesto vibes.
- **`/about`** — the broader picture: the problem ramblin.dev is responding to, where the name comes from (Guthrie epigraph), the long-term profit-sharing dream and core-company pay-ratio cap, the kinds of projects Ivan wants to build, and how to help. Lives off the landing page so it doesn't set the tone for every visit, but is linked from it.

Both pages use the plain-spoken tone decided earlier.

## 1. Landing page (`/`) — what ramblin.dev is now

The current `content/pages/index.md` is a two-sentence stub. Replace with copy describing ramblin.dev as it exists today, plus the signup form and projects list.

**Must cover:**
- Founded and solely run (today) by Ivan VenOsdel; a home for his independent software ideas.
- **The name.** Short version of what "ramblin'" means here — the old American sense of freedom-through-community-exchange (Depression-era / folk-tradition connotation), applied to creative work. One or two sentences; the longer treatment lives on `/about`.
- The intent that these projects cross-promote each other and collectively fund ongoing development.
- Default funding model: premium subscriptions/licenses and voluntary support (GitHub Sponsors, Patreon, etc.) of a specific product or of ramblin.dev itself.
- The kinds of apps and sites Ivan personally likes to build — **pro-social**: things that foster human connection, support mental health, lean FOSS/transparent, and treat the user as the customer rather than the product (i.e., avoiding ad targeting, data resale, attention farming). Framed here as a description of Ivan's taste, *not* a company-wide rule a future creator would be bound to — the broader policy framing belongs on `/about`.
- A one-line pointer to `/about` for readers who want the longer-term picture.
- **Mailing-list signup, prominently placed.** This is the most visible call-to-action on the landing page — not tucked into the footer, not on a separate `/subscribe` page.
- Projects list or pointer to `/projects` (see section 2).

**Decided:**
- **Tone: plain-spoken.** Person-introducing-themselves voice, not flag-planting. Hedges age better than declarations.
- **Pay-ratio cap does *not* appear on the landing page** — it lives on `/about`.

## 2. Projects list

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

**Status:** First project (Rural Hide + Seek, `ruralhs.ramblin.dev`) is listed inline on the landing page under an "Out so far" section. Per-project Markdown files and a dedicated `/projects` page are still TBD — revisit when a second project is close to shipping or when status indicators (live / beta / archived) start being useful.

## Cross-cutting / smaller items

- **Favicon + open-graph metadata.** Currently neither is set in `themes/ramblin-simple/templates/base.html`. Add a favicon and OG/Twitter tags so shared links render decently.
- **Page `<title>`.** `base.html` currently uses `{{ SITENAME }}` for every page; should include the page title when on a sub-page.
- **Accessibility pass.** Verify contrast in `style.css`, ensure semantic landmarks, alt text discipline once images appear.
- **Mobile check.** Theme has a viewport tag but no responsive review has been done.
- **License / footer.** Footer shows copyright, email, and a link to `/about`. Still needs a link to the repo.
- **Retire `uv-shim.sh`.** Delete it and simplify `netlify.toml` once Netlify's build image ships `uv` natively.
- **Analytics.** If we ever want traffic numbers, pick a privacy-respecting option (Plausible, GoatCounter, server-log-based). No Google Analytics on the ramblin.dev marketing site.

## Explicitly out of scope (for now)

- Blog/article publishing pipeline (no posts planned yet; `content/content/` stays empty).
- User accounts on ramblin.dev itself (accounts belong to individual products).
- Social media presence beyond email.
- Hiring/onboarding flows (aspirational; revisit if ramblin.dev ever grows beyond solo).
