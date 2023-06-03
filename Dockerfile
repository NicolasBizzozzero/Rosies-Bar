# syntax=docker/dockerfile:1

FROM python:3.11
WORKDIR /app

# Install whole project
COPY . .

# Update & Install packages
# Setup Python virtualenv
ENV PATH_VIRTUAL_ENV=/venv
RUN python -m venv $PATH_VIRTUAL_ENV
ENV PATH="$PATH_VIRTUAL_ENV/bin:$PATH"

## Python packages
RUN --mount=type=cache,target=.cache/pip python -m pip install --upgrade pip
RUN --mount=type=cache,target=.cache/pip python -m pip install -r requirements.txt

# Run entrypoint
CMD ["/bin/bash", "script/start.sh"]
