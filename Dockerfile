FROM python:3-slim

ARG HOST=0.0.0.0
ARG PORT=8012
ENV HOST=${HOST}
ENV PORT=${PORT}
ENV PATH="/usr/local/bin:${PATH}"
RUN pip install uv \
    && uv pip install --system ansible-tower-mcp

ENTRYPOINT exec ansible-tower-mcp --transport "http" --host "${HOST}" --port "${PORT}"
