"""
Загрузка файлов: аргументом метода и полем объекта (attach://). Проверяется то,
что получил фейковый Telegram, — настоящий multipart-запрос.
"""

from pathlib import Path
from typing import BinaryIO

import pytest
from aiohttp import web

from selfrot import Bot, BotDefaults
from selfrot.methods import SendMediaGroup
from selfrot.methods.base import _Attachments
from selfrot.types import (
    InputFile,
    InputMediaPhoto,
    InputMediaVideo,
    InputSticker,
)

from .conftest import TOKEN, FakeTelegram, Upload, message_result


@pytest.fixture
def album(telegram: FakeTelegram) -> None:
    telegram.on("sendMediaGroup", [message_result()])


class TestTopLevel:
    async def test_file_argument_is_a_multipart_part(self, telegram, bot):
        await bot.send_photo(1, photo=InputFile(b"img", "cat.jpg"), caption="кот")

        method, body = telegram.last()
        assert method == "sendPhoto"
        assert body == {
            "chat_id": 1,
            "caption": "кот",
            "photo": Upload("cat.jpg", "image/jpeg", b"img"),
        }


class TestAttach:
    async def test_album_mixes_uploads_and_file_ids(self, telegram, bot, album, tmp_path):
        clip = tmp_path / "clip.mp4"
        clip.write_bytes(b"video-bytes")

        await bot.send_media_group(
            1,
            media=[
                InputMediaPhoto(media=InputFile(b"a", "a.jpg"), caption="первое"),
                InputMediaPhoto(media="AgACAgI-file-id"),
                InputMediaVideo(
                    media=InputFile.from_path(clip),
                    thumbnail=InputFile(b"t", "thumb.jpg"),
                ),
            ],
        )

        body = telegram.last()[1]
        assert body["media"] == [
            {"type": "photo", "media": "attach://file0", "caption": "первое"},
            {"type": "photo", "media": "AgACAgI-file-id"},
            {"type": "video", "media": "attach://file1", "thumbnail": "attach://file2"},
        ]
        assert body["file0"] == Upload("a.jpg", "image/jpeg", b"a")
        assert body["file1"] == Upload("clip.mp4", "video/mp4", b"video-bytes")
        assert body["file2"] == Upload("thumb.jpg", "image/jpeg", b"t")

    async def test_same_file_object_is_uploaded_once(self, telegram, bot, album):
        cover = InputFile(b"c", "cover.jpg")
        await bot.send_media_group(
            1,
            media=[
                InputMediaVideo(media="v1", cover=cover),
                InputMediaVideo(media="v2", cover=cover),
            ],
        )

        body = telegram.last()[1]
        assert [item["cover"] for item in body["media"]] == ["attach://file0"] * 2
        assert "file1" not in body

    async def test_any_object_with_attach_field(self, telegram, bot):
        telegram.on("addStickerToSet", True)
        await bot.add_sticker_to_set(
            7,
            "pack_by_test_bot",
            InputSticker(
                sticker=InputFile(b"webp", "s.webp"), format="static", emoji_list=["😀"]
            ),
        )

        body = telegram.last()[1]
        assert body["sticker"]["sticker"] == "attach://file0"
        assert body["file0"].content == b"webp"

    async def test_defaults_keep_the_file(self, telegram, album):
        class Configured(Bot):
            defaults = BotDefaults(parse_mode="HTML")

        api = Configured(TOKEN)
        try:
            await api.send_media_group(
                1, media=[InputMediaPhoto(media=InputFile(b"a", "a.jpg"), caption="<b>1</b>")]
            )
        finally:
            await api.close_session()

        body = telegram.last()[1]
        assert body["media"][0]["media"] == "attach://file0"
        assert body["media"][0]["parse_mode"] == "HTML"
        assert body["file0"].content == b"a"

    def test_without_files_payload_stays_plain_json(self):
        payload = SendMediaGroup(
            chat_id=1, media=[InputMediaPhoto(media="id1"), InputMediaPhoto(media="id2")]
        ).to_payload()
        assert payload == {
            "chat_id": 1,
            "media": [{"type": "photo", "media": "id1"}, {"type": "photo", "media": "id2"}],
        }

    def test_part_names_do_not_shadow_method_arguments(self):
        attachments = _Attachments(taken={"file0", "file2"})
        names = [attachments.attach(InputFile(b"x")) for _ in range(2)]
        assert names == ["attach://file1", "attach://file3"]


class TestFilesFromDisk:
    @pytest.fixture
    def opened(self, monkeypatch) -> list[BinaryIO]:
        """Все файлы, которые транспорт открыл с диска."""
        files: list[BinaryIO] = []
        original = InputFile._open

        async def tracking(self: InputFile):
            content = await original(self)
            if not isinstance(content, bytes):
                files.append(content)
            return content

        monkeypatch.setattr(InputFile, "_open", tracking)
        return files

    async def test_closed_after_request(self, telegram, bot, album, tmp_path, opened):
        path = tmp_path / "a.jpg"
        path.write_bytes(b"a")
        await bot.send_media_group(1, media=[InputMediaPhoto(media=InputFile.from_path(path))])

        assert len(opened) == 1 and opened[0].closed

    async def test_closed_when_telegram_fails(self, telegram, bot, tmp_path, opened):
        path = tmp_path / "a.jpg"
        path.write_bytes(b"a")
        telegram.on("sendPhoto", lambda _b: web.Response(status=502, text="<html>"))

        with pytest.raises(Exception):
            await bot.send_photo(1, photo=InputFile.from_path(path))
        assert opened and all(file.closed for file in opened)

    async def test_retry_sends_the_whole_file_again(self, telegram, bot, tmp_path):
        path = tmp_path / "big.bin"
        content = bytes(range(256)) * 4096  # 1 МБ: несколько частей у aiohttp
        path.write_bytes(content)
        state = {"n": 0}

        def flood_once(body):
            state["n"] += 1
            assert body["document"].content == content
            if state["n"] == 1:
                return web.json_response(
                    {
                        "ok": False,
                        "error_code": 429,
                        "description": "Too Many Requests",
                        "parameters": {"retry_after": 0},
                    },
                    status=429,
                )
            return message_result()

        telegram.on("sendDocument", flood_once)
        await bot.send_document(1, document=InputFile.from_path(Path(path)))
        assert state["n"] == 2
