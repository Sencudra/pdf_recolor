import os
import logging
import shutil
import typing
import tqdm

from pathlib import Path
from argparse import ArgumentParser

from lib.replacements_config import ReplacementsConfig
from lib.log_formatter import Formatter
from lib.pdf import PDF
from lib.content_stream_modifier import ContentStreamModifier
from lib.content_stream_coder import ContentStreamCoder


def read_arguments():
    parser = ArgumentParser(description='Replace colors in PDF files')
    parser.add_argument('target_path', type=Path, help='Path to file or directory to modify.')
    parser.add_argument('--config-path', required=True, type=Path, help='Path to config with color mapping.')
    parser.add_argument('--output-path', required=False, type=Path, help='Alternative path to directory or file to save result.')
    parser.add_argument('--verbose', action='store_true', help='Debug mode')
    return parser.parse_args()


def setup_logging(is_in_debug: bool):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if is_in_debug else logging.CRITICAL)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(Formatter())
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)


def copy_to_new_path(source_path: Path, output_path: Path):
    if os.path.isfile(source_path):
        shutil.copy(source_path, output_path)
    else:
        shutil.copytree(source_path, output_path)

    logging.info(f"Copying <{source_path.absolute()}> to <{output_path.absolute()}>")


def files_to_modify(path_to_folder: Path) -> typing.List:
    result = []
    for root, _, files in os.walk(path_to_folder):
        for filename in files:
            path = Path(root) / filename
            if filename.endswith(".pdf"):
                result.append(path)
            elif filename == ".DS_Store": # TODO: better filtering
                continue
            else:
                logging.warning(f"Unable to convert: {path}")
    return result


def modify(source_path: Path, config: ReplacementsConfig, is_debug: bool):
    if os.path.isfile(source_path):
        files = [source_path]
    else:
        files = files_to_modify(source_path)

    coder = ContentStreamCoder()
    modifier = ContentStreamModifier(config)

    should_disable_tqdm = is_debug or len(files) == 1
    for file in tqdm.tqdm(files, disable=should_disable_tqdm):
        logging.info(f"Processing {file}")
        pdf = PDF(file)
        content_decoded = coder.decode(pdf.raw_content)
        modified = modifier.modify(content_decoded)       
        pdf.raw_content = coder.encode(modified)
        pdf.save()

if __name__ == "__main__":
    arguments = read_arguments()
    setup_logging(arguments.verbose)

    logging.info("Starting running tool.")
    config = ReplacementsConfig(arguments.config_path)
    logging.info(f"Config: {config}")

    source_path = arguments.target_path
    output_path = arguments.output_path

    if output_path == None:
        logging.info("Inplace modification mode detected")
    else:
        logging.info("Provided with output folder. Source files won't be touched")
        copy_to_new_path(source_path, output_path)
        source_path = output_path

    modify(source_path, config, arguments.verbose)

    logging.info("Done.")