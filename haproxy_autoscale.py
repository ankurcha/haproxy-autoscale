import boto
import logging
from mako.template import Template

def get_running_instances(autoscaling_groups=[]):
    '''
    Get all running instances. Only within a security group if specified.
    '''
    logging.debug('get_running_instances()')

    ec2_conn = boto.connect_ec2()

    # get all the available autoscaling groups
    autoscale_conn = boto.connect_autoscale()

    groups = autoscale_conn.get_all_groups(autoscaling_groups)
    
    instance_ids =[]
    for group in groups:
        for instance in group.instances:
            if instance.lifecycle_state == 'InService':
                instance_ids.append(instance.instance_id)

    if len(instance_ids) > 0:
        reservations = ec2_conn.get_all_instances(instance_ids)
        return [i for r in reservations for i in r.instances]
    else:
        return []


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
