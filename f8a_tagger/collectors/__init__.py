"""Keywords collectors."""

from .base import CollectorBase
from .maven import MavenCollector
from .npm import NpmCollector
from .pypi import PypiCollector
from .stackoverflow import StackOverflowCollector

assert CollectorBase
assert MavenCollector
assert NpmCollector
assert PypiCollector
assert StackOverflowCollector
