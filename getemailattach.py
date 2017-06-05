import sys
import email
import os

if len(sys.argv) < 2:
	print 'Usage:'
	print 'getemailattach.py <SOURCE_MIME_PATH> [<OUTPUT_FOLDER_PATH>] [-d]'
	print 'Parameters:'
	print '<SOURCE_MIME_PATH>\tRequired, support a file path or a folder path.'
	print '<OUTPUT_FOLDER_PATH>\tOptional, default value is the current path.'
	print '-d\t\t\tDelete source MIME files after completed.'
	quit()

arrSrcFile = []
destFolder = ''
ifDelete = False
successCount = 0
srcMIME = sys.argv[1]
if len(sys.argv) > 2:
	if sys.argv[2] == '-d':
		ifDelete = True
	else:
		destFolder = sys.argv[2]
		if len(sys.argv) > 3 and sys.argv[3] == '-d':
			ifDelete = True

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
		print('No attachment found in this email: ' + mimeFileItem)
		continue
	for i in range(1, attachmentCount):
		attachmentItem = mimeMsg.get_payload()[i]
		attachmentFilename = attachmentItem.get_filename()
		open(os.path.join(destFolder, attachmentFilename), 'wb').write(attachmentItem.get_payload(decode=True))
	if ifDelete == True:
		os.remove(mimeFileItem)
	successCount+=1
print(str(len(arrSrcFile)) + ' files found, ' + str(successCount) + ' successfully extracted.')
