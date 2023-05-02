from django.shortcuts import render
from . import config
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
import json
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View


def food_search(request):
    results = []

    # Check if request method is POST
    if request.method == 'POST':
        # Get search parameters from form data
        query = request.POST.get('query')
        min_calories = request.POST.get('min_calories')
        max_calories = request.POST.get('max_calories')
        health = request.POST.get('health')
        diet = request.POST.get('diet')
        cuisine = request.POST.get('cuisine')
        meal_type = request.POST.get('meal_type')

        # Construct API URL and parameters
        app_id = config.EDAMAM_APP_ID
        app_key = config.EDAMAM_API_KEY
        url = f'https://api.edamam.com/api/food-database/v2/parser?app_id={app_id}&app_key={app_key}&ingr={query}&nutrients=ENERC_KCAL'

        if min_calories:
            url += f'&nutrients.ENERC_KCAL.min={min_calories}'
        if max_calories:
            url += f'&nutrients.ENERC_KCAL.max={max_calories}'
        if health:
            url += '&health=' + health
        if diet:
            url += '&diet=' + diet
        if cuisine:
            url += '&cuisineType=' + cuisine
        if meal_type:
            url += '&mealType=' + meal_type

        # Send API request and get results
        response = requests.get(url)
        data = response.json()
        hits = data.get('hints')

        # Check if results exist
        if hits:
            foods = [hit.get('food') for hit in hits]

            # Paginate results
            paginator = Paginator(foods, 20) # Show 20 foods per page
            page_number = request.GET.get('page')
            try:
                foods_page = paginator.page(page_number)
            except PageNotAnInteger:
                foods_page = paginator.page(1)
            except EmptyPage:
                foods_page = paginator.page(paginator.num_pages)

            # Build context for rendering results
            context = {'foods': foods_page, 'query': query}

            # Render food.html template with context
            return render(request, 'food_search/food.html', context)
        else:
            # Build context for rendering "No results found" message
            context = {'query': query}

            # Render no_results.html template with context
            return render(request, 'food_search/error.html', context)

    # Render search.html template if request method is not POST
    return render(request, 'food_search/food.html')

    
'''
import requests
from django.shortcuts import render

def nutrients_view(request):
    if request.method == 'POST':
        food_id = request.POST['food_id']
        measure_uri = request.POST['measure_uri']
        quantity = request.POST['quantity']
        app_id = config.EDAMAM_APP_ID # replace with your app ID
        app_key = config.EDAMAM_API_KEY # replace with your app key
        url = f'https://api.edamam.com/api/food-database/v2/nutrients?app_id={app_id}&app_key={app_key}'
        payload = {
            'ingredients': [{
                'foodId': food_id,
                'measureURI': measure_uri,
                'quantity': quantity
            }]
        }
        response = requests.post(url, json=payload)
        data = response.json()
        return render(request, 'nutrients_results.html', {'data': data})
    return render(request, 'nutrients_form.html')

'''




'''
class NutrientsView(View):
    
    def post(self, request, food_id,measure_uri):
        api_id = config.EDAMAM_APP_ID
        api_key = config.EDAMAM_API_KEY

        
        if not measure_uri:
            return HttpResponseBadRequest("Invalid request: measure_uri is required.")
        
        url = 'https://api.edamam.com/api/food-database/v2/nutrients'
        payload = {'app_id': api_id, 'app_key': api_key, 'ingredients': [{'quantity': 1, 'measureURI': 'measure_uri', 'foodId': food_id}]}
        response = requests.post(url, json=payload)
        
        if response.status_code != 200:
            return HttpResponseBadRequest(f"Failed to retrieve nutrient information: {response.json()['message']}")
        
        data = response.json()
        nutrients = data['totalNutrients']
        diet_labels = data.get('dietLabels', [])
        health_labels = data.get('healthLabels', [])
        
        return render(request, 'food_search/nutrients.html', {'nutrients': nutrients, 'diet_labels': diet_labels, 'health_labels': health_labels})
'''