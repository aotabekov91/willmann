from .feh import get_mode as get_mode_feh
from .vim import get_mode as get_mode_vim
from .qutebrowser import get_mode as get_mode_qutebrowser
from .chrome import get_mode as get_mode_chrome
from .ranger import get_mode as get_mode_ranger
from .tmux import get_mode as get_mode_tmux
from .anki import get_mode as get_mode_anki


def get_mode():
    return [get_mode_anki(), 
            get_mode_tmux(),
            get_mode_ranger(),
            get_mode_chrome(),
            get_mode_qutebrowser(),
            get_mode_vim(),
            get_mode_feh()]

