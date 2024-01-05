import fuse
import sqlite3
import os
import csv
import io
import sys

from fuse import FUSE, FuseOSError, Operations

class SQLiteFS(Operations):
    def __init__(self, db_path):
        # Connect to the SQLite database
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def getattr(self, path, fh=None):
        # Return directory attributes for '/' and file attributes for tables
        if path == '/':
            # Directory attributes
            return {'st_mode': (fuse.S_IFDIR | 0o555), 'st_nlink': 2}
        else:
            # File attributes, read-only
            return {'st_mode': (fuse.S_IFREG | 0o444), 'st_size': 0}

    def readdir(self, path, fh):
        # List all tables in the database as files
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return ['.', '..'] + [row[0] for row in self.cursor.fetchall()]

    def read(self, path, size, offset, fh):
        # Execute a SELECT query on the table and return results as CSV
        table_name = path.lstrip('/')
        query = f"SELECT * FROM {table_name};"
        self.cursor.execute(query)
        
        # Use StringIO to create a file-like object to write the CSV data
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerows(self.cursor.fetchall())
        
        # Read the requested part of the CSV
        output.seek(offset)
        return output.read(size)

    def open(self, path, flags):
        # Only allow reading (O_RDONLY)
        if flags & os.O_RDONLY != os.O_RDONLY:
            raise FuseOSError(fuse.EACCES)
        return 0

    def release(self, path, fh):
        # Nothing special to do here since we're not modifying the database
        return 0

if __name__ == "__main__":
    # Set the path to your SQLite database
    db_path = sys.argv[1]
    # Mount the filesystem
    fuse = FUSE(SQLiteFS(db_path), '/mnt/sqlite_fs', foreground=True, ro=True)

