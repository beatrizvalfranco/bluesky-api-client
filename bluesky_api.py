from atproto import Client
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega as variáveis do .env

login = os.getenv('BLUESKY_LOGIN')
password = os.getenv('BLUESKY_PASSWORD')

def get_client():
    client = Client()
    client.login(login, password)
    return client

def get_post_data(handle, get_client_func):
    if not isinstance(handle, str):
        raise TypeError("O handle deve ser uma string.")
    client = get_client_func()
    try: 
        posts = client.app.bsky.feed.get_author_feed({'actor': handle, 'limit': 50})
    except Exception as e:
        print(f"Erro ao obter dados para o perfil {handle}: {e}")
        return pd.DataFrame()
    
# Extrair dados
    dados = []
    for item in posts['feed']:
        post = item.post
        record = post.record
        dados.append({
            'data': record.created_at,
            'texto': record.text,
            'likes': post.like_count,
            'reposts': post.repost_count,
            'respostas': post.reply_count,
            'uri': post.uri,
            'cid': post.cid
        })


# Criar DataFrame
    df = pd.DataFrame(dados)
    return df

if __name__ == "__main__":
    perfil = input("Qual perfil você quer consultar?").strip()
    if not perfil:
        raise ValueError("Você precisa informar um perfil válido!")

    handle = f"{perfil}.bsky.social"

    df = get_post_data(handle, get_client)

    print(f"Dados coletados de @{handle}:")
    print(df.head())