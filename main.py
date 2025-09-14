import flask
from flask import Flask, jsonify, send_file, request, render_template, redirect, Response
import requests
import io
import uuid
import random
from urllib.parse import quote, unquote
import string
from PIL import Image, ImageDraw  # Pillow library
import json

app = Flask('app')

# Cache for storing images and URLs
image_cache = {}
url_map = {}

# Generate a unique short ID for URL
def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choice(chars) for _ in range(length))
        if short_id not in url_map:
            return short_id

@app.route('/')
def home():
    return render_template('index.html')

# ------------------- Animal APIs -------------------

@app.route('/api/dog')
def get_dog():
    try:
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        if response.status_code == 200:
            data = response.json()
            dog_image_url = data.get('message', '')
            if dog_image_url:
                img_response = requests.get(dog_image_url)
                if img_response.status_code == 200:
                    image_id = str(uuid.uuid4())
                    image_cache[image_id] = img_response.content
                    base_url = request.url_root.rstrip('/')
                    return jsonify({
                        'success': True,
                        'image_id': image_id,
                        'image_url': f'{base_url}/dog/images/{image_id}.png',
                        'status': data.get('status', '')
                    })
        return jsonify({'success': False, 'error': 'Failed to fetch dog image'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/cat')
def get_cat():
    try:
        response = requests.get('https://api.thecatapi.com/v1/images/search')
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                cat_image_url = data[0].get('url', '')
                img_response = requests.get(cat_image_url)
                if img_response.status_code == 200:
                    image_id = str(uuid.uuid4())
                    image_cache[image_id] = img_response.content
                    base_url = request.url_root.rstrip('/')
                    return jsonify({
                        'success': True,
                        'image_id': image_id,
                        'image_url': f'{base_url}/cat/images/{image_id}.png'
                    })
        return jsonify({'success': False, 'error': 'Failed to fetch cat image'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/neko')
def get_neko():
    try:
        response = requests.get('https://nekos.best/api/v2/neko')
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            if results:
                neko_image_url = results[0].get('url', '')
                img_response = requests.get(neko_image_url)
                if img_response.status_code == 200:
                    image_id = str(uuid.uuid4())
                    image_cache[image_id] = img_response.content
                    base_url = request.url_root.rstrip('/')
                    return jsonify({
                        'success': True,
                        'image_id': image_id,
                        'image_url': f'{base_url}/neko/images/{image_id}.png',
                        'results': results
                    })
        return jsonify({'success': False, 'error': 'Failed to fetch neko image'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/meme')
def get_meme():
    try:
        response = requests.get('https://meme-api.com/gimme')
        if response.status_code == 200:
            data = response.json()
            meme_image_url = data.get('url', '')
            if meme_image_url:
                img_response = requests.get(meme_image_url)
                if img_response.status_code == 200:
                    image_id = str(uuid.uuid4())
                    image_cache[image_id] = img_response.content
                    base_url = request.url_root.rstrip('/')
                    return jsonify({
                        'success': True,
                        'image_id': image_id,
                        'image_url': f'{base_url}/meme/images/{image_id}.png',
                        'postLink': data.get('postLink', ''),
                        'subreddit': data.get('subreddit', '').replace('r/', ''),
                        'title': data.get('title', ''),
                        'author': data.get('author', '').replace('u/', ''),
                        'ups': data.get('ups', 0)
                    })
        return jsonify({'success': False, 'error': 'Failed to fetch meme'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Helper functions for generating random IDs and HWIDs
def generate_random_hwid_fluxus(length=96):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(chars) for _ in range(length))

def generate_random_hwid_arceus(length=18):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(chars) for _ in range(length))

def generate_random_id_delta(length=64):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(chars) for _ in range(length))

def generate_random_id_deltaios(length=64):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(chars) for _ in range(length))

def generate_random_id_cryptic(length=64):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(chars) for _ in range(length))

def generate_random_id_hydrogen(length=10):
    digits = '0123456789'
    return ''.join(random.choice(digits) for _ in range(length))

def generate_random_hwid_vegax():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    parts = []
    for i in range(5):
        part_length = 8 if random.random() < 0.5 else 7
        part = ''.join(random.choice(chars) for _ in range(part_length))
        parts.append(part)
    return '-'.join(parts)

def generate_random_hwid_trigonevo():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    
    def random_string(length):
        return ''.join(random.choice(chars) for _ in range(length))
    
    return f"{random_string(8)}-{random_string(4)}-{random_string(4)}-{random_string(4)}-{random_string(12)}"

def generate_random_id_cacti(length=64):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(chars) for _ in range(length))

def generate_random_hwid_evon():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    
    def random_string(length):
        return ''.join(random.choice(chars) for _ in range(length))
    
    return f"{random_string(8)}-{random_string(4)}-{random_string(4)}-{random_string(4)}-{random_string(12)}"

@app.route('/api/roblox')
def get_roblox_info():
    username = request.args.get('username', '').strip()
    if not username:
        return jsonify({'error': 'Roblox username is required'}), 400
    
    try:
        # First, get user ID from username
        search_response = requests.post('https://users.roblox.com/v1/usernames/users', 
                                       json={'usernames': [username], 'excludeBannedUsers': False})
        
        if search_response.status_code != 200 or not search_response.json().get('data'):
            return jsonify({'error': 'Roblox user not found'}), 404
        
        user_id = search_response.json()['data'][0]['id']
        
        # Get detailed user information using concurrent requests
        user_response = requests.get(f'https://users.roblox.com/v1/users/{user_id}')
        avatar_response = requests.get(f'https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=420x420&format=Png&isCircular=false')
        
        try:
            friends_response = requests.get(f'https://friends.roblox.com/v1/users/{user_id}/friends/count')
            friends_count = friends_response.json().get('count', 0) if friends_response.status_code == 200 else 0
        except:
            friends_count = 0
        
        if user_response.status_code != 200:
            return jsonify({'error': 'Failed to fetch user data'}), 500
        
        user = user_response.json()
        avatar_data = avatar_response.json().get('data', [{}])[0] if avatar_response.status_code == 200 else {}
        
        return jsonify({
            'id': user.get('id'),
            'username': user.get('name'),
            'displayName': user.get('displayName'),
            'description': user.get('description', 'No description available'),
            'created': user.get('created'),
            'isBanned': user.get('isBanned'),
            'externalAppDisplayName': user.get('externalAppDisplayName'),
            'hasVerifiedBadge': user.get('hasVerifiedBadge'),
            'avatar': {
                'imageUrl': avatar_data.get('imageUrl'),
                'state': avatar_data.get('state', 'Unavailable')
            },
            'friends': friends_count,
            'profileUrl': f'https://www.roblox.com/users/{user_id}/profile'
        })
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            if e.response.status_code == 404:
                return jsonify({'error': 'Roblox user not found'}), 404
            elif e.response.status_code == 429:
                return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429
        return jsonify({'error': 'Failed to fetch Roblox user data'}), 500
    except Exception as e:
        return jsonify({'error': 'Failed to fetch Roblox user data'}), 500

@app.route('/api/gen')
def generate_link():
    service = request.args.get('service', '').lower()
    if not service:
        return jsonify({'result': 'Service parameter is required'}), 400
    
    generators = {
        'fluxus': lambda: f"https://flux.li/android/external/start.php?HWID={generate_random_hwid_fluxus()}",
        'arceus': lambda: f"https://spdmteam.com/key-system-1?hwid={generate_random_hwid_arceus()}&zone=Europe/Rome&os=android",
        'delta': lambda: f"https://gateway.platoboost.com/a/8?id={generate_random_id_delta()}",
        'deltaios': lambda: f"https://gateway.platoboost.com/a/2?id={generate_random_id_deltaios()}",
        'cryptic': lambda: f"https://gateway.platoboost.com/a/39097?id={generate_random_id_cryptic()}",
        'hydrogen': lambda: f"https://gateway.platoboost.com/a/2569?id={generate_random_id_hydrogen()}",
        'vegax': lambda: f"https://pandadevelopment.net/getkey?service=vegax&hwid={generate_random_hwid_vegax()}&provider=linkvertise",
        'trigon': lambda: f"https://trigonevo.fun/whitelist/?HWID={generate_random_hwid_trigonevo()}",
        'cacti': lambda: f"https://gateway.platoboost.com/a/23344?id={generate_random_id_cacti()}",
        'evon': lambda: f"https://pandadevelopment.net/getkey?service=evon&hwid={generate_random_hwid_evon()}"
    }
    
    if service not in generators:
        return jsonify({'result': 'Invalid executor key provided'}), 400
    
    return jsonify({'result': generators[service]()})

@app.route('/api/discord')
def get_discord_info():
    code = request.args.get('code', '').strip()
    if not code:
        return jsonify({'error': 'Discord invite code or URL is required'}), 400
    
    try:
        # Extract invite code from URL or use as-is
        invite_code = code
        if 'discord.gg/' in code:
            invite_code = code.split('discord.gg/')[1]
        
        # Get invite information
        response = requests.get(f'https://discord.com/api/v10/invites/{invite_code}?with_counts=true&with_expiration=true')
        
        if response.status_code == 404:
            return jsonify({'error': 'Discord invite not found or has expired'}), 404
        elif response.status_code == 429:
            return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429
        elif response.status_code != 200:
            return jsonify({'error': 'Failed to fetch Discord server data'}), 500
        
        invite_data = response.json()
        
        if not invite_data.get('guild'):
            return jsonify({'error': 'No server information found for this invite'}), 404
        
        guild = invite_data['guild']
        guild_id = guild['id']
        
        return jsonify({
            'id': guild_id,
            'name': guild.get('name'),
            'description': guild.get('description', 'No description available'),
            'icon': f"https://cdn.discordapp.com/icons/{guild_id}/{guild['icon']}.png" if guild.get('icon') else None,
            'banner': f"https://cdn.discordapp.com/banners/{guild_id}/{guild['banner']}.png" if guild.get('banner') else None,
            'splash': f"https://cdn.discordapp.com/splashes/{guild_id}/{guild['splash']}.png" if guild.get('splash') else None,
            'verification_level': guild.get('verification_level'),
            'member_count': invite_data.get('approximate_member_count', 0),
            'online_count': invite_data.get('approximate_presence_count', 0),
            'boost_level': guild.get('premium_subscription_count', 0) // 2,
            'features': guild.get('features', []),
            'vanity_url_code': guild.get('vanity_url_code'),
            'invite_info': {
                'code': invite_data.get('code'),
                'expires_at': invite_data.get('expires_at'),
                'uses': invite_data.get('uses', 0),
                'max_uses': invite_data.get('max_uses', 0),
                'inviter': {
                    'username': invite_data['inviter']['username'],
                    'discriminator': invite_data['inviter']['discriminator'],
                    'avatar': f"https://cdn.discordapp.com/avatars/{invite_data['inviter']['id']}/{invite_data['inviter']['avatar']}.png" if invite_data['inviter'].get('avatar') else None
                } if invite_data.get('inviter') else None,
                'channel': {
                    'name': invite_data['channel']['name'],
                    'type': invite_data['channel']['type']
                } if invite_data.get('channel') else None
            },
            'created_at': str(int((int(guild_id) / 4194304) + 1420070400000))
        })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch Discord server data'}), 500

@app.route('/server')
def discord_redirect():
    return redirect('https://discord.gg/VvWgjhHyQN')

# Helper function to download avatar
def download_avatar(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
        return None
    except Exception:
        return None

# Helper function to create circular avatar
def circle_avatar(avatar):
    # Create a mask for circular cropping
    mask = Image.new('L', avatar.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, avatar.size[0], avatar.size[1]), fill=255)
    
    # Apply the mask to the avatar
    result = Image.new('RGBA', avatar.size, (0, 0, 0, 0))
    result.paste(avatar, (0, 0))
    result.putalpha(mask)
    return result

@app.route('/api/mydog')
def create_mydog_image():
    avatar1_url = request.args.get('avatar1', '').strip()
    avatar2_url = request.args.get('avatar2', '').strip()
    
    if not avatar1_url or not avatar2_url:
        return jsonify({'error': 'Both avatar1 and avatar2 parameters are required'}), 400
    
    try:
        # Load base image
        base_image = Image.open('base_mydog.jpg').convert('RGBA')
        
        # Download avatars
        avatar1 = download_avatar(avatar1_url)
        avatar2 = download_avatar(avatar2_url)
        
        if avatar1 is None or avatar2 is None:
            return jsonify({'error': 'Failed to retrieve one or both avatars'}), 500
        
        # Resize and make circular
        avatar1_resized = circle_avatar(avatar1.resize((230, 230)))
        avatar2_resized = circle_avatar(avatar2.resize((310, 310)))
        
        # Paste avatars onto base image
        base_image.paste(avatar1_resized, (370, 0), avatar1_resized)
        base_image.paste(avatar2_resized, (0, 220), avatar2_resized)
        
        # Save to buffer
        final_buffer = io.BytesIO()
        base_image.save(final_buffer, 'PNG')
        final_buffer.seek(0)
        
        # Store in cache and return
        image_id = str(uuid.uuid4())
        image_cache[image_id] = final_buffer.getvalue()
        base_url = request.url_root.rstrip('/')
        
        return jsonify({
            'success': True,
            'image_id': image_id,
            'image_url': f'{base_url}/mydog/images/{image_id}.png'
        })
    except Exception as e:
        return jsonify({'error': f'Failed to create image: {str(e)}'}), 500

@app.route('/mydog/images/<image_id>.png')
def serve_mydog_image(image_id):
    if image_id in image_cache:
        return send_file(io.BytesIO(image_cache[image_id]), mimetype='image/png')
    return jsonify({'error': 'Image not found'}), 404

@app.route('/api/weather')
def get_weather():
    place = request.args.get('p', '').strip()
    
    if not place:
        return jsonify({'error': 'Parameter "p" (place) is required'}), 400
    
    try:
        response = requests.get(f'https://api.popcat.xyz/v2/weather?q={place}', timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({'error': 'Weather data not found for the specified location'}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to fetch weather data: {str(e)}'}), 500

@app.route('/api/welcomecard')
def get_welcome_card():
    background = request.args.get('background', '').strip()
    text1 = request.args.get('text1', '').strip()
    text2 = request.args.get('text2', '').strip()
    text3 = request.args.get('text3', '').strip()
    avatar = request.args.get('avatar', '').strip()
    
    # All parameters are required
    if not all([background, text1, text2, text3, avatar]):
        return jsonify({'error': 'All parameters are required: background, text1, text2, text3, avatar'}), 400
    
    try:
        # Build the PopCat API URL with all parameters
        api_url = f'https://api.popcat.xyz/v2/welcomecard?background={background}&text1={text1}&text2={text2}&text3={text3}&avatar={avatar}'
        
        response = requests.get(api_url, timeout=15)
        
        if response.status_code == 200:
            # Store the image in cache
            image_id = str(uuid.uuid4())
            image_cache[image_id] = response.content
            base_url = request.url_root.rstrip('/')
            
            return jsonify({
                'success': True,
                'image_id': image_id,
                'image_url': f'{base_url}/welcomecard/images/{image_id}.png'
            })
        else:
            return jsonify({'error': 'Failed to generate welcome card'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to create welcome card: {str(e)}'}), 500

@app.route('/welcomecard/images/<image_id>.png')
def serve_welcome_card_image(image_id):
    if image_id in image_cache:
        return send_file(io.BytesIO(image_cache[image_id]), mimetype='image/png')
    return jsonify({'error': 'Image not found'}), 404


@app.route('/dog/images/<image_id>.png')
def serve_dog_image(image_id):
    if image_id in image_cache:
        return send_file(io.BytesIO(image_cache[image_id]), mimetype='image/png')
    return jsonify({'error': 'Image not found'}), 404

@app.route('/cat/images/<image_id>.png')
def serve_cat_image(image_id):
    if image_id in image_cache:
        return send_file(io.BytesIO(image_cache[image_id]), mimetype='image/png')
    return jsonify({'error': 'Image not found'}), 404

@app.route('/neko/images/<image_id>.png')
def serve_neko_image(image_id):
    if image_id in image_cache:
        return send_file(io.BytesIO(image_cache[image_id]), mimetype='image/png')
    return jsonify({'error': 'Image not found'}), 404

@app.route('/meme/images/<image_id>.png')
def serve_meme_image(image_id):
    if image_id in image_cache:
        return send_file(io.BytesIO(image_cache[image_id]), mimetype='image/png')
    return jsonify({'error': 'Image not found'}), 404

@app.route('/generate/images/<image_id>.png')
def serve_generated_image(image_id):
    if image_id in image_cache:
        return send_file(io.BytesIO(image_cache[image_id]), mimetype='image/png')
    return jsonify({'error': 'Image not found'}), 404

# ------------------- Utility APIs -------------------

@app.route('/api/image')
def get_image():
    try:
        prompt = request.args.get('prompt', '')
        if not prompt:
            return jsonify({'success': False, 'error': 'Prompt parameter is required'}), 400
        encoded_prompt = quote(prompt)
        width = random.randint(1024, 2048)
        height = random.randint(1024, 2048)
        seed = random.randint(100000, 999999)
        api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model=midjourney&nologo=true&private=false&enhance=true&seed={seed}"
        img_response = requests.get(api_url)
        if img_response.status_code == 200:
            image_id = str(uuid.uuid4())
            image_cache[image_id] = img_response.content
            base_url = request.url_root.rstrip('/')
            return jsonify({
                'success': True,
                'image_id': image_id,
                'image_url': f'{base_url}/generate/images/{image_id}.png',
                'prompt': prompt,
                'width': width,
                'height': height,
                'seed': seed
            })
        return jsonify({'success': False, 'error': 'Failed to generate image'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/randomcolor')
def get_random_color():
    hex_color_code = '#{:06x}'.format(random.randint(0, 0xFFFFFF))
    return jsonify({'success': True, 'color': hex_color_code})

@app.route('/api/color/info')
def get_color_info():
    """Get info about a color in HEX and RGB"""
    color = request.args.get('color', '').lstrip('#').lower()
    if not color or len(color) != 6:
        return jsonify({
            'success': False,
            'error': 'Invalid color format. Use hex like #0099ff'
        }), 400
    try:
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
        base_url = request.url_root.rstrip('/')
        preview_url = f"{base_url}/color/preview/{color}.png"
        return jsonify({
            'success': True,
            'color': f'#{color}',
            'preview_url': preview_url
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/color/preview/<color>.png')
def color_preview(color):
    """Generate a solid color preview image"""
    try:
        color = color.lower()
        if len(color) != 6:
            return jsonify({'error': 'Invalid color'}), 400
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
        img = Image.new("RGB", (100, 100), (r, g, b))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shorten')
def shorten_url():
    url = request.args.get('url', '')
    if not url:
        return jsonify({'success': False, 'error': 'URL parameter is required'}), 400
    short_id = generate_short_id()
    url_map[short_id] = url
    base_url = request.url_root.rstrip('/')
    return jsonify({
        'success': True,
        'original_url': url,
        'short_id': short_id,
        'short_url': f'{base_url}/s/{short_id}'
    })

@app.route('/s/<short_id>')
def redirect_to_url(short_id):
    original_url = url_map.get(short_id)
    if original_url:
        return redirect(original_url)
    return jsonify({'error': 'Short URL not found'}), 404

@app.route('/api/github')
def get_github_info():
    username = request.args.get('username', '')
    if not username:
        return jsonify({'error': 'GitHub username is required'}), 400
    
    try:
        # Get both user info and repositories concurrently
        user_response = requests.get(f'https://api.github.com/users/{username}')
        repos_response = requests.get(f'https://api.github.com/users/{username}/repos?per_page=100')
        
        if user_response.status_code == 404:
            return jsonify({'error': 'GitHub user not found'}), 404
        elif user_response.status_code != 200:
            return jsonify({'error': 'Failed to fetch GitHub data'}), 500
        
        user = user_response.json()
        repos = repos_response.json() if repos_response.status_code == 200 else []
        
        # Calculate comprehensive statistics
        total_stars = sum(repo.get('stargazers_count', 0) for repo in repos)
        total_forks = sum(repo.get('forks_count', 0) for repo in repos)
        languages = list(set(repo.get('language') for repo in repos if repo.get('language')))
        
        # Find most starred repository
        most_starred_repo = None
        if repos:
            sorted_repos = sorted(repos, key=lambda x: x.get('stargazers_count', 0), reverse=True)
            if sorted_repos:
                most_starred_repo = sorted_repos[0].get('name')
        
        return jsonify({
            'username': user.get('login'),
            'name': user.get('name'),
            'bio': user.get('bio'),
            'location': user.get('location'),
            'company': user.get('company'),
            'blog': user.get('blog'),
            'avatar': user.get('avatar_url'),
            'followers': user.get('followers'),
            'following': user.get('following'),
            'publicRepos': user.get('public_repos'),
            'created': user.get('created_at'),
            'statistics': {
                'totalStars': total_stars,
                'totalForks': total_forks,
                'languages': languages[:10],
                'mostStarredRepo': most_starred_repo
            }
        })
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            if e.response.status_code == 404:
                return jsonify({'error': 'GitHub user not found'}), 404
        return jsonify({'error': 'Failed to fetch GitHub data'}), 500
    except Exception as e:
        return jsonify({'error': 'Failed to fetch GitHub data'}), 500

@app.route('/api/pokemon')
def get_pokemon_info():
    pokemon_name = request.args.get('name', '').lower().strip()
    if not pokemon_name:
        return jsonify({'success': False, 'error': 'Pokémon name parameter is required'}), 400
    try:
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}')
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                'success': True,
                'name': data['name'],
                'stats': {s['stat']['name']: s['base_stat'] for s in data['stats']},
                'abilities': [a['ability']['name'] for a in data['abilities']],
                'types': [t['type']['name'] for t in data['types']],
                'image_url': data['sprites']['front_default']
            })
        return jsonify({'success': False, 'error': 'Pokémon not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/password')
def generate_password():
    try:
        length = int(request.args.get('length', 12))
        if not 8 <= length <= 64:
            return jsonify({'success': False, 'error': 'Length 8-64 required'}), 400
        chars = string.ascii_lowercase
        if request.args.get('uppercase', 'true') == 'true':
            chars += string.ascii_uppercase
        if request.args.get('digits', 'true') == 'true':
            chars += string.digits
        if request.args.get('special', 'true') == 'true':
            chars += string.punctuation
        password = ''.join(random.choice(chars) for _ in range(length))
        return jsonify({'success': True, 'password': password})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/fakeip')
def generate_fake_ip():
    try:
        # Generate random IP address for testing purposes
        ip_parts = [random.randint(1, 254) for _ in range(4)]
        fake_ip = '.'.join(map(str, ip_parts))
        return jsonify({
            'success': True,
            'ip': fake_ip,
            'type': 'IPv4'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/nitro')
def generate_nitro_code():
    try:
        # Generate fake Discord Nitro code for testing purposes
        chars = string.ascii_letters + string.digits
        code_length = random.choice([16, 17, 18, 19])  # Typical Nitro code lengths
        fake_code = ''.join(random.choice(chars) for _ in range(code_length))
        return jsonify({
            'success': True,
            'code': fake_code,
            'url': f'https://discord.gift/{fake_code}',
            'note': 'This is a fake code for testing purposes only'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ------------------- Error -------------------

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
