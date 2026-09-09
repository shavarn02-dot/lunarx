FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies for OpenCV and geospatial tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code and scripts
COPY . /app/

# Download real Chandrayaan-2 datasets on image build
RUN python scripts/download_data.py && python scripts/prepare_test_pairs.py

EXPOSE 8501

CMD ["streamlit", "run", "app/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
