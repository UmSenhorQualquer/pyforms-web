import datetime
from pyforms_web.controls.control_base import ControlBase
import simplejson

class ControlPieChart(ControlBase):

	def __init__(self, *args, **kwargs):
		self._legend = []
		super(ControlPieChart, self).__init__(*args, **kwargs)

	def init_form(self): return "new ControlPieChart('{0}', {1})".format( self._name, simplejson.dumps(self.serialize()) )



	@property
	def legend(self):return self._legend
	@legend.setter
	def legend(self, value):
		if self._legend!=value: self.mark_to_update_client()
		self._legend = value


	@property
	def value(self):
		rows = []
		for row in self._value:
			new_row = []
			for value in row:
				if value is None: break
				if isinstance(value[0], datetime.datetime): value[0] = str(value[0])
				if isinstance(value[0], datetime.date): value[0] = str(value[0])
				if isinstance(value[0], str): value[0] = str(value[0])
				if isinstance(value[1], str): value[1] = str(value[1])
				new_row.append(value)
			rows.append(new_row)
		return rows

	@value.setter
	def value(self, value): ControlBase.value.fset(self, value)


	def serialize(self):
		data  = ControlBase.serialize(self)
		data.update({ 
			'legend': 	self.legend, 
			'value': 	self._value 
		})
		return data


	def deserialize(self, properties):
		ControlBase.deserialize(self, properties)
		self.legend = properties[u'legend']
		self.value 	= properties[u'value']
		