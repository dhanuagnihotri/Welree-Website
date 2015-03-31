import os

SERVICES = {
    "nginx":
        {
            "port": 33100,
            "gunicorn_port": 33101,
            "templates": ["{project_dir}/nginx.conf.template"],
            "start": "nginx -c {project_dir}/nginx.conf",
            "restart": "kill -s SIGHUP {pid}",
        },
    "gunicorn":
        {
            "port": 33101,
            "templates": ["{project_dir}/settings_gunicorn.py.template"],
            "before": "./before_deploy.sh",
            "start": "gunicorn -D -c settings_gunicorn.py welree.wsgi:application",
            "after": "./after_deploy.sh",
            "restart": "kill -s SIGHUP {pid}",
        },
    "solr": {
            "port": 33102,
            "start": "java -Djetty.port={port} -Djetty.pid={project_dir}/run/solr.pid -Dsolr.solr.home={project_dir}/../solr -jar start.jar",
            "cwd": os.getenv("SOLR_EXAMPLE"),
            "daemonizes": False,
        },
    "memcached":
        {
            "pidfile": "{project_dir}/run/memcached.pid",
            "start": "memcached -d -m 32 -s {project_dir}/run/memcached.sock -P {project_dir}/run/memcached.pid",
        }
}

