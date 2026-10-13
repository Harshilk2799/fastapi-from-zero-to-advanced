FROM python:3.13.5 

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1  

WORKDIR /app 

COPY requirements.txt . 

RUN pip3 install --no-cache-dir -r requirements.txt 

COPY . /app/

CMD [ "fastapi", "dev", "--host", "0.0.0.0", "--port", "8000" ]


