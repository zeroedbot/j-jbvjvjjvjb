# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from . import *


@vc_asst("(leave|stop)$")
async def stop_vc(event):
    CallsClient.stop_playout()
    await eor(event, "∆ Stopped Successfully")
