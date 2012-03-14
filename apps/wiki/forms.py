from django.forms import forms, ModelForm
from apps.wiki.models import *
class TextForm(ModelForm):
	class Meta:
		model = Section
		fields =('title', 'content')
		widgets = {
			'content': forms.Textarea(attrs = {'cols':100, 'rows': 20}),
			}
class CreateWikiForm(ModelForm):
	class Meta:
		model = Wiki
		fields = ('title','description', 'gradelevel','subject','lessontype')
class ImageForm(ModelForm):
	class Meta:
		model = Image
		fields = ('title','photo')