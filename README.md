# Anubis

> Disposable private socks5 proxy behind Heroku's infrastructure.

## Install

Install the dependencies with:

```bash
apt-get install python3 python3-dev python3-pip git
pip3 install --upgrade git+https://github.com/arthaud/python3-pwntools.git
```

## Usage

```bash
python3 anubis.py --username your-heroku-email --password your-heroku-password
```

Send traffic to port `1080/tcp` and enjoy your socks5 proxy. (Proxychains)

## Roadmap

* Add error checks.
* Fix logging issues.

## Disclaimer

Contents are provided as is for educational purposes only, use at your own risk.

## License

Code released under the [MIT](LICENSE) license.
