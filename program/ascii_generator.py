class face:
   def __init__(face):
      from PIL import Image
      pic = Image.open('/home/Justin/image.jpg', 'r')
      pic = pic.resize((300, 150))
      face.pic = pic.convert('L')
      face.BAL = 0  
   def pixel_to_letter(face, value):
      if(value in xrange(0, face.BAL)):
         return '0'
      elif(value in xrange(face.BAL, 256)):
         return '1'
   
   def img_to_ascii(face, pic):
      dump = ''
      for y in xrange(0, pic.getbbox()[-1]):
         for x in xrange(0, pic.getbbox()[-2]):
            dump += face.pixel_to_letter(pic.getpixel((x,y)))
         dump += '\n'
      return dump


f = face()
for f.BAL in xrange(50, 256):
   print f.img_to_ascii(f.pic).replace('1', ' ')
