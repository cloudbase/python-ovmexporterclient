#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup

PROJECT = 'ovm-exporter'
VERSION = '0.1'
long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='Coriolis OVM exporter CLI',
    long_description=long_description,

    author='Gabriel Adrian Samfira',
    author_email='gsamfira@cloudbasesolutions.com',

    url='https://github.com/gabriel-samfira/python-ovmexporterclient',
    download_url='https://github.com/openstack/python-ovmexporterclient/tarball/master',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Intended Audience :: Developers',
        'Environment :: Console',
    ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff', 'requests'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'ovm-exporter = ovmexporter.main:main'
        ],
        'ovmexporter.cli': [
            'vms_list = ovmexporter.vm:VirtualMachines',
            'vms_show = ovmexporter.vm:ShowVirtualMachine',
            'snapshot_list = ovmexporter.snapshots:ListSnapshots',
            'snapshot_show = ovmexporter.snapshots:ShowSnapshot',
            'snapshot_create = ovmexporter.snapshots:CreateSnapshot',
            'snapshot_delete = ovmexporter.snapshots:DeleteSnapshot',
            'snapshot_purge = ovmexporter.snapshots:PurgeSnapshots',
            'snapshot_download = ovmexporter.snapshots:DownloadSnapshot',
        ],
    },

    zip_safe=False,
)
