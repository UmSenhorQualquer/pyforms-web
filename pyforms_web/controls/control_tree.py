from pyforms_web.controls.control_base import ControlBase
import simplejson

class TreeNode(object):

    node_id_counter = 0

    def __init__(self, name, parent=None, icon=None):
        TreeNode.node_id_counter += 1

        self.childs  = []
        self.name    = name
        self.parent  = parent
        self.icon    = icon
        self.node_id = str(TreeNode.node_id_counter)

        if parent is not None:
            parent.childs.append(self)

    def to_dict(self):
        data = {'name': self.name, 'icon': self.icon, 'node_id': self.node_id}
        data['childs'] = [child.to_dict() for child in self.childs]
        return data



class ControlTree(ControlBase):

    def __init__(self, *args, **kwargs):
        self.root = TreeNode('Root')
        super().__init__(*args, **kwargs)

    def init_form(self):
        return "new ControlTree('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )

    def create_child(self, name, parent=None, icon=None):
        if parent is None: parent = self.root
        return TreeNode(name, parent, icon)

    def find_node_id(self, node_id, node=None):
        if node_id is None: return None

        if node.node_id==node_id:
            return node
        else:
            for n in node.childs:
                res = self.find_node_id(node_id, n)
                if res: return res
            return None


    def serialize(self):
        data = super().serialize()
        data.update({
            'root':  self.root.to_dict(),
            'value': self._value.node_id if self._value else None
        })
        return data


    def deserialize(self, properties):
        if properties.get('value', None):
            properties['value'] = self.find_node_id( 
                properties.get('value', None),
                self.root
            )
        
        super().deserialize(properties)
        