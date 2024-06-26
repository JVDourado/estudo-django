from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import Registerform

def register_view(request):

    register_form_data = request.session.get('register_form_data', None)

    form = Registerform(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
    })

def register_create(request):
    if not request.POST:
        raise Http404()
    
    POST = request.POST
    request.session['register_form_data'] = POST
    form = Registerform(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'User created successfully, please log in.')
    
        del(request.session['register_form_data'])
    
    return redirect ('authors:register')