VERSION = (0, 2, 2, 'final', 0)
__version__ = '.'.join((str(each) for each in VERSION[:4]))

#-------------------------------------------------------------------------------
def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '%s pre-alpha' % version
    else:
        version = '%s %s' % (version, VERSION[3])
        if VERSION[3] != 'final':
            version = '%s %s' % (version, VERSION[4])

    return version
