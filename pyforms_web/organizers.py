class no_columns(object):
    def __init__(self, *args, **kwargs):
        self.css   = kwargs.get('css', '')
        self.style = kwargs.get('style', '')
        self.items = args
    def __getitem__(self,index): return self.items[index]
    def __setitem__(self,index,value): self.items[index] = value
    def __len__(self):  return len(self.items)
    def __iter__(self): 
        self._index = -1; return self
    def __next__(self): 
        self._index += 1
        if self._index>=len(self.items): raise StopIteration
        return self.items[self._index]


class segment(object):
    def __init__(self, *args, **kwargs): 
        self.css   = kwargs.get('css', '')
        self.field_css   = kwargs.get('field_css', '')
        self.style = kwargs.get('style', '')
        self.field_style = kwargs.get('field_style', '')
        self.items = args
    def __getitem__(self,index): return self.items[index]
    def __setitem__(self,index,value): self.items[index] = value
    def __len__(self):  return len(self.items)
    def __iter__(self): 
        self._index = -1; return self
    def __next__(self): 
        self._index += 1
        if self._index>=len(self.items): raise StopIteration
        return self.items[self._index]
