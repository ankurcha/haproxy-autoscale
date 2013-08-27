import boto
import logging
import settings
from mako.template import Template

def get_running_instances(autoscaling_groups=[]):
    '''
    Get all running instances. Only within a security group if specified.
    '''
    logging.debug('get_running_instances()')

    ec2_conn = boto.connect_ec2()

    # get all the available autoscaling groups
    autoscale_conn = boto.connect_autoscale()

    groups = autoscale_conn.get_all_groups(settings.autoscaling_groups)
    
    instance_ids =[]
    for group in groups:
        instances = []
        for instance in instances:
            if instance.state == 'inService':
                instance_ids.append(instance.instance_id)

    reservations = ec2_conn.get_all_instances(instance_ids)
    return [i for r in reservations for i in r.instances]


def file_contents(filename=None, content=None):
    '''
    Just return the contents of a file as a string or write if content
    is specified. Returns the contents of the filename either way.
    '''
    logging.debug('file_contents()')
    if content:
        f = open(filename, 'w')
        f.write(content)
        f.close()
    
    try:
        f = open(filename, 'r')
        text = f.read()
        f.close()
    except:
        text = None

    return text


def generate_haproxy_config(template=None, instances=None):
    '''
    Generate an haproxy configuration based on the template and instances list.
    '''
    return Template(filename=template).render(instances=instances)
