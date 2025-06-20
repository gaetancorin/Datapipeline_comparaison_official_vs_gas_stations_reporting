FROM python:3.9.15 as builder

WORKDIR /Flask_API
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY run.py run.py
COPY config/ config/
COPY data/ data/
COPY App/ App/

ENTRYPOINT [ "python" ]
CMD [ "run.py" ]
