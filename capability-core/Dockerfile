FROM python:3.12-slim

WORKDIR /opt/siiaos/capability-core

COPY capability-core/ /opt/siiaos/capability-core/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SIIAOS_CORE_BIND=0.0.0.0 \
    SIIAOS_CORE_PORT=8765

EXPOSE 8765

HEALTHCHECK --interval=30s --timeout=3s --start-period=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8765/health', timeout=2)"

CMD ["python", "sidecar.py"]
