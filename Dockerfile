FROM python:3.11-slim

# set workdir
WORKDIR /app

# system deps for some packages (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# copy requirements and install
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# copy app
COPY . /app

# make start script executable
RUN chmod +x /app/start.sh

# expose a default port (platform will set $PORT)
EXPOSE 8000 8501

# default command uses start.sh which selects Streamlit or uvicorn based on LAUNCH_MODE
CMD ["/bin/bash", "./start.sh"]
