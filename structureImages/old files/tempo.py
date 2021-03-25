from PIL import Image
im = Image.open('/storage/emulated/0/0Python/Git/gameOfLife/structure images/Screenshot_20210325-124400_Material_Files.png')
pixelMap = im.load()

img = Image.new( im.mode, im.size)
pixelsNew = img.load()
for i in range(img.size[0]):
    for j in range(img.size[1]):
        if (0, 0, 0) in pixelMap[i,j]:
            pixelsNew[i,j] = (255, 0, 0)
        else:
            pixelsNew[i,j] = pixelMap[i,j]
img.save('out.jpg')