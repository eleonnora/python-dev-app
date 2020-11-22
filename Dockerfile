FROM python:2.7

WORKDIR /python_dev_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

ENV PATH=/root/.local:$PATH

EXPOSE 5000

CMD [ "python", "run.py" ]