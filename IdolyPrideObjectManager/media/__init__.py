"""
media/
Multimedia (images, audio, video, etc.) management.
Instantiated by PrideResource or descendants.
"""

import UnityPy

from ..const import PRIDE_UNITY_VERSION
from .dummy import PrideDummyMedia

UnityPy.config.FALLBACK_UNITY_VERSION = PRIDE_UNITY_VERSION
