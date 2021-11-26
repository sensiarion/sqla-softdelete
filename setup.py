from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='sqla_softdelete',
    packages=['sqla_softdelete'],
    version='1.3',
    license='GPLv3+',
    long_description=long_description,
    long_description_content_type="text/markdown",
    description='SQLAlchemy soft delete',
    author='Izert Mansur (forked from Vitaly Efremov)',
    author_email='izertmi@gmail.com',
    url='https://github.com/sensiarion/sqla-softdelete',
    download_url='https://github.com/sensiarion/sqla-softdelete/releases/tag/1.3',
    keywords=['SQLAlchemy', 'Soft delete'],
    install_requires=[
        'sqlalchemy>=1.4.1',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
