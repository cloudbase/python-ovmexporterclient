# Python OVM exporter client

Python client and command line tool for the Coriolis OVM exporter servie.

## Getting started

Installing the client:

```bash
pip3 install git+https://github.com/gabriel-samfira/python-ovmexporterclient
```

Getting a list of supported options and subcommands:

```bash
ovm-exporter --help
```

## Authentication

The client requires the following options to be set:

  * ```--ovm-endpoint``` - the base URL for the exporter (eg: https://192.168.1.100:5544)
  * ```--username``` - a username that has access to the OVM manager to which the compute node is connected to.
  * ```--password``` - the password associated with the username.

These options can also be set via environment variables:

```bash
export OVM_EXPORTER_USERNAME="admin"
export OVM_EXPORTER_ENDPOINT="https://192.168.1.100:5544"
export OVM_EXPORTER_PASSWORD="Passw0rd"
```

If you're using certificates issued by your own certificate authority, you will want to either use the ```--insecure``` flag, or set the ```--ca-path``` option. The CA path can also be set via environment variable:

```bash
export OVM_EXPORTER_CAFILE="/path/to/ca-certificate.pem"
```