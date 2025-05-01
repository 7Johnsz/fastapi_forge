def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
    return f"{size_bytes:.2f} GB"