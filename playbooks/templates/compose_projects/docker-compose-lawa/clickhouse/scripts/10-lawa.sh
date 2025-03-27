#!/bin/bash
set -euo pipefail

clickhouse-client --queries-file /var/lib/clickhouse/user_files/10-lawa.sql

