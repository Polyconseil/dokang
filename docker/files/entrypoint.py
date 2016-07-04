# -*- coding: utf-8 -*-
import os
from string import Template
from subprocess import call

from dokang.harvesters import sphinx_rtd_config
from dokang_pdf import PdfHarvester

config_default_values = {
    'DOKANG_UPLOAD_TOKEN': None,  # Token is required
    'DOKANG_NAME': 'My docs',
    'DOKANG_DESCRIPTION': 'Documentations of all my projects',
    'DOKANG_SERVER_TRUSTED_PROXY': '',  # The IP address of the proxy to pass to waitress server's trusted_proxy
}


def sphinx_rtd_config_with_pdf():
    return sphinx_rtd_config(pdf=PdfHarvester)


def generate_dokang_config_file():
    if not os.environ.get('DOKANG_UPLOAD_TOKEN'):
        raise ValueError('%s is required.' % 'DOKANG_UPLOAD_TOKEN')

    with open('prod.template.ini', 'rt') as prod_template:
        prod_template_str = prod_template.read()

    template = Template(prod_template_str)

    config_str = template.substitute(**{
        key: os.environ.get(key, default)
        for key, default in config_default_values.items()
    })

    with open('prod.ini', 'w') as out:
        out.write(config_str)


if __name__ == "__main__":
    generate_dokang_config_file()

    call(["/home/dokang/venv/bin/pserve", "prod.ini"])
