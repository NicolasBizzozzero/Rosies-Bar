#!/bin/sh
# -v : Logging path output into host's computer
# -e : Timezone as stated here : https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
# -t : container name


docker run \
  -v /var/log/rosies_bar:/app/log \
  -e "TZ=Europe/Paris" \
  -t rosies_bar:latest
