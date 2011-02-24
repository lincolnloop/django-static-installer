from distutils.core import setup
from static_installer import get_version

setup(
    name='django-static-installer',
    version=get_version(),
    description="A static file dependency downloader/manager",
    #long_description=open('README.rst').read(),
    author='Marco Louro',
    author_email='marco@lincolnloop.com',
    license='BSD',
    url='http://github.com/lincolnloop/django-static-installer/',
    packages=[
        'static_installer',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
