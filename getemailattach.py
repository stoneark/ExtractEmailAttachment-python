# getemailattach.py
# Version: 2.0
# Date: 2017-6-9
# By: StoneArk
# Extract email attachments from MIME.

import sys
import email
import os

def parseEmailFiles(arrFiles, destFolder, ifDelete):
	successCount = 0
	for mimeFileItem in arrFiles:
		mimeMsg = email.message_from_file(open(mimeFileItem))
		if mimeMsg.is_multipart() == False:
			print('Unable to load file: ' + mimeFileItem)
			continue
		extractSuccess = extractAttachment(mimeMsg, destFolder)
		if extractSuccess == True:
			successCount+=1
			if ifDelete == True:
				os.remove(mimeFileItem)
	return successCount

def parseEmailString(strMIME, destFolder):
	mimeMsg = email.message_from_string(strMIME)
	if mimeMsg.is_multipart() == False:
		print('Unable to load email content')
		return False
	extractSuccess = extractAttachment(mimeMsg, destFolder)
	return extractSuccess

def extractAttachment(mimeMsg, destFolder):
	attachmentCount = len(mimeMsg.get_payload())
	if attachmentCount < 2:
		print('No attachment found in this email: ' + mimeFileItem)
		return False
	for i in range(1, attachmentCount):
		attachmentItem = mimeMsg.get_payload()[i]
		attachmentFilename = attachmentItem.get_filename()
		open(os.path.join(destFolder, attachmentFilename), 'wb').write(attachmentItem.get_payload(decode=True))
	return True

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print 'Usage:'
		print 'getemailattach.py <SOURCE_MIME_PATH> [<OUTPUT_FOLDER_PATH>] [-d]'
		print 'Or'
		print 'getemailattach.py -stdin [<OUTPUT_FOLDER_PATH>]'
		print '\nParameters:'
		print '<SOURCE_MIME_PATH>\tRequired, support a file path or a folder path.'
		print '<OUTPUT_FOLDER_PATH>\tOptional, default value is the current path.'
		print '-d\t\t\tDelete source MIME files after completed.'
		print '-stdin\t\t\tRead email from standard input.'
		quit()

	srcMIME = sys.argv[1]
	if srcMIME == '-stdin':
		# From standard input.
		destFolder = ''
		if len(sys.argv) > 2 and sys.argv[2] != '-d':
			destFolder = sys.argv[2]

		strMIME = sys.stdin.read()
		ifSuccess = parseEmailString(strMIME, destFolder)
		if ifSuccess == True:
			print('Attachment extracted successfully from stdin.')
		else:
			print('Attachment extracted FAILED from stdin.')
	else:
		# From local file or folder.
		arrSrcFile = []
		destFolder = ''
		ifDelete = False
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

		successCount = parseEmailFiles(arrSrcFile, destFolder, ifDelete)
		print(str(len(arrSrcFile)) + ' files found, ' + str(successCount) + ' successfully extracted.')
