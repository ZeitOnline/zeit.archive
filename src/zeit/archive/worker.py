import sys
import gocept.runner
import zeit.archive.interfaces
import zeit.archive.volume


@gocept.runner.once(principal="zope.volumebuilder")
def build_main():
    url = sys.argv[1]
    zeit.archive.volume.rebuildVolume(url)

