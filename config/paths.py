from utils import ResourceLoader

resource_loader = ResourceLoader()
MUSIC_DIR = resource_loader.resources_dir.joinpath( 'audio/music' )

MUSIC_RECURSIVE_TREE = resource_loader.get_recursive_tree( MUSIC_DIR )
MUSICS = sorted( MUSIC_RECURSIVE_TREE['file'] )
