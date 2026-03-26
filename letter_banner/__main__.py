"""Allow running as ``python -m letter_banner``."""
import sys
from .cli import main

sys.exit(main())
