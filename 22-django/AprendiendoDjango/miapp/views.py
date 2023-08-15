from django.shortcuts import render, HttpResponse, redirect
from miapp.models import Article
from django.db.models import Q
from miapp.forms import FormArticle
from django.contrib import messages

# Create your views here.
# MVC = Modelo Vista Controlador -> Acciones (metodos)
# MVT = Modelo Template Vista -> Acciones (metodos)

layout = """
<h1>Sitio web con Django | Víctor Robles</h1>
<hr/>
<ul>
    <li>
        <a href="/inicio">Inicio</a>
    </li>
    <li>
        <a href="/hola-mundo">Hola Mundo</a>
    </li>
    <li>
        <a href="/pagina-pruebas">Página de pruebas</a>
    </li>
    <li>
        <a href="/contacto-dos">Contacto</a>
    </li>
</ul>
<hr/>
"""

def index(request):
    
    """
    html = ""
        <h1>Inicio</h1>
        <p>Años hasta el 2050:</p>
        <ul>
    ""
    year = 2021
    while year <= 2050:

        if year % 2 == 0:
            html += f"<li>{str(year)}</li>"

        year += 1

    html += "</ul>"
    """
    year = 2021
    hasta = range(year, 2051)

    nombre = 'Víctor Robles 2'
    lenguajes = ['JavaScript', 'Python', 'PHP', 'C']

    return render(request, 'index.html', {
        'title': 'Inicio 2',
        'mi_variable': 'Soy un dato que está en la vista',
        'nombre': nombre,
        'lenguajes': lenguajes,
        'years': hasta
    })

def hola_mundo(request):
    return render(request, 'hola_mundo.html')

def pagina(request, redirigir=0):

    if redirigir == 1:
        return redirect('contacto', nombre="Víctor", apellidos="Robles")

    return render(request, 'pagina.html', {
        'texto': 'Este mi texto',
        'lista': ['uno', 'dos', 'tres']
    })

def contacto(request, nombre="", apellidos=""):
    html = ""

    if nombre and apellidos:
        html += "<p>El nombre completo es:</p>"
        html += f"<h3>{nombre} {apellidos}<h3>"

    return HttpResponse(layout+f"<h2>Contacto</h2>"+html)


def crear_articulo(request, title, content, public):
    articulo = Article(
        title = title,
        content = content,
        public = public
    )

    articulo.save()

    return HttpResponse(f"Articulo creado: <strong>{articulo.title}</strong> - {articulo.content}")

def save_article(request):

    if request.method == 'POST':

        title = request.POST['title']

        if len(title) <= 5:
            return HttpResponse("El titulo es muy pequeño")        

        content = request.POST['content']
        public = request.POST['public']

        articulo = Article(
            title = title,
            content = content,
            public = public
        )

        articulo.save()

        return HttpResponse(f"Articulo creado: <strong>{articulo.title}</strong> - {articulo.content}")

    else:
        return HttpResponse("<h2>No se ha podido crear el articulo</h2>")        


def create_article(request):

    return render(request, 'create_article.html')


def create_full_article(request):

    if request.method == 'POST':

        formulario = FormArticle(request.POST)

        if formulario.is_valid():
            data_form = formulario.cleaned_data

            title = data_form.get('title')
            content = data_form['content']
            public = data_form['public']

            articulo = Article(
                title = title,
                content = content,
                public = public
            )

            articulo.save()

            # Crear mensaje flash (sesión que solo se muestra 1 vez)
            messages.success(request, f'Has creado correctamente el articulo {articulo.id}')

            return redirect('articulos')
            # return HttpResponse(articulo.title + ' - ' + articulo.content + ' - ' + str(articulo.public))

    else:
        formulario = FormArticle()

    return render(request, 'create_full_article.html', {
        'form': formulario
    })


def articulo(request):
    
    try:
        articulo = Article.objects.get(title="Superman", public=False)
        response = f"Articulo: <br/> {articulo.id}. {articulo.title}"
    except:
        response = "<h1>Artículo no encontrado</h1>"

    return HttpResponse(response)

def editar_articulo(request, id):

    articulo = Article.objects.get(pk=id)

    articulo.title = "Batman"
    articulo.content = "Pelicula del 2017"
    articulo.public = True

    articulo.save()

    return HttpResponse(f"Articulo {articulo.id} editado: <strong>{articulo.title}</strong> - {articulo.content}")

def articulos(request):

    articulos = Article.objects.filter(public=True).order_by('-id')

    """
    articulos = Article.objects.filter(id__lte=12, title__contains="2")

    articulos = Article.objects.filter(
        Q(title__contains="2") | Q(public=True)
    )

    articulos = Article.objects.filter(
                                    title="Articulo",
                                ).exclude(
                                    public=False
                                )
    """
    # articulos = Article.objects.raw("SELECT * FROM miapp_article WHERE title='Articulo 2' AND public=0 ")

    return render(request, 'articulos.html', {
        'articulos': articulos
    })

def borrar_articulo(request, id):
    articulo = Article.objects.get(pk=id)
    articulo.delete()

    return redirect('articulos')

    