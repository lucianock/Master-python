from django.shortcuts import render

# Create your views here.
def page(request):

    return render(request, "pages/page.html", {
        "title" : "Pagina invidiual",
        "page" : "Hola Mundo desde la app Pages"
    })