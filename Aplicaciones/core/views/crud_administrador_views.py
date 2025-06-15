from django.db import transaction
from django.shortcuts import render, redirect


def index(request):
    return render(request, 'administrador/index.html')

def create(request):
    return render(request, 'administrador/create.html')

