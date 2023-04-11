from .loginApp import *
from .fileApp import *
from .personalApp import *
from .searchApp import *
from .adminApp import *
from .reportApp import *
from .historyApp import *

__all__ = [
    *loginApp.__all__,
    *fileApp.__all__,
    *personalApp.__all__,
    *searchApp.__all__,
    *adminApp.__all__,
    *reportApp.__all__,
    *historyApp.__all__,
]