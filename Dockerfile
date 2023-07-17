FROM python:3-slim
ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip install fastapi fastapi-sqlalchemy pydantic alembic psycopg2 python-dotenv
RUN pip3 install -r requirements.txt
COPY . /app
EXPOSE 8000

# Define the command to run the FastAPI app using uvicorn
CMD uvicorn app.main:fastapi_app --host 0.0.0.0 --port 8000 --reload
