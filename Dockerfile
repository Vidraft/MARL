FROM python:3.12-slim

WORKDIR /app

# Disable ALL optional Gradio features that could hang
ENV GRADIO_SSR_MODE=false
ENV GRADIO_ANALYTICS_ENABLED=false
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860
ENV HF_HUB_DISABLE_TELEMETRY=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    python -c "import gradio; print(f'gradio {gradio.__version__}')"

COPY . .
RUN python -c "from marl import Marl; print('MARL OK')"

EXPOSE 7860
CMD ["python", "app.py"]
