from os import path

__version__ = '0.7.0'

package_dir = path.abspath(path.dirname(__file__))


from . import op
from . import context
