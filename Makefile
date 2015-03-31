PIP = bin/pip

all: sysdep
	virtualenv .
	$(PIP) install -r requirements.txt

sysdep:
	@sudo apt-get install -y python-virtualenv python-dev libyaml-dev

.PHONY: clean
clean:
	rm -rf bin lib local share include *.pyc
