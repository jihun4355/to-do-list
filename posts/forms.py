# from django import forms
# from .models import Post

# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
       
#         #fields = ('title', 'content', 'writer')
# #------------------------------------
#         fields = ['title', 'content', 'writer', 'due_date', 'is_completed', 'priority']
#         widgets = {
#             'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
#         }

#     def __init__(self, *args, **kwargs):
#         super(PostForm, self).__init__(*args, **kwargs)
#         self.fields['due_date'].input_formats = ('%Y-%m-%dT%H:%M',)
# #------------------------------------        




from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'due_date', 'is_completed', 'priority']  # 필요한 필드만 포함시킵니다.
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'content': '내용',
            'due_date': '작업 날짜',
            'is_completed': '완료 여부',
            'priority': '중요도',
        }