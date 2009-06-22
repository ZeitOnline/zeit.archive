import zope.interface


class IArchiveVolume(zope.interface.Interface):
    """Represents a centerpage containing article teaser 
    of a previous volume."""

    def rebuildVolume():
        """Rebuilds a page from scratch adding every article of this volume."""

    def addTeaser():
        """Add a single teaser to an existing volume."""

    def removeTeaser():
        """Remove a single teaser from an existing volume."""
