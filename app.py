from flask import Flask, request, redirect, render_template, url_for, jsonify, flash
import string, random, io, os, re
import qrcode
from supabase import create_client
from datetime import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Load environment variables
load_dotenv()

from config import config

app = Flask(__name__)

# Load configuration
config_name = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Validate configuration only if not in testing mode
if not app.config.get('TESTING', False):
    try:
        config[config_name].validate()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please check your environment variables and .env file")
        if config_name == 'production':
            raise
        # In development, continue with warnings
        print("Running in development mode with missing configuration...")

# Rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=app.config.get('RATELIMIT_STORAGE_URL', 'memory://')
)
limiter.init_app(app)

# Supabase config - only initialize if credentials are available
supabase = None
if app.config.get('SUPABASE_URL') and app.config.get('SUPABASE_KEY'):
    try:
        supabase = create_client(app.config['SUPABASE_URL'], app.config['SUPABASE_KEY'])
    except Exception as e:
        print(f"Failed to initialize Supabase client: {e}")
else:
    print("Warning: Supabase credentials not configured")

def is_valid_url(url):
    """Validate URL format"""
    if not url or not isinstance(url, str):
        return False
    
    try:
        # First check if it already has a valid scheme
        result = urlparse(url)
        if result.scheme and result.netloc:
            return result.scheme in ('http', 'https', 'ftp')
        
        # If no scheme, try adding https and validate again
        if not result.scheme and '.' in url:
            test_url = 'https://' + url
            result = urlparse(test_url)
            # Must have a valid domain with at least one dot
            return (result.scheme == 'https' and 
                   result.netloc and 
                   '.' in result.netloc and 
                   not result.netloc.startswith('.') and
                   not result.netloc.endswith('.'))
        
        return False
    except Exception:
        return False

def generate_short_id(num_chars=None):
    """Generate a unique short ID"""
    if num_chars is None:
        num_chars = app.config.get('SHORT_ID_LENGTH', 6)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=num_chars))

def check_duplicate_url(original_url):
    """Check if URL already exists in database"""
    if not supabase:
        print("Supabase client not initialized")
        return None
        
    try:
        result = supabase.table('urls').select('*').eq('original_url', original_url).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error checking duplicate: {e}")
        return None

def upload_qr_to_supabase(image, filename):
    """Upload QR code image to Supabase storage"""
    if not supabase:
        print("Supabase client not initialized")
        return None
        
    try:
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Check if file already exists and delete it
        try:
            supabase.storage.from_('qr-codes').remove([filename])
        except:
            pass  # File doesn't exist, which is fine
        
        supabase.storage.from_('qr-codes').upload(filename, buffer.read())
        public_url = f"{app.config['SUPABASE_URL']}/storage/v1/object/public/qr-codes/{filename}"
        return public_url
    except Exception as e:
        print(f"Error uploading QR code: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def home():
    short_url = None
    qr_url = None
    error_message = None
    success_message = None

    if request.method == 'POST':
        try:
            original_url = request.form.get('url', '').strip()
            
            # Validate URL
            if not original_url:
                error_message = "Please enter a URL"
            elif len(original_url) > app.config.get('MAX_URL_LENGTH', 2048):
                error_message = "URL is too long"
            elif not is_valid_url(original_url):
                error_message = "Please enter a valid URL (e.g., example.com or https://example.com)"
            else:
                # Add protocol if missing
                if not original_url.startswith(('http://', 'https://')):
                    original_url = 'https://' + original_url
                
                # Check for duplicate URL (only if Supabase is available)
                existing_url = None
                if supabase:
                    existing_url = check_duplicate_url(original_url)
                    
                if existing_url:
                    short_url = request.host_url + existing_url['short_id']
                    qr_url = existing_url['qr_url']
                    success_message = "URL already shortened! Here's your existing link:"
                elif not supabase:
                    error_message = "Database connection not available. Please check configuration."
                else:
                    # Generate unique short ID
                    attempts = 0
                    short_id = None
                    while attempts < 10:
                        short_id = generate_short_id()
                        try:
                            existing = supabase.table('urls').select('id').eq('short_id', short_id).execute()
                            if not existing.data:
                                break
                        except Exception as e:
                            print(f"Error checking short ID uniqueness: {e}")
                            break
                        attempts += 1
                    
                    if attempts >= 10:
                        error_message = "Unable to generate unique short URL. Please try again."
                    else:
                        # Generate QR code
                        short_url = request.host_url + short_id
                        qr = qrcode.QRCode(
                            version=1, 
                            box_size=app.config.get('QR_CODE_SIZE', 10), 
                            border=app.config.get('QR_CODE_BORDER', 5)
                        )
                        qr.add_data(short_url)
                        qr.make(fit=True)
                        qr_image = qr.make_image(fill_color="black", back_color="white")
                        
                        # Upload QR code
                        qr_url = upload_qr_to_supabase(qr_image, f"{short_id}.png")
                        
                        if qr_url:
                            # Save to Supabase DB
                            try:
                                result = supabase.table('urls').insert({
                                    'original_url': original_url,
                                    'short_id': short_id,
                                    'qr_url': qr_url,
                                    'click_count': 0,
                                    'created_at': datetime.utcnow().isoformat()
                                }).execute()
                                
                                if result.data:
                                    success_message = "URL shortened successfully!"
                                else:
                                    error_message = "Failed to save URL. Please try again."
                            except Exception as e:
                                print(f"Error saving URL to database: {e}")
                                error_message = "Failed to save URL. Please try again."
                        else:
                            error_message = "Failed to generate QR code. Please try again."
                            
        except Exception as e:
            print(f"Error in home route: {e}")
            error_message = "An unexpected error occurred. Please try again."

    return render_template('index.html', 
                         short_url=short_url, 
                         qr_url=qr_url, 
                         error_message=error_message,
                         success_message=success_message)

@app.route('/<short_id>')
def redirect_to_url(short_id):
    try:
        # Validate short_id format (allow flexible length)
        if not re.match(r'^[a-zA-Z0-9]+$', short_id) or len(short_id) < 4 or len(short_id) > 12:
            return render_template('404.html'), 404
            
        if not supabase:
            return render_template('404.html'), 404
            
        result = supabase.table('urls').select('*').eq('short_id', short_id).execute()
        data = result.data

        if data:
            original_url = data[0]['original_url']
            url_id = data[0]['id']
            current_count = data[0]['click_count']

            # Increment click count
            try:
                supabase.table('urls').update({
                    'click_count': current_count + 1,
                    'last_accessed': datetime.utcnow().isoformat()
                }).eq('id', url_id).execute()
            except Exception as e:
                print(f"Error updating click count: {e}")
                # Continue with redirect even if count update fails

            return redirect(original_url)

        return render_template('404.html'), 404
        
    except Exception as e:
        print(f"Error in redirect route: {e}")
        return render_template('404.html'), 404

@app.route('/analytics/<short_id>')
def analytics(short_id):
    """Show analytics for a shortened URL"""
    try:
        if not supabase:
            return render_template('404.html'), 404
            
        result = supabase.table('urls').select('*').eq('short_id', short_id).execute()
        data = result.data
        
        if data:
            url_data = data[0]
            return render_template('analytics.html', url_data=url_data)
        else:
            return render_template('404.html'), 404
            
    except Exception as e:
        print(f"Error in analytics route: {e}")
        return render_template('404.html'), 404

@app.route('/api/analytics/<short_id>')
def api_analytics(short_id):
    """API endpoint for analytics data"""
    try:
        if not supabase:
            return jsonify({'error': 'Database not available'}), 503
            
        result = supabase.table('urls').select('*').eq('short_id', short_id).execute()
        data = result.data
        
        if data:
            return jsonify(data[0])
        else:
            return jsonify({'error': 'URL not found'}), 404
            
    except Exception as e:
        print(f"Error in API analytics route: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template('ratelimit.html'), 429

if __name__ == '__main__':
    app.run(debug=True)