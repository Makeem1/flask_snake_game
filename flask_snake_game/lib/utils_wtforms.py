from flask_wtf import Form

class ModelForm(Form):
    """External class written by Nick for copying flask_wtf's Form crsf protection"""
    def __init__(self, obj=None, prefix='', **kwargs):
        Form.__init__(
            self, obj=obj, prefix=prefix, **kwargs
        )
        self._obj = obj