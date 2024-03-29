# Imported from https://github.com/sandy1709/catuserbot

import io

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern="^.itos$")
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("ngab ini bukan gambar balas ke gambar_-")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("ngab!, Ini bukan gambar!!! ")
        return
    chat = "@buildstickerbot"
    await event.edit("Membuat Sticker...")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=164977173)
            )
            msg = await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("unblock me (@buildstickerbot) and try again")
            return
        if response.text.startswith("Hi!"):
            await event.edit(
                "Can you kindly disable your forward privacy settings for good?"
            )
        else:
            await event.delete()
            await bot.send_read_acknowledge(conv.chat_id)
            await event.client.send_message(event.chat_id, response.message)
            await event.client.delete_message(event.chat_id, [msg.id, response.id])


@register(outgoing=True, pattern="^.stoi$")
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("Balas di Sticker Goblok!!")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("Balas di Sticker Tolol!!")
        return
    chat = "@FormatFactory_bot"
    await event.edit("Mengubah ke gambar..")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=611085086)
            )
            msg = await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("unblock me (@FormatFactory_bot) to work")
            return
        if response.text.startswith("Aku hanya paham stiker"):
            await event.edit(
                "Sorry i cant't convert it check wheter is non animated sticker or not"
            )
        else:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=611085086)
            )
            response = await response
            if response.text.startswith("..."):
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=611085086)
                )
                response = await response
                await event.delete()
                await event.client.send_message(
                    event.chat_id, response.message, reply_to=reply_message.id
                )
                await event.client.delete_message(event.chat_id, [msg.id, response.id])
            else:
                await event.edit("try again")
        await bot.send_read_acknowledge(conv.chat_id)


@register(outgoing=True, pattern="^.get$")
async def sticker_to_png(sticker):
    if not sticker.is_reply:
        await sticker.edit("`NULL information to feftch...`")
        return False

    img = await sticker.get_reply_message()
    if not img.document:
        await sticker.edit("Ini Bukan sticker ngab!!!...`")
        return False

    await sticker.edit("`Stiker berhasil di ubah!`")
    image = io.BytesIO()
    await sticker.client.download_media(img, image)
    image.name = "sticker.png"
    image.seek(0)
    await sticker.client.send_file(
        sticker.chat_id, image, reply_to=img.id, force_document=True
    )
    await sticker.delete()
    return


CMD_HELP.update(
    {
        "stickers_v2": ">`.itos`"
        "\nUsage: balas .itos ke gambar untuk mengubahnya menjadi stiker  "
        "\n\n>`.stoi`"
        "\nUsage: balas ke stiker untuk mendapatkan preview stiker."
        "\n\n>`.get`"
        "\nUsage: balas ke stiker untuk mendapatkan file 'PNG' stiker."
    }
)
