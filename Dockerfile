FROM python:3.12.3-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_USER=1

ENV TZ=Asia/Seoul

WORKDIR /app

COPY ./Pipfile ./Pipfile.lock /app/

RUN pip install pipenv && \
    mkdir -p ~/.local/bin && \
    ln -s $(which pipenv) ~/.local/bin/pipenv

ENV PATH="/root/.local/bin:$PATH"

RUN pipenv install --deploy --system

RUN playwright install
RUN playwright install-deps

COPY . /app

EXPOSE 8503

CMD ["streamlit", "run", "src/main.py", "--server.port=8503", "--server.address=0.0.0.0" ]
