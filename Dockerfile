FROM python:alpine

ENV USER=pudl
ENV UID=50000
ENV GID=50000
ENV HOME=/home/pudl

RUN apk add build-base

# Install Python Requirements

# Separate COPY means we can use the cached and installed requirements even if
# the rest of the code changes.

WORKDIR /install
COPY requirements.txt ./
RUN pip install --prefix /usr/local -r requirements.txt

# Install zen_tools
WORKDIR /install/zen_tools
COPY ./ ./
RUN pip install --prefix /usr/local ./

# Set up local user
RUN addgroup --gid ${GID} ${USER} \
    && adduser \
    --disabled-password \
    --gecos "" \
    --home "${HOME}" \
    --ingroup "${USER}" \
    --uid "${UID}" \
    "${USER}"

WORKDIR ${HOME}
USER ${USER}

CMD zen_store.py --help;
