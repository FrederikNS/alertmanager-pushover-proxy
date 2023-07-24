FROM python:3.10-alpine
RUN mkdir /opt/python-gzipbomb
WORKDIR /opt/python-gzipbomb
RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system
COPY app.py .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
