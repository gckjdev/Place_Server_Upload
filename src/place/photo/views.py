from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
from orange.django.place.models import Photo
from orange.django.place.utils import get_json_response

def upload(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('success')
    else:
        form = PhotoForm()
    return render_to_response('upload.html', {'form': form})

def get(request, post_id):
    photos = Photo.objects.all()
    return get_json_response(Photo, photos)

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo

