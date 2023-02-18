"""Convenience module for dealing with different OS."""

import platform


class Platform:
    """Clean way to identify platform OS."""
    MAC: str = "Darwin"
    WINDOWS: str = "Windows"
    LINUX: str = "Linux"

    @staticmethod
    def is_mac() -> bool:
        """True if running on Macintosh; otherwise False."""
        return platform.system() == Platform.MAC
    
    @staticmethod
    def is_windows() -> bool:
        """True if running on Windows; otherwise False."""
        return platform.system() == Platform.WINDOWS
    
    @staticmethod
    def is_linux() -> bool:
        """True if running on Linux; otherwise False."""
        return platform.system() == Platform.LINUX
