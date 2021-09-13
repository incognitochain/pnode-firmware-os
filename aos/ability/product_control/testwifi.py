from aos.system.configs.channel import DEVICE_TYPE
from aos.system.libs.util import Util
Util.cmd("sudo nmcli c down Hotspot",True)
Util.cmd("sudo nmcli d wifi connect Autonomous password @11235813",True)
