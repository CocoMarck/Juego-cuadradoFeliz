from utils import ResourceLoader

resource_loader = ResourceLoader()
MUSIC_DIR = resource_loader.resources_dir.joinpath( 'audio/music' )
SPRITES_DIR = resource_loader.resources_dir.joinpath( 'sprites' )

MUSIC_RECURSIVE_TREE = resource_loader.get_recursive_tree( MUSIC_DIR )
SPRITES_RECURSIVE_TREE = resource_loader.get_recursive_tree( SPRITES_DIR )

MUSICS = sorted( MUSIC_RECURSIVE_TREE['file'] )
SPRITES = sorted( SPRITES_RECURSIVE_TREE['file'] )
