import os
import random
import string
import requests
import re
import nodriver as uc
import asyncio
from pystyle import Write, Colors
import html2text
from colorama import init, Fore
from raducord import Logger
from datetime import datetime
import time
import tempfile
import json
from bs4 import BeautifulSoup

init(autoreset=True)

def display_banner():
    Write.Print("""

          ███████╗██████╗ ██╗ ██████╗     ██████╗ ███████╗███╗   ██╗
          ██╔════╝██╔══██╗██║██╔════╝    ██╔════╝ ██╔════╝████╗  ██║
          █████╗  ██████╔╝██║██║         ██║  ███╗█████╗  ██╔██╗ ██║
          ██╔══╝  ██╔═══╝ ██║██║         ██║   ██║██╔══╝  ██║╚██╗██║
          ███████╗██║     ██║╚██████╗    ╚██████╔╝███████╗██║ ╚████║
          ╚══════╝╚═╝     ╚═╝ ╚═════╝     ╚═════╝ ╚══════╝╚═╝  ╚═══╝

                          V2 - Made By HassanXTech .gg/dreamlove
""", Colors.blue_to_purple, interval=0.00000000000)

os.system("cls" if os.name == "nt" else "clear")
os.system("title 𝙴𝚙𝚒𝚌𝙶𝚊𝚖𝚎𝚜 Promo Gen/ 𝐃𝐢𝐬𝐜𝐨𝐫𝐝: anomus.ly")
display_banner()

from utils.string_generator import generate_random_string
from utils.url_extractor import extract_urls
from utils.file_manager import save_promo_link, ensure_directories

class BrowserManager:
    def __init__(self):
        self.browser = None
        self.page = None

    async def start(self):
        try:
            self.browser = await uc.start(headless=False, expert=True)
            self.page = await self.browser.get('https://www.epicgames.com/id/register/date-of-birth?lang=en-US&redirect_uri=https%3A%2F%2Fstore.epicgames.com%2Fen-US%2Fp%2Fdiscord--discord-nitro&client_id=875a3b57d3a640a6b7f9b4e883463ab4')
            await self.page.wait_for('body', timeout=120)
            return True
        except Exception as e:
            Logger.warning(f'Browser, Error starting browser: {e}, Error')
            return False

    async def stop(self):
        try:
            if self.browser is not None:
                await self.browser.stop()
                Logger.info('Browser, Browser stopped successfully, Process')
            else:
                Logger.info('Browser, No browser to stop (already None), Process')
        except Exception as e:
            Logger.warning(f'Browser, Error stopping browser: {e}, Error')
        finally:
            self.browser = None
            self.page = None

class EmailParser:
    def save_email_html(self, email_data, idx):
        html_content = email_data.get("html", "No HTML content available")
        filename = f"htmlcode_{idx}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(html_content)
            return filename
        except Exception as e:
            Logger.warning(f"File, Error saving HTML content: {e}, Error")
            return None

    def extract_otp_from_html(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()
            otp_match = re.search(r'<tr>\s*<td[^>]*?>\s*(\d+)\s*<br>', html_content)
            if otp_match:
                otp = otp_match.group(1)
                return otp
            return None
        except Exception as e:
            Logger.warning(f"File, Error reading file {file_path}: {e}, Error")
            return None

    def extract_promo_link_from_html(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()
            promo_link_pattern = r'link="([^"]+)"'
            match = re.search(promo_link_pattern, html_content)
            if match:
                link = match.group(1)
                return link
            return None
        except Exception as e:
            Logger.warning(f"File, Error extracting promo link: {e}, Error")
            return None

    def delete_file(self, file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            Logger.warning(f"File, Error deleting file {file_path}: {e}, Error")

    def extract_otp_from_email(self, email_data, idx):
        file_path = self.save_email_html(email_data, idx)
        if file_path:
            otp = self.extract_otp_from_html(file_path)
            self.delete_file(file_path)
            return otp
        return None

    def extract_promo_link_from_email(self, email_data, idx):
        file_path = self.save_email_html(email_data, idx)
        if file_path:
            link = self.extract_promo_link_from_html(file_path)
            self.delete_file(file_path)
            return link
        return None

class PrivateMailClient:
    def __init__(self):
        self.api_url = "http://148.135.137.110:3000/emails"
        self.api_password = "Pixi#1..promo"
        self.domain_name = "pixiboost.fun"
        self.email = None

    def create_temp_email(self):
        random_mail_name = generate_random_string(15)
        self.email = f"{random_mail_name}@{self.domain_name}"
        Logger.success(f'Email, Private Email Created: {self.email}, Success')
        return self.email, None

    def get_docs(self, email):
        headers = {"Authorization": f"Bearer {self.api_password}"}
        response = requests.get(f"{self.api_url}/{email}", headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch emails (Status {response.status_code}): {response.text}")
        return response.json()

    def get_otp(self):
        Logger.info('Email, Waiting for OTP email, Process')
        while True:
            try:
                documents = self.get_docs(self.email)
                if not documents:
                    time.sleep(5)
                    continue

                for doc in documents:
                    html_content = doc.get('html', '')
                    soup = BeautifulSoup(html_content, 'html.parser')
                    visible_text = soup.get_text(separator=' ').lower()
                    plain_text = doc.get('text', '').lower()
                    combined_text = plain_text + ' ' + visible_text

                    match = re.search(r"please use this code to verify your email address.*?(\d{6})", combined_text, re.DOTALL)
                    if match:
                        otp = match.group(1)
                        Logger.success(f'OTP, OTP found: {otp}, Success')
                        return otp

                time.sleep(5)

            except Exception as e:
                Logger.warning(f'Email, Error getting OTP: {str(e)}, Error')
                break

        Logger.warning('Email, Timeout reached. OTP not found, Error')
        return None

    def get_promo_link(self):
        Logger.info('Email, Waiting for promo email, Process')
        email_parser = EmailParser()
        max_attempts = 60 
        attempts = 0

        while attempts < max_attempts:
            try:
                documents = self.get_docs(self.email)
                if not documents:
                    Logger.info(f'Email, Waiting for email to arrive for {self.email}, Process')
                    time.sleep(5)
                    attempts += 1
                    continue

                for idx, doc in enumerate(documents):
                    with tempfile.NamedTemporaryFile('w+', delete=False, suffix='.txt', encoding='utf-8') as tmpfile:
                        json.dump(doc, tmpfile)
                        temp_filename = tmpfile.name

                    with open(temp_filename, 'r', encoding='utf-8') as f:
                        file_text = f.read()

                    os.remove(temp_filename)

                    promo_links = extract_urls(file_text)
                    if promo_links:
                        link = promo_links[0] if promo_links else None
                        if link:
                            Logger.success(f'Promo, Discord promo link found, Success')
                            return link

                    promo_link = email_parser.extract_promo_link_from_email(doc, idx)
                    if promo_link:
                        Logger.success(f'Promo, Promo link found via EmailParser, Success')
                        return promo_link

                time.sleep(5)
                attempts += 1

            except Exception as e:
                Logger.warning(f'Email, Error getting promo link: {str(e)}, Error')
                time.sleep(5)
                attempts += 1

        Logger.warning('Email, Timeout reached. Promo link not found, Error')
        return None

class AccountCreationError(Exception):
    pass

class ElementNotFoundError(Exception):
    pass

class EmailVerificationError(Exception):
    pass

class FormSubmissionError(Exception):
    pass

class EpicGamesAccountCreator:
    def __init__(self, browser_manager, mail_client, max_retries=3):
        self.browser_manager = browser_manager
        self.mail_client = mail_client
        self.page = None
        self.email = None
        self.token = None
        self.max_retries = max_retries
        self.logger = Logger

    async def create_account(self):
        try:
            if not self.browser_manager or not self.browser_manager.page:
                raise AccountCreationError("Browser manager or page not available")

            self.page = self.browser_manager.page

            await self._select_birth_date()
            await self._fill_registration_form()
            await self._submit_form()
            account_created = await self._verify_email()

            if account_created:
                return await self._get_discord_promo()

            return False

        except Exception as e:
            self.logger.warning(f"Account, Account creation failed: {str(e)}, Error")
            raise AccountCreationError(f"Failed to create account: {str(e)}")

    async def _select_birth_date(self):
        try:
            await self._safe_sleep(1)

            month_element = await self._wait_for_element('div#month', 15000)
            await self._safe_click(month_element)
            await self._safe_sleep(1)

            jan_option = await self._find_month_option()
            await self._safe_click(jan_option)
            await self._safe_sleep(0.5)

            day_element = await self._wait_for_element('div#day', 15000)
            await self._safe_click(day_element)
            await self._safe_sleep(1)

            day_option = await self._find_day_option()
            await self._safe_click(day_option)

            year_input = await self._wait_for_element('input#year', 15000)
            birth_year = random.randint(1990, 2005)
            await self._safe_send_keys(year_input, str(birth_year))

            continue_button = await self._find_continue_button()
            await self._safe_click(continue_button)

        except Exception as e:
            raise AccountCreationError(f"Failed to select birth date: {str(e)}")

    async def _find_month_option(self):
        for attempt in range(30):
            try:
                options = await self.page.query_selector_all('li[role="option"]')
                if not options:
                    await self._safe_sleep(0.5)
                    continue

                for option in options:
                    try:
                        text = (option.text or "").strip().lower()
                        if "jan" in text:
                            return option
                    except Exception:
                        continue

            except Exception as e:
                self.logger.warning(f"Month, Attempt {attempt + 1} failed to find month options: {e}, Error")

            await self._safe_sleep(0.5)

        raise ElementNotFoundError("Could not find 'Jan' option after 30 attempts")

    async def _find_day_option(self):
        for attempt in range(30):
            try:
                options = await self.page.query_selector_all('li[role="option"]')
                if not options:
                    await self._safe_sleep(0.5)
                    continue

                for option in options:
                    try:
                        text = (option.text or "").strip()
                        if text in ["1", "01"] or (text.isdigit() and int(text) == 1):
                            return option
                    except (ValueError, AttributeError):
                        continue

            except Exception as e:
                self.logger.warning(f"Day, Attempt {attempt + 1} failed to find day options: {e}, Error")

            await self._safe_sleep(0.5)

        try:
            options = await self.page.query_selector_all('li[role="option"]')
            if options:
                return options[0]
        except Exception:
            pass

        raise ElementNotFoundError("Could not find any day options after 30 attempts")

    async def _find_continue_button(self):
        for attempt in range(20):
            try:
                buttons = await self.page.query_selector_all('button')
                for button in buttons:
                    try:
                        text = (button.text or "").lower()
                        if "continue" in text:
                            return button
                    except Exception:
                        continue
            except Exception as e:
                self.logger.warning(f"Continue, Attempt {attempt + 1} failed to find continue button: {e}, Error")

            await self._safe_sleep(0.5)

        raise ElementNotFoundError("Could not find the 'Continue' button after 20 attempts")

    async def _fill_registration_form(self):
        try:
            if not hasattr(self.mail_client, 'create_temp_email'):
                raise AccountCreationError("Mail client does not have create_temp_email method")

            self.email, self.token = self.mail_client.create_temp_email()
            if not self.email:
                raise AccountCreationError("Failed to create temporary email")

            email_input = await self._find_input_field("Email", 15000)
            await self._safe_send_keys(email_input, self.email)
            await self._safe_sleep(0.5)

            random_name = generate_random_string(8)
            if not random_name:
                random_name = "DefaultName"

            firstname_input = await self._find_input_field("First Name", 15000)
            await self._safe_send_keys(firstname_input, random_name)

            lastname_input = await self._find_input_field("Last Name", 15000)
            await self._safe_send_keys(lastname_input, random_name)

            random_display_name = generate_random_string(13) + "bioz"
            if len(random_display_name) < 5:
                random_display_name = "DefaultDisplayName"

            displayname_input = await self._find_input_field("Display Name", 15000)
            await self._safe_send_keys(displayname_input, random_display_name)

            password = "pixixardpromogen123"
            if not password:
                raise AccountCreationError("Password not found")

            password_input = await self._find_input_field("Password", 15000)
            await self._safe_send_keys(password_input, password)

            await self._handle_checkboxes()
            await self._safe_sleep(1.5)

        except Exception as e:
            raise AccountCreationError(f"Failed to fill registration form: {str(e)}")

    async def _find_input_field(self, field_name, timeout):
        try:
            return await self.page.find(field_name, best_match=True, timeout=timeout)
        except Exception as e:
            raise ElementNotFoundError(f"Could not find input field '{field_name}': {str(e)}")

    async def _handle_checkboxes(self):
        try:
            checkboxes = await self.page.query_selector_all('input[type="checkbox"]')
            if len(checkboxes) >= 2:
                await self._safe_click(checkboxes[1])
        except Exception as e:
            self.logger.warning(f"Checkbox, Failed to handle checkboxes: {e}, Error")

    async def _submit_form(self):
        for attempt in range(30):
            try:
                continue_button = await self.page.query_selector('#btn-submit')
                if continue_button:
                    attributes = continue_button.attributes or {}
                    is_enabled = "disabled" not in attributes
                    if is_enabled:
                        await self._safe_click(continue_button)
                        return

            except Exception as e:
                self.logger.warning(f"Submit, Submit attempt {attempt + 1} failed: {e}, Error")

            await self._safe_sleep(0.5)

        raise FormSubmissionError("Could not find enabled submit button after 30 attempts")

    async def _verify_email(self):
        try:
            verify_element = await self.page.find("Please Verify", best_match=True, timeout=5000)
            if not verify_element:
                self.logger.info("Email, Email verification not required, Process")
                return True

        except Exception:
            self.logger.info("Email, Email verification not required or element not found, Process")
            return True

        for retry in range(self.max_retries):
            try:
                if not hasattr(self.mail_client, 'get_otp'):
                    raise EmailVerificationError("Mail client does not have get_otp method")

                otp = self.mail_client.get_otp()
                if not otp:
                    await self._safe_sleep(2)
                    continue

                otp_str = str(otp).strip()
                if len(otp_str) < 4:
                    raise EmailVerificationError(f"Invalid OTP length: {len(otp_str)}")

                for i, character in enumerate(otp_str):
                    try:
                        input_box = await self._wait_for_element(f'input[name="code-input-{i}"]', 10000)
                        await self._safe_send_keys(input_box, character)
                    except Exception as e:
                        raise EmailVerificationError(f"Failed to enter OTP character {i}: {str(e)}")

                verify_button = await self._find_verify_button()
                await self._safe_click(verify_button)
                await self._safe_sleep(2)

                try:
                    verify_button = await self._find_verify_button()
                    await self._safe_click(verify_button)
                except ElementNotFoundError:
                    pass

                try:
                    done_linking_button = await self._find_done_linking_button()
                    await self._safe_click(done_linking_button)
                    self.logger.info("Linking, Successfully clicked 'Done linking' button, Success")
                    await self._safe_sleep(2)
                except ElementNotFoundError as e:
                    self.logger.warning(f"Linking, Done linking button not found: {e}, Error")

                await self._safe_sleep(5)
                return True

            except Exception as e:
                self.logger.warning(f"Email, Email verification attempt {retry + 1} failed: {e}, Error")
                if retry == self.max_retries - 1:
                    raise EmailVerificationError(f"Email verification failed after {self.max_retries} attempts: {str(e)}")
                await self._safe_sleep(3)

        return False

    async def _find_done_linking_button(self):
        for attempt in range(20):
            try:
                button = await self.page.query_selector('#link-success')
                if button:
                    return button

                buttons = await self.page.query_selector_all('button')
                for button in buttons:
                    try:
                        text = (button.text or "").lower().strip()
                        if "done linking" in text:
                            return button
                    except Exception:
                        continue

                button = await self.page.query_selector('button[aria-label="Continue"]')
                if button:
                    button_text = (button.text or "").lower().strip()
                    if "done linking" in button_text:
                        return button

            except Exception as e:
                self.logger.warning(f"Linking, Done linking button search attempt {attempt + 1} failed: {e}, Error")

            await self._safe_sleep(0.5)

        raise ElementNotFoundError("Could not find 'Done linking' button after 20 attempts")

    async def _find_verify_button(self):
        for attempt in range(20):
            try:
                buttons = await self.page.query_selector_all('button')
                for button in buttons:
                    try:
                        text = (button.text or "").lower()
                        if "verify email" in text or "verify" in text:
                            return button
                    except Exception:
                        continue
            except Exception as e:
                self.logger.warning(f"Verify, Verify button search attempt {attempt + 1} failed: {e}, Error")

            await self._safe_sleep(0.5)

        raise ElementNotFoundError("Could not find verify email button after 20 attempts")

    async def _get_discord_promo(self):
        """Handle the Discord promo acquisition process - Direct approach"""
        try:
            self.logger.info('Discord, Proceeding to Discord promo, Process')
            await self._safe_sleep(7)

            await self._click_get_button()

            await self._place_order()

            # await self._accept_terms()

            await self._wait_for_thank_you()

            await self._handle_email_success()

            self.logger.success('Discord, Process completed successfully, Success')
            return True

        except Exception as e:
            self.logger.warning(f'Discord, Error during Discord promo process: {e}, Error')
            return False

    async def _click_get_button(self):
        """Click the Get button with retry logic"""
        get_button = None

        for attempt in range(30):
            try:
                get_button = await self.page.query_selector('button[data-testid="purchase-cta-button"]')
                if get_button:
                    attributes = get_button.attributes or {}
                    is_enabled = "disabled" not in attributes
                    if is_enabled:
                        break

            except Exception as e:
                self.logger.warning(f'Get, Get button search attempt {attempt + 1} failed: {e}, Error')

            await self._safe_sleep(0.5)

        if not get_button:
            raise ElementNotFoundError("Could not find enabled get button after 30 attempts")

        try:
            await self._safe_sleep(2)
            await self._safe_click(get_button)
            await self._safe_sleep(5)

            self.logger.success('Get, Get button clicked successfully, Success')

        except Exception as e:
            raise AccountCreationError(f"Failed to click get button: {str(e)}")

    async def _place_order(self):
        """Place the order with retry logic"""
        for retry in range(self.max_retries):
            try:
                place_order_button = await self._find_element_by_text("Place Order", 15000)
                if not place_order_button:
                    raise ElementNotFoundError("Place Order button not found")

                await self._safe_click(place_order_button)
                await self._safe_sleep(5)

                self.logger.success('Order, Order placed successfully, Success')
                return

            except Exception as e:
                self.logger.warning(f'Order, Place order attempt {retry + 1} failed: {e}, Error')
                if retry == self.max_retries - 1:
                    raise AccountCreationError(f"Failed to place order after {self.max_retries} attempts: {str(e)}")
                await self._safe_sleep(2)

    # async def _accept_terms(self):
    #     """Accept terms if required"""
    #     try:
    #         i_accept_button = await self._find_element_by_text("I Accept", 6000)
    #         if i_accept_button:
    #             await self._safe_click(i_accept_button)
    #             await self._safe_sleep(2)
    #             self.logger.success('Terms, Terms accepted successfully, Success')
    #         else:
    #             self.logger.info('Terms, No terms acceptance required, Process')

    #     except Exception as e:
    #         self.logger.info(f'Terms, Terms acceptance not required or failed: {e}, Process')

    async def _wait_for_thank_you(self):
        """Wait for thank you confirmation message"""
        try:
            self.logger.info('Confirmation, Waiting for thank you message, Process')

            thank_you_element = await self._find_element_by_text("Thank", 45000)
            if not thank_you_element:
                thank_you_element = await self._find_element_by_text("Thanks", 10000)

            if thank_you_element:
                self.logger.success('Confirmation, Thank you message found, Success')
                await self._safe_sleep(10)
            else:
                self.logger.warning('Confirmation, Thank you message not found continuing anyway, Warning')

        except Exception as e:
            self.logger.warning(f'Confirmation, Error waiting for thank you message: {e}, Error')

    async def _handle_email_success(self):
        """Handle email extraction and save promo link"""
        try:
            if not self.mail_client:
                raise EmailVerificationError("Mail client not available")

            self.logger.info('Email, Extracting promo link from email, Process')

            import asyncio
            try:
                loop = asyncio.get_event_loop()
                promo_link = await asyncio.wait_for(
                    loop.run_in_executor(None, self.mail_client.get_promo_link),
                    timeout=300
                )
            except asyncio.TimeoutError:
                self.logger.warning('Email, Email checking timed out after 5 minutes, Warning')
                return True

            if not promo_link:
                self.logger.warning('Email, No promo link found in email, Warning')
                return True

            if not any(keyword in promo_link.lower() for keyword in ['discord.gg', 'promos.discord.gg', '/nitro', 'discord.com/nitro']):
                self.logger.warning(f'Email, Found link but not a Discord promo link, Warning')
                save_promo_link(promo_link)
                return True

            save_promo_link(promo_link)
            self.logger.success(f'Email, Valid Discord promo link saved, Success')

        except Exception as e:
            self.logger.warning(f'Email, Email handling failed: {str(e)}, Error')
            return True

    async def _find_element_by_text(self, text, timeout):
        """Find element by text with timeout"""
        try:
            return await self.page.find(text, best_match=True, timeout=timeout)
        except Exception as e:
            self.logger.warning(f'Element, Element with text {text} not found: {e}, Error')
            return None

    async def _wait_for_element(self, selector, timeout):
        try:
            return await self.page.wait_for(selector, timeout=timeout)
        except Exception as e:
            raise ElementNotFoundError(f"Element '{selector}' not found within {timeout}ms: {str(e)}")

    async def _safe_click(self, element):
        if not element:
            raise ElementNotFoundError("Cannot click on None element")
        try:
            await element.mouse_click("left")
        except Exception as e:
            raise AccountCreationError(f"Failed to click element: {str(e)}")

    async def _safe_send_keys(self, element, text):
        if not element:
            raise ElementNotFoundError("Cannot send keys to None element")
        if not text:
            raise AccountCreationError("Cannot send empty text")
        try:
            await element.send_keys(str(text))
        except Exception as e:
            raise AccountCreationError(f"Failed to send keys '{text}': {str(e)}")

    async def _safe_sleep(self, duration):
        try:
            await asyncio.sleep(max(0, duration))
        except Exception as e:
            self.logger.warning(f"Sleep, Sleep interrupted: {e}, Error")

def save_account_info(email_address, password):
    """Save account information to file"""
    with open("accounts.txt", "a", encoding="utf-8") as file:
        file.write(f"Email: {email_address}, Password: {password}\n")
    Logger.success('Account info saved to accounts.txt, File, Success')

def save_email_token(email, token):
    """Save email and token for reference"""
    if token:
        with open("saved_emails.txt", "a", encoding="utf-8") as file:
            file.write(f"Email: {email}, Token: {token}\n")
        Logger.success('Email and Token saved to saved_emails.txt, File, Success')

async def check_terms_checkbox(tab):
    """Check only the Terms of Service checkbox (required)"""
    try:
        await tab.sleep(1)

        try:
            tos_checkbox = await tab.select("#tos")
            if tos_checkbox:
                await tos_checkbox.scroll_into_view()
                await tos_checkbox.click()
                return True
            else:
                tos_label = await tab.select("label[for='tos']")
                if tos_label:
                    await tos_label.click()
                    return True
        except Exception:
            try:
                tos_element = await tab.find("Terms of Service")
                if tos_element:
                    await tos_element.click()
                    return True
            except Exception:
                return False
    except Exception:
        return False

async def input_verification_code(tab, code):
    """Input verification code into the form"""
    try:
        code = str(code).zfill(6)
        for i in range(6):
            input_field = await tab.select(f"input[name='code-input-{i}']")
            if input_field:
                await input_field.clear_input()
                await input_field.send_keys(code[i])
        Logger.success('Verification code entered successfully, Code, Success')
    except Exception as e:
        Logger.warning(f'Error entering verification code, {e}, Error')

def get_current_time():
    """Get current time formatted"""
    return datetime.now().strftime("%H:%M:%S")

async def fill_date_of_birth(tab):
    """Fill date of birth using proper Epic Games dropdown handling - Day first, then Month"""
    try:
        Logger.info('Filling date of birth, Form, Process')

        await tab.sleep(2)

        day_element = await tab.select("#day")
        if day_element:
            await day_element.scroll_into_view()
            await tab.sleep(0.5)
            await day_element.mouse_click()

            day_options = ["15", "02", "2", "01", "1", "10"]
            for option_text in day_options:
                try:
                    day_option = await tab.find(option_text, best_match=True)
                    if day_option:
                        await day_option.scroll_into_view()
                        await day_option.click()
                        break
                except Exception:
                    continue

        month_element = await tab.select("#month")
        if month_element:
            await month_element.scroll_into_view()
            await tab.sleep(0.5)
            await month_element.mouse_click()

            month_options = ["Jan", "January", "01", "1"]
            for option_text in month_options:
                try:
                    month_option = await tab.find(option_text, best_match=True)
                    if month_option:
                        await month_option.scroll_into_view()
                        await month_option.click()
                        break
                except Exception:
                    continue

        year_element = await tab.select("#year")
        if year_element:
            await year_element.scroll_into_view()
            await year_element.clear_input()
            await year_element.send_keys("1990")

        continue_button = await tab.select("#continue")
        if continue_button:
            await continue_button.scroll_into_view()
            await continue_button.click()
        else:
            continue_button = await tab.find("Continue", best_match=True)
            if continue_button:
                await continue_button.click()

        await tab.sleep(2)

    except Exception as e:
        Logger.warning(f'Error in fill_date_of_birth function: {e}, DOB, Error')

async def epicgames_generator():
    """Main function to generate EpicGames account and get promo using the new class-based approach"""
    Logger.info('EpicGames, Starting account generation, Process')

    mail_client = PrivateMailClient()
    browser_manager = BrowserManager()

    try:
        await browser_manager.start()

        account_creator = EpicGamesAccountCreator(browser_manager, mail_client)

        success = await account_creator.create_account()

        if success:
            Logger.success('Process completed successfully!, Success')
            return True
        else:
            Logger.warning('Account, Account creation failed, Error')
            return False

    except IndexError as e:
        Logger.warning(f'Process, Index error during process: {e}, Error')
        return True
    except Exception as e:
        Logger.warning(f'Process, Error during process: {e}, Error')
        return False
    finally:
        try:
            if browser_manager and browser_manager.browser:
                await browser_manager.stop()
            else:
                Logger.info('Browser, No browser to stop (already None), Process')
        except Exception as e:
            Logger.warning(f'Browser, Error in finally block: {e}, Error')

def display_credits():
    """Display credits information"""
    Write.Print("""

    ╔══════════════════════════════════════════════════════════════╗
    ║                           CREDITS                            ║
    ╠══════════════════════════════════════════════════════════════╣
    ║                                                              ║
    ║  Program Owner: Hassan Tech                                    ║
    ║  Discord: anomus.ly                                          ║
    ║  GitHub: https://github.com/hassanxtech                         ║
    ║  Discord Server: https://discord.gg/dreamlove                     ║
    ║  Contact: instagram.com/hsx.esticxs                          ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝

    """, Colors.blue_to_purple, interval=0.00000000000)

    Write.Input("\nPress Enter to return to main menu...", Colors.blue_to_purple)

def show_menu():
    """Display the main menu"""
    Write.Print("""

[1] Generate EpicGames Account & Discord Promo
[2] Credits
[3] Exit
""", Colors.blue_to_purple, interval=0.00000000000)

    return Write.Input('\nanomus@epicgames>>', Colors.blue_to_purple)

async def main():
    """Main program loop"""
    ensure_directories()

    while True:
        opc = show_menu()

        if opc == '1':
            await continuous_generation_loop()
            break
        elif opc == '2':
            display_credits()
            os.system("cls" if os.name == "nt" else "clear")
            display_banner()
        elif opc == '3':
            Logger.info('System, Exiting, Process')
            break
        else:
            Logger.warning('Menu, Invalid option selected, Error')

async def continuous_generation_loop():
    """Continuous loop for generating accounts and Discord promos"""
    generation_count = 0

    while True:
        try:
            generation_count += 1
            Logger.info(f'Loop, Starting generation #{generation_count}, Process')

            success = await epicgames_generator()

            if success:
                Logger.success(f'Loop, Generation #{generation_count} completed successfully, Success')
            else:
                Logger.warning(f'Loop, Generation #{generation_count} failed, Error')

            Logger.info('Loop, Waiting 5 seconds before next generation, Process')
            await asyncio.sleep(5)

        except KeyboardInterrupt:
            Logger.info('Loop, Generation loop stopped by user, Process')
            break
        except Exception as e:
            Logger.warning(f'Loop, Error in generation loop: {e}, Error')
            Logger.info('Loop, Waiting 10 seconds before retry, Process')
            await asyncio.sleep(10)

if __name__ == '__main__':
    uc.loop().run_until_complete(main())
