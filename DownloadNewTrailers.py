import os
import re
import subprocess
import time
import requests
import sys

# Check and install required packages if missing
def check_and_install_package(package, install_command):
    try:
        __import__(package)
        print(f"✅ {package} is already installed.")
    except ImportError:
        print(f"❌ {package} is not installed. Installing...")
        subprocess.run(install_command, check=True)

# Verify yt-dlp is installed
def verify_yt_dlp():
    yt_dlp_path = os.getenv("YTDLP", "")
    
    if not yt_dlp_path:
        print("❌ yt-dlp environment variable 'YTDLP' is not set.")
        yt_dlp_url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
        yt_dlp_path = r'C:\Tools\yt-dlp.exe'
        
        # Download yt-dlp
        subprocess.run(['curl', '-L', yt_dlp_url, '-o', yt_dlp_path], check=True)
        
        # Set yt-dlp environment variable
        os.environ["YTDLP"] = yt_dlp_path
        print(f"✅ yt-dlp environment variable 'YTDLP' set to: {yt_dlp_path}")
    else:
        print(f"✅ yt-dlp is already installed at {yt_dlp_path}")


# Install and setup ChromeDriver if not already installed
def verify_chromedriver():
    if not os.getenv("ChromeDriver"):
        print("❌ ChromeDriver path not set. Installing ChromeDriver...")
        chromedriver_url = "https://googlechromelabs.github.io/chrome-for-testing/#stable"
        chromedriver_zip_path = r'C:\Tools\chromedriver.zip'
        # Download the ChromeDriver zip
        subprocess.run(['curl', '-L', chromedriver_url, '-o', chromedriver_zip_path], check=True)
        # Extract ChromeDriver
        subprocess.run(['powershell', '-Command', f'Expand-Archive -Path {chromedriver_zip_path} -DestinationPath C:\\Tools\\'], check=True)
        # Set the ChromeDriver environmental variable
        os.environ["ChromeDriver"] = chromedriver_path
    else:
        print("✅ ChromeDriver is already installed.")

# Verify FFmpeg is installed and in PATH
def verify_ffmpeg():
    ffmpeg_path = r'C:\Tools\ffmpeg\bin\ffmpeg.exe'  # Path to FFmpeg executable
    ffmpeg_bin_dir = r'C:\Tools\ffmpeg\bin'  # Directory containing ffmpeg.exe
    
    # Check if FFmpeg is installed at the expected location
    if not os.path.exists(ffmpeg_path):
        print("❌ FFmpeg is not installed. Installing FFmpeg...")
        ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z"
        ffmpeg_zip_path = r'C:\Tools\ffmpeg.7z'
        # Download FFmpeg
        subprocess.run(['curl', '-L', ffmpeg_url, '-o', ffmpeg_zip_path], check=True)
        # Extract FFmpeg
        subprocess.run(['powershell', '-Command', f'Expand-Archive -Path {ffmpeg_zip_path} -DestinationPath C:\\Tools\\'], check=True)
    
    # Check if FFmpeg is already in the PATH environment variable
    path_env = os.getenv('PATH', '')
    if ffmpeg_bin_dir not in path_env:
        print(f"❌ FFmpeg is not in the system PATH. Adding {ffmpeg_bin_dir} to the PATH.")
        # Add FFmpeg to the system PATH (temporary for the session)
        os.environ['PATH'] = path_env + os.pathsep + ffmpeg_bin_dir
        print(f"✅ Added {ffmpeg_bin_dir} to PATH.")
    else:
        print("✅ FFmpeg is already in the system PATH.")

# Ensure download directory exists
download_dir = r'C:\Videos'  # Set the download directory path
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Verify required Python packages before importing
check_and_install_package('selenium', [sys.executable, '-m', 'pip', 'install', 'selenium'])
check_and_install_package('bs4', [sys.executable, '-m', 'pip', 'install', 'beautifulsoup4'])
check_and_install_package('requests', [sys.executable, '-m', 'pip', 'install', 'requests'])

# Now we can safely import packages after checking if they are installed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Configuration Paths
yt_dlp_path = r'C:\Tools\yt-dlp.exe'  # Path to yt-dlp executable
chromedriver_path = r'C:\Tools\chromedriver.exe'  # Path to ChromeDriver executable

# Verify yt-dlp, ChromeDriver, and FFmpeg
verify_yt_dlp(yt_dlp_path)
verify_chromedriver()
verify_ffmpeg()

# Setup Chrome headless
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

# Initialize ChromeDriver
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    # Step 1: Open trailer round-up page
    print("🔗 Visiting: https://www.themoviebox.net/s/trailer-round-up")
    driver.get("https://www.themoviebox.net/s/trailer-round-up")

    # Step 2: Wait for JS to load a link with "trailer-round-up" in the URL
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/p/trailer-round-up')]"))
        )
        matching_link = element.get_attribute("href")
        print(f"✅ Found matching link: {matching_link}")
    except Exception as e:
        print(f"❌ No matching link found (wait timed out). Error: {e}")
        driver.quit()
        exit(1)

    # Step 3: Open the matching link
    print(f"🔗 Visiting secondary page: {matching_link}")
    driver.get(matching_link)

    # Step 4: Set a 5-minute timeout while scrolling to load content
    max_wait_time = 300  # 5 minutes in seconds
    start_time = time.time()

    # Scroll to the bottom to load more content (for lazy-loaded elements)
    print("🔽 Scrolling to the bottom of the page to load more content...")

    while time.time() - start_time < max_wait_time:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for content to load after scrolling

        # Debug: Check how many iframes are detected during scrolling
        iframe_elements = driver.find_elements(By.XPATH, "//iframe[contains(@src, 'youtube-nocookie.com')]")
        print(f"❓ Found {len(iframe_elements)} iframes containing 'youtube-nocookie.com'.")
        
        if iframe_elements:
            print(f"✅ Found {len(iframe_elements)} YouTube iframe(s). Proceeding to extract links.")
            break  # Exit the loop once iframes are loaded

    else:
        print("⚠️ Timeout reached while waiting for YouTube iframes to load. Proceeding with available content.")

    # Step 5: Extract YouTube links (including iframe embeds)
    print("🔍 Extracting YouTube links...")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    raw_html = str(soup)

    # Find normal YouTube links
    normal_links = re.findall(
        r'(https?://(?:www\.)?(?:youtube\.com/watch\?v=[\w-]+|youtu\.be/[\w-]+))',
        raw_html
    )
    print(f"❓ Found {len(normal_links)} normal YouTube links via regex.")

    # Find YouTube embed iframe links, including youtube-nocookie.com
    iframe_elements = driver.find_elements(By.XPATH, "//iframe[contains(@src, 'youtube.com/embed/') or contains(@src, 'youtube-nocookie.com/embed/')]")
    
    embed_links = []
    for iframe in iframe_elements:
        src = iframe.get_attribute('src')
        if not src:
            src = iframe.get_attribute('data-src')  # Sometimes 'data-src' is used instead of 'src'
        
        # Check if the src contains either youtube.com/embed or youtube-nocookie.com/embed
        if src and ('youtube.com/embed/' in src or 'youtube-nocookie.com/embed/' in src):
            embed_links.append(src)

    print(f"❓ Found {len(embed_links)} embedded YouTube iframe links.")

    # Extract video IDs from the embed links (src attribute)
    embed_links = [f'https://www.youtube.com/watch?v={vid_id.split("/")[-1]}' for vid_id in embed_links]

    # Combine and deduplicate
    youtube_links = list(set(normal_links + embed_links))

    if not youtube_links:
        print("❌ No YouTube links found.")
    else:
        print(f"🎬 Found {len(youtube_links)} total YouTube links. Downloading...")

        # Verify yt-dlp is installed and executable
        verify_yt_dlp(yt_dlp_path)

        for link in youtube_links:
            print(f"⬇️ Downloading: {link}")
            try:
                subprocess.run([
                    yt_dlp_path,
                    '-P', download_dir,
                    '-f', 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',  # 1080p download
                    '--merge-output-format', 'mp4',
                    '--embed-thumbnail',
                    '--add-metadata',  # Embed description in metadata
                    '--output', os.path.join(download_dir, '%(title)s - %(upload_date)s.%(ext)s'),  # Format the filename
                    link
                ], check=True)
            except subprocess.CalledProcessError:
                print(f"❌ Failed to download: {link}")

finally:
    print("✅ Finished. Closing browser.")
    driver.quit()
