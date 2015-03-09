from django.template.loader import get_template
from django.template import Template, Context
from django.shortcuts import render_to_response
from django.http import HttpResponse
from newbooks.models import Book, MyModel
#from django.views.generic.simple import direct_to_template

def base(request):
    return render_to_response('base.html')

def book_list(request):
    names = 'Django book'
    return render_to_response('book_list.html',{'names':names})

def dislpay_meta(request):
    try:
        values = request.META.items()
        values.sort()
    except KeyError:
        values = ('value','unknown')
    return render_to_response('meta.html', {'values':values})

def search_form(request):
    return render_to_response('search_form.html')

def search(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        elif len(q) > 20:
            errors.append('Please enter at most 20 characters.')
        else:
            books = Book.objects.filter(title__icontains=q)
            return render_to_response('search_results.html', {'books': books, 'query': q})
    return render_to_response('search_form.html', {'errors':errors })
    
def foobar_view(request, template_name):
    m_list = MyModel.objects.filter(author='kk')
    print m_list
    return render_to_response(template_name, {'m_list': m_list})

def my_view(request, month, day):
    l_list = []
    l_list.append(month)
    l_list.append(day)
    return render_to_response('template1.html', {'m_list': l_list})

def event_list(request, model):
    obj_list = model.objects.all()
    template_name = 'mysite/%s_list.html' % model.__name__.lower()
    return render_to_response(template_name, {'object_list': obj_list})

def method_splitter(request, *args, **kwargs):
    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)
    if request.method == 'GET' and get_view is not None:
        return get_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
        return post_view(request, *args, **kwargs)
    raise Http404

def about_pages(request, page):
    return ''
