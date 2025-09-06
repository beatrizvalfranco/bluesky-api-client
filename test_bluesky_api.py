import pytest
from bluesky_api import get_client, get_post_data


def test_valid_handle():
    df = get_post_data('xxx123xxxkkk', get_client)
    assert df.empty, "Erro: perfil inexistente"

def test_active_handle():
    perfil = 'guiadosurf'
    handle = f"{perfil}.bsky.social"
    df = get_post_data(handle, get_client)
    assert len(df) > 0, f"Posts retornados: {len(df)}"
 
def test_handle_type():
    with pytest.raises(TypeError):
        get_post_data(12345, get_client)