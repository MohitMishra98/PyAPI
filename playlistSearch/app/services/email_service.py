import logging
import smtplib
from email.message import EmailMessage
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    def _send_email(
        self,
        recipient: str,
        subject: str,
        body_text: str,
        body_html: Optional[str] = None,
    ) -> None:
        """
        Send an email via SMTP. Requires SMTP credentials in .env.
        No email content or tokens are printed to the console.
        """
        if not (settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASSWORD):
            raise RuntimeError(
                "SMTP credentials are not configured. Please set SMTP_HOST, "
                "SMTP_PORT, SMTP_USER, and SMTP_PASSWORD in your .env file."
            )

        try:
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
            msg["To"] = recipient
            msg.set_content(body_text)

            if body_html:
                msg.add_alternative(body_html, subtype="html")

            # Support SSL port 465 or STARTTLS port 587
            if settings.SMTP_PORT == 465:
                with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT or 587) as server:
                    if settings.SMTP_TLS:
                        server.starttls()
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                    server.send_message(msg)

            logger.info(f"Email '{subject}' successfully sent to {recipient}")
        except Exception as e:
            logger.error(f"Failed to send email to {recipient}: {e}", exc_info=True)
            raise

    def send_verification_email(self, email_to: str, token: str) -> None:
        """
        Send a beautifully styled email with a CTA button, raw link, and token for email verification.
        """
        verification_url = f"{settings.FRONTEND_URL.rstrip('/')}/verify-email?token={token}"
        subject = f"{settings.PROJECT_NAME} - Verify Your Email Address"

        body_text = (
            f"Hello,\n\n"
            f"Thank you for registering at {settings.PROJECT_NAME}.\n\n"
            f"Please verify your email address by visiting this link:\n"
            f"{verification_url}\n\n"
            f"If you are using the API directly, your verification token is:\n"
            f"{token}\n\n"
            f"This link and token will expire in {settings.EMAIL_VERIFY_TOKEN_EXPIRE_HOURS} hours.\n\n"
            f"If you did not sign up for an account, please ignore this email."
        )

        body_html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Verify Your Email</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f4f6f8; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f6f8; padding: 40px 20px;">
    <tr>
      <td align="center">
        <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 580px; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); border: 1px solid #e2e8f0;">
          
          <!-- Header -->
          <tr>
            <td style="background-color: #1e293b; padding: 28px 36px; text-align: left;">
              <h1 style="margin: 0; color: #ffffff; font-size: 20px; font-weight: 600; letter-spacing: -0.025em;">
                {settings.PROJECT_NAME}
              </h1>
            </td>
          </tr>

          <!-- Main Content -->
          <tr>
            <td style="padding: 36px 36px 28px 36px;">
              <h2 style="margin: 0 0 16px 0; color: #0f172a; font-size: 18px; font-weight: 600;">
                Verify your email address
              </h2>
              <p style="margin: 0 0 24px 0; font-size: 15px; line-height: 1.6; color: #475569;">
                Thank you for creating an account with {settings.PROJECT_NAME}. Please confirm your email address by clicking the button below:
              </p>

              <!-- Action Button -->
              <table width="100%" cellpadding="0" cellspacing="0" style="margin: 28px 0;">
                <tr>
                  <td align="center">
                    <a href="{verification_url}" target="_blank" style="display: inline-block; background-color: #2563eb; color: #ffffff; text-decoration: none; padding: 14px 32px; border-radius: 6px; font-size: 15px; font-weight: 600; text-align: center; box-shadow: 0 2px 4px rgba(37, 99, 235, 0.25);">
                      Verify Email Address
                    </a>
                  </td>
                </tr>
              </table>

              <!-- Raw Link Fallback -->
              <div style="margin-top: 32px; padding: 20px; background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px;">
                <p style="margin: 0 0 8px 0; font-size: 13px; font-weight: 600; color: #334155;">
                  Button not working?
                </p>
                <p style="margin: 0 0 8px 0; font-size: 13px; color: #64748b; line-height: 1.5;">
                  Copy and paste this URL directly into your web browser:
                </p>
                <p style="margin: 0; font-size: 12px; word-break: break-all; line-height: 1.4;">
                  <a href="{verification_url}" target="_blank" style="color: #2563eb; text-decoration: underline;">
                    {verification_url}
                  </a>
                </p>
              </div>

              <!-- Raw Token Block -->
              <div style="margin-top: 16px; padding: 16px 20px; background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px;">
                <p style="margin: 0 0 6px 0; font-size: 13px; color: #64748b;">
                  Or use this verification token directly:
                </p>
                <code style="display: block; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 12px; color: #0f172a; word-break: break-all; background-color: #e2e8f0; padding: 8px 12px; border-radius: 4px;">
                  {token}
                </code>
              </div>

              <p style="margin: 28px 0 0 0; font-size: 13px; line-height: 1.5; color: #94a3b8;">
                This link and token will expire in {settings.EMAIL_VERIFY_TOKEN_EXPIRE_HOURS} hours. If you did not create an account, you can safely disregard this email.
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background-color: #f8fafc; padding: 20px 36px; border-top: 1px solid #e2e8f0; text-align: center;">
              <p style="margin: 0; font-size: 12px; color: #94a3b8;">
                © {settings.PROJECT_NAME}. All rights reserved.
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

        self._send_email(recipient=email_to, subject=subject, body_text=body_text, body_html=body_html)

    def send_password_reset_email(self, email_to: str, token: str) -> None:
        """
        Send a beautifully styled email with a CTA button, raw link, and token for password reset.
        """
        reset_url = f"{settings.FRONTEND_URL.rstrip('/')}/reset-password?token={token}"
        subject = f"{settings.PROJECT_NAME} - Password Reset Request"

        body_text = (
            f"Hello,\n\n"
            f"We received a request to reset your password for {settings.PROJECT_NAME}.\n\n"
            f"Please reset your password by visiting this link:\n"
            f"{reset_url}\n\n"
            f"If you are using the API directly, your reset token is:\n"
            f"{token}\n\n"
            f"This link and token will expire in {settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS} hours.\n\n"
            f"If you did not request a password reset, you can safely ignore this email."
        )

        body_html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Reset Your Password</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f4f6f8; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f6f8; padding: 40px 20px;">
    <tr>
      <td align="center">
        <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 580px; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); border: 1px solid #e2e8f0;">
          
          <!-- Header -->
          <tr>
            <td style="background-color: #1e293b; padding: 28px 36px; text-align: left;">
              <h1 style="margin: 0; color: #ffffff; font-size: 20px; font-weight: 600; letter-spacing: -0.025em;">
                {settings.PROJECT_NAME}
              </h1>
            </td>
          </tr>

          <!-- Main Content -->
          <tr>
            <td style="padding: 36px 36px 28px 36px;">
              <h2 style="margin: 0 0 16px 0; color: #0f172a; font-size: 18px; font-weight: 600;">
                Password Reset Request
              </h2>
              <p style="margin: 0 0 24px 0; font-size: 15px; line-height: 1.6; color: #475569;">
                We received a request to reset the password for your account. You can set a new password by clicking the button below:
              </p>

              <!-- Action Button -->
              <table width="100%" cellpadding="0" cellspacing="0" style="margin: 28px 0;">
                <tr>
                  <td align="center">
                    <a href="{reset_url}" target="_blank" style="display: inline-block; background-color: #dc2626; color: #ffffff; text-decoration: none; padding: 14px 32px; border-radius: 6px; font-size: 15px; font-weight: 600; text-align: center; box-shadow: 0 2px 4px rgba(220, 38, 38, 0.25);">
                      Reset Password
                    </a>
                  </td>
                </tr>
              </table>

              <!-- Raw Link Fallback -->
              <div style="margin-top: 32px; padding: 20px; background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px;">
                <p style="margin: 0 0 8px 0; font-size: 13px; font-weight: 600; color: #334155;">
                  Button not working?
                </p>
                <p style="margin: 0 0 8px 0; font-size: 13px; color: #64748b; line-height: 1.5;">
                  Copy and paste this URL directly into your web browser:
                </p>
                <p style="margin: 0; font-size: 12px; word-break: break-all; line-height: 1.4;">
                  <a href="{reset_url}" target="_blank" style="color: #dc2626; text-decoration: underline;">
                    {reset_url}
                  </a>
                </p>
              </div>

              <!-- Raw Token Block -->
              <div style="margin-top: 16px; padding: 16px 20px; background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px;">
                <p style="margin: 0 0 6px 0; font-size: 13px; color: #64748b;">
                  Or use this reset token directly in the app:
                </p>
                <code style="display: block; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 12px; color: #0f172a; word-break: break-all; background-color: #e2e8f0; padding: 8px 12px; border-radius: 4px;">
                  {token}
                </code>
              </div>

              <p style="margin: 28px 0 0 0; font-size: 13px; line-height: 1.5; color: #94a3b8;">
                This link will expire in {settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS} hours. If you did not request this password reset, please ignore this email.
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background-color: #f8fafc; padding: 20px 36px; border-top: 1px solid #e2e8f0; text-align: center;">
              <p style="margin: 0; font-size: 12px; color: #94a3b8;">
                © {settings.PROJECT_NAME}. All rights reserved.
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

        self._send_email(recipient=email_to, subject=subject, body_text=body_text, body_html=body_html)


email_service = EmailService()
