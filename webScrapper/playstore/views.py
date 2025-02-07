from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.http import JsonResponse
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
from .models import TopApps, Category
import time
import threading
import queue


# Create your views here.
def top_apps(request):
    payload = {}
    for category in Category.objects.all():
        apps = TopApps.objects.filter(category=category).values()
        payload[category.name] = apps

    return render(request, 'top_apps.html', {'payload': payload})

def get_top_apps(output_queue: queue.Queue) -> None:
    url = 'https://play.google.com/store/games?hl=en_GB'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'sT93pb.DdYX5.OnEJge'))
    )

    tops = {
        'Top for': [],
        'Top grossing': [],
        'Top selling': []
    }

    for top_name in tops.keys():
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{top_name}')]"))
        )
        button.click()
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        parent_list = soup.select_one('div[jsname="fh1pXc"]')
        if parent_list:
            for application in parent_list.select('.Si6A0c.itIJzb'):
                app = {
                    'name': application.select_one('div[jsname="fh1pXc"] .sT93pb.DdYX5.OnEJge').text if application.select_one('div[jsname="fh1pXc"] .sT93pb.DdYX5.OnEJge') else None,
                    'score': float(application.select_one('span.sT93pb.CKzsaf .w2kbF').text) if application.select_one('span.sT93pb.CKzsaf .w2kbF') else None,
                    'icon': application.select_one('img').get('src') if application.select_one('img') else None,
                    'tags': ', '.join([tag.text for tag in application.select('div.ubGTjb .sT93pb.w2kbF')[:-1]]) if application.select('div.ubGTjb .sT93pb.w2kbF') else None,
                    'webpage': application.get('href') if application.get('href') else None
                }
                tops[top_name].append(app)

    driver.quit()
    output_queue.put(tops)

def set_database(top_apps: dict) -> None:
    TopApps.objects.all().delete()

    for category_name, apps in top_apps.items():
        category, _ = Category.objects.get_or_create(name=category_name)
        for app in apps:
            app_obj = TopApps.objects.create(
                name=app['name'],
                category=category,
                score=app['score'],
                icon=app['icon'],
                tags=app['tags'],
                webpage=app['webpage']
            )
            app_obj.save()

def fetch_top_apps():
    payload = {}
    for category in Category.objects.all():
        apps = TopApps.objects.filter(category=category).values()
        payload[category.name] = list(apps)  # Convert queryset to list
    return payload

@api_view(['POST'])
def update_top_apps(request):
    top_apps = queue.Queue()
    apps_thread = threading.Thread(target=get_top_apps, args=(top_apps,))
    apps_thread.start()
    apps_thread.join()
    set_database(top_apps.get())
    return JsonResponse({'status': 'success', 'message': 'Top apps updated successfully'})

@api_view(['GET'])
def get_apps(request):
    payload = fetch_top_apps()
    return JsonResponse(payload)