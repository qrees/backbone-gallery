from django import forms

from albums.models import File


class FileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ('file', 'album')

    def save(self, commit=True):
        instance = super(FileForm, self).save(commit=False)
        instance.name = instance.file.name
        if commit:
            instance.save()
        return instance