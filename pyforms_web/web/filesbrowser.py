from django.core.exceptions import ObjectDoesNotExist
from pyforms_web.basewidget import BaseWidget
from pyforms_web.controls.control_text import ControlText
from pyforms_web.controls.control_combo import ControlCombo
from pyforms_web.controls.control_list import ControlList
from pyforms_web.controls.control_checkbox import ControlCheckBox
from pyforms_web.controls.control_button import ControlButton
from pyforms_web.web.middleware import PyFormsMiddleware
from django.utils import timezone

import uuid, time, os

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1000.0: return "%3.1f%s" % (num, x)
        num /= 1000.0
    return "%3.1f%s" % (num, 'TB')


class FilesBrowserApp(BaseWidget):

    TITLE = 'Files browser'
    LAYOUT_POSITION = 4
    
    def __init__(self, *args, **kwargs):
        super(FilesBrowserApp,self).__init__(*args, **kwargs)
        
        self._control_id    = ControlText('Input id')
        self._only_folders  = ControlCheckBox('Only folders')
        self._directory     = ControlText(
            'Current directory',
            default='/'
        )
        self._files_table   = ControlList(
            'Files',
            horizontal_headers=['','File','Type','Size'],
            select_entire_row=True,
            readonly=True,
            row_double_click_event=self.__file_dblclick
        )
        
        self._formset = [
            '_directory',
            '_files_table',
        ]

        self.file_selected_event = kwargs.get('file_selected_event', self.file_selected_event)

        self.populate_table()



    def file_selected_event(self, filepath):
        pass


    def __file_dblclick(self):
        selected_row = self._files_table.value[self._files_table.selected_row_index]
        filename     = selected_row[1]
        filepath     = os.path.join(self._directory.value, filename)

        if os.path.isdir(filepath):
            if selected_row[1]=='..':
                self._directory.value = os.path.dirname(self._directory.value)
            else:
                self._directory.value = filepath
            self.populate_table()
        else:
            self.file_selected_event(filepath)

    def populate_table(self):
        request     = PyFormsMiddleware.get_request()
        self._directory.value = request.GET.get('p',self._directory.value)
        #storage    = conf.MAESTRO_STORAGE_MANAGER.get(request.user)
        path        = self._directory.value


        files       = []
        for index, filename in enumerate( os.listdir(path) ):
            filepath = os.path.join(path, filename)
            is_dir   = os.path.isdir(filepath)
            filetype = ''
            filesize = 0
            if not is_dir:
                _, filetype = os.path.splitext(filename)
                filetype = filetype[1:]
                filesize = os.path.getsize(filepath)

            if self._only_folders.value and not is_dir: continue

            link     = ''
            function = ''
            if is_dir:
                #function = 'javascript:add_file2control("{1}", "{0}");'.format(f.fullpath, self._control_id.value)
                link = """<a target='_blank' href='{0}' ><i class='selected radio icon' ></id></a>""".format( function )

            if self._only_folders.value:
                #function = 'javascript:add_file2control("{1}", "{0}");'.format(f.fullpath, self._control_id.value)
                link = """<a target='_blank' href='{0}' ><i class='selected radio icon' ></id></a>""".format( function )

            files.append([
                "<i class='folder icon' ></id>" if is_dir else "<i class='file outline icon' ></id>",
                filename, 
                filetype, 
                '' if is_dir else sizeof_fmt( filesize ),
            ])

        self._files_table.value = ([['','..', 'dir']] if path!='/' else []) + sorted(files, key=lambda a: (a[2], a[1]))

