from PIL import Image, ImageDraw
import face_recognition

#https://www.youtube.com/watch?v=aYsQBZwD3oE&ab_channel=RishabTeachesTech

image = face_recognition.load_image_file("image.jpeg")

face_locations = face_recognition.face_locations(image)

print("{} Gesichter gefunden.".format(len(face_locations)))

pil_image = Image.fromarray(image)
draw = ImageDraw.Draw(pil_image)

for face_location in face_locations:
    top, right, bottom, left = face_location
    print("Bild hier: {}, Left: {}, Bottom {}, Right: {}".format(top, left, bottom, right))

    draw.rectangle(((left, top), (right,bottom)), outline=(0, 255, 0), width=9)

pil_image.show()