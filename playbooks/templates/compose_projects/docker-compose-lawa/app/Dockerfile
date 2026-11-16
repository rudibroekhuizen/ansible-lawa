# syntax=docker/dockerfile:1

# --- Build dash-mantine-components direct vanuit GitHub ----------------------
# De GitHub-repo bevat alleen broncode: de JS-bundles en de Python-bestanden
# worden gegenereerd (build:js + build:backends), zoals in de DMC CI-workflow.
FROM node:22-bookworm-slim AS dmc-builder
ARG DMC_REPO=https://github.com/rudibroekhuizen/dash-mantine-components
ARG DMC_BRANCH=add-lightbox
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip git \
    && rm -rf /var/lib/apt/lists/*
# dash-generate-components zit sinds dash 2.x in het dash-pakket zelf;
# dash[dev] levert de CLI + z'n dependencies (fire, coloredlogs, PyYAML)
RUN pip3 install --break-system-packages "dash[dev]>=4.5.0"
RUN git clone --depth 1 --branch ${DMC_BRANCH} ${DMC_REPO} /dmc
WORKDIR /dmc
RUN --mount=type=cache,target=/root/.npm npm ci
# npm run zet node_modules/.bin op PATH, zodat build:backends react-docgen vindt
RUN npm run build:js && npm run build:backends

# --- App ----------------------------------------------------------------------
FROM python:3.13

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# dash-mantine-components (branch ${DMC_BRANCH}) uit de builder-stage installeren
COPY --from=dmc-builder /dmc /tmp/dash-mantine-components
RUN pip3 install --no-deps /tmp/dash-mantine-components

COPY . .

CMD [ "python3", "-u", "app.py"]
