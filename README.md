# 🔗 URL Shortener

A modern, fast, and secure URL shortening service built with Flask and Supabase. Transform long URLs into short, shareable links with QR codes and analytics.

## ✨ Features

- **🚀 Lightning Fast** - Instant URL shortening with minimal latency
- **🔒 Secure & Private** - Rate limiting, input validation, and secure data handling
- **📊 Click Analytics** - Track clicks, creation dates, and access patterns
- **📱 QR Code Generation** - Automatic QR code creation for easy mobile sharing
- **🎨 Modern UI** - Beautiful, responsive design with smooth animations
- **🛡️ Rate Limiting** - Protection against abuse with configurable limits
- **🔄 Duplicate Detection** - Smart handling of already shortened URLs
- **📱 Mobile Responsive** - Optimized for all device sizes

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Supabase account and project
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd URL-Shortner
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_anon_key
   FLASK_SECRET_KEY=your_secret_key_here
   FLASK_ENV=development
   ```

5. **Set up Supabase database**
   
   Create a table named `urls` in your Supabase project:
   ```sql
   CREATE TABLE urls (
       id SERIAL PRIMARY KEY,
       original_url TEXT NOT NULL,
       short_id VARCHAR(10) UNIQUE NOT NULL,
       qr_url TEXT,
       click_count INTEGER DEFAULT 0,
       created_at TIMESTAMP DEFAULT NOW(),
       last_accessed TIMESTAMP
   );
   ```

6. **Set up Supabase storage**
   
   Create a storage bucket named `qr-codes` in your Supabase project and make it public.

7. **Run the application**
   ```bash
   python app.py
   ```

   Visit `http://localhost:5000` to use the application.

## 🔧 Configuration

The application supports multiple configuration environments:

- **Development** (`FLASK_ENV=development`) - Debug mode enabled
- **Production** (`FLASK_ENV=production`) - Optimized for deployment
- **Testing** (`FLASK_ENV=testing`) - For running tests

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SUPABASE_URL` | Your Supabase project URL | Yes | - |
| `SUPABASE_KEY` | Your Supabase anon key | Yes | - |
| `FLASK_SECRET_KEY` | Secret key for Flask sessions | Yes | - |
| `FLASK_ENV` | Environment (development/production/testing) | No | `development` |
| `REDIS_URL` | Redis URL for rate limiting (optional) | No | `memory://` |

## 📊 API Endpoints

### Web Interface
- `GET /` - Main application interface
- `POST /` - Shorten a URL
- `GET /<short_id>` - Redirect to original URL
- `GET /analytics/<short_id>` - View URL analytics

### API Endpoints
- `GET /api/analytics/<short_id>` - Get analytics data as JSON



## 🛡️ Security Features

- **Rate Limiting**: Configurable limits (default: 10/min, 50/hour, 200/day)
- **Input Validation**: URL format validation and sanitization
- **Environment Variables**: Sensitive data stored securely
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **CSRF Protection**: Flask secret key for session security

## 📱 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## 🔄 Rate Limits

Default rate limits (configurable):
- 10 requests per minute
- 50 requests per hour
- 200 requests per day

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request



## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Issues](../../issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## 🙏 Acknowledgments

- Flask framework for the web application
- Supabase for backend services
- QRCode library for QR code generation
- Modern CSS techniques for beautiful UI

---

**Made with ❤️ for the developer community**