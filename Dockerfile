FROM ubuntu:oracular

SHELL [ "/bin/bash", "-c" ]

# Install some utilities frequently used
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    gpg \
    wget \
    nano \
    rsync \ 
    iputils-ping \
    jq \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/{apt,dpkg,cache,log}

# Install latest Python3
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev

WORKDIR /opt/python

RUN python3 -m venv --system-site-packages /opt/python/venv

RUN { \
    echo '#!/bin/bash' ; \
    echo 'source /opt/python/venv/bin/activate' ; \
    echo 'if [[ "${1}" != "" ]]; then bash -c "${@}"; else bash -i; fi' ; \
    } > /opt/python/shell ; \
    chmod +x /opt/python/shell

SHELL [ "/opt/python/shell" ]

SHELL [ "/bin/bash", "-c" ]

COPY /requirements.txt /opt/python/

RUN { \
    echo '#!/bin/bash'; \
    echo 'echo "Container: python"'; \
    echo 'set -e'; \
    echo 'echo "Setting pip environment to /opt/python"'; \
    echo 'if [ ! -e /opt/python/venv/bin/activate ]; then'; \
    echo '  echo "Running in development mode. Initializing venv."'; \
    echo '  python3 -m venv --system-site-packages /opt/python/venv'; \
    echo '  source /opt/python/venv/bin/activate'; \
    echo '  pip install -r requirements.txt'; \
    echo 'else'; \
    echo '  source /opt/python/venv/bin/activate'; \
    echo 'fi'; \
    echo ''; \
    echo 'if [[ "${1}" == "/bin/bash" ]] || [[ "${1}" =~ ^(/opt/python/)?shell$ ]]; then'; \
    echo '  echo "Dropping to shell"'; \
    echo '  shift' ; \
    echo '  echo "Running: ${@}"' ; \
    echo '  if [[ "${1}" != "" ]]; then' ; \
    echo '    bash -c "${@}"'; \
    echo '  else' ; \
    echo '    exec /bin/bash -i'; \
    echo '  fi' ; \
    echo 'else'; \
    echo '  python thoughtful.py "${@}" || echo "Chat application closed."'; \
    echo 'fi'; \
    } > /entrypoint.sh \
    && chmod +x /entrypoint.sh

ENV PATH=/opt/python:$PATH

ENTRYPOINT [ "/entrypoint.sh" ]

COPY /thoughtful.py /opt/python/

