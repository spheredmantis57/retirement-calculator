# Retirement Calculator

## Introduction
This project takes information to ger working year and retirement amortizations.
It has a module that can be used for different investment calculations.

## Usage

### Development

NOTE: Don't run this for production web hosting

usage: main.py [-h] [--cli]

optional arguments:
  -h, --help  show this help message and exit
  --cli       Set this flag to enable the CLI mode

### Production

Use a production server, such as the WSGI implementation Gunicorn

```
# Ctrl+C-able
gunicorn -b 0.0.0.0:8000 main:APP [--log-config FILE]

# daemon
gunicorn -b 0.0.0.0:8000 main:APP -D [--log-config FILE]
```

## Contact Information
Github: [spheredmantis57](https://github.com/spheredmantis57)
LinkedIn: [Randall Dowling](https://www.linkedin.com/in/randall-dowling/)
