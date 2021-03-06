FROM python:3.8 AS base

COPY video_rss/requirements.txt /requirements.txt
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev \
    && pip install --user -r /requirements.txt \
    && rm -rf /var/lib/apt/lists/

COPY video_rss/ /app/video_rss
COPY *.py /app/

WORKDIR /app

ENTRYPOINT [ "python", "-u", "main.py" ]
CMD []