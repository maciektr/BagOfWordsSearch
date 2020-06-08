from .gather_pages import GatherPages
from .search_preproc import SearchPreprocessing


class PreprocessingManager:
    def __init__(self, app):
        print('Downloading sources:')
        sources = app.config.get('PAGES_SOURCE')
        folder = app.config.get('BASE_DIR') + '/' + app.config.get('PAGES_FOLDER')
        gather = GatherPages(folder)
        gather.load_from_sources(sources)

        print('Preprocessing sources:')
        search_proc = SearchPreprocessing(folder)
        search_proc.read_pages()
        print('Terms recognized: ', len(search_proc.get_all_terms()))
        print('Articles loaded: ', search_proc.n_articles_loaded())
        search_proc.approx_k = search_proc.n_articles_loaded()*13//100
        search_proc.get_matrix()
        app.search = search_proc.search
