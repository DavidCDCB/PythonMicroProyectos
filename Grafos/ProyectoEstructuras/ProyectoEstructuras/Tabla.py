import plotly.graph_objects as go

class Graficador():
    def __init__(self, matriz, fil, col):
        matriz = self.girarMatriz(matriz)
        fil.insert(0, "Simbolos")
        fil = self.colocarNegrillaEje(fil)
        col = self.colocarNegrillaEje(col)
        matriz.insert(0,col)
        fig = go.Figure(data=[go.Table(
            header=dict(
                values=fil,
                font=dict(color='black', size=15),
                height=30,
                fill_color='#0043b3',
            ),
            cells=dict(
                values=matriz,
                font=dict(color='black', size=15),
                height=30,
                fill=dict(color=['#0043b3', '#0a6ab6']),
            )
        )])
        fig.show()

    def colocarNegrillaEje(self, eje):
        for index in range(0, len(eje)):
            eje[index] = "<b>" + str(eje[index]) + "<b>"
        return eje

    """Gira la matriz 90 grados"""
    def girarMatriz(self, matriz):
        matrizAux = []
        listasCreadas = False
        for list in range(len(matriz)):
            for prod in range(len(matriz[list])):
                if listasCreadas:
                    matrizAux[prod].append(matriz[list][prod])
                else:
                    matrizAux.append([matriz[list][prod]])
            listasCreadas = True
        return matrizAux