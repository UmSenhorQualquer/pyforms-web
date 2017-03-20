from funding_opportunities_models.models import FundingOpportunity
from pyforms_web.web.BaseWidget import BaseWidget
from pyforms_web.web.Controls.ControlQueryList import ControlQueryList
from orquestra.plugins import LayoutPositions
from funding_opportunities_apps.app_viewfund import ViewFundApp

class ModelListAdmin(BaseWidget):
	

	_uid 			= 'latest-opportunities-app'
	#groups	 		= ['superuser']
	icon			= 'dollar'
	label 			= 'Latest opportunities'
	menu 			= 'dashboard'
	menu_order 		= 0
	layout_position = LayoutPositions.APPEND_HOME
	
	def __init__(self):
		super(ReadOnlyModelAdmin, self).__init__(self.label)

		self._list = ControlQueryList('Latest inserted opportunities')

		self._list.item_selection_changed_event = self.__item_selection_changed_event

		self.formset = ['_list']
		self.populate_list()

	def populate_list(self):
		self._list.list_display = ['fundingopportunity_name','fundingopportunity_value','currency__currency_name' ]
		self._list.value = FundingOpportunity.objects.order_by('-pk')[:5]

	def __item_selection_changed_event(self):
		a = ViewFundApp(self._list.selected_row_id)
		a._uid = self._list.selected_row_id