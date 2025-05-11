FROM python:3.10-slim

WORKDIR /app

# install your deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy in the FastAPI app
COPY . .

# launch with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
