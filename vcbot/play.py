# Ultroid - UserBot
# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.


from . import *


@vc_asst("play")
async def join_handler(event):
    xqsong = event.text.split(" ", 1)
    try:
        qsong = xqsong[1]
    except IndexError:
        repl = await event.get_reply_message()
        qsong = ""
    if not (qsong or repl and repl.file):
        return await event.reply("Please give a song name.")
    x = await event.reply("`Downloading...`")
    if qsong:
        song, thumb, title, duration = await download(event, qsong, event.chat_id)
    else:
        dl = await repl.download_media()
        song = f"VCSONG_{event.chat_id}.raw"
        await bash(f"ffmpeg -i {dl} -f s16le -ac 2 -ar 48000 -acodec pcm_s16le {song}")
        try:
            thumb = await repl.download_media(thumb=-1)
        except IndexError:
            thumb = None
        title, duration = repl.file.title, repl.file.duration
    CallsClient.input_file_name = song
    # group_call = CallsClient.get_file_group_call(song, play_on_repeat=False)
    try:
        await CallsClient.start(event.chat_id)
    except RuntimeError:
        return await x.edit("No voice call active !")
    await x.delete()
    if event.chat_id in CURRENT.keys() and CURRENT[event.chat_id]:
        add_to_queue(event.chat_id, song, qsong, inline_mention(event.sender), duration)
        return await event.reply(f"Added {qsong} to Queue at #{list(QUEUE[chat.id].keys())[-1]}")
    await event.reply(
        "Started playing {} in {}.\nDuration: {}".format(
            title, event.chat_id, time_formatter(duration * 1000)
        ),
        file=thumb,
    )
    CURRENT.update({event.chat_id, True})
    # os.remove(song)
