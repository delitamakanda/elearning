from django import forms
from blog.models import Post, Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    to = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'form-control'}))


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))

    class Meta:
        model = Comment
        fields = ('body',)


class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    header = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    status = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'form-control'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Post
        fields = ('title', 'header', 'body', 'status', 'tags',)
