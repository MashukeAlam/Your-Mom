from pynput import mouse, keyboard
from pynput.mouse import Listener
from pynput.keyboard import Key, Listener
import pygetwindow
import logging
from datetime import datetime

with open('current.log', 'w'):
    pass

logging.basicConfig(filename="current.log", level=logging.INFO)
logger = logging.getLogger()

def make_html():
    lines = []
    with open('current.log') as file:
        lines = [line.rstrip() for line in file]
        lines = list(map(lambda l: l.replace("INFO:root:", ""), lines))
        # print(lines)
        now = datetime.now().strftime("%d%m%Y--%H%M%S")
        # print(now)
        filename = "LOG_{}.html".format(now)
        open(filename, 'x')
        f = open(filename, 'a')

        f.write("<!doctype html><head><link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css\" integrity=\"sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh\" crossorigin=\"anonymous\"><title>LOG</title></head><style>table {  font-family: arial, sans-serif; border-collapse: collapse; width: 100%;}td, th { border: 1px solid #dddddd;text-align: left;padding: 8px;}tr .mouse {background-color: #96e3aa}tr .key {background-color: #ffc67a}</style><body><h3>" + now + "</h3><table><tr><th>Device</th><th>Key</th><th>Button</th><th>Coord</th><th>Window</th></tr>")
        # print(11)
        for line in lines:
            if "Mouse" in line:
                line = line.split(" ")
                button = line[3]
                coord = line[1] + "," + line[2] 
                window = line[-1]
                f.write("<tr><td class='mouse'>Mouse</td><td class='mouse'>N/A</td><td class='mouse'>{}</td><td class='mouse'>{}</td><td class='mouse'>{}</td></tr>".format(button, coord, window))
            elif "Key" in line:
                line = line.split(" ")
                key = line[1]
                window = line[-1]
                f.write("<tr><td class='key'>Keyboard</td><td class='key'>{}</td><td class='key'>N/A</td><td class='key'>N/A</td><td class='key'>{}</td></tr>".format(key, window))
        
        f.write("</table></body></html>")






def click(x, y, button, pressed):
    if pressed:
        # print(x, y, button)
        logger.info("Mouse: {} {} {} {}".format(x, y, button, pygetwindow.getActiveWindowTitle().replace(' ', '')))



def on_release(key):
    # print('{0} release'.format(key))
    logger.info("Key: {} {}".format(key, pygetwindow.getActiveWindowTitle().replace(' ', '')))
    
    if key == Key.esc:
        # Stop listener
        k_listener.stop()
        m_listener.stop()
        make_html()

with keyboard.Listener(on_release=on_release) as k_listener, \
        mouse.Listener(on_click=click) as m_listener:
    k_listener.join()
    m_listener.join()



