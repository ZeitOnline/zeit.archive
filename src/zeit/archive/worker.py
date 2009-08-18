import sys
import gocept.runner
import zeit.archive.interfaces
import zeit.archive.index


@gocept.runner.once(principal="zope.archiveindexbuilder")
def build_main():
    url = sys.argv[1]
    zeit.archive.index.rebuildVolume(url)

