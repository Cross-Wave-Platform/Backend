# base image
FROM mcr.microsoft.com/mssql/server:2019-latest AS kit_base
USER root
SHELL [ "/bin/bash","-c" ]
WORKDIR /app
COPY . ./
RUN sed -i 's/archive.ubuntu.com/free.nchc.org.tw/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install -r proj_setup/requirements.txt

# test env
FROM kit_base AS kit_test
WORKDIR /app
ENV ACCEPT_EULA=Y \
    SA_PASSWORD=Kit2021db
COPY --from=kit_base /app ./
RUN /bin/bash proj_setup/sql_setup.sh && \
    python3 -m test.test

CMD /opt/mssql/bin/sqlservr > /dev/null 2>&1 & \
    python3 app.py