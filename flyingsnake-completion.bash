#!/usr/bin/env bash
#
# Bash completion for flyingsnake.
#
# Copyright (C) 2019 Emanuele Petriglia <inbox@emanuelepetriglia.com>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>.

_flyingsnake() {
  local current previous options words
  COMPREPLY=()
  current="${COMP_WORDS[$COMP_CWORD]}"
  previous="${COMP_WORDS[$COMP_CWORD - 1]}"
  options="-c --colors --background --no-background --blocks --no-blocks"
  options="$options --walls --no-walls --liquids --no-liquids --wires"
  options="$options --no-wires --paint --no-paint --help"

  if [[ "$current" == -* ]]; then
    words="$options"
  elif [[ "$previous" == "-c" || "$previous" == "--colors" ]]; then
    words="$(compgen -A file -X '!*.json')" # colors file.
  else
    words="$(compgen -A file -X '!*.wld')" # Terraria world map.
  fi

  mapfile -t COMPREPLY < <(compgen -W "$words" -- "$current")
  return 0
}

complete -F _flyingsnake flyingsnake
