# start with py3.11
FROM python:3.11-slim

# work folder inside container
WORKDIR /app

# first just copy and install requirements
COPY requirements-docker.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt



# then copy other codes
COPY src/ ./src/
COPY data/ ./data/
COPY conftest.py .

# port that API works on
EXPOSE 8000


# run cpmmand
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]