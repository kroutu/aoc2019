from PIL import Image

# Lecture fichier d'entrée
donnees = open("aoc8.txt",'r')
pixels = list(map(int,donnees.read()))
donnees.close()

imageSize = 25 * 6
layers = [pixels[i:i+imageSize] for i in range(0,len(pixels),imageSize)]

# Part 1
countingZeros = [layer.count(0) for layer in layers]
fewestZeros = countingZeros.index(min(countingZeros))
print(layers[fewestZeros].count(1) * layers[fewestZeros].count(2))

# Part 2
imageList = []
for i in range(imageSize):
    for layer in layers:
        if layer[i] != 2:
            imageList.append(layer[i])
            break
        
image = Image.new("1", (25,6))
image.putdata(imageList)
image.convert("P").resize((25*50,6*50)).show()