from setuptools import setup

setup(
    name='khaled',
    version='0.0.1',
    include_package_data=True,
    packages=['khaled'],
    license='LICENSE',
    long_description=open('README.md').read(),
    install_requires=['pydub', 'flask'],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ]
)
