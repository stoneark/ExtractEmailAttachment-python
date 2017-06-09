# ExtractEmailAttachment-python
A simple python script to extract attachments from email source file (MIME).

## Usage
```bash
python getemailattach.py <SOURCE_MIME_PATH> [<OUTPUT_FOLDER_PATH>] [-d]
```

Or
```bash
python getemailattach.py -stdin [<OUTPUT_FOLDER_PATH>]
```

## Parameters
* <SOURCE_MIME_PATH>: Required, support a file path or a folder path.
* <OUTPUT_FOLDER_PATH>: Optional, default value is the current path.
* -d: Delete source MIME files after completed.
* -stdin: Read email from standard input.