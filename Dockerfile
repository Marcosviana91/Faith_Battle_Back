FROM python:3.12

WORKDIR /api
COPY . .

RUN rm -rf .venv
RUN rm -rf database
RUN python -m pip install -r req.txt


# VOLUME /api/database

CMD [ "fastapi", "run", "main.py", "--port", "3188" ]
EXPOSE 3188

# docker build -t faith-battle-back:latest .

# docker run -d -p 8002:8002 --name [apelido] websocket-test