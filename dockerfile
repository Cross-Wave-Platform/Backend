FROM mcr.microsoft.com/mssql/server:2019-latest

USER root
ENV ACCEPT_EULA=Y \
    SA_PASSWORD=Kit2021db \
    PATH=/app/bin:$PATH
SHELL [ "/bin/bash","-c" ]

WORKDIR /app
COPY proj_setup ./proj_setup
RUN /bin/bash proj_setup/setup.sh
RUN pip3 install -r proj_setup/requirements.txt
RUN /opt/mssql/bin/sqlservr & \
    /bin/bash proj_setup/sql.sh

CMD /bin/bash proj_setup/run.sh