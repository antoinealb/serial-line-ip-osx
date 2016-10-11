from setuptools import setup

setup(
    name='slip',
    version='1.0.0',
    description='Serial Line IP adapter',
    author='WISE Robotics',
    author_email='contact@wise-robotics.com',
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

    entry_points={
        'console_scripts': [
            'slip2tun=slip.slip2tun:main',
        ]
    }
)

