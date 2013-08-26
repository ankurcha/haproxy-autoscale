global  
    maxconn 4096
    user haproxy
    group haproxy
    daemon

defaults
    log global
    log /var/log/haproxy.log local0 err
    mode http
    option httplog
    option dontlognull
    option redispatch
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms
    retries 3

frontend http-in
    bind *:8002
    default_backend gunicorn_group

backend gunicorn_group
    mode http
    balance roundrobin
    % for instance in instances['security-group-1']:
    server ${ instance.id } ${ instance.private_dns_name }:8000 maxconn 32
    % endfor