"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

import numpy as np
from scipy import ndimage as ndi
from skimage.feature import blob_log
from typing import List

if TYPE_CHECKING:
    import napari

def gaussian_high_pass(image: np.ndarray, sigma: float = 2):
    low_pass = ndi.gaussian_filter(image, sigma)
    high_passed_im = image - low_pass
    
    return high_passed_im


def detect_spots(image: np.ndarray, high_pass_sigma: float = 2, spot_threshold: float = 0.01, blob_sigma: float = 2):

    filtered_spots = gaussian_high_pass(image, high_pass_sigma)
    
    blobs_log = blob_log(filtered_spots, max_sigma=blob_sigma, num_sigma=1, threshold=spot_threshold)
    
    points_coords = blobs_log[:, 0:2]
    sizes = 2 * np.sqrt(2) * blobs_log[:, 2]

    layer_data = (
        points_coords,
        {
            "face_color": "magenta",
            "size": sizes
        },
        "Points"
    )

    image_layer_data = (
        filtered_spots,
        {
            
        },
        "Image"
    )
    return (image_layer_data, layer_data)


def example_function_widget(img_layer: "napari.layers.Image") -> List["napari.types.LayerDataTuple"]:
    print(f"you have selected {img_layer}")
    image = img_layer.data
    image_layer_data, detected_spots = detect_spots(image)
    return [image_layer_data, detected_spots]

"""class ExampleQWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        btn = QPushButton("Click me!")
        btn.clicked.connect(self._on_click)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(btn)

    def _on_click(self) -> List["napari.types.LayerDataTuple"]:
        print("napari has", len(self.viewer.layers), "layers")
        image = img_layer.data
        image_layer_data, detected_spots = detect_spots(image)
        print('Spots detected')
        return [image_layer_data, detected_spots]"""