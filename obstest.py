import obsws_python as obs
import time

cl = obs.ReqClient(host='192.168.1.140', port=4455, password='mylife')

# load conn info from config.toml
# cl = obs.ReqClient()

# GetVersion
# resp = cl.get_version()
# print (resp)

# SetCurrentProgramScene
# cl.set_current_program_scene("BRB")
cl.set_current_program_scene("slate")
cl.start_record()
time.sleep(5)
cl.set_current_program_scene("record")