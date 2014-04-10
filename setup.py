import setuptools

setuptools.setup(name='vmtp-mud',
                 version='0.0',
                 description='A simple learning MUD',
                 author='Ivan Kalinin',
                 author_email='pupssman@gmail.com',
                 packages=['vmtp_mud'],
                 entry_points={'console_scripts': ['vmtp-mud = vmtp_mud.client:main',
                                                   'vmtp-mud-server = vmtp_mud.server:main', ]}
                 )
