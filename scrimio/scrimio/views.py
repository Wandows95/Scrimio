from django.shortcuts import render

# Scrimio Home Page
def index(request):
	return render(request, 'scrimio/index.html')