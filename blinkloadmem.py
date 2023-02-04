#!/usr/bin/python3
import os, psutil
import time

########################################################
##
## CONFIGURATION

# Define the colors to use for different load levels
# Define them in ascending order. Otherwise things will be weird.
loadscaledef = [
    {
    "value": 0,
    "color": [0, 0, 255]
    },
    {
    "value": 2,
    "color": [0, 255, 0]
    },
    {
    "value": 4,
    "color": [255, 255, 0]
    },
    {
    "value": 6,
    "color": [255, 0, 0]
    }
  ]

memscaledef = [
    {
    "value": 0,
    "color": [0, 0, 255]
    },
    {
    "value": 50,
    "color": [0, 255, 0]
    },
    {
    "value": 75,
    "color": [255, 255, 0]
    },
    {
    "value": 100,
    "color": [255, 0, 0]
    }
  ]

blinkcmd = "blink1-tool -q"

##########################################################
##
## FUNCTIONS
def _getload():
  return os.getloadavg()[0]

def _getmem():
  return psutil.virtual_memory().percent

def _setblink(led, rgb):
  cmd = blinkcmd + " -l " + str(led) + " --rgb=" + str(rgb[0]) + "," + str(rgb[1]) + "," + str(rgb[2])
  os.system(cmd)

def _interpolatecolor(color1, color2, proportion):
  return round(color1 + (color2 - color1) * proportion)


def _getcolor(value, scaledef):

  result = [128, 128, 128]

  if value <= scaledef[0]["value"]:
    result = scaledef[0]["color"]
  elif value >= scaledef[-1]["value"]:
    result = scaledef[-1]["color"]
  else:

    preventry = None
    nextentry = None

    for i in range(0, len(scaledef)):
      if scaledef[i]["value"] == value:
        preventry = scaledef[i]
        nextentry = scaledef[i]
      elif scaledef[i]["value"] < value and scaledef[i + 1]["value"] > value:
        preventry = scaledef[i]
        nextentry = scaledef[i + 1]




    if preventry["color"] == nextentry["color"]:
      result = preventry["color"]
    else:
      colorproportion = (value - preventry["value"]) / (nextentry["value"] - preventry["value"])
      redvalue = _interpolatecolor(preventry["color"][0], nextentry["color"][0], colorproportion)
      greenvalue = _interpolatecolor(preventry["color"][1], nextentry["color"][1], colorproportion)
      bluevalue = _interpolatecolor(preventry["color"][2], nextentry["color"][2], colorproportion)

      result = [redvalue, greenvalue, bluevalue]



  return result


###################################################
##
## MAIN
def main():
  while True:
    load = _getload()
    loadcolor = _getcolor(load, loadscaledef)
    _setblink(1, loadcolor)

    mem = _getmem()
    memcolor = _getcolor(mem, memscaledef)
    _setblink(2, memcolor)

    time.sleep(5)



if __name__ == '__main__':
  main()
