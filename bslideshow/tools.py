#!/usr/bin/env python2.7
#coding:utf-8

#Split video (desde segundo 184 y dura 7 segundos)
#ffmpeg -i thirds.mp4 -ss 184 -t 7 t1.mp4

#Scalar video
#ffmpeg -i video_1920.mp4 -vf scale=640:360 video_640.mp4 -hide_banner

#Convertir video en imágenes
#ffmpeg -i thirds.mp4 -vsync 0 out%d.png

#Plantillas posibles para lower thirds
'''

[sellt6]: https://www.youtube.com/watch?v=1j2SdLcKX8I&list=PLPxLHRwHzxIRMrKy08_azqvmfZeeqHK6r&index=155
[sellt5]: https://www.youtube.com/watch?v=mdn-x5UW_9E&list=PLPxLHRwHzxIRMrKy08_azqvmfZeeqHK6r&index=151
[sellt4]: https://www.youtube.com/watch?v=Rdl4TUVQMpw&list=PLPxLHRwHzxIRMrKy08_azqvmfZeeqHK6r&index=149
[sellt3]: https://www.youtube.com/watch?v=QC0QjW2EWEo&list=PLPxLHRwHzxIRMrKy08_azqvmfZeeqHK6r&index=120
[sellt2]: https://www.youtube.com/watch?v=7ghdipr6d9w&index=105&list=PLPxLHRwHzxIRMrKy08_azqvmfZeeqHK6r

[sellt1]: https://www.youtube.com/watch?v=zpvpUrsCne8&index=13&list=PLPxLHRwHzxIRMrKy08_azqvmfZeeqHK6r

https://mega.nz/#F!LD5zRAwK!dgkpxG7HT9Lw6ANe7ro9Ug

'''

#Generar banner
#cd /media/jmramoss/ALMACEN/slideshow/blender-2.79b-linux-glibc219-x86_64
#./blender /media/jmramoss/ALMACEN/pypi/slideshow/third4.blend --background --python /media/jmramoss/ALMACEN/pypi/slideshow/vse5.py 
#/media/jmramoss/ALMACEN/slideshow/blender-2.79b-linux-glibc219-x86_64/blender /media/jmramoss/ALMACEN/pypi/slideshow/third4.blend --background --python /media/jmramoss/ALMACEN/pypi/slideshow/vse5.py 

#import bpy
import sys
import subprocess
import tempfile
import os
import requests
import tarfile

BLENDER_URL = 'https://ftp.halifax.rwth-aachen.de/blender/release/Blender2.79/blender-2.79b-linux-glibc219-x86_64.tar.bz2'

class BlenderTools:

  '''
DEBUG: pocos frames
DRAFT : Baja resolución
PRODUCTION: Máxima resolución
  '''

  def __init__ (self):
    self.fps = 24
    self.blender = True
    self.verbose = True
    #self.test = False
    self.runMode = 'PRODUCTION'
    pass

  def getResource (self, key):
    result = None
    
    home = os.path.expanduser("~")
    target = os.path.join(home, ".__blender__")
    target = os.path.join(target, "resources")
    if not os.path.isdir(target):
      os.makedirs(target)
    
    targetFile = os.path.join(target, key)
    if not os.path.isfile(targetFile):
      sys.path.append(os.path.dirname(__file__))
      from downloader import Downloader
      downloader = Downloader()
      arrayKey = key.split(os.sep)
      targetFolder = os.path.dirname(targetFile)
      os.makedirs(targetFolder)
      #print("download on " + targetFolder)
      result = downloader.downloadFile(arrayKey[0], arrayKey[1], targetFolder)
    else:
      result = targetFile
    
    return result

  def installBlender (self):
    #https://www.blender.org/download/Blender2.79/blender-2.79b-linux-glibc219-x86_64.tar.bz2/
    url = BLENDER_URL
    r = requests.get(url, allow_redirects=True)

    home = os.path.expanduser("~")
    
    target= os.path.join(home, ".__blender__")
    os.mkdir(target)
    
    basename = os.path.basename(url)
    ftar = os.path.join(home, basename)
    open(ftar, 'wb').write(r.content)
    tar = tarfile.open(ftar, "r:bz2")
    tar.extractall(target)
    tar.close()
    
    pass
    
  def checkInstallBlender (self):
    result = None

    home = os.path.expanduser("~")
    target= os.path.join(home, ".__blender__")

    onlyfiles = [os.path.join(target, f) for f in os.listdir(target) if os.path.isdir(os.path.join(target, f))]
    executable = os.path.join(onlyfiles[0], 'blender')
    if os.path.isfile(executable):
      result = executable

    return result

  def runBlender (self, templatePath, scriptPath):
    #templatePath = "/media/jmramoss/ALMACEN/pypi/slideshow/empty.blend"
    #scriptPath = "/media/jmramoss/ALMACEN/pypi/slideshow/generate_banner.py"
    blenderPath = None
    #blenderPath = "/media/jmramoss/ALMACEN/slideshow/blender-2.79b-linux-glibc219-x86_64/blender"
    
    blenderPath = self.checkInstallBlender()
    if blenderPath is None:
      self.installBlender()
      blenderPath = self.checkInstallBlender()
    
    args = [blenderPath, templatePath, "--background", "--python", scriptPath]
    if self.verbose:
      subprocess.call(args)
    else:
      FNULL = open(os.devnull, 'w')
      subprocess.call(args, stdout=FNULL, stderr=FNULL)
    pass

  def runMethodBlender (self, templatePath, method, args, movieOutput=None):
    result = None

    result = self.createTmpMoviePath() if movieOutput is None else movieOutput

    iargs = ""
    argsIdx = 0
    margs = []
    for arg in args:
      if type(arg) == str:
        margs.append("'" + arg + "'")
      else:
        margs.append(arg)
      iargs += (", " if len(iargs) > 0 else "") + "{" + str(argsIdx) + "}"
      argsIdx += 1
    margs.append("'" + result + "'")
    iargs += (", " if len(iargs) > 0 else "") + "{" + str(argsIdx) + "}"
    
    scriptPath = "/media/jmramoss/ALMACEN/pypi/slideshow/____fg_23.py"
    #templatePath = "/media/jmramoss/ALMACEN/pypi/slideshow/empty.blend"

    script = open(scriptPath, "w") 

    script.write("#!/usr/bin/env python2.7" + "\n")
    script.write("#coding:utf-8" + "\n")
    script.write("" + "\n")

    script.write("import os" + "\n")
    script.write("import sys" + "\n")
    script.write("sys.path.append(os.path.dirname(__file__))" + "\n")
    script.write("from tools import BlenderTools" + "\n")
    script.write("import bpy" + "\n")
    script.write("" + "\n")
    script.write("tools = BlenderTools()" + "\n")
    script.write("tools.blender = False" + "\n")
    script.write("tools.runMode = '{0}'".format(self.runMode) + "\n")
    script.write("tools." + method + "(" + iargs.format(*margs) + ")" + "\n")
 
    script.close()

    self.runBlender(templatePath, scriptPath)

    return result



  '''
  def runAddForeground (self, moviePath, foregroundPath, movieOutput=None):
    result = None

    result = self.createTmpMoviePath() if movieOutput is None else movieOutput

    scriptPath = "/media/jmramoss/ALMACEN/pypi/slideshow/____fg.py"
    templatePath = "/media/jmramoss/ALMACEN/pypi/slideshow/empty.blend"

    script = open(scriptPath, "w") 

    script.write("#!/usr/bin/env python2.7" + "\n")
    script.write("#coding:utf-8" + "\n")
    script.write("" + "\n")

    script.write("import os" + "\n")
    script.write("import sys" + "\n")
    script.write("sys.path.append(os.path.dirname(__file__))" + "\n")
    script.write("from tools import BlenderTools" + "\n")
    script.write("import bpy" + "\n")
    script.write("" + "\n")
    script.write("tools = BlenderTools()" + "\n")
    script.write("tools.blender = False" + "\n")
    script.write("tools.runMode = '{0}'".format(self.runMode) + "\n")
    script.write("tools.addForeground('{0}', '{1}', '{2}')".format(moviePath, foregroundPath, result) + "\n")
 
    script.close()

    self.runBlender(templatePath, scriptPath)

    return result
  '''
  
  '''
    subprocess.call(["/media/jmramoss/ALMACEN/slideshow/blender-2.79b-linux-glibc219-x86_64/blender", "/media/jmramoss/ALMACEN/pypi/slideshow/empty.blend", "--background", "--python", "/media/jmramoss/ALMACEN/pypi/slideshow/generate_banner.py"])



  '''
  def addForeground (self, moviePath, foregroundPath, movieOutput=None):
    result = None

    foregroundPath = self.getResource("footages/foreground.mp4")

    if self.blender:
      #result = self.runAddForeground(moviePath, foregroundPath, movieOutput)
      result = self.runMethodBlender("/media/jmramoss/ALMACEN/pypi/slideshow/empty.blend", "addForeground", (moviePath, foregroundPath), movieOutput=movieOutput)
    else:
      import bpy
      context = bpy.context
      scene = context.scene
      scene.sequence_editor_create()
      sed = scene.sequence_editor
      sequences = sed.sequences

      #moviePath = "/media/jmramoss/ALMACEN/pypi/slideshow/video2.mp4"
      video1 = sequences.new_movie("video1", moviePath, 1, 1)
      audio1 = sequences.new_sound("audio1", moviePath, 2, 1)

      #foreground = sequences.new_movie("fg1", "/media/jmramoss/ALMACEN/pypi/slideshow/foreground2.mp4", 2, 1)
      #print("LENGTH FOREGROUND = " + str(foreground.frame_duration))
      #print("LENGTH VIDEO = " + str(video1.frame_duration))

      duration_cubierta = 0
      offset_layer = 3

      #       frame_end=frame_end, 
      #add_strip = sequences.new_effect("minameAdd", 'ADD', offset_layer, frame_start=1, seq1=foreground, seq2=video1)

      #foregroundPath = "/media/jmramoss/ALMACEN/pypi/slideshow/foreground2.mp4"
      while duration_cubierta < video1.frame_duration:
        foreground = sequences.new_movie("fg" + str(offset_layer), foregroundPath, offset_layer, duration_cubierta + 1)
        #       frame_end=frame_end, 
        add_strip = sequences.new_effect("minameAdd" + str(offset_layer), 'ADD', offset_layer + 1, frame_start=duration_cubierta + 1, seq1=foreground, seq2=video1)
        duration_cubierta += foreground.frame_duration
        offset_layer += 2

      result = self.saveMovie(frameStart=1, frameEnd=video1.frame_duration, movieOutput=movieOutput)

    return result

  '''
  def runGenerateBanner (self, title, subtitle = None, title_right = None, subtitle_right = None, movieOutput=None):
    result = None

    result = self.createTmpMoviePath() if movieOutput is None else movieOutput

    scriptPath = "/media/jmramoss/ALMACEN/pypi/slideshow/___gb.py"
    templatePath = "/media/jmramoss/ALMACEN/pypi/slideshow/generateBanner.blend"

    script = open(scriptPath, "w") 

    script.write("#!/usr/bin/env python2.7" + "\n")
    script.write("#coding:utf-8" + "\n")
    script.write("" + "\n")
    script.write("import os" + "\n")
    script.write("import sys" + "\n")
    script.write("sys.path.append(os.path.dirname(__file__))" + "\n")
    script.write("from tools import BlenderTools" + "\n")
    script.write("import bpy" + "\n")
    script.write("" + "\n")
    script.write("tools = BlenderTools()" + "\n")
    script.write("tools.blender = False" + "\n")
    script.write("tools.runMode = '{0}'".format(self.runMode) + "\n")
    script.write("tools.generateBanner('{0}', '{1}', '{2}', '{3}', '{4}')".format(title, subtitle, title_right, subtitle_right, result) + "\n")
 
    script.close()

    self.runBlender(templatePath, scriptPath)
    
    return result
  '''
  
  '''
    subprocess.call(["/media/jmramoss/ALMACEN/slideshow/blender-2.79b-linux-glibc219-x86_64/blender", "/media/jmramoss/ALMACEN/pypi/slideshow/generateBanner.blend", "--background", "--python", "/media/jmramoss/ALMACEN/pypi/slideshow/generate_banner.py"])
  '''
  def generateBanner (self, title, subtitle = None, title_right = None, subtitle_right = None, movieOutput=None):
    result = None

    if self.blender:
      #result = self.runGenerateBanner(title, subtitle, title_right, subtitle_right, movieOutput)
      result = self.runMethodBlender("/media/jmramoss/ALMACEN/pypi/slideshow/generateBanner.blend", "generateBanner", (title, subtitle, title_right, subtitle_right), movieOutput=movieOutput)
    else:
      import bpy
      context = bpy.context
      scene = context.scene

      oTitle = bpy.data.objects['Title']
      oTitle.data.body = title if title is not None else ""#"Lorem Ipsum"

      oSubtitle = bpy.data.objects['Subtitle']
      oSubtitle.data.body = subtitle if subtitle is not None else ""#"Descripción de Lorem Ipsum"

      oTitleRight = bpy.data.objects['title_right']
      oTitleRight.data.body = title_right if title_right is not None else ""#"Periquito"#""#"Dic 2017"

      oSubtitleRight = bpy.data.objects['subtitle_right']
      oSubtitleRight.data.body = subtitle_right if subtitle_right is not None else ""#"Nuevo año 2019"#""#"Curso 2017-2018"

      img = bpy.data.images["logo3.png"]
      img.filepath = "//logo3.png"

      result = self.saveMovie(frameStart=1, frameEnd=250, movieOutput=movieOutput)

    return result

  '''
  def runOffset (self, moviePath, framesOffset = 48, color=None, movieOutput=None):
    result = None

    result = self.createTmpMoviePath() if movieOutput is None else movieOutput

    scriptPath = "/media/jmramoss/ALMACEN/pypi/slideshow/___bo.py"
    templatePath = "/media/jmramoss/ALMACEN/pypi/slideshow/empty.blend"

    script = open(scriptPath, "w") 

    script.write("#!/usr/bin/env python2.7" + "\n")
    script.write("#coding:utf-8" + "\n")
    script.write("" + "\n")
    script.write("import os" + "\n")
    script.write("import sys" + "\n")
    script.write("sys.path.append(os.path.dirname(__file__))" + "\n")
    script.write("from tools import BlenderTools" + "\n")
    script.write("import bpy" + "\n")
    script.write("" + "\n")
    script.write("tools = BlenderTools()" + "\n")
    script.write("tools.blender = False" + "\n")
    script.write("tools.runMode = '{0}'".format(self.runMode) + "\n")
    script.write("tools.addOffset('{0}', {1}, {2}, '{3}')".format(moviePath, framesOffset, color, result) + "\n")
 
    script.close()

    self.runBlender(templatePath, scriptPath)
    
    return result
  '''


  '''
    subprocess.call(["/media/jmramoss/ALMACEN/slideshow/blender-2.79b-linux-glibc219-x86_64/blender", "/media/jmramoss/ALMACEN/pypi/slideshow/empty.blend", "--background", "--python", "/media/jmramoss/ALMACEN/pypi/slideshow/generate_banner.py"])
  '''
  def addOffset (self, moviePath, framesOffset = 48, color=None, movieOutput=None):
    result = None

    if self.blender:
      #result = self.runOffset(moviePath, framesOffset, color, movieOutput)
      result = self.runMethodBlender("/media/jmramoss/ALMACEN/pypi/slideshow/empty.blend", "addOffset", (moviePath, framesOffset, color), movieOutput=movieOutput)
    else:
      import bpy
      context = bpy.context
      scene = context.scene
      scene.sequence_editor_create()
      sed = scene.sequence_editor
      sequences = sed.sequences

      #moviePath = "/media/jmramoss/ALMACEN/pypi/slideshow/banner.mp4"

      color = sequences.new_effect("color", 'COLOR', 1, 1, framesOffset)
      color.color = (0.006, 0.991, 0.006)

      video1 = sequences.new_movie("video1", moviePath, 2, framesOffset)
      audio1 = sequences.new_sound("audio1", moviePath, 3, framesOffset)

      #print("LENGTH VIDEO = " + str(video1.frame_duration))

      result = self.saveMovie(frameStart=1, frameEnd=framesOffset + video1.frame_duration, movieOutput=movieOutput)

    return result

  '''
  def runDoAddBanner (self, moviePath, bannerPath, movieOutput=None):
    result = None

    result = self.createTmpMoviePath() if movieOutput is None else movieOutput

    scriptPath = "/media/jmramoss/ALMACEN/pypi/slideshow/__ab.py"
    templatePath = "/media/jmramoss/ALMACEN/pypi/slideshow/banner_overlap2.blend"

    script = open(scriptPath, "w") 

    script.write("#!/usr/bin/env python2.7" + "\n")
    script.write("#coding:utf-8" + "\n")
    script.write("" + "\n")
    script.write("import os" + "\n")
    script.write("import sys" + "\n")
    script.write("sys.path.append(os.path.dirname(__file__))" + "\n")
    script.write("from tools import BlenderTools" + "\n")
    script.write("import bpy" + "\n")
    script.write("" + "\n")
    script.write("tools = BlenderTools()" + "\n")
    script.write("tools.blender = False" + "\n")
    script.write("tools.runMode = '{0}'".format(self.runMode) + "\n")
    script.write("tools.doAddBanner('{0}', '{1}', '{2}')".format(moviePath, bannerPath, result) + "\n")
 
    script.close()

    self.runBlender(templatePath, scriptPath)
    
    return result
  '''
  
  '''
    subprocess.call(["/media/jmramoss/ALMACEN/slideshow/blender-2.79b-linux-glibc219-x86_64/blender", "/media/jmramoss/ALMACEN/pypi/slideshow/banner_overlap2.blend", "--background", "--python", "/media/jmramoss/ALMACEN/pypi/slideshow/add_banner.py"])
  '''
  def doAddBanner (self, moviePath, bannerPath, movieOutput=None):
    result = None

    if self.blender:
      #result = self.runDoAddBanner(moviePath, bannerPath, movieOutput)
      result = self.runMethodBlender("/media/jmramoss/ALMACEN/pypi/slideshow/banner_overlap2.blend", "doAddBanner", (moviePath, bannerPath), movieOutput=movieOutput)
    else:
      import bpy
      #nodes = bpy.data.scenes['Scene'].node_tree.nodes
      #print(str(nodes))
      #clip_path = 
      #get the new movie clip
      #movie_clip = bpy.data.movieclips.get(clip_name)
      ##assign movie clip to the node

      #moviePath = "/media/jmramoss/ALMACEN/pypi/slideshow/video3.mp4"
      movieClip = bpy.data.movieclips.load(moviePath)
      bpy.context.scene.node_tree.nodes['video'].clip = movieClip

      #bannerPath = "/media/jmramoss/ALMACEN/pypi/slideshow/banner.mp4"
      #bannerPath = "/media/jmramoss/ALMACEN/pypi/slideshow/banner_offset.mkv"
      bannerClip = bpy.data.movieclips.load(bannerPath)
      bpy.context.scene.node_tree.nodes['banner'].clip = bannerClip

      #print(">>>>>>>")
      #print(str(bpy.data.movieclips))
      #video
      #banner
      #nodes['Alpha Over'].premul

      frameEnd = bpy.context.scene.node_tree.nodes['video'].clip.frame_duration
      result = self.saveMovie(frameStart=1, frameEnd=frameEnd, movieOutput=movieOutput)

    return result

  '''
  def runDoAddMusic (self, moviePath, musicPath, movieOutput=None):
    result = None

    result = self.createTmpMoviePath() if movieOutput is None else movieOutput

    scriptPath = "/media/jmramoss/ALMACEN/pypi/slideshow/__am.py"
    templatePath = "/media/jmramoss/ALMACEN/pypi/slideshow/empty.blend"

    script = open(scriptPath, "w") 

    script.write("#!/usr/bin/env python2.7" + "\n")
    script.write("#coding:utf-8" + "\n")
    script.write("" + "\n")
    script.write("import os" + "\n")
    script.write("import sys" + "\n")
    script.write("sys.path.append(os.path.dirname(__file__))" + "\n")
    script.write("from tools import BlenderTools" + "\n")
    script.write("import bpy" + "\n")
    script.write("" + "\n")
    script.write("tools = BlenderTools()" + "\n")
    script.write("tools.blender = False" + "\n")
    script.write("tools.runMode = '{0}'".format(self.runMode) + "\n")
    script.write("tools.doAddMusic('{0}', '{1}', '{2}')".format(moviePath, musicPath, result) + "\n")
 
    script.close()

    self.runBlender(templatePath, scriptPath)
    
    return result
  '''
  
  '''
    subprocess.call(["/media/jmramoss/ALMACEN/slideshow/blender-2.79b-linux-glibc219-x86_64/blender", "/media/jmramoss/ALMACEN/pypi/slideshow/banner_overlap2.blend", "--background", "--python", "/media/jmramoss/ALMACEN/pypi/slideshow/add_banner.py"])
  '''
  def doAddMusic (self, moviePath, musicPath, movieOutput=None):
    result = None

    if self.blender:
      #result = self.runDoAddMusic(moviePath, musicPath, movieOutput)
      result = self.runMethodBlender("/media/jmramoss/ALMACEN/pypi/slideshow/empty.blend", "doAddMusic", (moviePath, musicPath), movieOutput=movieOutput)
    else:
      import bpy
      context = bpy.context
      scene = context.scene
      scene.sequence_editor_create()
      sed = scene.sequence_editor
      sequences = sed.sequences

      #moviePath = "/media/jmramoss/ALMACEN/pypi/slideshow/video2.mp4"
      video1 = sequences.new_movie("video1", moviePath, 1, 1)
      audio1 = sequences.new_sound("audio1", musicPath, 2, 1)

      result = self.saveMovie(frameStart=1, frameEnd=video1.frame_duration, movieOutput=movieOutput)

    return result







  '''
  def runDoAddTransition (self, movie1Path, movie2Path, movieOutput=None):
    result = None

    result = self.createTmpMoviePath() if movieOutput is None else movieOutput

    scriptPath = "/media/jmramoss/ALMACEN/pypi/slideshow/__tr.py"
    templatePath = "/media/jmramoss/ALMACEN/pypi/slideshow/transition.blend"

    script = open(scriptPath, "w") 

    script.write("#!/usr/bin/env python2.7" + "\n")
    script.write("#coding:utf-8" + "\n")
    script.write("" + "\n")
    script.write("import os" + "\n")
    script.write("import sys" + "\n")
    script.write("sys.path.append(os.path.dirname(__file__))" + "\n")
    script.write("from tools import BlenderTools" + "\n")
    script.write("import bpy" + "\n")
    script.write("" + "\n")
    script.write("tools = BlenderTools()" + "\n")
    script.write("tools.blender = False" + "\n")
    script.write("tools.runMode = '{0}'".format(self.runMode) + "\n")
    script.write("tools.doAddTransition('{0}', '{1}', '{2}')".format(movie1Path, movie2Path, result) + "\n")
 
    script.close()

    self.runBlender(templatePath, scriptPath)
    
    return result
  '''
  
  '''
    subprocess.call(["/media/jmramoss/ALMACEN/slideshow/blender-2.79b-linux-glibc219-x86_64/blender", "/media/jmramoss/ALMACEN/pypi/slideshow/banner_overlap2.blend", "--background", "--python", "/media/jmramoss/ALMACEN/pypi/slideshow/add_banner.py"])
  '''
  def doAddTransition (self, movie1Path, movie2Path, movieOutput=None):
    result = None

    if self.blender:
      #result = self.runDoAddTransition(movie1Path, movie2Path, movieOutput)
      result = self.runMethodBlender("/media/jmramoss/ALMACEN/pypi/slideshow/transition.blend", "doAddTransition", (movie1Path, movie2Path), movieOutput=movieOutput)
    else:
      import bpy
      context = bpy.context
      scene = context.scene
      #scene.sequence_editor_create()
      sed = scene.sequence_editor
      sequences = sed.sequences

      # deselect all
      #bpy.ops.object.select_all(action='DESELECT')
      # selection
      #bpy.data.objects['Camera'].select = True
      # remove it
      #bpy.ops.object.delete() 

      #bpy.ops.object.select_all(action='DESELECT')
      #sequences['video1'].select = True
      #sequences['audio1'].select = True
      #sequences['video2'].select = True
      #sequences['audio2'].select = True
      #bpy.ops.object.delete() 

      '''
      sequences['video1'].filepath = movie1Path
      sequences['audio1'].sound.filepath = movie1Path

      sequences['video2'].filepath = movie2Path
      sequences['audio2'].sound.filepath = movie2Path
      '''

      #moviePath = "/media/jmramoss/ALMACEN/pypi/slideshow/video2.mp4"
      
      transitionPath = "/media/jmramoss/ALMACEN/pypi/slideshow/transition2.mp4"
      movieClip = bpy.data.movieclips.load(transitionPath)
      bpy.context.scene.node_tree.nodes['movieTransition'].clip = movieClip
      
      
      video1 = sequences.new_movie("video1", movie1Path, 1, 1)
      audio1 = sequences.new_sound("audio1", movie1Path, 2, 1)
      
      video2 = sequences.new_movie("video2", movie2Path, 1, video1.frame_duration + 1)
      audio2 = sequences.new_sound("audio2", movie2Path, 2, video1.frame_duration + 1)
      
      transition = sequences['transition']
      transition.frame_start = video1.frame_duration - int(transition.frame_final_duration / 2)
      
      frameEnd = video1.frame_duration + video2.frame_duration
      result = self.saveMovie(frameStart=1, frameEnd=frameEnd, movieOutput=movieOutput)

    return result












  def rmFile (self, path):
    if os.path.isfile(path):
      os.remove(path)
      #print("File Removed!")

  def createTmpMoviePath (self):
    result = None
    result = tempfile.mkstemp(prefix='.movie', suffix='.mp4')[1]
    return result

  def addBanner (self, moviePath, title, subtitle = None, title_right = None, subtitle_right = None, framesOffset = 48, color=None, movieOutput=None):
    result = None
    print("generating banner")
    banner = self.generateBanner(title, subtitle, title_right, subtitle_right)
    print("banner = " + banner)
    print("banner generado")
    if framesOffset > 0:
      print("generating offset")
      banner2 = self.addOffset(banner, framesOffset, color)
      print("banner2 = " + banner2)
      print("offset generado")
      #self.rmFile(banner)
      banner = banner2

    print("generating foreground")
    movieFg = self.addForeground(moviePath, "/media/jmramoss/ALMACEN/pypi/slideshow/foreground2.mp4", movieOutput=None)
    print("movieFg = " + movieFg)
    print("foreground generado")

    print("adding banner")
    result = self.doAddBanner(movieFg, banner, movieOutput=None)
    print("result = " + result)
    print("banner added")
    
    print("adding music")
    result = self.doAddMusic(result, moviePath, movieOutput)
    print("result = " + result)
    print("music added")

    
    return result
  
  def saveMovie (self, frameStart=1, frameEnd=250, movieOutput=None):
    result = None

    if self.runMode == 'DEBUG':
      frameEnd = min(24*8, frameEnd)
    
    #frame_end = bpy.context.scene.node_tree.nodes['video'].clip.frame_duration

    import bpy
    context = bpy.context
    scene = context.scene

    scene.frame_start = frameStart
    scene.frame_end = frameEnd
    scene.frame_step = 1
    scene.render.fps = self.fps

    
    resolution_x = 1920
    resolution_y = 1080

    if self.runMode == 'DEBUG':
      resolution_x = 192
      resolution_y = 108
    elif self.runMode == 'DRAFT':
      resolution_x = 192*2
      resolution_y = 108*2
    elif self.runMode == 'PRODUCTION':
      resolution_x = 1920
      resolution_y = 1080
      
    scene.render.resolution_x = resolution_x
    scene.render.resolution_y = resolution_y
    scene.render.resolution_percentage = 100#100

    #Type: enum in [‘BMP’, ‘IRIS’, ‘PNG’, ‘JPEG’, ‘JPEG2000’, ‘TARGA’, ‘TARGA_RAW’, ‘CINEON’, ‘DPX’, ‘OPEN_EXR_MULTILAYER’, ‘OPEN_EXR’, ‘HDR’, ‘TIFF’, ‘AVI_JPEG’, ‘AVI_RAW’, ‘FRAMESERVER’, ‘H264’, ‘FFMPEG’, ‘THEORA’, ‘XVID’], default ‘TARGA’
    scene.render.image_settings.file_format = 'FFMPEG'

    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    
    rateFactor = 'LOSSLESS'
    preset = 'VERYSLOW'
    if self.runMode == 'DEBUG':
      rateFactor = 'LOWEST'
      preset = 'ULTRAFAST'
    elif self.runMode == 'DRAFT':
      rateFactor = 'MEDIUM'
      preset = 'MEDIUM'
    elif self.runMode == 'PRODUCTION':
      rateFactor = 'LOSSLESS'
      preset = 'VERYSLOW'

    #constant_rate_factor = 'LOWEST', 'MEDIUM', 'HIGH', 'PERC_LOSSLESS', 'LOSSLESS'
    scene.render.ffmpeg.constant_rate_factor = rateFactor

    #ffmpeg_preset = 'ULTRAFAST', 'MEDIUM', 'VERYSLOW'
    scene.render.ffmpeg.ffmpeg_preset = preset

    #audio_codec #FFmpeg audio codec to use
    #Type:	enum in [‘NONE’, ‘MP2’, ‘MP3’, ‘AC3’, ‘AAC’, ‘VORBIS’, ‘FLAC’, ‘PCM’], default ‘NONE’
    scene.render.image_settings.color_mode = 'RGB'
    
    scene.render.ffmpeg.audio_codec = 'MP3'
    scene.render.ffmpeg.audio_bitrate = 192

    result = self.createTmpMoviePath() if movieOutput is None else movieOutput
    
    srcTmpDir = os.path.dirname(result)
    tmpDir = tempfile.mkdtemp(prefix=".tmp", dir=srcTmpDir)
    tmpRender = os.path.join(tmpDir, 'movie')
    #print("TEMP RENDER = " + tmpRender)
    
    scene.render.filepath = tmpRender
    bpy.ops.render.render(animation=True)

    onlyfiles = [os.path.join(tmpDir, f) for f in os.listdir(tmpDir) if os.path.isfile(os.path.join(tmpDir, f))]    
    if onlyfiles is not None and len(onlyfiles) == 1:
      #print(str(onlyfiles[0]))
      #print("exit")
      #quit()
      os.rename(onlyfiles[0], result)
      os.rmdir(tmpDir)
    else:
      result = None

    return result

#tools = BlenderTools()
#tools.installBlender()
#print(tools.checkInstallBlender())

if True and __name__ == '__main__':
  tools = BlenderTools()
  tools.runMode = 'DRAFT'
  #res = tools.addForeground("/media/jmramoss/ALMACEN/pypi/slideshow/video3.mp4", "/media/jmramoss/ALMACEN/pypi/slideshow/foreground2.mp4", movieOutput=None)
  res = tools.addForeground("/media/jmramoss/ALMACEN/pypi/slideshow/video3.mp4", "/media/jmramoss/ALMACEN/pypi/slideshow/foreground2.mp4", "/media/jmramoss/ALMACEN/pypi/slideshow/fg444.mp4")
  print("res = " + res)
  #banner = tools.generateBanner("ESTO<<< FUNCIONA?", "PROBAaddcNDO", "Swwí", "Nbbbo", "/media/jmramoss/ALMACEN/pypi/slideshow/genBanner45.mp4")
  #print("banner = " + banner)
  #tools.runOffset ("/media/jmramoss/ALMACEN/pypi/slideshow/test1.mkv", framesOffset = 48, color=None, movieOutput="/media/jmramoss/ALMACEN/pypi/slideshow/offset_test1.mp4")
  #tools.doAddBanner("/media/jmramoss/ALMACEN/pypi/slideshow/video3.mp4", "/media/jmramoss/ALMACEN/pypi/slideshow/offset_test1.mkv", movieOutput="/media/jmramoss/ALMACEN/pypi/slideshow/video3_with_banner222.mp4")
  #tools.addBanner("/media/jmramoss/ALMACEN/pypi/slideshow/Background.mp4", "Bosque", "con niebla", "Forest", "with fog", framesOffset = 48, color=None, movieOutput="/media/jmramoss/ALMACEN/pypi/slideshow/video3_modificado56.mp4")
  #tools.blender = False
  #tools.addBanner("/media/jmramoss/ALMACEN/pypi/slideshow/long_video_audio.mp4", "Bosque", "con niebla", "nnnnnnnn", "joy con", framesOffset = 48, color=None, movieOutput="/media/jmramoss/ALMACEN/pypi/slideshow/long_modificado6.mp4")
  #tools.doAddTransition("/media/jmramoss/ALMACEN/pypi/slideshow/video1.mp4", "/media/jmramoss/ALMACEN/pypi/slideshow/video3.mp4", movieOutput="/media/jmramoss/ALMACEN/pypi/slideshow/traaaaa10.mp4")
  
  

  #print("banner generado " + str(banner))
  '''
  print("arguments#### (start)")
  print(str(sys.argv))
  print("arguments#### (end)")
  if sys.argv is not None and len(sys.argv) > 0 and sys.argv[0].endswith("blender"):
    import bpy
    addBanner()
    saveMovie()
  else:
    #subprocess.call(["ls", "-l"])
    subprocess.call(["/media/jmramoss/ALMACEN/slideshow/blender-2.79b-linux-glibc219-x86_64/blender", "/media/jmramoss/ALMACEN/pypi/slideshow/banner_overlap2.blend", "--background", "--python", "/media/jmramoss/ALMACEN/pypi/slideshow/add_banner.py"])

  '''
