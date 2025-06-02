import time
from datetime import datetime, date
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, ForeignKey, select, and_
from sqlalchemy.orm import sessionmaker
from concurrent.futures import ThreadPoolExecutor
import logging
import requests
from unidecode import unidecode

# Função auxiliar para gerar o slug da URL

def normalize_title_to_link(title):
    return unidecode(title.lower().replace(' ', '-').replace('/', '-'))

# Configuração de logs
logging.basicConfig(
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

# Banco de dados PostgreSQL
engine = create_engine("postgresql+psycopg2://postgres:abc%401234@localhost:5432/kabum")
metadata = MetaData()

produtos = Table("produtos", metadata,
    Column("id", Integer, primary_key=True),
    Column("nome", String),
    Column("url", String, unique=True),
    Column("imagem", String),
    Column("categoria", String),
)
precos = Table("precos", metadata,
    Column("id", Integer, primary_key=True),
    Column("produto_id", Integer, ForeignKey("produtos.id")),
    Column("preco", Float),
    Column("data_coleta", DateTime),
)
metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Função que obtém todas as categorias disponíveis na API pública da KaBuM
API_CATEGORIAS_URL = "https://servicespub.prod.api.aws.grupokabum.com.br/marketplace/category/v1/tree"

def obter_categorias():
    return []  # substituída por lista fixa no

def processar_categoria(categoria_url):
    session = Session()
    slug = categoria_url.strip("/").split("/")[-1]
    logging.info(f"Iniciando coleta da categoria: {slug}")

    base_api = f"https://servicespub.prod.api.aws.grupokabum.com.br/catalog/v2/products-by-category/{slug}"

    try:
        resp = requests.get(f"{base_api}?page_number=1&page_size=100")
        resp.raise_for_status()
        total_pages = resp.json()["meta"]["total_pages_count"]
    except Exception as e:
        logging.error(f"Erro ao acessar API da categoria {slug}: {e}")
        session.close()
        return

    for page in range(1, total_pages + 1):
        url = f"{base_api}?page_number={page}&page_size=100"
        try:
            response = requests.get(url)
            response.raise_for_status()
            produtos_api = response.json()["data"]

            for item in produtos_api:
                try:
                    attr = item["attributes"]
                    nome = attr["title"]
                    preco = attr["price_with_discount"]
                    id_produto = item["id"]
                    url_produto = f"https://www.kabum.com.br/produto/{id_produto}/{normalize_title_to_link(nome)}"
                    imagem = str(attr.get("photos", {}).get("g", ""))
                    data_coleta = datetime.now()

                    result = session.execute(select(produtos.c.id).where(produtos.c.url == url_produto)).first()
                    if result:
                        produto_id = result[0]
                    else:
                        res = session.execute(produtos.insert().values(nome=nome, url=url_produto, imagem=imagem, categoria=categoria_url))
                        session.flush()
                        produto_id = res.inserted_primary_key[0]
                        logging.info(f"Produto inserido: {nome}")

                    preco_ja_registrado = session.execute(
                        select(precos.c.id).where(
                            and_(
                                precos.c.produto_id == produto_id,
                                precos.c.data_coleta >= datetime.combine(date.today(), datetime.min.time())
                            )
                        )
                    ).first()

                    if not preco_ja_registrado:
                        session.execute(precos.insert().values(produto_id=produto_id, preco=preco, data_coleta=data_coleta))
                        logging.info(f"Preço registrado: {nome} - R$ {preco:.2f}")
                    else:
                        logging.debug(f"Preço já registrado hoje: {nome} - R$ {preco:.2f}")

                except Exception as e:
                    session.rollback()
                    logging.exception("Erro ao processar produto da API")

        except Exception as e:
            logging.error(f"Erro na requisição da página {page} da categoria {slug}: {e}")

        time.sleep(0.3)

    session.commit()
    session.close()
    logging.info(f"Finalizada coleta da categoria: {slug}")

def coletar_produtos():
    categorias = [
        "hardware", "perifericos", "gamer", "beleza-saude", "celular-smartphone", "informatica",
        "computadores", "seguranca", "eletroportateis", "ferramentas", "automacao", "brinquedos",
        "geek", "projetores", "conectividade", "tv", "audio", "eletrodomesticos", "beneficio",
        "bebes", "servicos-digitais", "tablets-ipads-e-e-readers", "telefonia-fixa", "energia",
        "escritorio", "espaco-gamer", "ar-e-ventilacao", "cameras-e-drones", "casa-inteligente",
        "moda", "robotica"
    ]
    categorias = [f"https://www.kabum.com.br/{slug}" for slug in categorias]

    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(processar_categoria, categorias)

    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(processar_categoria, categorias)

if __name__ == "__main__":
    try:
        coletar_produtos()
    except KeyboardInterrupt:
        logging.warning("Execução interrompida manualmente.")
