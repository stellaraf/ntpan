# ntpan

This is a hastily written app to gather a list of devices from Palo Alto Panorama, connect to each device over SSH, run `show ntp`, parse the output, and email it in a basic report.

It's ugly, messy, has no comments or docs, but it works (for now).

## Configuration

A config file at `/etc/ntpan/config.yaml` is required to run. See `config.example.yaml` for an example.

## Running

To run the service, run `python3 -m ntpan.scheduler`
