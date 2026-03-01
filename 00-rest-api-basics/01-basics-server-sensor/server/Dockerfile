FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

# 3. Direktinstallation der Abhängigkeiten (um Caching-Probleme zu vermeiden)
RUN pip install --no-cache-dir flask requests

# 4. Den Server-Code kopieren (Pfad relativ zum Build-Kontext "Root")
COPY server/server_api.py .

EXPOSE 5000

CMD ["python", "server_api.py"]