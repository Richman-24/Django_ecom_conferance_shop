from django import forms

from goods.models import Comment

# Сделать валидатор оценки от 1 ло 5, и в базе тоже
# Добавить фильт матерных слов

class CommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Введите текст комментария",
                "rows": 5,
            }
        ),
    )
    rating = forms.IntegerField()

    class Meta:
        model = Comment
        fields = ("text", "rating")
