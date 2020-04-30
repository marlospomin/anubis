#!/bin/bash

# variables
app_name="anubis-proxy-$(cat /proc/sys/kernel/random/uuid | head -c 6)"
auth_password="CHISEL_AUTH=AnUb1sP44sW0rDGo3sHeR3"

# debugging prefixes
info="\033[0;34m[*]\033[m"
success="\033[0;32m[+]\033[m"
failure="\033[0;31m[-]\033[m"
warn="\033[1;33m[!]\033[m"

# banner
banner() {
echo " _______ __    _ __   __ _______ ___ _______ "
echo "|   _   |  |  | |  | |  |  _    |   |       |"
echo "|  |_|  |   |_| |  | |  | |_|   |   |  _____|"
echo "|       |       |  |_|  |       |   | |_____ "
echo "|       |  _    |       |  _   ||   |_____  |"
echo "|   _   | | |   |       | |_|   |   |_____| |"
echo "|__| |__|_|  |__|_______|_______|___|_______|"
echo ""
}

# usage
usage() {
  if [ -n "$1" ]; then
    echo -e "Error: $1\n";
  fi

  echo "Usage: $0 [-e your-heroku-email] [-p your-heroku-password]"
  echo "  -e, --email            Your Heroku email"
  echo "  -p, --password         Your Heroku password"
  echo ""
  echo "Example: $0 -e root@example.com -p P44sW0rDGo3sHeR3"
  exit 1
}

# check if required binaries are present
check() {
  echo -e "$info Checking if heroku cli is present"

  if ! [ -x "$(command -v heroku)" ]; then
    echo -e "$failure Heroku not found"
    echo -e "$info Installing heroku cli"
    wget -qO- "https://cli-assets.heroku.com/install.sh" | sh
    echo -e "$success Done"
  else
    echo -e "$success $(which heroku) found"
  fi

  echo -e "$info Checking if chisel is present"

  if ! [ -f ./chisel ]; then
    echo -e "$failure Chisel not found"
    echo -e "$info Downloading chisel"
    wget -qO- "https://github.com/jpillora/chisel/releases/download/v1.4.0/chisel_1.4.0_linux_amd64.gz" | gzip -d - > chisel
    echo -e "$info Done"
  else
    echo -e "$success $(pwd)/chisel found"
  fi
}

# login on Heroku
login() {
  echo -e "$info Logging in on heroku"
  echo -e "$warn Press ENTER to complete the login"

  expect > /dev/null <(cat << EOF
spawn heroku login -i
expect "Email:"
send "$email\r"
expect "Password:"
send "$password\r"
interact
EOF
  )

  echo -e "$success Logged in as $email"
}

# Create a new app
create() {
  echo -e "$info Creating an app, this may take a while..."
  heroku apps:create $1 > /dev/null 2>&1
  heroku stack:set container > /dev/null 2>&1
  heroku config:set $2 > /dev/null 2>&1
  echo -e "$info Uploading project"
  git push heroku master > /dev/null 2>&1
  echo -e "$success App deployed successfully"
}

# Delete an app and logout
cleanup() {
  echo -e "$info Destroying your app"
  heroku apps:destroy $1 --confirm="$1"
  echo -e "$success App destroyed"

  echo -e "$info Logging out"
  heroku logout > /dev/null 2>&1
}

# Execute our proxy
execute() {
  declare app_name=$1
  declare proxy_location="https://$app_name.herokuapp.com"
  declare auth_password=$2

  trap cleanup $1 INT

  echo -e "$info Connecting to the proxy"
  echo -e "$warn Press CTRL-C to destroy the app and cleanup"

  ./chisel client --keepalive 10s --auth $auth_password $proxy_location socks
}

# Parse arguments
while [[ "$#" > 0 ]]; do case $1 in
  -e|--email) email="$2"; shift;shift;;
  -p|--password) password="$2";shift;shift;;
  *) usage "Unknown parameter passed: $1"; shift; shift;;
esac; done

# Check if required arguments are present
if [ -z "$email" ]; then usage "Email not set."; fi;
if [ -z "$password" ]; then usage "Password not set."; fi;

# ...
# Execution flow
# ...

banner
check
login
create $app_name $auth_password
execute $app_name $auth_password
