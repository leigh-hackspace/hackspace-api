FROM python:3.11.4-alpine3.18

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./hackspaceapi /code/hackspaceapi

CMD ["uvicorn", "hackspaceapi.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]