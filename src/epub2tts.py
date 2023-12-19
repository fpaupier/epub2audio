import argparse
import os

import sys
import warnings

from EpubToAudiobook import EpubToAudiobook

book = os.getenv("BOOK", "default_book.epub")
tts_files = os.getenv("TTS_FILES", "default.wav").split(",")
tts_provider = os.getenv("TTS_PROVIDER", "coqui")


def main():
    warnings.filterwarnings("ignore", category=UserWarning)
    parser = argparse.ArgumentParser(
        prog="EpubToAudiobook",
        description="Read an epub (or other source) to audiobook format",
    )
    parser.add_argument("sourcefile", type=str, help="The epub or text file to process")
    parser.add_argument(
        "--engine",
        type=str,
        default="tts",
        nargs="?",
        const="tts",
        help="Which TTS to use [tts|xtts|openai]",
    )
    parser.add_argument(
        "--xtts",
        type=str,
        help="Sample wave/mp3 file(s) for XTTS v2 training separated by commas",
    )
    parser.add_argument("--openai", type=str, help="OpenAI API key if engine is OpenAI")
    parser.add_argument(
        "--model",
        type=str,
        nargs="?",
        const="tts_models/en/vctk/vits",
        default="tts_models/en/vctk/vits",
        help="TTS model to use, default: tts_models/en/vctk/vits",
    )
    parser.add_argument(
        "--speaker",
        type=str,
        default="p335",
        nargs="?",
        const="p335",
        help="Speaker to use (ex p335 for VITS, or onyx for OpenAI)",
    )
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Scan the epub to show beginning of chapters, then exit",
    )
    parser.add_argument(
        "--start",
        type=int,
        nargs="?",
        const=1,
        default=1,
        help="Chapter/part to start from",
    )
    parser.add_argument(
        "--end",
        type=int,
        nargs="?",
        const=999,
        default=999,
        help="Chapter/part to end with",
    )
    parser.add_argument(
        "--language",
        type=str,
        nargs="?",
        const="en",
        default="en",
        help="Language of the epub, default: en",
    )
    parser.add_argument(
        "--minratio",
        type=int,
        nargs="?",
        const=88,
        default=88,
        help="Minimum match ratio between text and transcript",
    )
    parser.add_argument(
        "--skiplinks", action="store_true", help="Skip reading any HTML links"
    )
    parser.add_argument(
        "--bitrate",
        type=str,
        nargs="?",
        const="69k",
        default="69k",
        help="Specify bitrate for output file",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()
    print(args)

    if args.openai:
        args.engine = "openai"
    if args.xtts:
        args.engine = "xtts"
    mybook = EpubToAudiobook(
        source=args.sourcefile,
        start=args.start,
        end=args.end,
        skiplinks=args.skiplinks,
        engine=args.engine,
        minratio=args.minratio,
        model_name=args.model,
        debug=args.debug,
        language=args.language,
    )

    print("Language selected: " + mybook.language)

    if mybook.sourcetype == "epub":
        mybook.get_chapters_epub()
    else:
        mybook.get_chapters_text()
    if args.scan:
        sys.exit()
    mybook.read_book(
        voice_samples=args.xtts,
        engine=args.engine,
        openai=args.openai,
        model_name=args.model,
        speaker=args.speaker,
        bitrate=args.bitrate,
    )


if __name__ == "__main__":
    main()
