import os
import pikepdf
import logging
import coloredlogs
import argparse

# Configuration
PDF_PASSWORD = "SecretPassword"

# Configure logging
script_name = os.path.basename(__file__)
log_file = f"{script_name}.log"

# Set up file logging
logging.basicConfig(
    level=logging.DEBUG,
    filename=log_file,
    filemode="a",
    encoding="utf-8",
    format='[%(asctime)s] [%(levelname)s] %(message)s'
)

# Set up console logging
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
coloredlogs.install(
    level=logging.DEBUG,
    logger=logger,
    fmt='[%(asctime)s] [%(levelname)s] %(message)s'
)


def process_pdf(filepath):
    if not filepath.lower().endswith(".pdf"):
        logger.error(f"{filepath} is not a PDF file.")
        return

    logger.info(f"Processing file: {filepath}")
    try:
        # Try to open the PDF to check if it's password-protected
        pikepdf.open(filepath)
        logger.info(f"{os.path.basename(filepath)} is not password protected.")
    except pikepdf.PasswordError:
        try:
            # Try to unlock the PDF with the given password
            with pikepdf.open(filepath, password=PDF_PASSWORD, allow_overwriting_input=True) as pdf:
                pdf.save(filepath)
                logger.info(f"Successfully removed password from {os.path.basename(filepath)}.")
        except pikepdf.PasswordError:
            logger.error(f"Incorrect password for {os.path.basename(filepath)}.")
        except Exception as e:
            logger.error(f"Failed to remove password from {os.path.basename(filepath)}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a PDF file.")
    parser.add_argument("file", help="Path to the PDF file to be processed")
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        logger.error(f"The file {args.file} does not exist.")
    else:
        process_pdf(args.file)

    os.system("pause")
