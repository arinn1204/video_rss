FROM python:3.8 AS base

COPY video_rss/requirements.txt /requirements.txt
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev \
    && pip install --user -r /requirements.txt \
    && rm -rf /var/lib/apt/lists/

COPY video_rss/*.py /app/
COPY video_rss/database/ /app/database
COPY video_rss/logging/ /app/logging
COPY video_rss/rss/ /app/rss
COPY video_rss/transmission/ /app/transmission
COPY video_rss/torrents/ /app/torrents

WORKDIR /app

ENTRYPOINT [ "python", "-u", "main.py" ]
CMD []