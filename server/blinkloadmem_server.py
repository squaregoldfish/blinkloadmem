'''
Server for blinkloadmem.

Listens on a socket, and when a client connects returns a JSON string
and then closes the connection.

The JSON string will be of the form:

{
  "cpu": {
    "count": <cpu count>
    "load": <system load>
  }
  "memory": {
    "percent_used": <mem used>
  }
}

The percentage of memory used is as reported by ps_util.virtual_memory()
'''
import os
import psutil
import multiprocessing
import argparse
import socket
import json

def _get_cpu_count():
  return multiprocessing.cpu_count()

def _get_load():
  return round(os.getloadavg()[0], 2)

def _get_mem():
  return round(psutil.virtual_memory().percent)

def _make_json():
   output = {
      "cpu": {
         "count": _get_cpu_count(),
         "load": _get_load()
      },
      "memory": {
         "percent_used": _get_mem()
      }
   }

   return json.dumps(output)


parser = argparse.ArgumentParser(
  prog='blinkloadmem_server.py',
  description='server for blinkloadmem'
)

parser.add_argument('host')
parser.add_argument('port', type=int)

args = parser.parse_args()

print(f'Starting server on {args.host}:{args.port}')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((args.host, args.port))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                try:
                    conn.sendall(str.encode(_make_json()))
                finally:
                    conn.close()
    finally:
        s.close()
