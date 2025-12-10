import socket

from app import app
from waitress import serve


def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        # Create a socket to get the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "localhost"


if __name__ == "__main__":
    local_ip = get_local_ip()
    port = 8080

    print("=" * 60)
    print("Excel to PDF Converter - Production Server")
    print("=" * 60)
    print(f"\n✓ Server starting on port {port}...")
    print(f"\n📍 Access the application at:")
    print(f"   Local:   http://127.0.0.1:{port}")
    print(f"   Network: http://{local_ip}:{port}")
    print("\n📢 Share this URL with office workers:")
    print(f"   http://{local_ip}:{port}")
    print("\n⚠️  Keep this window open to keep the server running")
    print("   Press Ctrl+C to stop the server")
    print("=" * 60)
    print("\n")

    # Start the production server with Waitress
    # - host='0.0.0.0' allows access from other computers on the network
    # - threads=4 allows handling multiple users simultaneously
    # - url_scheme='http' for local network use
    serve(app, host="0.0.0.0", port=port, threads=4, url_scheme="http")
