import time
import json
import socket
from blink1.blink1 import blink1

COLOR_SCALE = [
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

def _interpolate_color(color1, color2, proportion):
  return round(color1 + (color2 - color1) * proportion)

def get_color(percent):
  result = [128, 128, 128]

  if percent <= COLOR_SCALE[0]["value"]:
    result = COLOR_SCALE[0]["color"]
  elif percent >= COLOR_SCALE[-1]["value"]:
    result = COLOR_SCALE[-1]["color"]
  else:
    prev_entry = COLOR_SCALE[0]
    next_entry = COLOR_SCALE[1]

    for i in range(0, len(COLOR_SCALE)):
      if COLOR_SCALE[i]["value"] == percent:
        prev_entry = COLOR_SCALE[i]
        next_entry = COLOR_SCALE[i]
      elif COLOR_SCALE[i]["value"] < percent and COLOR_SCALE[i + 1]["value"] > percent:
        prev_entry = COLOR_SCALE[i]
        next_entry = COLOR_SCALE[i + 1]

    if prev_entry["color"] == next_entry["color"]:
      result = prev_entry["color"]
    else:
      color_proportion = (percent - prev_entry["value"]) / (next_entry["value"] - prev_entry["value"])
      red_value = _interpolate_color(prev_entry["color"][0], next_entry["color"][0], color_proportion)
      green_value = _interpolate_color(prev_entry["color"][1], next_entry["color"][1], color_proportion)
      blue_value = _interpolate_color(prev_entry["color"][2], next_entry["color"][2], color_proportion)

      result = [red_value, green_value, blue_value]

  return result




########

with open('client_config.json') as f:
    config = json.loads(f.read())

with blink1() as b1:
    while True:
        try:
            server_found = False

            server_index = 0
            while not server_found and server_index < len(config):
                host = config[server_index]['host']
                port = config[server_index]['port']
                
                try:
                    data = None                    
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(2)
                        s.connect((host, port))
                        data = s.recv(1024)
                        
                    if data is not None:
                        data = json.loads(data)

                        load_percent = int(data['cpu']['load'] / data['cpu']['count'] * 100)
                        mem_percent = int(data['memory']['percent_used'])

                        load_color = get_color(load_percent)
                        b1.fade_to_rgb(300, load_color[0], load_color[1], load_color[2], 1)

                        mem_color = get_color(mem_percent)
                        b1.fade_to_rgb(300, mem_color[0], mem_color[1], mem_color[2], 2)
                        

                        server_found = True
                except OSError as e:
                    # This is usually a failure to connect
                    # Not a problem since we move on to the next server
                    pass

                server_index += 1

            if not server_found:
                b1.play(5,7)

        except Exception as e:
            print(e)
            b1.play(0,2)

        time.sleep(5)



    b1.play(0,2)
    time.sleep(10)


#while True:
#    for server in config:
#        print(server)

#    time.sleep(5)