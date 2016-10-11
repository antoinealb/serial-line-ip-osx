from setuptools import setup

setup(
    name='slip2tun',
    version='1.0.0',
    description='Serial Line IP adapter',
    author='Antoine Albertelli',
    author_email='antoine.albertelli@wise-robotics.com',
    license='BSD',
    packages=['slip'],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Embedded Systems',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        ],
    test_requires=['hypothesis'],
    install_requires=[
        'pyserial',
        ],

    entry_points={
        'console_scripts': [
            'slip2tun=slip.slip2tun:main',
        ]
    }
)

