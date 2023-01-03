#!/usr/bin/env bash
set -euo pipefail

script_dir="$(readlink -f "$(dirname "${0}")")"

is_dark() {
	hexinput=$(echo "${1}" | tr '[:lower:]' '[:upper:]')
	half_darker=$("${script_dir}/darker.sh" "${hexinput}" 128)
	if [[ "${half_darker}" = "000000" ]] ; then
		return 0;
	else
		return 1;
	fi
}

is_dark "$@"
