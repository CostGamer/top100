FROM python:3.13-slim

RUN apt-get update && apt-get install -y libpq-dev

WORKDIR /backend

COPY /pyproject.toml /pyproject.toml

RUN pip3 install poetry \
  && poetry config virtualenvs.create false \
  && poetry install 

COPY . .

CMD ["uvicorn", "src.backend.main:setup_app", "--host", "0.0.0.0", "--port", "5000"]
