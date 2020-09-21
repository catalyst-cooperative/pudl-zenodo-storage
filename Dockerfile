FROM python:alpine

ARG UID
ARG GID
ENV USER=pudl
ENV HOME=/home/pudl
ENV PUDL_IN=${HOME}/pudl/

RUN apk add build-base

# Install Python Requirements

# Separate COPY means we can use the cached and installed requirements even if
# the rest of the code changes.

WORKDIR /install
COPY requirements.txt ./
RUN pip install --prefix /usr/local -r requirements.txt

# Install zenodo_tools
WORKDIR /install/zenodo_tools
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
RUN mkdir -m 775 -p ${PUDL_IN}

ENTRYPOINT ["zenodo_store.py", "--verbose"]
