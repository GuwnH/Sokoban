from django import forms
from .models import Guide

class GuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = ['game', 'guide_level', 'guide_text', 'number_of_moves', 'colors_required']
        widgets = {
            'game': forms.Select(attrs={'class': 'form-control'}),
            'guide_level': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter level number'}),
            'guide_text': forms.Textarea(attrs={'class': 'form-control', 'maxlength': '10000', 'placeholder': 'Write your guide...'}),
            'number_of_moves': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter number of moves'}),
            'colors_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }