#!/bin/bash
set -euo pipefail

clickhouse-client --queries-file /var/lib/clickhouse/user_files/5-lawa.sql
