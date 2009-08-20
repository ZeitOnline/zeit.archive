import zope.interface


class IArchiveIndex(zope.interface.Interface):
    """Represents a centerpage containing article teaser 
    for the print archive."""

    def addTeaser():
        """Add a single teaser to an existing volume."""

    def removeTeaser():
        """Remove a single teaser from an existing volume."""


class IArchiveVolume(zope.interface.Interface):
    """Represents an archive volume index."""


class IArchiveYear(zope.interface.Interface):
    """Represents an archive year index."""
