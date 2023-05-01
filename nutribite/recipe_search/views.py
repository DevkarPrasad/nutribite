from django.shortcuts import render
from . import config
from django.http import HttpResponse
import json
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def recipe_search(request):
    recipes_page = None  # Define recipes_page with a default value

    # Check if request method is POST
    if request.method == 'POST':
        # Get search parameters from form data
        query = request.POST.get('query')
        health = request.POST.get('health')
        diet = request.POST.get('diet')
        cuisine = request.POST.get('cuisine')
        meal_type = request.POST.get('meal_type')

        # Construct API URL and parameters
        url = f'https://api.edamam.com/api/recipes/v2?type=public&q={query}'
        params = {'app_id': config.EDAMAM_APP_ID, 'app_key': config.EDAMAM_API_KEY}

        # Add optional search parameters to API URL
        if health:
            url += '&health=' + health
        if diet:
            url += '&diet=' + diet
        if cuisine:
            url += '&cuisineType=' + cuisine
        if meal_type:
            url += '&mealType=' + meal_type

        # Send API request and get results
        response = requests.get(url, params=params)
        results = response.json()

        # Check API response status code
        if response.status_code == 200:
            hits = results.get('hits')
            recipes = [hit.get('recipe') for hit in hits]

            # Paginate recipes list
            paginator = Paginator(recipes, 10)
            page_number = request.GET.get('page')
            try:
                recipes_page = paginator.page(page_number)
            except PageNotAnInteger:
                recipes_page = paginator.page(1)
            except EmptyPage:
                recipes_page = paginator.page(paginator.num_pages)
            context = {'hits': hits , 'recipes': recipes_page}
            return render(request, 'recipes_search/recipe.html', context)

        # Handle API errors
        elif response.status_code in [400, 401, 403, 404]:
            context = {'error': 'Invalid request or credentials'}
            return render(request, 'recipes_search/error.html', context)

        elif response.status_code == 429:
            context = {'error': 'API rate limit exceeded'}
            return render(request, 'recipes_search/error.html', context)

        else:
            context = {'error': 'Unknown error'}
            return render(request, 'recipes_search/error.html', context)

    # Render recipe.html template with context
    context = {'recipes_page': recipes_page}  # Assign recipes_page to context
    return render(request, 'recipes_search/recipe.html', context)