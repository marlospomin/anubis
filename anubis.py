#!/usr/bin/env python3

from pwn import *
from shutil import which
from os import path, getcwd
from subprocess import DEVNULL
from optparse import OptionParser
from subprocess import call as system

# Helper functions

def checkHerokuCli():
    # Checks if heroku executable is installed
    if not which("heroku"):
        # Log progress
        progress = log.progress("Installing heroku cli")
        # Commands to install heroku
        commands = [
            "wget -q https://cli-assets.heroku.com/install.sh",
            "sh intall.sh",
            "rm install.sh"
        ]
        # For each command run it on a shell
        for command in commands:
            system(command.split(), stdout=DEVNULL)
        # Log success
        progress.success("Done")
    else:
        # Log success
        log.success("%s found" % which("heroku"))

def checkChiselBinary():
    # Checks if chisel binary is present
    if not path.exists("chisel"):
        # Commands to install chisel
        commands = [
            "wget -q https://github.com/jpillora/chisel/releases/download/1.3.1/chisel_linux_amd64.gz",
            "gunzip -f -q chisel_linux_amd64.gz",
            "mv chisel_linux_amd64 chisel",
            "chmod +x chisel"
        ]
        # Log progress
        progress = log.progress("Setting up chisel")
        # For each command run it on a shell
        for command in commands:
            system(command.split())
        # Log success
        progress.success("Done")
    else:
        # Log success
        log.success("%s/chisel found" % getcwd())

def loginHeroku(username, password):
    # Log progress
    log.info("Logging in...")
    # Start process
    cli = process("heroku login --interactive".split())
    # Recv first line
    cli.recvline()
    # Recv prompt
    cli.recv(64)
    # Send username
    cli.sendline(username)
    # Recv password
    cli.recv(64)
    # Send password
    cli.sendline(password)
    # Wait for signal
    cli.poll()

def createApp(name, username, password):
    # Progress
    progress = log.progress("Creating a heroku app")
    # Proxy password
    env_password = "CHISEL_AUTH=%s:%s" % (username, password)
    # Create the app
    system(["heroku", "apps:create", name], stdout=DEVNULL)
    system(["heroku", "stack:set", "container"], stdout=DEVNULL)
    system(["heroku", "config:set", env_password], stdout=DEVNULL)
    # Deploy
    system("git push heroku master".split(), stdout=DEVNULL)
    # Log success
    progress.success("Done")
    # Log info
    log.info("App deployed at: https://%s.herokuapp.com" % name)

# Core functions

def setup():
    # Login
    loginHeroku(username, password)
    # Create our proxy app
    createApp(appname, username, password)

def execute(name, username, password):
    # Log
    log.info("Lauching proxy...")
    # Store variables
    credentials = "%s:%s" % (username, password)
    url = "https://%s.herokuapp.com" % name
    # Attempt to spawn chisel
    try:
        # Log warning
        log.warn("Press CTRL-C to destroy your proxy")
        # Run chisel to connect to the server
        system(["./chisel", "client", "--keepalive", "10s", "--auth", credentials, url, "socks"], stdout=DEVNULL)
    except KeyboardInterrupt:
        # Log
        progress = log.progress("Destroying your app")
        # Stop proxy client
        system("pkill chisel".split())
        # Destroy app
        terminate(name)
        # Log success
        progress.success("Done")
    finally:
        # Log progress
        progress = log.progress("Logging out")
        # Logout
        system("heroku logout".split(), stdout=DEVNULL)
        # Log success
        progress.success("Done")

def terminate(name):
    # Destroy an app
    system(["heroku", "apps:destroy", name, "-c", name])

# Main function

def main():
    # Check binaries
    checkHerokuCli()
    checkChiselBinary()
    # Run setup
    setup()
    # Run your proxy
    execute(appname, username, password)

# Run main() upon script call
if __name__ == "__main__":
    # Initialize parser
    parser = OptionParser(usage="usage: %prog [options] arguments")
    # Add options
    parser.add_option("-u", "--username", dest="username", help="heroku username")
    parser.add_option("-p", "--password", dest="password", help="heroku password")
    # Parse arguments
    (options, args) = parser.parse_args()
    # If username/passwor isn't supplied error out
    if not options.username or not options.password:
        parser.error("missing username/password")
    # Re assign variables
    username = options.username
    password = options.password
    # Store appname
    appname = "%s-proxy-%s" % (username[0:8], password[0:4])
    # Start the program
    main()
