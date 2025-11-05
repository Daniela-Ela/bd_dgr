#Suponiendo un diccionario con al siguiente estructura, crea un programa que calcule cuántas categorías hay, cuántos productos tiene cada categoría y cuántos productos hay en total.
productos = {
    "Electrónica": ["Smartphone", "Laptop", "Tablet", "Auriculares", "Smartwatch"],
    "Hogar": ["Aspiradora", "Microondas", "Lámpara", "Sofá", "Cafetera"],
    "Ropa": ["Camisa", "Pantalones", "Chaqueta", "Zapatos", "Bufanda"],
    "Deportes": ["Pelota de fútbol", "Raqueta de tenis", "Bicicleta", "Pesas", "Cuerda de saltar"],
    "Juguetes": ["Muñeca", "Bloques de construcción", "Peluche", "Rompecabezas", "Coche de juguete"],
}
categorias = 0
procat = 0
producto = 0
for i in range(len(productos)):
    categorias += 1
    for j in productos[list(productos.keys())[i]]:
        procat += 1
        producto += 1
    print(f"Categoría: {list(productos.keys())[i]} - {procat} productos")
    procat = 0
print(f"Total de categorías: {categorias}")
print(f"Total de productos: {producto}")

    