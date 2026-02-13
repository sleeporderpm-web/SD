FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create .streamlit directory
RUN mkdir -p ~/.streamlit

# Create Streamlit config for container
RUN echo "\
[server]\n\
port = 8080\n\
headless = true\n\
enableXsrfProtection = false\n\
\n\
[client]\n\
showErrorDetails = true\n\
" > ~/.streamlit/config.toml

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health || exit 1

# Run Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
