from django.http import Http404
from django.db.models import Q
from utils.pagination import make_pagination
from recipes.models import Recipe, Category
from django.shortcuts import get_list_or_404, render
# Create your views here.

def home(request):
    recipes = Recipe.objects.filter(
        is_published = True
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, 12)

    return render(request, 'recipes/pages/home.html', context={
        'recipes': page_obj,
        'pages': pagination_range
    })

def category(request, category_id):
    recipes = get_list_or_404(
        Category.objects.get(
            id = id,
            is_published = True,
        ).order_by('-id')
    )

    page_obj, pagination_range = make_pagination(request, recipes, 6)

    return render(request, 'recipes/pages/category.html', context={
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title': f'{recipes[0].category.name} - Category |'
    })

def recipe(request, id):
    recipes = Recipe.objects.get(id=id)
    return render(request, 'recipes/pages/recipe.html', context={
        'recipe': recipes,
        'is_detail_page': True,
    })

def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains = search_term) | 
            Q(description__icontains = search_term),
        ),
        is_published = True,
    )

    page_obj, pagination_range = make_pagination(request, recipes, 6)
    
    return render(request, 'recipes/pages/search.html',{
        'title': f'search for "{search_term}"',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'addtional_url_query': f'&q={search_term}',
    })