# 安装模块 pip install PyEmail

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender = '147010753@qq.com'  # 发件人邮箱账号
my_pass = 'xxxxxxxxxxxxxx'    # 发件人邮箱授权码, 不是qq密码 教程https://zhuanlan.zhihu.com/p/643897161
my_user = '147010753@qq.com'    # 收件人邮箱账号，发送给自己


def email_func(Email_content = None, Email_subject = None):
	try:
		msg = MIMEText(Email_content, 'plain', 'utf-8')
		msg['From'] = formataddr(["天涯", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
		msg['To'] = formataddr(["tianya", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
		msg['Subject'] = Email_subject  # 邮件的主题，也可以说是标题

		server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
		server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱授权码
		server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
		server.quit()  # 关闭连接
		print("邮件发送成功")
	except Exception:
		print("邮件发送失败")

if __name__ == '__main__':
	email_func("网络请求出错了，请重新运行程序！", "python爬虫")
