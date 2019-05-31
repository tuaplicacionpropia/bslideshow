#!/usr/bin/env python2.7
#coding:utf-8


#import bpy
import os
import math
import random
from PIL import Image
import time

import codecs
import hjson

from bslideshow.slideshow import Slideshow
from bslideshow.tools import BlenderTools

class Director(BlenderTools):

  def __init__ (self):
    self.slideshow = None
    self.frame = 0.0
    BlenderTools.__init__(self)

  def buildSlideshow (self, i, folderImages):
    #folderImages = "/media/jmramoss/ALMACEN/unai_colegio_primaria/Tutoria_1A_2017_2018/01_21dic17_bailamos/.bak2"
    slideshow = Slideshow('background' + str(i))
    #slideshow.selectPhotos("/media/jmramoss/ALMACEN/slideshow/grid_frames/")
    slideshow.selectPhotos(folderImages)
    slideshow.shufflePhotos()
    slideshow.draw()
    #slideshow.alignColumn(separator=0.05)
    slideshow.alignGrid(separator=0.2)
    slideshow.shuffleTranslate()
    slideshow.shuffleRotateZ()
    return slideshow

  def buildScene (self, folderImages):
    import bpy
    cam = bpy.data.objects['Camera']
    print(str(type(cam)))
    from pprint import pprint
    pprint(cam)
    print(str(cam.items()))
    cam.data.clip_start = 0.001
    #for i in range(1, 10):
    #  add_image("/media/jmramoss/ALMACEN/slideshow/ramsau-3564068_960_720.jpg", i)
    slideshow = self.buildSlideshow(0, folderImages)
    slideshow.parentObj.location[0] += 0.0
    slideshow.parentObj.location[1] += 0.0
    slideshow.parentObj.location[2] += 0.0
    self.slideshow = slideshow

    posZ = -0.5
    separator = 0.02

    slideshow = self.buildSlideshow(1, folderImages)
    slideshow.parentObj.location[0] += (random.uniform(-0.3, 0.3) * 1)
    slideshow.parentObj.location[1] += (random.uniform(-0.3, 0.3) * 1)
    slideshow.parentObj.location[2] += (2.0 * posZ)

    slideshow = self.buildSlideshow(2, folderImages)
    slideshow.parentObj.location[0] += -self.slideshow.getDimensions()[0] - separator
    slideshow.parentObj.location[1] += 0
    slideshow.parentObj.location[2] += posZ

    slideshow = self.buildSlideshow(3, folderImages)
    slideshow.parentObj.location[0] += self.slideshow.getDimensions()[0] + separator
    slideshow.parentObj.location[1] += 0
    slideshow.parentObj.location[2] += posZ

    slideshow = self.buildSlideshow(4, folderImages)
    slideshow.parentObj.location[0] += 0
    slideshow.parentObj.location[1] += self.slideshow.getDimensions()[1] + separator
    slideshow.parentObj.location[2] += posZ

    slideshow = self.buildSlideshow(5, folderImages)
    slideshow.parentObj.location[0] += 0
    slideshow.parentObj.location[1] += -self.slideshow.getDimensions()[1] - separator
    slideshow.parentObj.location[2] += posZ


    slideshow = self.buildSlideshow(6, folderImages)
    slideshow.parentObj.location[0] += -self.slideshow.getDimensions()[0] - separator
    slideshow.parentObj.location[1] += -self.slideshow.getDimensions()[1] - separator
    slideshow.parentObj.location[2] += posZ

    slideshow = self.buildSlideshow(7, folderImages)
    slideshow.parentObj.location[0] += self.slideshow.getDimensions()[0] + separator
    slideshow.parentObj.location[1] += self.slideshow.getDimensions()[1] + separator
    slideshow.parentObj.location[2] += posZ

    slideshow = self.buildSlideshow(8, folderImages)
    slideshow.parentObj.location[0] += -self.slideshow.getDimensions()[0] - separator
    slideshow.parentObj.location[1] += self.slideshow.getDimensions()[1] + separator
    slideshow.parentObj.location[2] += posZ

    slideshow = self.buildSlideshow(9, folderImages)
    slideshow.parentObj.location[0] += self.slideshow.getDimensions()[0] + separator
    slideshow.parentObj.location[1] += -self.slideshow.getDimensions()[1] - separator
    slideshow.parentObj.location[2] += posZ


  '''
    for i in range(2):
      slideshow = Slideshow('background' + str(i))
      #slideshow.selectPhotos("/media/jmramoss/ALMACEN/slideshow/grid_frames/")
      slideshow.selectPhotos("/media/jmramoss/ALMACEN/unai_colegio_primaria/Tutoria_1A_2017_2018/01_21dic17_bailamos/.bak2")
      slideshow.shufflePhotos()
      slideshow.draw()
      #slideshow.alignColumn()
      slideshow.alignGrid()
      slideshow.shuffleTranslate()
      slideshow.shuffleRotateZ()
      slideshow.parentObj.location[0] += (random.uniform(-0.3, 0.3) * i)
      slideshow.parentObj.location[1] += (random.uniform(-0.3, 0.3) * i)
      slideshow.parentObj.location[2] += (-0.1 * i)
      if i == 0:
        self.slideshow = slideshow
  '''

  '''
	#obj_camera = bpy.context.scene.camera

	# Set camera translation
	#scene.camera.location.x = 0.0
	#scene.camera.location.y = 0.0
	#scene.camera.location.z = 80.0


	#fov = 50.0
	#pi = 3.14159265
	# Set camera fov in degrees
	#scene.camera.data.angle = fov*(pi/180.0)
  '''
  def camLookAt (self):
    import bpy
    if(len(bpy.data.cameras) == 1):
      obj = bpy.data.objects['Camera'] # bpy.types.Camera
      obj.location.x = 10.0
      obj.location.y = -5.0
      obj.location.z = 5.0
    pass

  '''
	# Set camera rotation in euler angles
        #rx = 0.0
        #ry = 0.0
        #rz = 0.0
	#scene.camera.rotation_mode = 'XYZ'
	#scene.camera.rotation_euler[0] = rx*(pi/180.0)
	#scene.camera.rotation_euler[1] = ry*(pi/180.0)
	#scene.camera.rotation_euler[2] = rz*(pi/180.0)
  '''
  def camRotate (self, rx, ry, rz):
    import bpy
    if(len(bpy.data.cameras) == 1):
      obj = bpy.data.objects['Camera'] # bpy.types.Camera
      obj.rotation_mode = 'XYZ'
      obj.rotation_euler[0] = rx*(math.pi/180.0)
      obj.rotation_euler[1] = ry*(math.pi/180.0)
      obj.rotation_euler[2] = rz*(math.pi/180.0)
    pass

  def showPicture (self, picName):
    import bpy
    pic = bpy.data.objects[picName]
    obj = bpy.data.objects['Camera'] # bpy.types.Camera
    obj.rotation_mode = 'XYZ'
    obj.location.x = pic.location.x
    obj.location.y = pic.location.y
    obj.location.z = pic.location.z + 4.0
    rx = 0
    ry = 0
    rz = 0
    obj.rotation_euler[0] = rx*(math.pi/180.0)
    obj.rotation_euler[1] = ry*(math.pi/180.0)
    obj.rotation_euler[2] = rz*(math.pi/180.0)

  ''' Animation
      #if(len(bpy.data.cameras) == 1):
      #    obj = bpy.data.objects['Camera'] # bpy.types.Camera
      #    obj.location.x = 0.0
      #    obj.location.y = -10.0
      #    obj.location.z = 10.0
      #    obj.keyframe_insert(data_path="location", frame=10.0)
      #    obj.location.x = 10.0
      #    obj.location.y = 0.0
      #    obj.location.z = 5.0
      #    obj.keyframe_insert(data_path="location", frame=20.0)
  '''
  def showSlideshow2 (self, numPhotos, maxFrames):
    import bpy
    incFrames = math.ceil(maxFrames / numPhotos)
    for i in range(numPhotos):
      idx = i + 1
      picName = 'pic' + str(idx)
      self.showPicture(picName)
      frame = i * incFrames
      cam = bpy.data.objects['Camera'] # bpy.types.Camera
      if i == 0:
        cam.keyframe_insert(data_path="location", frame=frame+(2*24))
      else:
        cam.keyframe_insert(data_path="location", frame=frame-(2*24))
      cam.keyframe_insert(data_path="location", frame=frame)

  def showSlideshow3 (self, numPhotos, maxFrames):
    import bpy
    incFrames = math.ceil(maxFrames / numPhotos)

    cam = bpy.data.objects['Camera'] # bpy.types.Camera
    startCamLocationZ = cam.location.z

    for i in range(numPhotos):
      idx = i + 1
      picName = 'pic' + str(idx)
      self.showPicture(picName)
      frame = i * incFrames

      incZ = random.uniform(-3.0, 3.0)
      cam.location.z = startCamLocationZ + incZ

      rx = 3.0 if i % 2 == 0 else 0.0
      ry = 0.0 if i % 2 == 0 else 6.0
      rz = 0.0 if i % 2 == 0 else 15.0
      cam.rotation_euler[1] = rx*(math.pi/180.0)
      cam.rotation_euler[1] = ry*(math.pi/180.0)
      cam.rotation_euler[2] = rz*(math.pi/180.0)

      if i == 0:
        cam.keyframe_insert(data_path="location", frame=frame+(2*24))
        cam.keyframe_insert(data_path="rotation_euler", frame=frame+(2*24))
      else:
        cam.keyframe_insert(data_path="location", frame=frame-(2*24))
        cam.keyframe_insert(data_path="rotation_euler", frame=frame-(2*24))
      cam.keyframe_insert(data_path="location", frame=frame)
      cam.keyframe_insert(data_path="rotation_euler", frame=frame)



  def showSlideshowDuration (self, duration=120):
    import bpy

    numPhotos = len(self.slideshow.photos)#16

    cam = bpy.data.objects['Camera'] # bpy.types.Camera
    startCamLocationZ = cam.location.z

    idx = random.randint(1, numPhotos)
    picName = 'pic' + str(idx)
    pic = bpy.data.objects[picName]

    cam.rotation_mode = 'XYZ'
    cam.location.x = pic.location.x + random.uniform(-0.01, 0.01)
    cam.location.y = pic.location.y + random.uniform(-0.01, 0.01)
    cam.location.z = pic.location.z + random.uniform(3.5, 5.0)
    cam.rotation_euler[0] = random.uniform(0.0, 6.0)*(math.pi/180.0)
    cam.rotation_euler[1] = random.uniform(0.0, 6.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame)
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame)

    cam.location.x += random.uniform(-0.01, 0.01)
    cam.location.y += random.uniform(-0.01, 0.01)
    cam.location.z -= random.uniform(1.0, 2.5)
    cam.rotation_euler[0] = random.uniform(0.0, 15.0)*(math.pi/180.0)
    cam.rotation_euler[1] = random.uniform(0.0, 15.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame + duration)
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame + duration)

    self.frame = self.frame + duration + 12.0






  def showSlideshow (self, numPhotos, maxFrames):
    import bpy
    incFrames = math.ceil(maxFrames / numPhotos)

    cam = bpy.data.objects['Camera'] # bpy.types.Camera
    startCamLocationZ = cam.location.z

    idx = random.randint(1, numPhotos)
    picName = 'pic' + str(idx)
    pic = bpy.data.objects[picName]

    cam.rotation_mode = 'XYZ'
    cam.location.x = pic.location.x + random.uniform(-0.01, 0.01)
    cam.location.y = pic.location.y + random.uniform(-0.01, 0.01)
    cam.location.z = pic.location.z + random.uniform(3.5, 5.0)
    cam.rotation_euler[0] = random.uniform(0.0, 6.0)*(math.pi/180.0)
    cam.rotation_euler[1] = random.uniform(0.0, 6.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame)
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame)

    cam.location.x += random.uniform(-0.01, 0.01)
    cam.location.y += random.uniform(-0.01, 0.01)
    cam.location.z -= random.uniform(1.0, 2.5)
    cam.rotation_euler[0] = random.uniform(0.0, 15.0)*(math.pi/180.0)
    cam.rotation_euler[1] = random.uniform(0.0, 15.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame + incFrames)
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame + incFrames)

    self.frame = self.frame + incFrames + 12.0



  def showRowColumnDuration (self, duration=120):
    import bpy

    numPhotos = len(self.slideshow.photos)#16

    cam = bpy.data.objects['Camera'] # bpy.types.Camera
    startCamLocationZ = cam.location.z

    startIdx = random.randint(1, numPhotos)
    picName = 'pic' + str(startIdx)
    pic = bpy.data.objects[picName]

    cam.rotation_mode = 'XYZ'
    cam.location.x = pic.location.x + random.uniform(-0.01, 0.01)
    cam.location.y = pic.location.y + random.uniform(-0.01, 0.01)
    cam.location.z = pic.location.z + random.uniform(3.5, 5.0)
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame)
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame)

    endIdx = random.randint(1, numPhotos)
    picName = 'pic' + str(endIdx)
    pic = bpy.data.objects[picName]

    cam.location.x = pic.location.x + random.uniform(-0.01, 0.01)
    cam.location.y = pic.location.y + random.uniform(-0.01, 0.01)
    cam.location.z = pic.location.z + random.uniform(3.5, 5.0)
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame + duration)
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame + duration)

    self.frame = self.frame + duration + 12.0



  def showRowColumn (self, numPhotos, maxFrames):
    import bpy
    incFrames = math.ceil(maxFrames / numPhotos)

    cam = bpy.data.objects['Camera'] # bpy.types.Camera
    startCamLocationZ = cam.location.z

    startIdx = random.randint(1, numPhotos)
    picName = 'pic' + str(startIdx)
    pic = bpy.data.objects[picName]

    cam.rotation_mode = 'XYZ'
    cam.location.x = pic.location.x + random.uniform(-0.01, 0.01)
    cam.location.y = pic.location.y + random.uniform(-0.01, 0.01)
    cam.location.z = pic.location.z + random.uniform(3.5, 5.0)
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame)
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame)

    endIdx = random.randint(1, numPhotos)
    picName = 'pic' + str(endIdx)
    pic = bpy.data.objects[picName]

    cam.location.x = pic.location.x + random.uniform(-0.01, 0.01)
    cam.location.y = pic.location.y + random.uniform(-0.01, 0.01)
    cam.location.z = pic.location.z + random.uniform(3.5, 5.0)
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame + incFrames)
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame + incFrames)

    self.frame = self.frame + incFrames + 12.0


  def showZoomInOutDuration (self, duration=120):
    import bpy

    numPhotos = len(self.slideshow.photos)#16

    cam = bpy.data.objects['Camera'] # bpy.types.Camera
    startCamLocationZ = cam.location.z

    startIdx = random.randint(1, numPhotos)
    picName = 'pic' + str(startIdx)
    pic = bpy.data.objects[picName]


    startZ = random.uniform(2.0, 5.0)

    cam.rotation_mode = 'XYZ'
    cam.location.x = pic.location.x + random.uniform(-0.01, 0.01)
    cam.location.y = pic.location.y + random.uniform(-0.01, 0.01)
    cam.location.z = pic.location.z + 1.0 + startZ
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame)
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame)

    endZ = startZ - 3.0 if startZ > 3.0 else startZ + 2.0

    cam.location.x = pic.location.x + random.uniform(-0.01, 0.01)
    cam.location.y = pic.location.y + random.uniform(-0.01, 0.01)
    cam.location.z = pic.location.z + 1.0 + endZ
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame + duration)
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame + duration)

    self.frame = self.frame + duration + 12.0



  def showZoomInOut (self, numPhotos, maxFrames):
    import bpy
    incFrames = math.ceil(maxFrames / numPhotos)

    cam = bpy.data.objects['Camera'] # bpy.types.Camera
    startCamLocationZ = cam.location.z

    startIdx = random.randint(1, numPhotos)
    picName = 'pic' + str(startIdx)
    pic = bpy.data.objects[picName]


    startZ = random.uniform(2.0, 5.0)

    cam.rotation_mode = 'XYZ'
    cam.location.x = pic.location.x + random.uniform(-0.01, 0.01)
    cam.location.y = pic.location.y + random.uniform(-0.01, 0.01)
    cam.location.z = pic.location.z + 1.0 + startZ
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame)
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame)

    endZ = startZ - 3.0 if startZ > 3.0 else startZ + 2.0

    cam.location.x = pic.location.x + random.uniform(-0.01, 0.01)
    cam.location.y = pic.location.y + random.uniform(-0.01, 0.01)
    cam.location.z = pic.location.z + 1.0 + endZ
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame + incFrames)
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame + incFrames)

    self.frame = self.frame + incFrames + 12.0


  #Se acerca y se aleja de una foto
  def showDeleite (self, numPhotos, maxFrames):
    import bpy
    incFrames = math.ceil(maxFrames / numPhotos)
    mitad1Frames = incFrames/2

    cam = bpy.data.objects['Camera'] # bpy.types.Camera
    startCamLocationZ = cam.location.z

    startIdx = random.randint(1, numPhotos)
    picName = 'pic' + str(startIdx)
    pic = bpy.data.objects[picName]

    initZ = 2.0
    startZ = random.uniform(2.0, 5.0)

    cam.rotation_mode = 'XYZ'
    cam.location.x = pic.location.x + random.uniform(-0.01, 0.01)
    cam.location.y = pic.location.y + random.uniform(-0.01, 0.01)
    cam.location.z = pic.location.z + initZ
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = 0.0*random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame)
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame)

    cam.location.x = pic.location.x + random.uniform(-0.01, 0.01)
    cam.location.y = pic.location.y + random.uniform(-0.01, 0.01)
    cam.location.z = pic.location.z + initZ + 3.0
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = 0.0*random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame + math.ceil(incFrames/2))
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame + math.ceil(incFrames/2))

    cam.location.x = pic.location.x + random.uniform(-0.01, 0.01)
    cam.location.y = pic.location.y + random.uniform(-0.01, 0.01)
    cam.location.z = pic.location.z + 3.0
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = 0.0*random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame + incFrames)
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame + incFrames)

    self.frame = self.frame + incFrames + 12.0





  def showDeleiteDuration (self, duration=120):
    import bpy

    numPhotos = len(self.slideshow.photos)#16
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> numPHOTOSOSSSSSSSSSSSS = " + str(numPhotos))

    cam = bpy.data.objects['Camera'] # bpy.types.Camera
    startCamLocationZ = cam.location.z

    startIdx = random.randint(1, numPhotos)
    picName = 'pic' + str(startIdx)
    pic = bpy.data.objects[picName]

    initZ = 2.0
    startZ = random.uniform(2.0, 5.0)

    cam.rotation_mode = 'XYZ'
    cam.location.x = pic.location.x + random.uniform(-0.01, 0.01)
    cam.location.y = pic.location.y + random.uniform(-0.01, 0.01)
    cam.location.z = pic.location.z + initZ
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = 0.0*random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame)
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame)

    cam.location.x = pic.location.x + random.uniform(-0.01, 0.01)
    cam.location.y = pic.location.y + random.uniform(-0.01, 0.01)
    cam.location.z = pic.location.z + initZ + 3.0
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = 0.0*random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame + math.ceil(duration/2))
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame + math.ceil(duration/2))

    cam.location.x = pic.location.x + random.uniform(-0.01, 0.01)
    cam.location.y = pic.location.y + random.uniform(-0.01, 0.01)
    cam.location.z = pic.location.z + 3.0
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = 0.0*random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame + duration)
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame + duration)

    self.frame = self.frame + duration + 12.0








  #Se acerca y se aleja de una foto
  def showDeleiteOnePhoto (self, duration=120):
    import bpy

    numPhotos = len(self.slideshow.photos)

    cam = bpy.data.objects['Camera'] # bpy.types.Camera
    startCamLocationZ = cam.location.z

    startIdx = random.randint(1, numPhotos)
    picName = 'pic' + str(startIdx)
    pic = bpy.data.objects[picName]

    initZ1 = random.uniform(4.0, 7.0)
    initZ2 = random.uniform(1.5, 3.0)
    factorRandom1 = random.uniform(0.50, 1.00)
    factorRandom2 = random.uniform(0.01, 0.05)

    cam.rotation_mode = 'XYZ'
    cam.location.x = pic.location.x + random.uniform(-0.01 - factorRandom1, 0.01 + factorRandom1)
    cam.location.y = pic.location.y + random.uniform(-0.01 - factorRandom1, 0.01 + factorRandom1)
    cam.location.z = pic.location.z + initZ1
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = 0.0*random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame)
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame)
    '''
    cam.location.x = pic.location.x + random.uniform(-0.01, 0.01)
    cam.location.y = pic.location.y + random.uniform(-0.01, 0.01)
    cam.location.z = pic.location.z + initZ + 3.0
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = 0.0*random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame + math.ceil(duration/2))
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame + math.ceil(duration/2))
    '''
    cam.location.x = pic.location.x + random.uniform(-0.01 - factorRandom2, 0.01 + factorRandom2)
    cam.location.y = pic.location.y + random.uniform(-0.01 - factorRandom2, 0.01 + factorRandom2)
    cam.location.z = pic.location.z + initZ2
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = 0.0*random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame + duration)
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame + duration)

    self.frame = self.frame + duration



  #Se acerca y se aleja de una foto
  def showDeleiteOnePhotoProject (self, duration=120):
    import bpy

    numPhotos = len(self.slideshow.photos)

    cam = bpy.data.objects['Camera'] # bpy.types.Camera
    startCamLocationZ = cam.location.z

    startIdx = random.randint(1, numPhotos)
    picName = 'pic' + str(startIdx)
    pic = bpy.data.objects[picName]

    initZ1 = random.uniform(1.5, 1.8)
    initZ2 = random.uniform(1.5, 1.8)
    initZ3 = random.uniform(1.5, 1.8)
    factorRandom1 = random.uniform(0.50, 1.00)
    factorRandom2 = random.uniform(0.01, 0.05)

    cam.rotation_mode = 'XYZ'

    cam.location.x = pic.location.x + random.uniform(-0.01 - factorRandom1, 0.01 + factorRandom1)
    cam.location.y = pic.location.y + random.uniform(-0.01 - factorRandom1, 0.01 + factorRandom1)
    cam.location.z = pic.location.z + initZ1
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = 0.0*random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame)
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame)
    '''
    cam.location.x = pic.location.x + random.uniform(-0.01, 0.01)
    cam.location.y = pic.location.y + random.uniform(-0.01, 0.01)
    cam.location.z = pic.location.z + initZ + 3.0
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = 0.0*random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame + math.ceil(duration/2))
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame + math.ceil(duration/2))
    '''
    cam.location.x = pic.location.x + random.uniform(-0.01 - factorRandom2, 0.01 + factorRandom2)
    cam.location.y = pic.location.y + random.uniform(-0.01 - factorRandom2, 0.01 + factorRandom2)
    cam.location.z = pic.location.z + initZ2
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = 0.0*random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame + (duration/2))
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame + (duration/2))


    cam.location.x = pic.location.x + random.uniform(-0.01 - factorRandom2, 0.01 + factorRandom2)
    cam.location.y = pic.location.y + random.uniform(-0.01 - factorRandom2, 0.01 + factorRandom2)
    cam.location.z = pic.location.z + initZ3
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = 0.0*random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame + (duration))
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame + (duration))


    self.frame = self.frame + duration

  #Se acerca y se aleja de una foto
  def showDeleiteOnePhotoSection (self, duration=120):
    import bpy

    numPhotos = len(self.slideshow.photos)

    cam = bpy.data.objects['Camera'] # bpy.types.Camera
    startCamLocationZ = cam.location.z

    startIdx = random.randint(1, numPhotos)
    picName = 'pic' + str(startIdx)
    pic = bpy.data.objects[picName]

    initZ1 = random.uniform(4.5, 6.0)
    initZ2 = random.uniform(3.0, 4.0)
    factorRandom1 = random.uniform(0.50, 1.00)
    factorRandom2 = random.uniform(0.01, 0.05)

    cam.rotation_mode = 'XYZ'
    cam.location.x = pic.location.x + random.uniform(-0.01 - factorRandom1, 0.01 + factorRandom1)
    cam.location.y = pic.location.y + random.uniform(-0.01 - factorRandom1, 0.01 + factorRandom1)
    cam.location.z = pic.location.z + initZ1
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = 0.0*random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame)
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame)
    '''
    cam.location.x = pic.location.x + random.uniform(-0.01, 0.01)
    cam.location.y = pic.location.y + random.uniform(-0.01, 0.01)
    cam.location.z = pic.location.z + initZ + 3.0
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = 0.0*random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame + math.ceil(duration/2))
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame + math.ceil(duration/2))
    '''
    cam.location.x = pic.location.x + random.uniform(-0.01 - factorRandom2, 0.01 + factorRandom2)
    cam.location.y = pic.location.y + random.uniform(-0.01 - factorRandom2, 0.01 + factorRandom2)
    cam.location.z = pic.location.z + initZ2
    cam.rotation_euler[0] = random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[1] = 0.0*random.uniform(0.0, 3.0)*(math.pi/180.0)
    cam.rotation_euler[2] = random.uniform(0.0, 1.0)*(math.pi/180.0)

    cam.keyframe_insert(data_path="location", frame=self.frame + duration)
    cam.keyframe_insert(data_path="rotation_euler", frame=self.frame + duration)

    self.frame = self.frame + duration






  def doAnimSceneDuration (self, folderImages, movieOutput=None):
    import bpy
    result = None
    bpy.context.scene.world.light_settings.use_ambient_occlusion = True
    bpy.context.scene.world.light_settings.ao_factor = 1.0

    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ folderImages = " + str(folderImages))
    self.buildScene(folderImages)
    #camLookAt()0
    self.camRotate(0, 0, 0)
    #showPicture('pic2')

    numPhotos = len(self.slideshow.photos)#16
    frameEnd = 8 * 120

    #renderOneFrame(50)
    self.showDeleiteDuration(duration=120)
    self.showDeleiteDuration(duration=120)

    self.showZoomInOutDuration(duration=120)
    self.showZoomInOutDuration(duration=120)

    self.showRowColumnDuration(duration=120)
    self.showRowColumnDuration(duration=120)

    self.showSlideshowDuration(duration=120)
    self.showSlideshowDuration(duration=120)

    result = self.saveMovie(frameStart=1, frameEnd=frameEnd, movieOutput=movieOutput)
    return result





  def doAnimScene (self, folderImages, movieOutput=None):
    import bpy
    result = None
    bpy.context.scene.world.light_settings.use_ambient_occlusion = True
    bpy.context.scene.world.light_settings.ao_factor = 1.0

    self.buildScene(folderImages)
    #camLookAt()0
    self.camRotate(0, 0, 0)
    #showPicture('pic2')

    numPhotos = len(self.slideshow.photos)#16
    pps = 1.0
    fps = self.fps
    frameEnd = numPhotos * pps * fps


    #renderOneFrame(50)
    self.showDeleite(numPhotos, frameEnd)
    self.showDeleite(numPhotos, frameEnd)

    self.showZoomInOut(numPhotos, frameEnd)
    self.showZoomInOut(numPhotos, frameEnd)

    self.showRowColumn(numPhotos, frameEnd)
    self.showRowColumn(numPhotos, frameEnd)

    self.showSlideshow(numPhotos, frameEnd)
    self.showSlideshow(numPhotos, frameEnd)

    result = self.saveMovie(frameStart=1, frameEnd=frameEnd, movieOutput=movieOutput)
    return result


  def doAnimSceneTitle (self, folderImages, movieOutput=None):
    import bpy
    result = None
    bpy.context.scene.world.light_settings.use_ambient_occlusion = True
    bpy.context.scene.world.light_settings.ao_factor = 1.0

    self.buildScene(folderImages)
    #camLookAt()0
    self.camRotate(0, 0, 0)
    #showPicture('pic2')

    numPhotos = len(self.slideshow.photos)#16
    pps = 1.0
    fps = self.fps
    frameEnd = numPhotos * pps * fps


    #renderOneFrame(50)
    self.showDeleite(numPhotos, frameEnd)

    self.showZoomInOut(numPhotos, frameEnd)

    self.showDeleite(numPhotos, frameEnd)

    result = self.saveMovie(frameStart=1, frameEnd=frameEnd, movieOutput=movieOutput)
    return result


  def animSceneDuration (self, folderImages, movieOutput=None):
    result = None

    if self.blender:
      templatePath = self.getResource('empty.blend', 'templates')
      result = self.runMethodBlender(templatePath, "animSceneDuration", [folderImages], movieOutput=movieOutput)
    else:
      result = self.doAnimSceneDuration(folderImages, movieOutput)

    return result

  def animScene (self, folderImages, movieOutput=None):
    result = None

    if self.blender:
      templatePath = self.getResource('empty.blend', 'templates')
      result = self.runMethodBlender(templatePath, "animScene", [folderImages], movieOutput=movieOutput)
    else:
      result = self.doAnimScene(folderImages, movieOutput)

    return result

  def animSceneTitle (self, folderImages, movieOutput=None):
    result = None

    if self.blender:
      templatePath = self.getResource('empty.blend', 'templates')
      result = self.runMethodBlender(templatePath, "doAnimSceneTitle", [folderImages], movieOutput=movieOutput)
    else:
      result = self.doAnimSceneTitle(folderImages, movieOutput)

    return result

  def animSceneTitleItem (self, folderImages, durationFrames=120, mode='project', movieOutput=None):
    result = None

    if self.blender:
      templatePath = self.getResource('empty.blend', 'templates')
      result = self.runMethodBlender(templatePath, "doAnimSceneTitleItem", [folderImages, durationFrames, mode], movieOutput=movieOutput)
    else:
      result = self.doAnimSceneTitleItem(folderImages=folderImages, durationFrames=durationFrames, mode=mode, movieOutput=movieOutput)

    return result

  def doAnimSceneTitleItem (self, folderImages, durationFrames=120, mode='project', movieOutput=None):
    import bpy
    result = None
    bpy.context.scene.world.light_settings.use_ambient_occlusion = True
    bpy.context.scene.world.light_settings.ao_factor = 1.0

    self.buildScene(folderImages)
    #camLookAt()0
    self.camRotate(0, 0, 0)
    #showPicture('pic2')

    #renderOneFrame(50)
    if mode == 'project':
      self.showDeleiteOnePhotoProject(durationFrames)
    elif mode == 'section':
      self.showDeleiteOnePhotoSection(durationFrames)
    else:
      self.showDeleiteOnePhoto(durationFrames)

    result = self.saveMovie(frameStart=1, frameEnd=durationFrames, movieOutput=movieOutput)
    return result




if __name__ == '__main__':
  director = Director()
  director.runMode = 'DEBUG'
  out = director.animScene("/media/jmramoss/ALMACEN/unai_colegio_primaria/Tutoria_1A_2017_2018/01_21dic17_bailamos/.bak2")
  print(str(out))
  #director.addBgSound("/media/jmramoss/ALMACEN/mp3/Bruno_Mars_-_24K_Magic_Official_Video[myplaylist-youtubemp3.com].mp3", "metal")
  #director.saveMovie(True)
