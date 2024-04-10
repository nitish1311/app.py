import socket
import re

# Function to fetch HTML content from the given URL
def fetch_html(url):
    host = 'time.com'
    path = '/'
    request = f'GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n'
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, 80))
        s.sendall(request.encode())
        response = b''

        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk

    return response.decode()

# Function to extract the latest 6 stories from the HTML content
def extract_latest_stories(html_content):
    latest_stories = []
    if html_content:
        # Find all occurrences of the pattern for story titles
        matches = re.findall(r'<h2 class="title">.*?</h2>', html_content, re.DOTALL)
        for match in matches[:6]:  # Considering only the first 6 matches
            # Extract story title by removing HTML tags
            title = re.sub(r'<.*?>', '', match).strip()
            latest_stories.append(title)
    return latest_stories

# Function to handle HTTP requests
def handle_request(request):
    if request.startswith('GET /getTimeStories HTTP/1.1'):
        html_content = fetch_html('https://time.com')
        latest_stories = extract_latest_stories(html_content)
        response_body = ', '.join(['"' + story + '"' for story in latest_stories])
        return f'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n[{response_body}]'
    else:
        return 'HTTP/1.1 404 Not Found\r\n\r\nPage Not Found'

# Main function to create a web server
def main():
    host = ''
    port = 8080

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()

        print(f'Server is listening on http://{host}:{port}')

        while True:
            conn, addr = s.accept()
            with conn:
                request = conn.recv(4096).decode()
                print(f'Request from {addr[0]}:{addr[1]}:\n{request}')
                response = handle_request(request)
                conn.sendall(response.encode())

if __name__ == '__main__':
    main()
