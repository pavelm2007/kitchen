from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from .models import Category, Tip


class TipList(ListView):
    model = Tip
    paginate_by = 10
    paginator_class = Paginator
    template_name = 'tips/tip_list.html'

class TipDetail(DetailView):
    model = Tip
    template_name = 'tips/tip_detail.html'