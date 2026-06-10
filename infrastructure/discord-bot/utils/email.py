"""Email Notification Utilities.

Handles sending emails for contributor notifications, ticket updates, and acknowledgments.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailNotifier:
    """Email notification system for LILA Lab."""

    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "lila.lab0x@gmail.com")
        self.from_name = "LILA Lab"
        self.enabled = bool(self.smtp_user and self.smtp_password)

    def _send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        """Send an HTML email."""
        if not self.enabled:
            return False

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = to_email

            # Attach HTML content
            html_part = MIMEText(html_content, "html")
            msg.attach(html_part)

            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            return True
        except Exception as e:
            print(f"Email send failed: {e}")
            return False

    def send_welcome_email(self, to_email: str, name: str, discord_invite: str) -> bool:
        """Send welcome email to new contributor."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #006D77; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
                .footer {{ background: #333; color: white; padding: 15px; text-align: center; border-radius: 0 0 8px 8px; }}
                .button {{ display: inline-block; background: #E29578; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
                .link {{ color: #006D77; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to LILA Lab!</h1>
                </div>
                <div class="content">
                    <p>Dear {name},</p>

                    <p>Welcome to <strong>LILA Lab</strong> (Language Intelligence for Low-resource Applications)! We're thrilled to have you join our research collective.</p>

                    <p>LILA Lab is building NLP measurement infrastructure for languages underserved by current AI. Your contribution matters.</p>

                    <h3>Getting Started:</h3>
                    <ol>
                        <li>Join our Discord: <a href="{discord_invite}" class="link">discord.gg/TrrdKbky</a></li>
                        <li>Read the <a href="https://github.com/LilaLABx/LILA-LAB/blob/main/COLLABORATION.md" class="link">Collaboration Framework</a></li>
                        <li>Check the <a href="https://github.com/LilaLABx/LILA-LAB/blob/main/CONTRIBUTING.md" class="link">Contributing Guide</a></li>
                        <li>Introduce yourself in #general on Discord</li>
                    </ol>

                    <h3>8 Ways to Contribute:</h3>
                    <ul>
                        <li>Language Extension Paper</li>
                        <li>Cross-Domain Extension</li>
                        <li>Methodological Contribution</li>
                        <li>Replication + Validation</li>
                        <li>Citizen Science Annotation</li>
                        <li>Policy & Application Brief</li>
                        <li>Infrastructure & Tooling</li>
                        <li>Teaching Materials</li>
                    </ul>

                    <p>Questions? Reply to this email or ask in #support on Discord.</p>

                    <a href="https://github.com/LilaLABx/LILA-LAB" class="button">View Repository</a>
                </div>
                <div class="footer">
                    <p>LILA Lab | Language Intelligence for Low-resource Applications</p>
                    <p><a href="https://lila-lab.org" style="color: #E29578;">Website</a> |
                       <a href="https://github.com/LilaLABx/LILA-LAB" style="color: #E29578;">GitHub</a> |
                       <a href="{discord_invite}" style="color: #E29578;">Discord</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        return self._send_email(to_email, "Welcome to LILA Lab!", html)

    def send_ticket_update(
        self,
        to_email: str,
        name: str,
        ticket_id: str,
        ticket_title: str,
        status: str,
        message: str | None = None,
    ) -> bool:
        """Send ticket update notification."""
        status_color = "#28a745" if status == "closed" else "#006D77"
        status_text = "Closed" if status == "closed" else "Updated"

        message_html = ""
        if message:
            message_html = f"""
            <div style="background: #fff; padding: 15px; border-left: 4px solid {status_color}; margin: 15px 0;">
                <p><strong>New Message:</strong></p>
                <p>{message}</p>
            </div>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: {status_color}; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
                .footer {{ background: #333; color: white; padding: 15px; text-align: center; border-radius: 0 0 8px 8px; }}
                .button {{ display: inline-block; background: #E29578; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Ticket {status_text}</h1>
                </div>
                <div class="content">
                    <p>Dear {name},</p>

                    <p>Your ticket <strong>{ticket_id}</strong> has been {status.lower()}.</p>

                    <div style="background: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                        <p><strong>Ticket ID:</strong> {ticket_id}</p>
                        <p><strong>Title:</strong> {ticket_title}</p>
                        <p><strong>Status:</strong> {status.upper()}</p>
                    </div>

                    {message_html}

                    <p>Thank you for being part of LILA Lab!</p>

                    <a href="https://discord.gg/TrrdKbky" class="button">View on Discord</a>
                </div>
                <div class="footer">
                    <p>LILA Lab | Language Intelligence for Low-resource Applications</p>
                </div>
            </div>
        </body>
        </html>
        """
        return self._send_email(to_email, f"Ticket {status_text}: {ticket_id}", html)

    def send_contribution_acknowledgment(
        self,
        to_email: str,
        name: str,
        contribution_type: str,
        contribution_details: str,
    ) -> bool:
        """Send contribution acknowledgment email."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #E29578; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
                .footer {{ background: #333; color: white; padding: 15px; text-align: center; border-radius: 0 0 8px 8px; }}
                .highlight {{ background: #FFDDD2; padding: 15px; border-radius: 5px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Thank You for Your Contribution!</h1>
                </div>
                <div class="content">
                    <p>Dear {name},</p>

                    <p>On behalf of the entire LILA Lab team, thank you for your valuable contribution!</p>

                    <div class="highlight">
                        <p><strong>Contribution Type:</strong> {contribution_type}</p>
                        <p><strong>Details:</strong> {contribution_details}</p>
                    </div>

                    <p>Your work helps build NLP infrastructure for languages underserved by current AI. Every contribution matters.</p>

                    <h3>What Happens Next:</h3>
                    <ol>
                        <li>Your contribution will be reviewed by the team</li>
                        <li>You'll be added to our contributors list</li>
                        <li>Depending on the contribution type, you may receive authorship credit</li>
                    </ol>

                    <p>Stay connected:</p>
                    <ul>
                        <li>Discord: <a href="https://discord.gg/TrrdKbky">discord.gg/TrrdKbky</a></li>
                        <li>GitHub: <a href="https://github.com/LilaLABx/LILA-LAB">Repository</a></li>
                    </ul>
                </div>
                <div class="footer">
                    <p>LILA Lab | Language Intelligence for Low-resource Applications</p>
                </div>
            </div>
        </body>
        </html>
        """
        return self._send_email(to_email, "Thank You for Your Contribution to LILA Lab!", html)

    def send_monthly_digest(
        self,
        to_email: str,
        name: str,
        month: str,
        highlights: list[str],
        upcoming: list[str],
    ) -> bool:
        """Send monthly digest email."""
        highlights_html = "\n".join([f"<li>{h}</li>" for h in highlights])
        upcoming_html = "\n".join([f"<li>{u}</li>" for u in upcoming])

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #006D77; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
                .footer {{ background: #333; color: white; padding: 15px; text-align: center; border-radius: 0 0 8px 8px; }}
                .button {{ display: inline-block; background: #E29578; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>LILA Lab Monthly - {month}</h1>
                </div>
                <div class="content">
                    <p>Dear {name},</p>

                    <p>Here's what happened in the LILA Lab ecosystem this month.</p>

                    <h3>Highlights</h3>
                    <ul>{highlights_html}</ul>

                    <h3>Coming Up</h3>
                    <ul>{upcoming_html}</ul>

                    <h3>Get Involved</h3>
                    <p>We're always looking for contributors. Check out open issues on GitHub or join us on Discord.</p>

                    <a href="https://github.com/LilaLABx/LILA-LAB" class="button">View Repository</a>
                    <a href="https://discord.gg/TrrdKbky" class="button">Join Discord</a>
                </div>
                <div class="footer">
                    <p>LILA Lab | Language Intelligence for Low-resource Applications</p>
                    <p><a href="https://lila-lab.org" style="color: #E29578;">Website</a> |
                       <a href="https://github.com/LilaLABx/LILA-LAB" style="color: #E29578;">GitHub</a> |
                       <a href="https://discord.gg/TrrdKbky" style="color: #E29578;">Discord</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        return self._send_email(to_email, f"LILA Lab Monthly - {month}", html)


# Singleton instance
email_notifier = EmailNotifier()
