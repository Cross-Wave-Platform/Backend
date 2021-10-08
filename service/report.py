from email.mime.multipart import MIMEMultipart
from email import encoders
import mimetypes
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from config.config import get_yaml_config
import smtplib, os

__all__=['Send_Email']

class Send_Email:
	def __init__(self,subject,recipients):
		self.subject = subject
		self.recipients = recipients
		self.htmlbody = ''
		self.sender = get_yaml_config('sender')
		self.senderpass = get_yaml_config('sender_pass')
		self.attachments = []
		self.cwd = os.path.join(os.getcwd(),"storage/tmp_up")
		if not os.path.exists(self.cwd): 
			os.makedirs(self.cwd)
 
	def send(self):
		msg = MIMEMultipart('alternative')
		msg['From']=self.sender
		msg['Subject']=self.subject
		msg['To'] = ", ".join(self.recipients) # to must be array of the form ['mailsender135@gmail.com']
		msg.preamble = "preamble goes here"
		#check if there are attachments if yes, add them
		if self.attachments:
			self.attach(msg)
		#add html body after attachments
		msg.attach(MIMEText(self.htmlbody, 'html'))
		#send
		s = smtplib.SMTP('smtp.gmail.com:587')
		s.starttls()
		s.login(self.sender,self.senderpass)
		s.sendmail(self.sender, self.recipients, msg.as_string())
		#test
		s.quit()
	
	def htmladd(self, html):
		self.htmlbody = self.htmlbody+'<p></p>'+html
 
	def attach(self,msg):
		for f in self.attachments:
			
			ctype, encoding = mimetypes.guess_type(f)
			if ctype is None or encoding is not None:
				ctype = "application/octet-stream"
			
			maintype, subtype = ctype.split("/", 1)
 
 
			if maintype == "text":
				fp = open(f)
				# Note: we should handle calculating the charset
				attachment = MIMEText(fp.read(), _subtype=subtype)
				fp.close()
			elif maintype == "image":
				fp = open(f, "rb")
				attachment = MIMEImage(fp.read(), _subtype=subtype)
				fp.close()
			elif maintype == "audio":
				fp = open(f, "rb")
				attachment = MIMEAudio(fp.read(), _subtype=subtype)
				fp.close()
			else:
				fp = open(f, "rb")
				attachment = MIMEBase(maintype, subtype)
				attachment.set_payload(fp.read())
				fp.close()
				encoders.encode_base64(attachment)
			attachment.add_header("Content-Disposition", "attachment", filename=f.split('/')[-1])
			attachment.add_header('Content-ID', '<{}>'.format(f))
			msg.attach(attachment)
			os.remove(f)

	def addattach(self, files):
		f_list = []
		for file in files:
			cwd = os.path.join(self.cwd, file.filename)
			file.save(cwd)
			f_list.append(cwd)
		self.attachments = self.attachments + f_list