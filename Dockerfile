FROM python:3.8 AS base

COPY main/requirements.txt /requirements.txt
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev \
    && pip install --user -r /requirements.txt \
    && rm -rf /var/lib/apt/lists/ 

WORKDIR /app
COPY main/*.py /app

CMD [ "python3", "main.py" ]