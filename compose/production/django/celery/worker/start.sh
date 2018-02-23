#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


celery -A django-web-parser.taskapp worker -l INFO
