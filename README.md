# Anubis

> Disposable private socks5 proxy behind Heroku's infrastructure.

## Install

Install dependencies:

```bash
# Ubuntu/Debian
apt-get install python3 python3-dev python3-pip git
pip3 install --upgrade git+https://github.com/arthaud/python3-pwntools.git
```

## Usage

```bash
python3 anubis.py --email user@example.com --password YourPassword123
```

Send traffic to port `1080/tcp` and enjoy your socks5 proxy.

By default, the script will use credentials generated on the fly using your email and password combination for authentication, so only you will be able to access the proxy.

## Disclaimer

Contents provided for educational purposes only, use at your own risk.

## License

Code released under the [MIT](LICENSE) license.
