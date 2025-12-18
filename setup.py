from setuptools import setup, find_packages

setup(
    name='robotframework-robocorp-windows',
    version='1.0.0',
    description='Robot Framework library for Windows automation using robocorp-windows',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/robotframework-robocorp-windows',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'robotframework>=4.0.0',
        'robocorp-windows>=1.0.0'
    ],
    extras_require={
        'pywin32-300': ['pywin32>=300,<304'],
        'pywin32-300+': ['pywin32>=304']
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Framework :: Robot Framework',
        'Framework :: Robot Framework :: Library',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=['robotframework', 'testing', 'automation', 'windows', 'robocorp'],
    python_requires='>=3.8',
)
