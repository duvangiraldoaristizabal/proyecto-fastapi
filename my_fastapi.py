# main.py - La aplicación más simple del mundo 

from fastapi import FastAPI 

from fastapi.responses import HTMLResponse 

 

# Crear la aplicación 

app = FastAPI(title="Mi Primera App en Azure") 

 

# La página principal (HTML integrado) 

PAGINA_PRINCIPAL = """ 

<!DOCTYPE html> 

<html> 

<head> 

    <title>🧮 Mi Calculadora en Azure</title> 

    <style> 

        body {  

            font-family: Arial, sans-serif;  

            max-width: 600px;  

            margin: 50px auto;  

            text-align: center; 

            background-color: #f0f8ff; 

        } 

        .calculadora {  

            background: white;  

            padding: 30px;  

            border-radius: 10px;  

            box-shadow: 0 4px 6px rgba(0,0,0,0.1); 

        } 

        input {  

            width: 100px;  

            padding: 10px;  

            margin: 5px;  

            border: 2px solid #4CAF50; 

            border-radius: 5px; 

            text-align: center; 

            font-size: 16px; 

        } 

        button {  

            padding: 10px 20px;  

            margin: 5px;  

            background: #4CAF50;  

            color: white;  

            border: none;  

            border-radius: 5px; 

            font-size: 16px; 

            cursor: pointer; 

        } 

        button:hover { background: #45a049; } 

        .resultado {  

            font-size: 24px;  

            color: #333;  

            margin: 20px;  

            padding: 20px; 

            background: #e7f3ff; 

            border-radius: 5px; 

        } 

    </style> 

</head> 

<body> 

    <div class="calculadora"> 

        <h1>🧮 Mi Calculadora en la Nube</h1> 

        <p>¡Esta aplicación está corriendo en Azure! 🚀</p> 

         

        <div> 

            <input type="number" id="num1" placeholder="Número 1"> 

            <input type="number" id="num2" placeholder="Número 2"> 

        </div> 

         

        <div> 

            <button onclick="calcular('sumar')">➕ Sumar</button> 

            <button onclick="calcular('restar')">➖ Restar</button> 

            <button onclick="calcular('multiplicar')">✖️ Multiplicar</button> 

            <button onclick="calcular('dividir')">➗ Dividir</button> 

        </div> 

         

        <div id="resultado" class="resultado"> 

            El resultado aparecerá aquí 

        </div> 

    </div> 

 

    <script> 

        async function calcular(operacion) { 

            const num1 = document.getElementById('num1').value; 

            const num2 = document.getElementById('num2').value; 

             

            if (!num1 || !num2) { 

                alert('¡Por favor ingresa ambos números!'); 

                return; 

            } 

             

            try { 

                const respuesta = await fetch(/calcular/${operacion}?a=${num1}&b=${num2}); 

                const datos = await respuesta.json(); 

                 

                document.getElementById('resultado').innerHTML =  

                    <strong>${num1} ${obtenerSimbolo(operacion)} ${num2} = ${datos.resultado}</strong>; 

                     

            } catch (error) { 

                document.getElementById('resultado').innerHTML =  

                    '<span style="color: red;">Error en el cálculo</span>'; 

            } 

        } 

         

        function obtenerSimbolo(operacion) { 

            const simbolos = { 

                'sumar': '+', 

                'restar': '-',  

                'multiplicar': '×', 

                'dividir': '÷' 

            }; 

            return simbolos[operacion] || '?'; 

        } 

    </script> 

</body> 

</html> 

""" 

 

@app.get("/") 

def pagina_principal(): 

    """ 

    🏠 PÁGINA PRINCIPAL 

    Esto devuelve el HTML que ve el usuario 

    """ 

    return HTMLResponse(PAGINA_PRINCIPAL) 

 

@app.get("/calcular/{operacion}") 

def calcular(operacion: str, a: float, b: float): 

    """ 

    🧮 CALCULADORA 

    Recibe dos números y una operación, devuelve el resultado 

     

    Parámetros: 

    - operacion: sumar, restar, multiplicar, dividir 

    - a: primer número 

    - b: segundo número 

    """ 

     

    if operacion == "sumar": 

        resultado = a + b 

    elif operacion == "restar": 

        resultado = a - b 

    elif operacion == "multiplicar": 

        resultado = a * b 

    elif operacion == "dividir": 

        if b == 0: 

            return {"error": "No se puede dividir por cero"} 

        resultado = a / b 

    else: 

        return {"error": "Operación no válida"} 

     

    return { 

        "operacion": operacion, 

        "numero1": a, 

        "numero2": b, 

        "resultado": resultado 

    } 

 

@app.get("/info") 

def informacion_app(): 

    """ 

    ℹ️ INFORMACIÓN DE LA APP 

    Endpoint simple que muestra información básica 

    """ 

    return { 

        "mensaje": "¡Hola desde Azure!", 

        "app": "Mi Primera Calculadora", 

        "estado": "Funcionando perfectamente", 

        "ubicacion": "Nube de Azure ☁️" 

    } 

 

# Esto es necesario para Azure 

if __name__ == "_main_": 

    import uvicorn 

    import os 

    # Azure nos dice en qué puerto ejecutar la app 

    puerto = int(os.environ.get("PORT", 8000)) 

    uvicorn.run(app, host="0.0.0.0", port=puerto)