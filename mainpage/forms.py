from django.forms import  ModelForm
from .models import Article



class AddPost(ModelForm):
    """form for articles"""
    class Meta:
        model = Article
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs['.class'] = 'form-control'

        def save(self, commit=True):
            form = super().save(commit=False)
            if commit:
                form.save()
            return form


