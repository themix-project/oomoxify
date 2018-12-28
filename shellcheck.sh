#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

SCRIPT_DIR=$(readlink -e "$(dirname "${0}")")

(
	cd "${SCRIPT_DIR}"
	# shellcheck disable=SC2046
	shellcheck $(find . -name '*.sh')
)

echo '$$ shellcheck passed $$'
exit 0
