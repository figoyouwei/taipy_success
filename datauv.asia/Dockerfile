# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# NOTE: uv specific
# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer for uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.cargo/bin/:$PATH"

# Set the working directory in the container to a writable directory
WORKDIR /app

# Initialize uv workspace (creates a .venv)
RUN uv init --no-workspace

# Note: Explicitly create the virtual environment in the .venv directory
RUN uv venv .venv

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Activate the virtual environment and install dependencies via uv pip
RUN uv pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the app runs on
EXPOSE 2080

# Set the entrypoint to run the application
CMD ["uv", "run", "app.py"]
