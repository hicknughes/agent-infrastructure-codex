#!/bin/sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
TEMPLATE="$SCRIPT_DIR/../templates/AGENTS.md.template"

if [ -e AGENTS.md ]; then
    printf '%s\n' "AGENTS.md already exists; leaving it unchanged."
else
    cp "$TEMPLATE" AGENTS.md
    printf '%s\n' "Created AGENTS.md. Add repository-specific verify commands before relying on it."
fi

mkdir -p docs/plans docs/handoffs docs/adr
