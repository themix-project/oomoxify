#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

#set -x

hextoi() {
  value=${1}
  result=$(echo "ibase=16; ${value}" | bc)
  echo "${result}"
}


hex_to_rgba() {
  hexinput="$(tr '[:lower:]' '[:upper:]' <<< "$1")"
  alpha=${2-1.0}

  a="$(cut -c-2 <<< "$hexinput")"
  b="$(cut -c3-4 <<< "$hexinput")"
  c="$(cut -c5-6 <<< "$hexinput")"

  r=$(hextoi "${a}")
  g=$(hextoi "${b}")
  b=$(hextoi "${c}")

  LC_NUMERIC="C" printf 'rgba(%i, %i, %i, %0.2f)\n' "${r}" "${g}" "${b}" "${alpha}"
}

hex_to_rgba "$@"
