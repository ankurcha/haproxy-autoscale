# haproxy-autoscale #

## Description ##
Personal automatic updater for the HAProxy configuration using autoscaling
groups on Amazon EC2.

## Installation ##
Run `sudo python setup.py install` and if everything goes well you're ready to
configure (if you have complex needs) and run the update-haproxy.py command.

## Configuration ##
Most of the configuration is done via command line options. The only
configuration that may need to be done is the haproxy.cfg template. You can
customize it to suit your needs or you can specify a different on on the
command line. Make sure to read the existing template to see what variables
will be available to use.

## Usage ##
haproxy-autoscale was designed to be run from the load balancer itself as a cron
job. Ideally it would be run every minute.

    update-haproxy.py [-h] --autoscaling-group SECURITY_GROUP
                      [SECURITY_GROUP ...] [--output OUTPUT]
                      [--template TEMPLATE] [--haproxy HAPROXY] [--pid PID]

    Update haproxy to use all instances running in a security group.

    optional arguments:
      -h, --help            show this help message and exit
      --autoscaling-group SECURITY_GROUP [SECURITY_GROUP ...]
      --output OUTPUT       Defaults to haproxy.cfg if not specified.
      --template TEMPLATE
      --haproxy HAPROXY     The haproxy binary to call. Defaults to haproxy if not
                            specified.
      --pid PID             The pid file for haproxy. Defaults to
                            /var/run/haproxy.pid.

Example:

    /usr/bin/python update-haproxy.py --security-group='grupo-prueba' 'another-group'

## Changelog ##
* v0.1 - Initial release.
* v0.2 - Added ability to specify multiple security groups. This version is
       **not** compatible with previous versions' templates.
* v0.3 - Added support for all regions.
* v0.4 - Seahorsification