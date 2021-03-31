""" Mitto Plugin ReqRes """

# PEP440: these are used during the package build
try:
    from __version__ import __VERSION__
except ImportError:
    # pylint: disable=ungrouped-imports
    from mitto.version import version
    __VERSION__ = version(__file__)
__MAINTAINER__ = "ZUAR, Inc"
__EMAIL__ = "support@zuar.com"
