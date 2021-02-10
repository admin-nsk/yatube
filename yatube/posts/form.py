from django import forms
from .models import Post, Comments
from group.models import Group


class PostForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False,
                                   label='Рубрика', widget=forms.widgets.Select())

    class Meta:
        model = Post
        fields = ('group', 'text', 'image')


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ('text',)
        labels = {'text': 'Комментарий'}
        widgets = {'text': forms.Textarea()}