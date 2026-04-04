#!/usr/bin/env bash
# start.sh — Auto-detect and launch the appropriate app in this multi-app repository.
# Railpack will invoke this script when no single framework is detected at the root.

set -euo pipefail

log() { echo "[start.sh] $*"; }
err() { echo "[start.sh] ERROR: $*" >&2; exit 1; }

# ---------------------------------------------------------------------------
# 1. Determine the working directory
#    Priority: ai_shorts_generator (primary Python app) → root Python files
#              → any sub-directory with a package.json → root
# ---------------------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

APP_DIR=""
APP_TYPE=""
ENTRY_POINT=""

# --- Check for ai_shorts_generator (primary app) ---
if [[ -f "ai_shorts_generator/requirements.txt" ]]; then
    APP_DIR="ai_shorts_generator"
    APP_TYPE="python"
    # empire_pipeline.py is the full automation cycle; fall back to main.py
    if [[ -f "ai_shorts_generator/empire_pipeline.py" ]]; then
        ENTRY_POINT="empire_pipeline.py"
    elif [[ -f "ai_shorts_generator/main.py" ]]; then
        ENTRY_POINT="main.py"
    fi
fi

# --- Check for a root-level requirements.txt (generic Python app) ---
if [[ -z "$APP_DIR" && -f "requirements.txt" ]]; then
    APP_DIR="."
    APP_TYPE="python"
    if [[ -f "main.py" ]]; then
        ENTRY_POINT="main.py"
    elif [[ -f "viral_hunter.py" ]]; then
        ENTRY_POINT="viral_hunter.py"
    elif [[ -f "app.py" ]]; then
        ENTRY_POINT="app.py"
    else
        # Pick the first .py file found at the root
        ENTRY_POINT="$(find . -maxdepth 1 -name '*.py' | head -n 1)"
        ENTRY_POINT="${ENTRY_POINT#./}"
    fi
fi

# --- Check for a root-level package.json (Node.js app) ---
if [[ -z "$APP_DIR" && -f "package.json" ]]; then
    APP_DIR="."
    APP_TYPE="node"
fi

# --- Scan sub-directories for a package.json ---
if [[ -z "$APP_DIR" ]]; then
    for dir in */; do
        dir="${dir%/}"
        if [[ -f "$dir/package.json" ]]; then
            APP_DIR="$dir"
            APP_TYPE="node"
            break
        fi
    done
fi

# --- Scan sub-directories for a requirements.txt ---
if [[ -z "$APP_DIR" ]]; then
    for dir in */; do
        dir="${dir%/}"
        if [[ -f "$dir/requirements.txt" ]]; then
            APP_DIR="$dir"
            APP_TYPE="python"
            if [[ -f "$dir/main.py" ]]; then
                ENTRY_POINT="main.py"
            elif [[ -f "$dir/app.py" ]]; then
                ENTRY_POINT="app.py"
            fi
            break
        fi
    done
fi

[[ -z "$APP_DIR" ]] && err "Could not detect a Python or Node.js application. Add a requirements.txt or package.json."
[[ -z "$APP_TYPE" ]] && err "APP_TYPE is unset — this should not happen."

log "Detected app type : $APP_TYPE"
log "Application dir   : $APP_DIR"
[[ -n "$ENTRY_POINT" ]] && log "Entry point       : $ENTRY_POINT"

cd "$APP_DIR"

# ---------------------------------------------------------------------------
# 2. Install dependencies
# ---------------------------------------------------------------------------

if [[ "$APP_TYPE" == "python" ]]; then
    PYTHON_BIN="$(command -v python3 || command -v python || true)"
    [[ -z "$PYTHON_BIN" ]] && err "Python interpreter not found. Ensure Python 3 is installed."
    PIP_BIN="$(command -v pip3 || command -v pip || true)"
    [[ -z "$PIP_BIN" ]] && err "pip not found. Ensure pip is installed."

    log "Python : $PYTHON_BIN ($($PYTHON_BIN --version 2>&1))"
    log "pip    : $PIP_BIN"

    if [[ -f "requirements.txt" ]]; then
        log "Installing Python dependencies from requirements.txt …"
        "$PIP_BIN" install --no-cache-dir -r requirements.txt
    else
        log "No requirements.txt found — skipping pip install."
    fi

elif [[ "$APP_TYPE" == "node" ]]; then
    NODE_BIN="$(command -v node || true)"
    NPM_BIN="$(command -v npm || true)"
    [[ -z "$NODE_BIN" ]] && err "Node.js not found. Ensure Node.js is installed."
    [[ -z "$NPM_BIN" ]] && err "npm not found. Ensure npm is installed."

    log "Node : $NODE_BIN ($($NODE_BIN --version))"
    log "npm  : $NPM_BIN ($($NPM_BIN --version))"

    if [[ -f "package.json" ]]; then
        log "Installing Node.js dependencies …"
        "$NPM_BIN" install
    fi
fi

# ---------------------------------------------------------------------------
# 3. Start the application
# ---------------------------------------------------------------------------

log "Starting application …"

if [[ "$APP_TYPE" == "python" ]]; then
    PYTHON_BIN="$(command -v python3 || command -v python)"

    if [[ -n "$ENTRY_POINT" && -f "$ENTRY_POINT" ]]; then
        log "Running: $PYTHON_BIN $ENTRY_POINT"
        exec "$PYTHON_BIN" "$ENTRY_POINT"
    else
        # Last-resort: find any runnable .py at the current directory level
        FALLBACK="$(find . -maxdepth 1 -name '*.py' | head -n 1)"
        FALLBACK="${FALLBACK#./}"
        [[ -z "$FALLBACK" ]] && err "No Python entry point found in $APP_DIR."
        log "Running fallback: $PYTHON_BIN $FALLBACK"
        exec "$PYTHON_BIN" "$FALLBACK"
    fi

elif [[ "$APP_TYPE" == "node" ]]; then
    NPM_BIN="$(command -v npm)"
    NODE_BIN="$(command -v node)"

    # Prefer npm start if a start script is defined in package.json
    if "$NPM_BIN" run env 2>/dev/null | grep -q "^npm run start"; then
        log "Running: npm start"
        exec "$NPM_BIN" start
    elif [[ -f "index.js" ]]; then
        log "Running: node index.js"
        exec "$NODE_BIN" index.js
    elif [[ -f "server.js" ]]; then
        log "Running: node server.js"
        exec "$NODE_BIN" server.js
    elif [[ -f "app.js" ]]; then
        log "Running: node app.js"
        exec "$NODE_BIN" app.js
    else
        log "Running: npm start (fallback)"
        exec "$NPM_BIN" start
    fi
fi
