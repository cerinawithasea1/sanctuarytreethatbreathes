from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import logging
import re
import os

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Scraper:
    """Overdrive Audiobook Scraper"""
    def __init__(self, config, headless=True):
        self.config = config
        self.mp3_urls = {}
        self.cover_image_url = ""
        self.network_enabled = True  # Enable network traffic capture
        
        # URL patterns for MP3 detection
        self.url_patterns = [
            r'.*\.mp3(\?.*)?$',            # Standard MP3 URLs
            r'.*Part\d+\.mp3(\?.*)?$',     # Part number format
            r'.*_\d+\.mp3(\?.*)?$',        # Underscore format
            r'.*-\d+\.mp3(\?.*)?$',        # Dash format
            r'.*_part\d+\.mp3(\?.*)?$',    # Part label format
            r'.*audio.*\.mp3(\?.*)?$',     # Generic audio format
            r'.*media.*\.mp3(\?.*)?$'      # Media format
        ]
        
        # Fix URL construction - use the full library URL provided in config
        self.base_url = config["library"]
        if not self.base_url.startswith("https://"):
            self.base_url = "https://" + self.base_url
            
        # Set up Chrome options
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument("--headless=new")
        self.chrome_options.add_argument("--log-level=2")
        
        # Add additional options for better compatibility
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Enable performance and network logging
        self.chrome_options.set_capability("goog:loggingPrefs", {
            "performance": "ALL",
            "network": "ALL"
        })
        
        # Set up Selenium Wire options for capturing network traffic
        self.seleniumwire_options = {
            'disable_encoding': True,  # Don't encode request bodies
            'enable_har': True,        # Enable HAR format for requests
            'ignore_http_methods': ['OPTIONS'],  # Ignore OPTIONS requests
            'suppress_connection_errors': False,  # Show connection errors
        }
        
        self.driver = None
        self.driver = None
    
    def __del__(self):
        """Clean up resources when object is garbage collected"""
        self.cleanup()
    
    def cleanup(self):
        """Explicitly clean up resources"""
        if self.driver:
            try:
                logger.info("Closing browser session")
                self.driver.quit()
                self.driver = None
            except Exception as e:
                logger.error(f"Error closing browser: {e}")
    
    def getCookies(self):
        """Get cookies from current browser session"""
        if self.driver:
            return self.driver.get_cookies()
        return []
    
    def _login(self):
        """Perform login to Overdrive"""
        try:
            logger.info("Logging in...")
            self.driver.get(self.base_url + "/account/ozone/sign-in")
            
            # Wait for login elements to be present
            wait = WebDriverWait(self.driver, timeout=15)
            
            # Try first login format (username/password)
            try:
                signin_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'signin-button')))
                username_input = self.driver.find_element(By.ID, 'username')
                password_input = self.driver.find_element(By.ID, 'password')
                
                # Fill in credentials
                username_input.send_keys(self.config['user'])
                password_input.send_keys(self.config['pass'])
                
                # Click sign in
                signin_button.click()
                time.sleep(3)
                
                return self.driver.get_cookies()
            except (NoSuchElementException, TimeoutException) as e:
                logger.info(f"First login format failed: {e}, trying alternate format")
                
                # Try alternative login format (barcode/pin)
                try:
                    username_input = self.driver.find_element(By.ID, 'barcode')
                    password_input = self.driver.find_element(By.ID, 'pin')
                    signin_submit = self.driver.find_element(By.ID, 'signin-submit-button')
                    
                    username_input.send_keys(self.config['user'])
                    password_input.send_keys(self.config['pass'])
                    signin_submit.click()
                    time.sleep(3)
                    
                    return self.driver.get_cookies()
                except Exception as e2:
                    logger.error(f"Alternative login failed: {e2}")
                    return []
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return []
            
    def ensureLogin(self, cookies=None):
        """
        Ensures that a valid login session exists.
        Initializes the browser if needed, applies cookies if provided,
        and verifies if login is required.
        
        Args:
            cookies (list): Optional list of cookie dictionaries
            
        Returns:
            list: Updated cookies after ensuring login
        """
        try:
            # Initialize Chrome driver if not already done
            if not self.driver:
                logger.info("Initializing Chrome driver with network capture")
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(
                    service=service, 
                    options=self.chrome_options,
                    seleniumwire_options=self.seleniumwire_options
                )
                
                # Load base URL first (required before setting cookies)
                self.driver.get(self.base_url)
                
                # Add cookies if they exist
                if cookies:
                    try:
                        logger.info("Adding existing cookies")
                        for cookie in cookies:
                            try:
                                self.driver.add_cookie(cookie)
                            except Exception as e:
                                logger.warning(f"Could not add cookie: {e}")
                    except Exception as e:
                        logger.warning(f"Error applying cookies: {e}")
            
            # Test if current session is valid by accessing loans page
            logger.info("Checking if login is required")
            self.driver.get(self.base_url + "/account/loans")
            time.sleep(2)
            
            # Look for typical elements that indicate a successful login
            try:
                # Try to find the loans title element
                self.driver.find_element(By.CLASS_NAME, 'account-title')
                
                # If we get here without exception, we're already logged in
                logger.info("Already logged in")
                return self.driver.get_cookies()
            except NoSuchElementException:
                logger.info("Login required")
                return self._login()
                
        except Exception as e:
            logger.error(f"Error ensuring login: {e}")
            
            # Attempt to login as fallback
            return self._login()
    
    def getLoans(self):
        """
        Retrieves all borrowed books from the user's loans page.
        
        Returns:
            list: List of tuples in format (index, title, author, access_url)
        """
        try:
            logger.info("Navigating to loans page...")
            self.driver.get(self.base_url + "/account/loans")
            
            # Wait for the loans page to load
            wait = WebDriverWait(self.driver, timeout=15)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'account-title')))
            
            # Give page time to fully load
            time.sleep(2)
            
            logger.info("Finding borrowed books...")
            
            # Find all borrowed books
            try:
                # First try the current layout
                loans = self.driver.find_elements(By.CLASS_NAME, 'title-container')
                logger.info(f"Found {len(loans)} loans using primary selector")
            except Exception:
                try:
                    # Try alternative layout
                    loans = self.driver.find_elements(By.CLASS_NAME, 'title-element')
                    logger.info(f"Found {len(loans)} loans using secondary selector")
                except Exception as e:
                    logger.error(f"Could not find loans: {e}")
                    return []
            
            books = []
            
            # For each loan, extract title, author, and access URL
            for index, loan in enumerate(loans):
                try:
                    # Try to extract title and author
                    title_element = loan.find_element(By.CLASS_NAME, 'title-name')
                    title = title_element.text.strip()
                    
                    try:
                        author_element = loan.find_element(By.CLASS_NAME, 'creator-name')
                    except NoSuchElementException:
                        try:
                            author_element = loan.find_element(By.CLASS_NAME, 'secondary-creator')
                        except NoSuchElementException:
                            author_element = None
                    
                    author = author_element.text.strip() if author_element else "Unknown Author"
                    
                    # Try to find the "Listen now" link
                    try:
                        listen_link = loan.find_element(By.PARTIAL_LINK_TEXT, "Listen")
                        access_url = listen_link.get_attribute('href')
                    except NoSuchElementException:
                        try:
                            # Try alternate "Play/Download" button
                            button = loan.find_element(By.CSS_SELECTOR, 'button[aria-label*="Play"]')
                            parent = button.find_element(By.XPATH, './..')
                            access_url = parent.get_attribute('href')
                        except NoSuchElementException:
                            logger.warning(f"No listen link found for book: {title}")
                            continue
                    
                    books.append((index, title, author, access_url))
                    logger.info(f"Found book: {title} by {author}")
                    
                except Exception as e:
                    logger.warning(f"Error processing loan {index}: {e}")
                    continue
            
            logger.info(f"Retrieved {len(books)} books from loans page")
            return books
            
        except Exception as e:
            logger.error(f"Error retrieving loans: {e}")
            return []

    def getBook(self, books, book_index):
        """
        Navigate to the book's player page and extract audio files and metadata.
        
        Args:
            books: List of books returned by getLoans()
            book_index: Index of the selected book
            
        Returns:
            tuple: (urls, chapter_markers, cover_image_url, expected_time)
        """
        try:
            # Validate book index
            if book_index >= len(books):
                logger.error(f"Invalid book index: {book_index}, max is {len(books)-1}")
                return False
            
            # Get book details
            _, book_title, book_author, book_url = books[book_index]
            logger.info(f"Accessing '{book_title}' by {book_author}")
            
            # Clear previous request data
            self.driver.get("about:blank")
            self.mp3_urls = {}
            self.cover_image_url = ""
            
            # Navigate to the book's player page
            logger.info(f"Loading player at: {book_url}")
            self.driver.get(book_url)
            
            # Wait for player to load
            wait = WebDriverWait(self.driver, timeout=20)
            
            try:
                # Wait for key player elements
                chapter_previous = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'chapter-bar-prev-button')))
                chapter_next = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'chapter-bar-next-button')))
                time_previous = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'playback-controls-left')))
                time_next = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'playback-controls-right')))
                timeline_length = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'timeline-end-minutes')))
                timeline_current = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'timeline-start-minutes')))
                chapter_title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'chapter-bar-title')))
                
                logger.info("Player loaded successfully")
            except (TimeoutException, NoSuchElementException) as e:
                logger.error(f"Failed to load player elements: {e}")
                return False
            
            # Give player time to initialize
            time.sleep(2)
            
            # Navigate to the first chapter
            try:
                logger.info("Navigating to first chapter")
                while chapter_previous.is_enabled():
                    chapter_previous.click()
                    time.sleep(0.5)
                
                # Get expected total time of the audiobook
                timeline_length_elem = self.driver.find_element(By.CLASS_NAME, 'timeline-end-minutes')
                timeline_length_text = timeline_length_elem.find_element(By.CLASS_NAME, 'place-phrase-visual')
                expected_time = timeline_length_text.get_attribute("textContent").replace("-", "")
                logger.info(f"Total audiobook length: ~{expected_time}")
            except Exception as e:
                logger.error(f"Error navigating to first chapter: {e}")
                # Continue with best effort
                expected_time = "00:00:00"
            
            # Collect chapter markers
            chapter_markers = {}
            
            try:
                logger.info("Collecting chapter markers")
                
                # Get current chapter info
                current_title = chapter_title.get_attribute("textContent")
                timeline_current_elem = self.driver.find_element(By.CLASS_NAME, 'timeline-start-minutes')
                current_time_text = timeline_current_elem.find_element(By.CLASS_NAME, 'place-phrase-visual')
                chapter_markers[current_title] = current_time_text.get_attribute("textContent")
                
                # Navigate through all chapters
                chapter_count = 1
                while chapter_next.is_enabled():
                    logger.info(f"Processing chapter: {current_title}")
                    
                    # Trigger playback to ensure media loads
                    for i in range(2):
                        time_previous.click()
                        time.sleep(0.2)
                    for i in range(4):
                        time_next.click()
                        time.sleep(0.2)
                    
                    # Move to next chapter
                    chapter_next.click()
                    time.sleep(1.5)  # Allow time for chapter to load
                    
                    # Get new chapter info
                    try:
                        current_title = chapter_title.get_attribute("textContent")
                        current_time_text = timeline_current_elem.find_element(By.CLASS_NAME, 'place-phrase-visual')
                        if current_title not in chapter_markers:
                            chapter_markers[current_title] = current_time_text.get_attribute("textContent")
                            chapter_count += 1
                    except Exception as e:
                        logger.warning(f"Error getting chapter info: {e}")
                        continue
                
                logger.info(f"Collected {chapter_count} chapter markers")
                
            except Exception as e:
                logger.error(f"Error collecting chapter markers: {e}")
                # Continue with best effort - empty chapter markers
                if not chapter_markers:
                    chapter_markers = {"Chapter 1": "00:00:00"}
            
            # Extract MP3 URLs and cover image from network requests
            urls = {}
            cover_image_url = ""
            
            try:
                logger.info("Extracting audio files and cover image URLs")
                
                # Check all network requests
                for request in self.driver.requests:
                    if request.response:
                        url = request.url
                        
                        # Check for MP3 files
                        if url.endswith('.mp3') or 'mp3' in url:
                            for pattern in self.url_patterns:
                                if re.match(pattern, url):
                                    # Extract part number from URL
                                    try:
                                        if 'Part' in url:
                                            part_id = url.split("Part")[1].split(".mp3")[0]
                                        elif '_part' in url.lower():
                                            part_id = url.lower().split("_part")[1].split(".mp3")[0]
                                        elif '_' in url and url.split('_')[-1].split('.')[0].isdigit():
                                            part_id = url.split('_')[-1].split('.')[0]
                                        elif '-' in url and url.split('-')[-1].split('.')[0].isdigit():
                                            part_id = url.split('-')[-1].split('.')[0]
                                        else:
                                            # If no pattern matches, use a sequential number
                                            part_id = str(len(urls) + 1)
                                    except Exception:
                                        part_id = str(len(urls) + 1)
                                    
                                    # Add to URLs dict if not already present
                                    if part_id not in urls:
                                        urls[part_id] = url
                                        logger.info(f"Found audio part {part_id}")
                                    break
                        
                        # Check for cover image
                        if '.jpg' in url or '.jpeg' in url:
                            if 'cover' in url.lower() or 'image' in url.lower() or 'artwork' in url.lower():
                                cover_image_url = url
                                logger.info(f"Found cover image: {url}")
                
                # If no cover image found by keywords, use any image URL from the player domain
                if not cover_image_url:
                    for request in self.driver.requests:
                        if request.response:
                            url = request.url
                            if ('.jpg' in url or '.jpeg' in url) and 'listen.overdrive.com' in url:
                                cover_image_url = url
                                logger.info(f"Using alternative cover image: {url}")
                                break
                
                # Log results
                logger.info(f"Found {len(urls)} audio parts and cover image: {bool(cover_image_url)}")
                
                if not urls:
                    logger.error("No audio files were found!")
                    return False
                    
                return (urls, chapter_markers, cover_image_url, expected_time)
                
            except Exception as e:
                logger.error(f"Error extracting audio URLs: {e}")
                return False
                
        except Exception as e:
            logger.error(f"Error in getBook: {e}")
            return False
