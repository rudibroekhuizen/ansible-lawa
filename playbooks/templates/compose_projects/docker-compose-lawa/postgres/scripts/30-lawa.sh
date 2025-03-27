#!/bin/bash
set -euo pipefail


psql -v ON_ERROR_STOP=1 < /var/lib/postgresql/scripts/30-lawa.sql
