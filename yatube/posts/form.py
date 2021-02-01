from django import forms
from .models import Post
from group.models import Group


class PostForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False,
                                   label='Рубрика', widget=forms.widgets.Select())

    class Meta:
        model = Post
        fields = ('group', 'text')