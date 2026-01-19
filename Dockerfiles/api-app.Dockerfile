FROM python:3.10-slim AS build

ENV FLASK_APP=main.py

WORKDIR /app

COPY ./main.py .
COPY ./Dockerfiles/requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

FROM build


ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--port=5000" ]