#!/usr/bin/env bash
set -euxo pipefail

# TODO: Remove this file when netlify supports uv

# Install uv if missing (Netlify doesn't have it by default)
if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

# Sync dependencies and build site
uv sync --frozen || uv sync
uv run task build
