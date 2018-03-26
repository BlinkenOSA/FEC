from django.conf import settings
from django.utils import translation
from wagtailtinymce.rich_text import TinyMCERichTextArea


class TinyMCEEditorObject(TinyMCERichTextArea):
    options = {
            'buttons': [
                [
                    ['undo', 'redo'],
                    ['bold', 'italic', 'styleselect'],
                    ['bullist', 'numlist', 'outdent', 'indent'],
                    ['link', 'unlink'],
                    ['wagtaildoclink', 'wagtailimage', 'wagtailembed'],
                    ['code']
                ]
            ],
            'menus': False,
            'options': {
                'browser_spellcheck': True,
                'noneditable_leave_contenteditable': False,
                'language': 'EN',
                'language_load': True
            },
        }

    def __init__(self, attrs=None, **kwargs):
        translation.trans_real.activate(settings.LANGUAGE_CODE)
        super(TinyMCEEditorObject, self).__init__(attrs)
        self.kwargs.update(self.options)
