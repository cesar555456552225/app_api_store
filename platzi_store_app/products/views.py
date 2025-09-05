import requests
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader


def consultar_productos():
    url = "https://api.escuelajs.co/api/v1/products"
    response = requests.get(url)
    productos = []
    if response.status_code == 200:
        datos = response.json()
        for producto in datos:
            productos.append({
                "id": producto.get("id"),
                "titulo": producto.get("title"),
                "precio": producto.get("price"),
                "descripcion":producto.get("description"),
                "categoria": producto.get("category", {}).get("name"),
                "imagen": producto.get("images", [None])[0]
            })
    return productos

def producto_id(request, pk):
    url = f"https://api.escuelajs.co/api/v1/products/{pk}"
    response = requests.get(url)
    producto = None
    if response.status_code==200:
        datos =response.json()
        producto = ({
            "id" : datos.get("id"),
            "titulo" : datos.get("title"),
            "precio" : datos.get("price"),
            "categoria" : datos.get("category", {}).get("name"),
            "imagen" : datos.get("images", [None])[0],
        })
    return render(request, "detalle.producto.html", {"producto": producto})

def productos_view(request):
    productos = consultar_productos()
    return render(request, "lista_productos.html", {"productos": productos})



def agregar_producto(request):
    if request.method == "POST":
        url = "https://api.escuelajs.co/api/v1/products/"
        producto = {
            "title": request.POST.get("title"),
            "price": int(request.POST.get("price")),
            "description": request.POST.get("description"),
            "categoryId": int(request.POST.get("categoryId")),
            "images": [request.POST.get("image_url")]
        }
        response = requests.post(url, json=producto)
        if response.status_code == 201:
            return redirect("productos_view")
        else:
            error = response.text
            return render(request, "agregar_producto.html", {"error": error})
    return render(request, "agregar_producto.html")

def main(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def actualizar_producto(request, pk):
    url = f"https://api.escuelajs.co/api/v1/products/{pk}"
    if request.method == "POST":
        producto = {
            "title": request.POST.get("title"),
            "price": int(request.POST.get("price")),
            "description": request.POST.get("description"),
            "categoryId": int(request.POST.get("categoryId")),
            "images": [request.POST.get("image_url")]
        }
        response = requests.put(url, json=producto)
        if response.status_code == 200:
            return redirect("productos_view")
        else:
            error = response.text
            return render(request, "actualizar_producto.html", {"error": error, "pk": pk})
    else:
        response = requests.get(url)
        producto = None
        if response.status_code == 200:
            datos = response.json()
            producto = {
                "title": datos.get("title"),
                "price": datos.get("price"),
                "description": datos.get("description"),
                "categoryId": datos.get("category", {}).get("id"),
                "image_url": datos.get("images", [None])[0]
            }
        return render(request, "actualizar_producto.html", {"producto": producto, "pk": pk})

def eliminar_producto(request, pk):
    url=f"https://api.escuelajs.co/api/v1/products/{pk}"
    if request.method == "POST":
        response=requests.delete(url)
        if response.status_code == 200:
            return redirect("productos_view")
        else:
            error = response.text
            return render(request,"lista_productos.html", {"error":error, "pk":pk})
    else:
        return redirect("productos_view")