import logging
import smtplib
from email.message import EmailMessage
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    def _send_email(self, recipient: str, subject: str, body_text: str, body_html: Optional[str] = None) -> None:
        """
        Send an email via SMTP if configured, or log to console for development.
        """
        if settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASSWORD:
            try:
                msg = EmailMessage()
                msg["Subject"] = subject
                msg["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
                msg["To"] = recipient
                msg.set_content(body_text)
                if body_html:
                    msg.add_alternative(body_html, subtype="html")

                with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT or 587) as server:
                    if settings.SMTP_TLS:
                        server.starttls()
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                    server.send_message(msg)
                logger.info(f"Email successfully sent to {recipient}")
            except Exception as e:
                logger.error(f"Failed to send email to {recipient}: {e}", exc_info=True)
        else:
            # Development/local fallback: log clearly so developers can grab the token
            logger.info(
                f"\n{'='*70}\n"
                f"[EMAIL SERVICE - DEV MODE]\n"
                f"To: {recipient}\n"
                f"Subject: {subject}\n"
                f"Body:\n{body_text}\n"
                f"{'='*70}"
            )

    def send_verification_email(self, email_to: str, token: str) -> None:
        """
        Send an email with the verification token/link.
        """
        subject = f"{settings.PROJECT_NAME} - Verify your email address"
        body_text = (
            f"Hello,\n\n"
            f"Thank you for registering at {settings.PROJECT_NAME}.\n"
            f"Please use the following verification token to verify your email address:\n\n"
            f"Verification Token: {token}\n\n"
            f"This token will expire in {settings.EMAIL_VERIFY_TOKEN_EXPIRE_HOURS} hours.\n\n"
            f"If you did not create an account, please ignore this email."
        )
        body_html = (
            f"<p>Hello,</p>"
            f"<p>Thank you for registering at <strong>{settings.PROJECT_NAME}</strong>.</p>"
            f"<p>Please use the following verification token to verify your account:</p>"
            f"<p><code>{token}</code></p>"
            f"<p>This token will expire in {settings.EMAIL_VERIFY_TOKEN_EXPIRE_HOURS} hours.</p>"
            f"<p>If you did not create an account, please ignore this email.</p>"
        )
        self._send_email(recipient=email_to, subject=subject, body_text=body_text, body_html=body_html)

    def send_password_reset_email(self, email_to: str, token: str) -> None:
        """
        Send a password reset email with the reset token/link.
        """
        subject = f"{settings.PROJECT_NAME} - Password Reset Request"
        body_text = (
            f"Hello,\n\n"
            f"We received a request to reset your password for {settings.PROJECT_NAME}.\n"
            f"Please use the following token to reset your password:\n\n"
            f"Reset Token: {token}\n\n"
            f"This token will expire in {settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS} hours.\n\n"
            f"If you did not request a password reset, you can safely ignore this email."
        )
        body_html = (
            f"<p>Hello,</p>"
            f"<p>We received a request to reset your password for <strong>{settings.PROJECT_NAME}</strong>.</p>"
            f"<p>Please use the following token to reset your password:</p>"
            f"<p><code>{token}</code></p>"
            f"<p>This token will expire in {settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS} hours.</p>"
            f"<p>If you did not request a password reset, you can safely ignore this email.</p>"
        )
        self._send_email(recipient=email_to, subject=subject, body_text=body_text, body_html=body_html)


email_service = EmailService()
