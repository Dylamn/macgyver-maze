from .craftableitem import CraftableItem

from .ether import Ether
from .needle import Needle
from .plastictube import PlasticTube


class Syringe(CraftableItem):
    # The filename of the syringe image.
    _image_file = "seringue.png"

    # Item required to craft this item.
    items_required = [Ether, Needle, PlasticTube]
