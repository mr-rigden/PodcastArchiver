import argparse
import os
import subprocess
from urllib.parse import urlparse


from jinja2 import Environment, FileSystemLoader
from PIL import Image
from markdown import markdown
import requests
from slugify import slugify
import xmltodict

import logging
import logging

log_format = "%(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)
logger = logging.getLogger(__name__)


logger.debug("Initializing Program")
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

parser = argparse.ArgumentParser(description="A little program that downloads and compresses a podcast")
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("url", help="Podcast RSS URL", type=str)
args = parser.parse_args()

output_dir = os.path.join(os.getcwd(), 'output')

podcast = {}

def download_audio_files():
    logger.debug('  Downloading episode files')
    for episode in podcast['episodes']:
        download_audio_file(episode)

def download_audio_file(episode):
    logger.debug('          Downloading episode file')
    file_path = os.path.join(output_dir, podcast['rss']['channel']['slug'], 'audio', episode['file_name'])
    if not os.path.exists(file_path):
        r = requests.get(episode['enclosure']['@url'], allow_redirects=True)
        open(file_path, 'wb').write(r.content)

def download_and_resize_cover_image():
    logger.debug('  Downloading cover art')
    url = podcast['rss']['channel']['itunes:image']['@href']
    cover_art_path = os.path.join(output_dir, podcast['rss']['channel']['slug'], "cover_art.jpg")
    small_cover_art_path = os.path.join(output_dir, podcast['rss']['channel']['slug'], "small_cover_art.jpg")
    response = requests.get(url, stream=True)
    response.raw.decode_content = True
    img = Image.open(response.raw)
    img = img.convert('RGB')
    img.save(cover_art_path)
    img.thumbnail((1000, 1000))
    img.save(small_cover_art_path, optimize=True)



def make_slugs():
    logger.debug('  Making slugs')
    podcast['rss']['channel']['slug'] = slugify(podcast['rss']['channel']['title'])
    for item in podcast['rss']['channel']['item']:
        item['slug'] = slugify(item['title'])

def make_podcast_dirs():
    logger.debug('  Making directories')
    dirs = ['audio', 'episode']
    dir_path = os.path.join(output_dir, podcast['rss']['channel']['slug'])
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    for dir in dirs:
        dir_path = os.path.join(output_dir, podcast['rss']['channel']['slug'], dir)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

def process_episodes():
    logger.debug('  Processing episodes')
    global podcast
    podcast['episodes'] = []
    for item in podcast['rss']['channel']['item']:
        if 'enclosure' in item:
            item['url'] = item['enclosure']['@url']
            url_path = urlparse(item['url']).path
            item['file_name'] = os.path.basename(url_path)
            podcast['episodes'].append(item)



def process_podcast(url):
    logger.info('Processing podcast with URL: ' + url) 
    global podcast
    logger.debug('  Downloading RSS Feed') 
    r = requests.get(url)
    logger.debug('  Parsing XML') 
    podcast = xmltodict.parse(r.text)
    make_slugs()
    process_episodes()
    make_podcast_dirs()
    download_and_resize_cover_image()
    download_audio_files()
    render_front_page()
    render_episodes()
    save_feed(r.content)
    compress_output()


def render_front_page():
    logger.debug('  Rendering front page')
    frontpage_path = os.path.join(output_dir, podcast['rss']['channel']['slug'], "index.html")
    template = env.get_template('frontpage.html')
    output = template.render(podcast=podcast)
    with open(frontpage_path, 'w') as f:
        f.write(output)

def render_episodes():
    logger.debug('  Rendering episode pages')
    for episode in podcast['episodes']:
        render_episode(episode)

def render_episode(episode):
    logger.debug('          Rendering episode page')
    episode_dir = os.path.join(output_dir, podcast['rss']['channel']['slug'], 'episode', episode['slug'])
    if not os.path.exists(episode_dir):
        os.makedirs(episode_dir)
        
    episode['description'] = markdown(episode['description'], extensions=["mdx_linkify"])

    episode_path = os.path.join(episode_dir, "index.html")
    template = env.get_template('episode.html')
    output = template.render(episode=episode)
    with open(episode_path, 'w') as f:
        f.write(output)

def save_feed(content):
    logger.debug('  Saving RSS feed')
    file_path = os.path.join(output_dir, podcast['rss']['channel']['slug'], "rss.xml")
    open(file_path, 'wb').write(content)


def compress_output():
    return
    logger.debug('  Compressing podccast')
    target_dir = file_path = os.path.join(podcast['rss']['channel']['slug'])
    file_name = podcast['rss']['channel']['slug'] + '.tar.gz'
    file_path = os.path.join(output_dir, file_name)
    subprocess.call(['tar', '-C', output_dir, '-czf', file_name, target_dir], cwd=output_dir)


if __name__ == "__main__":
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    process_podcast(args.url)



