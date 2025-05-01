from dataclasses import dataclass

@dataclass
class MessageContent:
    id_error: str               # Unique identifier for the error
    path: str                   # The URL path where the error occurred
    method: str                 # The HTTP method used (e.g., GET, POST)
    ip_address: str             # The IP address of the client
    user_agent: str             # The user agent string of the client
    error: str                  # Description of the error encountered
    description: str | None     # Description of the information
