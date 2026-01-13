FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install uv && uv pip install --system -e .

COPY . .

EXPOSE 8000

CMD ["uvicorn", "phase_2_web.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
