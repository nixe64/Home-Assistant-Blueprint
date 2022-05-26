"""Support for the Amazon Polly text to speech service."""
from __future__ import annotations

import logging
import typing

import boto3
import botocore
import homeassistant.const as ha_const
import homeassistant.core as ha_core
import homeassistant.helpers.config_validation as cv
import homeassistant.helpers.typing as ha_typing
import voluptuous as vol
from homeassistant.components import tts

from .const import (AWS_CONF_CONNECT_TIMEOUT, AWS_CONF_MAX_POOL_CONNECTIONS,
                    AWS_CONF_READ_TIMEOUT, CONF_ACCESS_KEY_ID, CONF_CONFIG,
                    CONF_ENGINE, CONF_OUTPUT_FORMAT, CONF_REGION,
                    CONF_SAMPLE_RATE, CONF_SECRET_ACCESS_KEY, CONF_SPEECH_TYPE,
                    CONF_VOICE, CONTENT_TYPE_EXTENSIONS, DEFAULT_ENGINE,
                    DEFAULT_OUTPUT_FORMAT, DEFAULT_REGION,
                    DEFAULT_SAMPLE_RATES, DEFAULT_SPEECH_TYPE, DEFAULT_VOICE,
                    SUPPORTED_ENGINES, SUPPORTED_OUTPUT_FORMATS,
                    SUPPORTED_REGIONS, SUPPORTED_SAMPLE_RATES,
                    SUPPORTED_SAMPLE_RATES_MAP, SUPPORTED_SPEECH_TYPES,
                    SUPPORTED_VOICES)

_LOGGER: typing.Final = logging.getLogger(__name__)

PLATFORM_SCHEMA: typing.Final = tts.PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_REGION, default=DEFAULT_REGION): vol.In(SUPPORTED_REGIONS),
        vol.Inclusive(CONF_ACCESS_KEY_ID, ha_const.ATTR_CREDENTIALS): cv.string,
        vol.Inclusive(CONF_SECRET_ACCESS_KEY, ha_const.ATTR_CREDENTIALS): cv.string,
        vol.Exclusive(ha_const.CONF_PROFILE_NAME, ha_const.ATTR_CREDENTIALS): cv.string,
        vol.Optional(CONF_VOICE, default=DEFAULT_VOICE): vol.In(SUPPORTED_VOICES),
        vol.Optional(CONF_ENGINE, default=DEFAULT_ENGINE): vol.In(SUPPORTED_ENGINES),
        vol.Optional(CONF_OUTPUT_FORMAT, default=DEFAULT_OUTPUT_FORMAT): vol.In(
            SUPPORTED_OUTPUT_FORMATS
        ),
        vol.Optional(CONF_SAMPLE_RATE): vol.All(
            cv.string, vol.In(SUPPORTED_SAMPLE_RATES)
        ),
        vol.Optional(CONF_SPEECH_TYPE, default=DEFAULT_SPEECH_TYPE): vol.In(
            SUPPORTED_SPEECH_TYPES
        ),
    }
)


def get_engine(
    hass: ha_core.HomeAssistant,
    config: ha_typing.ConfigType,
    discovery_info: ha_typing.DiscoveryInfoType | None = None,
) -> tts.Provider | None:

    # pylint: disable=unused-argument

    """Set up Amazon Polly speech component."""
    output_format = config[CONF_OUTPUT_FORMAT]
    sample_rate = config.get(CONF_SAMPLE_RATE, DEFAULT_SAMPLE_RATES[output_format])
    if sample_rate not in SUPPORTED_SAMPLE_RATES_MAP[output_format]:
        _LOGGER.error(
            "%s is not a valid sample rate for %s", sample_rate, output_format
        )
        return None

    config[CONF_SAMPLE_RATE] = sample_rate

    profile: str | None = config.get(ha_const.CONF_PROFILE_NAME)

    if bool(profile):
        boto3.setup_default_session(profile_name=profile)

    aws_config = {
        CONF_REGION: config[CONF_REGION],
        CONF_ACCESS_KEY_ID: config.get(CONF_ACCESS_KEY_ID),
        CONF_SECRET_ACCESS_KEY: config.get(CONF_SECRET_ACCESS_KEY),
        CONF_CONFIG: botocore.client.Config(
            connect_timeout=AWS_CONF_CONNECT_TIMEOUT,
            read_timeout=AWS_CONF_READ_TIMEOUT,
            max_pool_connections=AWS_CONF_MAX_POOL_CONNECTIONS,
        ),
    }

    del config[CONF_REGION]
    del config[CONF_ACCESS_KEY_ID]
    del config[CONF_SECRET_ACCESS_KEY]

    polly_client = boto3.client("polly", **aws_config)

    supported_languages: list[str] = []

    all_voices: dict[str, dict[str, str]] = {}

    all_voices_req = polly_client.describe_voices()

    for voice in all_voices_req.get("Voices", []):
        voice_id: str | None = voice.get("Id")
        if voice_id is None:
            continue
        all_voices[voice_id] = voice
        language_code: str | None = voice.get("LanguageCode")
        if bool(language_code) and language_code not in supported_languages:
            supported_languages.append(str(language_code))

    return AmazonPollyProvider(polly_client, config, supported_languages, all_voices)


class AmazonPollyProvider(tts.Provider):
    """Amazon Polly speech api provider."""

    def __init__(
        self,
        polly_client: boto3.client,
        config: ha_typing.ConfigType,
        supported_languages: list[str],
        all_voices: dict[str, dict[str, str]],
    ) -> None:
        """Initialize Amazon Polly provider for TTS."""
        self.client = polly_client
        self.config = config
        self.supported_langs = supported_languages
        self.all_voices = all_voices
        self.default_voice: str = self.config[CONF_VOICE]
        self.name = "Amazon Polly"

    @property
    def supported_languages(self) -> list[str]:
        """Return a list of supported languages."""
        return self.supported_langs

    @property
    def default_language(self) -> str | None:
        """Return the default language."""
        return self.all_voices.get(self.default_voice, {}).get("LanguageCode")

    @property
    def default_options(self) -> dict[str, str]:
        """Return dict include default options."""
        return {CONF_VOICE: self.default_voice}

    @property
    def supported_options(self) -> list[str]:
        """Return a list of supported options."""
        return [
            CONF_VOICE,
            CONF_ENGINE,
            CONF_OUTPUT_FORMAT,
            CONF_SAMPLE_RATE,
            CONF_SPEECH_TYPE,
        ]

    def get_tts_audio(
        self,
        message: str,
        language: str | None = None,
        options: dict[str, str] | None = None,
    ) -> tts.TtsAudioType:
        """Request TTS file from Polly."""
        if options is None or language is None:
            _LOGGER.debug("language and/or options were missing")
            return None, None
        voice_id = options.get(CONF_VOICE, self.default_voice)
        voice_in_dict = self.all_voices[voice_id]
        if language != voice_in_dict.get("LanguageCode"):
            _LOGGER.error("%s does not support the %s language", voice_id, language)
            return None, None

        engine = options.get(CONF_ENGINE, None)
        output_format = options.get(CONF_OUTPUT_FORMAT, None)
        sample_rate = options.get(CONF_SAMPLE_RATE, None)
        text_type = options.get(CONF_SPEECH_TYPE, None)
        if not bool(engine):
            engine = self.config[CONF_ENGINE]
        if not bool(output_format):
            output_format = self.config[CONF_OUTPUT_FORMAT]
        if not bool(sample_rate):
            sample_rate = self.config[CONF_SAMPLE_RATE]
        if not bool(text_type):
            text_type = self.config[CONF_SPEECH_TYPE]

        _LOGGER.debug("Requesting TTS file for text: %s", message)
        resp = self.client.synthesize_speech(
            Engine=engine,
            OutputFormat=output_format,
            SampleRate=sample_rate,
            Text=message,
            TextType=text_type,
            VoiceId=voice_id,
        )

        _LOGGER.debug("Reply received for TTS: %s", message)
        return (
            CONTENT_TYPE_EXTENSIONS[resp.get("ContentType")],
            resp.get("AudioStream").read(),
        )
