import imaplib
import smtplib
import os
import httpx
from email import policy
from email.parser import BytesParser
from email.utils import parseaddr
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SRV_IMAP = os.environ["MAIL_IMAP"]
SRV_SMTP = os.environ["MAIL_IMAP"]
HD_MAIL = os.environ["MAIL_USER"]
PASSWORD = os.environ["MAIL_PASS"]
API_URL = os.environ["R_API_URL"]
AGENT_ID = os.environ["AGENT_ID"]
FOLDER_ID = os.environ["FOLDER_ID"]
IAM = os.environ["IAM"]


def get_msg_content(msg_data: bytes) -> dict[str, str]:
    msg = BytesParser(
        policy=policy.default
    ).parsebytes(msg_data)

    subject = str(msg.get("Subject", "Без темы"))
    
    sender_name, sender_addr = parseaddr(msg["From"])

    body = msg.get_body(
        preferencelist=("plain",)
    )

    text = body.get_content() if body else ""

    return {
        "sender_name": sender_name,
        "sender_addr": sender_addr,
        "subject": subject,
        "body": str(text)
    }

def ask_agent(question: str) -> str:
    headers = {
        "Authorization": f"Bearer {IAM}",
        "Content-Type": "application/json",
        "OpenAI-Project": FOLDER_ID,
    }

    # payload = {
    #     "prompt": {
    #         "id": AGENT_ID,
    #     },
    #     "input": question,
    # }

    payload = {
        "model": f"gpt://{FOLDER_ID}/yandexgpt/latest",
        "instructions": (
            "Ты сотрудник службы технической поддержки. "
            "Помогай сотрудникам решать рабочие вопросы."
        ),
        "input": question,
    }

    response = httpx.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=60,
    )
    print(response.status_code)
    print(response.text)

    response.raise_for_status()
    data = response.json()
    return data["output"][0]["content"][0]["text"]

def send_email(recipient: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = HD_MAIL
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP_SSL(SRV_SMTP, 465, timeout=30) as smtp:
        smtp.login(HD_MAIL, PASSWORD)
        smtp.send_message(message)

def process_tickets():
    if not all((SRV_IMAP, HD_MAIL, PASSWORD, SRV_IMAP, AGENT_ID)):
        raise ValueError("Connection parameters are not specified.")

    with imaplib.IMAP4_SSL(SRV_IMAP) as imap:
        imap.login(
            HD_MAIL, 
            PASSWORD
        )
        
        status, _ = imap.select("INBOX")

        if status != "OK":
            raise RuntimeError("Could not open INBOX")

        status, data = imap.search(
            None,
            "UNSEEN"
        )
        if status != "OK":
            raise RuntimeError("Unable to search for emails")

        mail_ids = data[0].split()
        for mail_id in mail_ids:
            let_status, msg_data = imap.fetch(
                mail_id,
                "(BODY.PEEK[])"
                )

            if let_status != "OK":
                print("Letter was doesn't read.")
                continue
            msg = get_msg_content(msg_data[0][1])
            answer = ask_agent(msg["body"])
            send_email(
                msg["sender_addr"],
                f"Re: {msg['subject']}",
                answer
            )
            imap.store(mail_id, "+FLAGS", "\\Seen")

def main():
    try:
        process_tickets()
    except imaplib.IMAP4.error as e:
        print(f'IMAP error: {e}')

if __name__ == "__main__":
    main()
