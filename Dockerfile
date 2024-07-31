FROM python:3.12

WORKDIR /api
COPY . .

RUN rm -rf .venv
RUN rm -rf database
RUN python -m pip install -r requirements.txt


# VOLUME /api/database

CMD [ "fastapi", "run", "main.py", "--port", "3110" ]
EXPOSE 3110

# docker build -t faith-battle-back:latest .

# docker run -d -p 3110:3110 --name faith-battle-back faith-battle-back