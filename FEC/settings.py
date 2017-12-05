import os
from split_settings.tools import optional, include

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

include(
    'components/base.py',
    'components/database.py',
    'components/production.py',
    optional('components/local.py')
)
