FROM python:3.11.9

WORKDIR /Flask_API
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
