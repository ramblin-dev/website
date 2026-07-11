# ramblin.dev

Source for the ramblin.dev website. Static site built with [Pelican](https://getpelican.com/), deployed via Netlify.

## What ramblin.dev is

ramblin.dev is a small software shop founded and currently solely run by Ivan VenOsdel. It builds small, independent software projects intended to cross-promote each other and collectively fund continued development.

### The name

"Ramblin'" is the old American sense of the word: a freedom of travel, movement, and living — surviving through informal exchange of effort within a community (think Depression-era ramblers, the Guthrie/folk tradition of trading work, songs, and shelter on the road). ramblin.dev applies that same spirit to creative work: a **freedom to make what we wish for others, and receive in kind** from a community doing the same. This is the load-bearing metaphor behind the project. Preserve it when editing copy — don't reduce "ramblin'" to a generic "wandering" or treat it as just an aesthetic. The community-exchange dimension is the whole point.

Core principles (these should be reflected in site copy and product decisions):

- **Pro-social bias.** Projects should skew toward things that are good for people — fostering genuine human connection, supporting mental health, FOSS, transparency, etc. Concrete preferences that fall under this umbrella:
  - **Strong preference for business models where the software user is the customer, not the product.** Models that monetize the user themselves — ad targeting, data resale, attention farming — tend to be anti-social by construction. Default funding model is therefore premium subscriptions/licenses plus voluntary support (GitHub Sponsors, Patreon, etc.) of either a specific product or ramblin.dev itself. This is a preference, not an absolute bar — a future creator with a genuine edge case shouldn't be pushed out over it, but the bar to justify it is high.
  - **Preference for FOSS and transparent development.**
  - **Preference for projects that foster human connection or mental wellbeing.**
- **Equitable compensation (aspirational, for if/when others join).** ramblin.dev is a single shop, not a holding company for separate creator-owned businesses — everyone who works here, including Ivan, is paid under one shared compensation structure, not a per-project revenue split.
- **Pay ratio cap:** no one at ramblin.dev earns more than 5x the lowest-paid person, measured as total compensation per hour worked — (pay + benefits + equity) ÷ hours worked over the compensation period. Comparing hourly rather than annual total is deliberate: it lets part-time staff, contractors, and freelancers fall under the same cap without being penalized for working fewer hours. No loopholes.
- **Goal:** a comfortable living for everyone doing work they love, plus shared marketing/promotion infrastructure — not getting rich.

Keep these intact when editing copy. If the user asks for shorter/punchier wording, preserve the substance (pro-social bias, voluntary-support default, single-shop equitable pay cap, comfortable-not-rich) rather than dropping principles. Don't promote the ad/data-selling preference back into an absolute rule.

## Site structure

- **`/` (landing, `content/pages/index.md`)** — what ramblin.dev is *today*: solo Ivan, his independent software projects, the mailing-list signup, the projects list. Plain-spoken, scannable. The pro-social bullet on this page is framed as *Ivan's personal taste in what to build*, not a policy that would bind a future creator.
- **`/about`** — broader picture of ramblin.dev: the name, the long-term plans (single-shop equitable compensation, the hourly pay-ratio cap), the kinds of projects Ivan wants to build, and how to help. Linked from the landing page; deliberately not the first thing a visitor reads.

When editing copy, keep this split intact — don't pull aspirational/long-term material onto the landing page, and don't reduce the landing-page pro-social paragraph to bare personal preference without the substance (user-as-customer, FOSS, human connection, mental health).

## Repo layout

- `content/pages/` — Pelican pages (Markdown). `index.md` is the landing page.
- `content/content/` — currently empty; reserved for articles/posts.
- `themes/ramblin-simple/` — the custom theme used by the site (templates + `static/style.css`). There is no third-party theme; edits go here.
- `pelicanconf.py` — dev config. `publishconf.py` — production overrides (sets `SITEURL = https://ramblin.dev`).
- `tasks.py` — Invoke/taskipy tasks (`build`, `serve`, `regenerate`, `livereload`, `publish`, …).
- `netlify.toml` — Netlify build config. Calls `./uv-shim.sh` and publishes `output/`.
- `uv-shim.sh` — Bootstrap script for Netlify: installs `uv` if missing, runs `uv sync` then `uv run task build`. **Temporary** — exists only because Netlify's build image doesn't ship `uv`. Delete when Netlify adds first-class `uv` support (TODO is noted in the script).
- `output/` — generated site (gitignored in practice; don't hand-edit).
- `.python-version` — pinned Python (3.12).

## Common commands

Use `uv` for everything; the project is managed by `uv` + `taskipy`.

```bash
uv sync                  # install deps
uv run task build        # build to output/ (dev settings)
uv run task serve        # serve output/ at localhost:8000
uv run task regenerate   # rebuild on file change
uv run task livereload   # rebuild + browser reload
uv run task preview      # build with production settings (publishconf.py)
uv run task clean        # remove output/
```

The `publish` task in `tasks.py` is rsync-based and **not** how this site deploys — deploys go through Netlify on push to `main`. Don't run it unless explicitly asked.

## Conventions

- New pages → `content/pages/*.md` with Pelican front-matter (`Title:`, `Date:`, `Category:`).
- New posts (when we start having them) → `content/content/*.md`.
- Theme changes → `themes/ramblin-simple/templates/*.html` and `themes/ramblin-simple/static/style.css`. Keep the theme minimal and dependency-free; no JS frameworks.
- For the ramblin.dev site itself (this repo), don't introduce trackers, profiling analytics, or third-party ad scripts. The pro-social-bias preference is about *what we build*; for our own marketing surface we hold the line tighter — there's no edge-case reason to monetize visitors here.
- Mailing-list / form integrations should be evaluated against the same standard (the provider's data practices matter).

## Status / roadmap

See `design-backlog.md` for the current backlog of site work (intro copy refresh, mailing-list signup, projects list, etc.). Update that file when scope or priorities change.
