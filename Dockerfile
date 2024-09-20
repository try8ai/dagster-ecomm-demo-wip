FROM quay.io/devfile/universal-developer-image:latest

USER root

RUN useradd -rm -d /home/dagster -s /bin/bash -g root -u 1234 dagster
RUN mkdir /home/dagster/superset
RUN chown dagster /home/dagster/superset

USER dagster

RUN python3 -m venv /tmp/venv
ENV PATH="/tmp/venv/bin:$PATH"

RUN pip3 install --upgrade pip
RUN pip3 install dagster dagster-webserver dagster_duckdb duckdb dbt-duckdb 'apache-superset>=4.0,<4.1' duckdb-engine dagster-dbt

WORKDIR /home/dagster/superset

RUN echo 'PS1="\u:\W > "' >> ~/.bashrc && . ~/.bashrc
ENV FLASK_APP="superset"
ENV SUPERSET_CONFIG_PATH="superset_config.py"

RUN echo "SECRET_KEY='$(openssl rand -base64 42)'" >> superset_config.py
RUN superset db upgrade
RUN superset fab create-admin --username admin --firstname admin --lastname admin --email admin@localhost --password admin
RUN superset init

WORKDIR /home/dagster
