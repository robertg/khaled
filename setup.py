from setuptools import setup

setup(
    name='khaled',
    version='0.0.1',
    include_package_data=True,
    packages=['khaled'],
    license='LICENSE',
    long_description=open('README.md').read(),
    install_requires=['pydub', 'flask', 'psycopg2', 'Flask-SQLAlchemy', 'cockroachdb','watson_developer_cloud'],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ]
)
