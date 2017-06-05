import sys
import email
import os

if len(sys.argv) < 2:
	print 'getemailattach.py <SOURCE_MIME_PATH> [<DESTINATION_FOLDER_PATH>]'
	quit()

arrSrcFile = []
destFolder = ''
srcMIME = sys.argv[1]
if (len(sys.argv) > 2):
	destFolder = sys.argv[2]

if os.path.isfile(srcMIME):
	arrSrcFile = [srcMIME]
else:
	arrSrcFile = [os.path.join(srcMIME, f) for f in os.listdir(srcMIME) if os.path.isfile(os.path.join(srcMIME, f))]

for mimeFileItem in arrSrcFile:
	mimeMsg = email.message_from_file(open(mimeFileItem))
	if mimeMsg.is_multipart() == False:
		print('Unable to load file: ' + mimeFileItem)
		continue
	attachmentCount = len(mimeMsg.get_payload())
	if attachmentCount < 2:
		print 'No attachment found in this email'
		quit()
	for i in range(1, attachmentCount):
		attachmentItem = mimeMsg.get_payload()[i]
		attachmentFilename = attachmentItem.get_filename()
		open(os.path.join(destFolder, attachmentFilename), 'wb').write(attachmentItem.get_payload(decode=True))
