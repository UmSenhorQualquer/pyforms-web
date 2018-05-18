try:
    import cv2, base64, numpy as np
    from PIL import Image
except:
    print( "control player will not work. Libraries missing")
from pyforms_web.controls.control_base import ControlBase
import simplejson
from io import BytesIO

class ControlPlayer(ControlBase):

    def __init__(self, *args, **kwargs):
        self._css = 'fluid'
        self._filename = ''
        self._video_index = 0
        self.process_frame_event = kwargs.get('process_frame_event', self.process_frame_event)
        ControlBase.__init__(self, *args, **kwargs)

        
    def init_form(self): 
        return "new ControlPlayer('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

    def process_frame_event(self, frame):  return frame

    def update_frame(self):          pass

    def videoPlay_clicked(self):    pass

    def save(self, data):           pass

    def load(self, data):           pass

    def refresh(self):
        self.mark_to_update_client()
            
    def convertFrameToTime(self, frame):
        currentMilliseconds = (frame / self.value.videoFrameRate) * 1000
        totalseconds = int(currentMilliseconds/1000)
        minutes = int(totalseconds / 60)
        seconds = totalseconds - (minutes*60)
        milliseconds = currentMilliseconds - (totalseconds*1000)
        return ( minutes, seconds, milliseconds )

    def videoProgress_valueChanged(self):   pass

    def videoProgress_sliderReleased(self): pass

    def videoFrames_valueChanged(self):     pass

    def isPlaying(self):    pass

    def changed(self):      pass

    def stop(self): pass 
    
    @property
    def value(self): 

        if self._value:
            return self._value
        elif self._filename:
            capture = cv2.VideoCapture( self._filename )
            capture.set(1, self._video_index)
            return capture

        return None


    @value.setter
    def value(self, value):
        if self._value!=value: self.mark_to_update_client()
        
        if isinstance( value, str ):
            if len(value.strip())==0: return
            #link = self.storage.public_download_link(value)
            #link = value#self.storage.public_download_link(value)
            #ControlBase.value.fset(self, cv2.VideoCapture( value ) )
            self._filename = value
        else:
            self._value = value

    


    def serialize(self):
        data = super(ControlPlayer,self).serialize()
        capture = self.value

        if capture:
            _, image = capture.read()

            if isinstance(image, np.ndarray):
                image = self.process_frame_event(image)
                if isinstance(image, list) or isinstance(image, tuple): image = tools.groupImage(image, True)
                
                if len(image.shape)>2: image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
          
                image = Image.fromarray(image)
                buff = BytesIO()
                image.save(buff, format="PNG")
                content = buff.getvalue()
                buff.close()
                data.update({ 'base64content': base64.b64encode(content) })

            data.update({ 'value':       self._filename   })
            data.update({ 'filename':    self._filename   })
            data.update({ 'startFrame':  0                })
            data.update({ 'endFrame':    1000             })
            data.update({ 'video_index': self.video_index })
        else:
            data.update({ 'base64content': 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=' })

        return data


    def deserialize(self, data):
        super(ControlPlayer,self).deserialize(data)
        self.video_index = data.get('video_index', 0)
         
    @property
    def video_index(self):
        if self._value:
            return int(self._value.get(1))
        elif self._filename:
            return self._video_index
        else:
            return 0

    @video_index.setter
    def video_index(self, value):
        
        if self._value:
            self._value.set(1, float(value))
            self.mark_to_update_client()
        
        elif self._filename: 
            self._video_index = float(value)
            self.mark_to_update_client()

        

    @property
    def image(self): 
        _, image = self._value.read()
        return image