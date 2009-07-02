import zeit.archive.interfaces


def build_main():
    url = sys.argv[1]
    zeit.archive.volume.rebuildVolume(url)

