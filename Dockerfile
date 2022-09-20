FROM python@sha256:2341ac5eedd71f1e6481afe854af572f5ec1b78fa3aea2293dba65942108e663
WORKDIR /opt
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . ./opt
CMD python main.py