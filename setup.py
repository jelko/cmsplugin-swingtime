from setuptools import setup, find_packages


VERSION = __import__("swingtime").__version__

setup(
    name="cmsplugin_swingtime",
    description="Event and occurrence scheduling application for Django CMS.",
    version=VERSION,
    author="Jelko Arnds",
    author_email="j.arnds@dienetzgestalter.de",
    url="https://github.com/jelko/cmsplugin_swingtime",
    license = 'BSD',
    install_requires = [
    ],
    classifiers = ['Development Status :: 3 - Alpha',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   "Topic :: Internet :: WWW/HTTP"
                   ],
    packages=find_packages(exclude=["example", "example.*"]),
)

