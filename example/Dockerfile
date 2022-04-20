FROM ubuntu

ENV DEBIAN_FRONTEND "noninteractive"
ENV TZ "America/New_York"

RUN set -x \
  && echo "Preparing system..." \
  && apt-get -y update \
  && apt-get -y install \
    curl \
    fuse \
    git \
    nginx \
    python3-dev \
    python3-pip \
  && curl https://get.docker.com | sh \
  && rm -rf /var/lib/apt/lists/* \
  && pip3 install --no-cache-dir --upgrade pip

RUN set -x \
  && echo "Preparing user..." \
  && useradd -ms /bin/bash -d /app app \
  && groupadd fuse \
  && adduser app fuse \
  && (groupadd docker || true) \
  && adduser app docker \
  && chown -R app:app /app \
  && chmod og+rwx -R /var/lib/nginx /var/log/nginx

RUN set -x \
  && echo "Installing jupyter kernel..." \
  && pip3 install --no-cache-dir ipython_genutils ipykernel \
  && python3 -m ipykernel install

ADD requirements.txt /app/requirements.txt
RUN set -x \
  && echo "Installing python dependencies from requirements.txt..." \
  && pip3 install --no-cache-dir -r /app/requirements.txt \
  && rm /app/requirements.txt

ARG appyter_version=appyter[production]@git+https://github.com/Maayanlab/appyter
RUN set -x \
  && echo "Installing appyter..." \
  && pip3 install --no-cache-dir --upgrade ${appyter_version}

USER app
WORKDIR /app
EXPOSE 5000
VOLUME /app/data

ENV PATH "/app:$PATH"
ENV PYTHONPATH "/app:$PYTHONPATH"
ENV APPYTER_PREFIX "/"
ENV APPYTER_HOST "0.0.0.0"
ENV APPYTER_PORT "5000"
ENV APPYTER_DEBUG "false"
ENV APPYTER_IPYNB "example.ipynb"

COPY --chown=app:app . /app

CMD [ "appyter" ]