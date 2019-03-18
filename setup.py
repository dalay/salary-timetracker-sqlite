from os.path import join, dirname
from distutils.core import setup
from setuptools import find_packages
from timetracker_sqlite import __version__

setup(
    name='salary-timetracker-sqlite',
    packages=find_packages(exclude=['test', '*.test', '*.test.*']),
    version=__version__,
    description='A simple and easy timetracker for loging working hours with sqlite db and automatic wage calculation.',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    license='GPL',
    author='Alexandr Jurow',
    author_email='pythonwayru@gmail.com',
    url='http://github.com/dalay/salary-timetracker-sqlite',
    download_url='https://github.com/dalay/salary-timetracker-sqlite/archive/v{}.tar.gz'.format(
        __version__),
    keywords=['timetracker', 'salary', 'freelance', 'sqlite'],
    install_requires=['click', 'prettytable'],
    entry_points={
        'console_scripts': [
            'tts = timetracker_sqlite:main',
            'timetracker-sqlite = timetracker_sqlite:main'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    ],
)
