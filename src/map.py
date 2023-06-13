from PIL import Image

# retorna os pixels de uma imagem
def getImagePixels():
    imagem = Image.open("imagens/mapa.png","r")
    pix_val = list(imagem.getdata())
    return pix_val, imagem.width, imagem.height

def getMatriz(mapa):
    # gera matriz do mapa
    mapa_matriz = []
    for _y in range(0,15):
        linha = []
        for _x in range(0,19):
            if mapa[(_y*19)+_x] == 0:
                linha.append(1)
            elif mapa[(_y*19)+_x] == 4:
                linha.append(2)
            elif mapa[(_y*19)+_x] == 3:
                linha.append(3)
            elif mapa[(_y*19)+_x] == 1:
                linha.append(4)
            else:
                linha.append(0)
        mapa_matriz.append(linha)

    return mapa_matriz

CELL_SIZE = 40
lst_pixels, MAP_WIDTH, MAP_HEIGHT = getImagePixels()
MAP = getMatriz(lst_pixels)
