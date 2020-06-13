from django import forms
from tinymce.models import HTMLField
from ckeditor_uploader.fields import RichTextUploadingField
from .models import BlogPost,Comment,Category

class BlogForm(forms.ModelForm):

	title = forms.CharField(required=True,label='Title',max_length=100,widget=forms.TextInput(attrs={'class': 'input--style-6'}))
	category = forms.ModelChoiceField(queryset=Category.objects.all(),required=True,widget=forms.Select(attrs={'class': 'input--style-6'}))
	image= forms.FileField(required=False,widget=forms.FileInput())
	body=RichTextUploadingField()
	class Meta:
		model = BlogPost
		fields = ['title','category','body','image']


class CommentForm(forms.ModelForm):
	body=forms.CharField(required=True,label='',widget=forms.TextInput(attrs={'class': 'form-control form-control-pill'}))
	class Meta:
		model = Comment
		fields = ['body']