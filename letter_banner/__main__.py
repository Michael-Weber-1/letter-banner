"""Allow running as ``python -m letter_banner``."""
import sys
from .cli import main

cfg = BannerConfig(
    ...
    bg_override = args.bg_override,
)

sys.exit(main())
