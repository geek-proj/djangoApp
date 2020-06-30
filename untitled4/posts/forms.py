from django import forms
from .models import Posts,Comments
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class PostForm(forms.ModelForm):

    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder':''})
    )
    image = forms.ImageField()

    class Meta:
        model = Posts
        fields = ('text','image')


    def save(self, user):
        post = Posts.objects.create(user=user,
                                    text=self.cleaned_data['text'],
                                    image=self.cleaned_data['image'])
        return post


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': ''})
    )

    class Meta:
        model = Comments
        fields = ('text',)

    def save(self, post):
        comment = Comments.objects.create(post=post,
                                       text=self.cleaned_data['text'])
        return comment