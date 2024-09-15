# Dockerfile
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DBT_VERSION=1.5.1

# Install necessary system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory in the container
WORKDIR /app/dbt

# Install dbt-core and dbt-bigquery dependencies
RUN pip install --upgrade pip && pip install python-dotenv dbt-core==${DBT_VERSION} dbt-bigquery

# Create the DBT profiles directory inside the container
RUN mkdir -p /root/.dbt

# Copy the local profiles.yml into the container's /root/.dbt folder
COPY ./dbt/profiles.yml /root/.dbt/profiles.yml

# Copy the local dbt folder to /app/dbt inside the container
COPY ./dbt /app/dbt

# Run dbt deps to install dependencies specified in packages.yml
RUN dbt deps

# Set entrypoint to run DBT commands, with command as argument (e.g., dbt run)
ENTRYPOINT ["dbt"]
