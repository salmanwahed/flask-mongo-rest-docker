FROM python:3.8-alpine
LABEL MAINTAINER="Salman Wahed <dev.salmanwahed@gmail.com>"
WORKDIR app
ADD . /app/
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "wsgi"]