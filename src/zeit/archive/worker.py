import sys
import gocept.runner
import zeit.archive.interfaces
import zeit.archive.volume


@gocept.runner.once()
def build_main():
    url = sys.argv[1]
    zeit.archive.volume.rebuildVolume(url)

