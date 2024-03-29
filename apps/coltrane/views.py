from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from .models import Category, Entry


# def category_detail(request, slug):
#     category = get_object_or_404(Category, slug=slug)
#     return object_list(request, queryset=category.live_entry_set(), extra_context={
#         'category': category
#     })


class EntryList(ListView):
    model = Entry
    paginate_by = 10
    paginator_class = Paginator
    template_name = 'coltrane/entry_list.html'

class EntryDetail(DetailView):
    model = Entry
    template_name = 'coltrane/entry_detail.html'