# ── Stage 1: builder ──────────────────────────────────────────────────────────
# Install Python dependencies in an isolated layer so the final image only
# carries the compiled wheels, not build tooling.
FROM python:3.11-slim AS builder

# Build-time deps needed to compile some wheels (e.g. cryptography, numpy)
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        libffi-dev \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY ai_shorts_generator/requirements.txt .

RUN pip install --upgrade pip \
 && pip install --prefix=/install --no-cache-dir -r requirements.txt


# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

# System libraries required at runtime:
#   ffmpeg          – video/audio processing (moviepy, imageio-ffmpeg)
#   libsm6          – OpenCV / moviepy shared memory support
#   libxext6        – X11 extension library (moviepy dependency)
#   libxrender-dev  – X rendering extension (moviepy dependency)
#   libglib2.0-0    – GLib (required by several media libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg \
        libsm6 \
        libxext6 \
        libxrender-dev \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy compiled Python packages from the builder stage
COPY --from=builder /install /usr/local

WORKDIR /app

# Copy the full repository so all modules are available
COPY . .

# Ensure the ai_shorts_generator package directory is on the Python path so
# intra-package imports (e.g. `from viral_hunter import ...`) resolve correctly
ENV PYTHONPATH="/app/ai_shorts_generator:${PYTHONPATH}"

# Create directories that the app writes to at runtime
RUN mkdir -p /app/downloads /app/output

# Default entry point: run the full empire pipeline.
# Override CMD at deploy time to run main.py directly if preferred:
#   CMD ["python", "ai_shorts_generator/main.py"]
CMD ["python", "ai_shorts_generator/empire_pipeline.py"]
