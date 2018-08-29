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
        kwargs['css']     = kwargs.get('css', 'fluid')
        self.draws_url    = kwargs.get('draws_url', None)
        self.video_fps    = kwargs.get('fps', None)
        self.video_width  = kwargs.get('width', None)
        self.video_height = kwargs.get('height', None)
        ControlBase.__init__(self, *args, **kwargs)

        
    def init_form(self): 
        return "new ControlPlayerJs('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )


    def serialize(self):
        data = super().serialize()
        data.update({
            'video_width':  self.video_width,
            'video_height': self.video_height,
            'draws_url':    self.draws_url
        })
        return data


