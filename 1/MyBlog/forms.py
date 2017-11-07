from django import forms


# Create your tests here.
class MsgPostForm(forms.Form): 
        rcontent = forms.CharField(widget=forms.Textarea(attrs={'size':500})) 
        def clean_contents(self):         
            contents=self.cleaned_data.get('rcontent','')         
            num_words=len(contents.split())         
            if num_words < 4:             
                raise forms.ValidationError('Not enough words!')         
            return contents
