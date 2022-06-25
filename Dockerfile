#FROM python:3.8-slim as base
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /app
EXPOSE 8000



#
# libpq-dev and python3-dev help with psycopg2
#RUN apt-get update \
#  && apt-get install -y --no-install-recommends python3-dev libpq-dev gcc curl wget unzip zip gnupg2 \
#  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
#  && rm -rf /var/lib/apt/lists/*
#  # You can add additional steps to the build by appending commands down here using the
#  # format `&& <command>`. Remember to add a `\` at the end of LOC 12.
#  # WARNING: Changes to this file may cause unexpected behaviors when building the app.
#  # Change it at your own risk.
#
#ENV CHROME_VERSION "google-chrome-stable"
#RUN sed -i -- 's&deb http://deb.debian.org/debian jessie-updates main&#deb http://deb.debian.org/debian jessie-updates main&g' /etc/apt/sources.list \
#  && apt-get update && apt-get install wget -y
#RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
#  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list \
#  && apt-get update && apt-get -qqy install ${CHROME_VERSION:-google-chrome-stable}
#
#RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
#RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
#RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
#
#WORKDIR /opt/webapp
#COPY Pipfile* /opt/webapp/
#
#RUN pip3 install --no-cache-dir -q 'pipenv==2018.11.26'
#RUN pipenv install --deploy --system
#COPY . /opt/webapp
#
#FROM base as release
#
#COPY --from=base /root/.local /root/.local
#COPY --from=base /opt/webapp/manage.py /opt/webapp/manage.py
#
#
#WORKDIR /opt/webapp
#ENV PATH=/root/.local/bin:$PATH
#ARG SECRET_KEY
#RUN python3 manage.py collectstatic --no-input
#
## Run the image as a non-root user
#RUN adduser --disabled-password --gecos "" django
#USER django

#CMD uvicorn app.main:app --reload
CMD daphne -p $PORT -b 0.0.0.0 app.main:app --reload
