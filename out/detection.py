
#~ import os
#~ import sys

from console.detection import is_a_tty, choose_palette, get_available_palettes
from console.style import ForegroundPalette, EffectsPalette

# these vars need to be available for Formatter objects:
#~ _out_file = sys.stderr



def _find_palettes(stream):
    ''' Need to configure palettes manually, since we are checking stderr. '''
    chosen = choose_palette(stream=stream)
    palettes = get_available_palettes(chosen)
    fg = ForegroundPalette(palettes=palettes)
    fx = EffectsPalette(palettes=palettes)
    return fg, fx, chosen, is_a_tty(stream)

#~ fg, fx, _CHOSEN_PALETTE = _find_palettes(_out_file)
