import argparse
import subprocess
import logging

from haproxy_autoscale import get_running_instances, file_contents, generate_haproxy_config

def main():
    # Parse up the command line arguments.
    parser = argparse.ArgumentParser(description='Update haproxy to use all instances running in a security group.')
    parser.add_argument('--autoscaling-group', required=True, nargs='+', type=str)
    parser.add_argument('--output', default='/etc/haproxy/haproxy.cfg',
                        help='Defaults to haproxy.cfg if not specified.')
    parser.add_argument('--template', default='templates/haproxy.tpl')
    parser.add_argument('--haproxy', default='/usr/sbin/haproxy',
                        help='The haproxy binary to call. Defaults to haproxy if not specified.')
    parser.add_argument('--pid', default='/run/haproxy.pid',
                        help='The pid file for haproxy. Defaults to /run/haproxy.pid.')
    args = parser.parse_args()

    # Fetch a list of all the instances in these security groups.
    logging.info('Getting instances for %s.' % str(args.autoscaling_group))
    instances = get_running_instances(autoscaling_groups=args.autoscaling_group)
    
    # Generate the new config from the template.
    logging.info('Generating configuration for haproxy.')
    new_configuration = generate_haproxy_config(template=args.template,
                                                instances=instances)
    
    # See if this new config is different. If it is then restart using it.
    # Otherwise just delete the temporary file and do nothing.
    logging.info('Comparing to existing configuration.')
    old_configuration = file_contents(filename=args.output)
    if new_configuration != old_configuration:
        logging.info('Existing configuration is outdated.')
        
        # Overwite the existing config file.
        logging.info('Writing new configuration.')
        file_contents(filename=args.output,
                      content=generate_haproxy_config(template=args.template, instances=instances))
        
        # Get PID if haproxy is already running.
        logging.info('Fetching PID from %s.' % args.pid)
        pid = file_contents(filename=args.pid)
        
        # Restart haproxy.
        logging.info('Restarting haproxy.')
        command = '''%s -p %s -f %s -sf %s''' % (args.haproxy, args.pid, args.output, pid or '')
        logging.info('Executing: %s' % command)
        subprocess.call(command, shell=True)
    else:
        logging.info('Configuration unchanged. Skipping restart.')

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()
