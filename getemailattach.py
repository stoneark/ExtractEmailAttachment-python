import sys
import email

if len(sys.argv) < 2:
	print 'getemailattach.py <SOURCE_MIME_FILE_PATH>'
	quit()

srcMIME = sys.argv[1]
emailMsg = email.message_from_file(open(srcMIME))
attachmentCount = len(emailMsg.get_payload())
if attachmentCount < 2:
	print 'No attachment found in this email'
	quit()
for i in range(1, attachmentCount):
	attachmentItem = emailMsg.get_payload()[i]
	attachmentFilename = attachmentItem.get_filename()
	open(attachmentFilename, 'wb').write(attachmentItem.get_payload(decode=True))
