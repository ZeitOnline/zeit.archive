import zope.interface


class IArchiveIndex(zope.interface.Interface):
    """Represents a centerpage containing article teaser 
    of a previous volume."""

    def addTeaser():
        """Add a single teaser to an existing volume."""

    def removeTeaser():
        """Remove a single teaser from an existing volume."""
