FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .
ENV REVIEWLENS_MODE=mock
EXPOSE 8000
CMD ["uvicorn", "reviewlens_mcp.web:app", "--host", "0.0.0.0", "--port", "8000"]

