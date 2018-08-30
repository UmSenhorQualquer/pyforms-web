try:
    import cv2, base64, numpy as np
    from PIL import Image
except:
    print( "control player will not work. Libraries missing")
from pyforms_web.controls.control_base import ControlBase
import simplejson
from io import BytesIO

class ControlPlayerJs(ControlBase):

    def __init__(self, *args, **kwargs):
        kwargs['css'] = kwargs.get('css', 'fluid')
        
        self._dataset_url = None
        
        self.video_fps    = kwargs.get('fps', None)
        self.video_width  = kwargs.get('width', None)
        self.video_height = kwargs.get('height', None)
        ControlBase.__init__(self, *args, **kwargs)

        
    def init_form(self): 
        return "new ControlPlayerJs('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

    def load_dataset(self, data_url):
        self._dataset_url = data_url
        self.mark_to_update_client()
        


    def serialize(self):
        data = super().serialize()
        data.update({
            'video_width':  self.video_width,
            'video_height': self.video_height
        })
        if self._dataset_url:
            data.update({ 'data_url': self._dataset_url })
            self._dataset_url = None
        return data


