from .gather_pages import GatherPages


class PreprocessingManager:
    def __init__(self, app):
        sources = app.config.get('PAGES_SOURCE')
        GatherPages.folder = app.config.get('BASE_DIR') + '/' + app.config.get('PAGES_FOLDER')
        gather = GatherPages()
        gather.load_from_sources(sources)

