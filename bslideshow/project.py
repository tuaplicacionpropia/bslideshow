#!/usr/bin/env python2.7
#coding:utf-8


#import bpy
import os
import shutil

import math
import random
from PIL import Image
import time

import codecs
import hjson

from bslideshow.director import Director
from bslideshow.slideshow import Slideshow
from bslideshow.tools import BlenderTools

class Project(object):

  def __init__ (self, path):
    self.path = path
    self.parents = []

  def generateMainSection (self, section):
    print("generate Main Section " + section['title'])
    sectTitle = self.generateTitleSection(section)
    outSections = list()
    for simpleSection in section['sections']:
      self.parents.append([simpleSection, section])
      outSection = self.generateSection(simpleSection)
      outSections.append(outSection)
    sectContent = self.mergeWithTransitions(section, outSections)
    print("sectContent = " + str(sectContent))
    quit()
    return result

  def generateTitleSection (self, section):
    result = None
    print("generate Title Section " + section['title'])

    sectionTitle = os.path.join(os.path.dirname(self.path), section['path'] + "_title" + ".mp4")
    if not os.path.isfile(sectionTitle):
      director = Director()
      director.runMode = 'LOW'
      #director.maxDebugFrames = 9999999
      director.frame_step = 1
      director.animSceneTitle(str(pathSection), movieOutput=str(sectionTitle))
    print("out section = " + sectionTitle)

    result = sectionTitle
    return result




  def mergeWithTransitions (self, section, sections=None):
    result = None
    #print("mergeWithTransitions " + section['title'])

    pathSection = os.path.join(os.path.dirname(self.path), section['path'] + "_transitions" + ".mp4")

    tools = BlenderTools()
    tools.runMode = 'LOW'
    tools.frame_step = 1
    
    if not os.path.isfile(pathSection):
      transitions = ['transition41.mp4', 'transition45.mp4', 'transition48.mp4', 'transition80.mp4', 'transition90.mp4']
      for item in sections:
        if result is None:
          result = pathSection
          shutil.copyfile(item, pathSection)
        else:
          tools.doAddTransition(movie1Path=str(pathSection), movie2Path=str(item), transitionPath=str(random.choice(transitions)), movieOutput=str(pathSection))

    result = pathSection

    return result

  def generateSection (self, section):
    result = None

    print("generate Section " + section['title'])
    director = Director()
    director.runMode = 'LOW'
    #director.maxDebugFrames = 9999999
    director.frame_step = 1
    pathSection = os.path.join(os.path.dirname(self.path), section['path'])

    sectionBase = os.path.join(os.path.dirname(self.path), section['path'] + "_base" + ".mp4")
    print("path section = " + pathSection)
    if not os.path.isfile(sectionBase):
      director.animScene(str(pathSection), movieOutput=str(sectionBase))
    print("out section = " + sectionBase)

    foregroundPath = 'overlay22.mp4'
    tools = BlenderTools()
    tools.runMode = 'LOW'
    #tools.maxDebugFrames = 99
    tools.frame_step = 1
    #tools.maxDebugFrames = 24

    sectionForeground = os.path.join(os.path.dirname(self.path), section['path'] + "_foreground" + ".mp4")
    if not os.path.isfile(sectionForeground):
      tools.addForeground(str(sectionBase), foregroundPath, movieOutput=str(sectionForeground))
    print("out2 section = " + sectionForeground)


    #tools.maxDebugFrames = 24
    sectionBanner = os.path.join(os.path.dirname(self.path), section['path'] + "_banner" + ".mp4")
    if not os.path.isfile(sectionBanner):
      tools.generateBanner(title = str(section['title']), subtitle = str(section['subtitle']), movieOutput=str(sectionBanner))
    print("banner section = " + sectionBanner)

    sectionBannerOffset = os.path.join(os.path.dirname(self.path), section['path'] + "_bannerOffset" + ".mp4")
    if not os.path.isfile(sectionBannerOffset):
      tools.addOffset(str(sectionBanner), framesOffset = 48, movieOutput=str(sectionBannerOffset))
    #bannerOffset = '/tmp/.movieRWAuLJ.mp4'
    print("bannerOffset section = " + sectionBannerOffset)


    sectionResult = os.path.join(os.path.dirname(self.path), section['path'] + "" + ".mp4")
    if not os.path.isfile(sectionResult):
      tools.doAddBanner(str(sectionForeground), str(sectionBannerOffset), movieOutput=str(sectionResult))
    print("result section = " + sectionResult)

    result = sectionResult
    return result

  def __saveObj__ (self, path, obj):
    fp = codecs.open(path, mode='w', encoding='utf-8')
    hjson.dump(obj, fp)

  def __loadObj__ (self, path):
    result = None
    fp = codecs.open(path, mode='r', encoding='utf-8')
    result = hjson.load(fp)
    return result

  def __get_parent__ (self, data):
    result = None
    for item in self.parents:
      if data == item[0]:
        result = item[1]
        break
    return result

  def generate (self):
    data = self.__loadObj__(self.path)
    self.parents.append([data, None])
    self.generateTitleSection(data)
    for mainSection in data['sections']:
      self.parents.append([mainSection, data])
      self.generateMainSection(mainSection)
    self.mergeWithTransitions(data)
 
    


if __name__ == '__main__':
  #p = Project("/home/jmramoss/hd/res_slideshow/project/myproject.hjson")
  #p.generate()
  tools = BlenderTools()
  tools.runMode = 'LOW'
  #tools.split(moviePath='/home/jmramoss/hd/res_slideshow/project/test.mp4', frameStart=1, frameEnd=4*96, movieOutput='/home/jmramoss/hd/res_slideshow/project/test_split.mp4')
  tools.fadeIn(moviePath='/home/jmramoss/hd/res_slideshow/project/test_split.mp4', duration=96, movieOutput='/home/jmramoss/hd/res_slideshow/project/test_fadeIn2.mp4')
  tools.fadeOut(moviePath='/home/jmramoss/hd/res_slideshow/project/test_fadeIn2.mp4', duration=96, movieOutput='/home/jmramoss/hd/res_slideshow/project/test_fadeOut2.mp4')
  #p.mergeWithTransitions(None, ["/tmp/.movie8p71ol.mp4", "/tmp/.moviehkqFpL.mp4", "/tmp/.movie5H4coh.mp4"])

