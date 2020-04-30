# Anubis

> Disposable private socks5 proxy behind Heroku's infrastructure.

## Usage

```bash
./anubis.sh -e root@example.com -p P44sW0rDGo3sHeR3
```

Send traffic to port `1080/tcp` and enjoy your socks5 proxy.

By default, the script will use credentials generated on the fly using your email and password combination for authentication, so only you will be able to access the proxy.

#### Help

```md
Usage: ./anubis.sh [-e your-heroku-email] [-p your-heroku-password]
  -e, --email            Your Heroku email
  -p, --password         Your Heroku password
```

## Disclaimer

Contents provided for educational purposes only, use at your own risk.

## License

Code released under the [MIT](LICENSE) license.
