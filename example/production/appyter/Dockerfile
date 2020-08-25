FROM ubuntu

ENV DEBIAN_FRONTEND "noninteractive"
ENV TZ "America/New_York"

RUN set -x \
  && echo "Preparing system..." \
  && apt-get -y update \
  && apt-get -y install git python3-pip python3-dev \
  && rm -rf /var/lib/apt/lists/* \
  && pip3 install --upgrade pip

RUN set -x \
  && echo "Installing jupyter kernel..." \
  && pip3 install ipykernel \
  && python3 -m ipykernel install

ARG appyter_version=git+git://github.com/Maayanlab/appyter.git
RUN set -x \
  && echo "Installing appyter..." \
  && pip3 install -Iv ${appyter_version}

ENV DEBUG=false

CMD [ "appyter" ]