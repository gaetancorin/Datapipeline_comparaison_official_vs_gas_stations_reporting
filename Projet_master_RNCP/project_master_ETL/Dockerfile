FROM python:3.11.9-slim

WORKDIR /project_master_ETL

# Install MongoDB tools (mongodump, mongorestore, etc.)
RUN apt-get update && apt-get install -y wget ca-certificates tar
RUN wget https://fastdl.mongodb.org/tools/db/mongodb-database-tools-debian11-x86_64-100.12.2.tgz -O /tmp/mongodb-tools.tgz
RUN tar -xzf /tmp/mongodb-tools.tgz -C /tmp
RUN cp /tmp/mongodb-database-tools-*/bin/* /usr/local/bin/
RUN apt-get remove -y wget && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY run.py run.py
COPY env/ env/
RUN rm env/.env && cp env/.env_prod env/.env
COPY App/ App/

# see logs in real times
ENV PYTHONUNBUFFERED=1

ENTRYPOINT [ "python" ]
CMD [ "run.py" ]
