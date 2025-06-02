
# Projeto Precinho 🏷️  
**Comparador de preços online entre diferentes lojas brasileiras.**

---

## 📌 Sobre o Projeto

O **Projeto Precinho** é uma plataforma desenvolvida para ajudar consumidores a **comparar preços de produtos entre lojas online brasileiras de forma automatizada**.  

Idealizado e desenvolvido por dois estudantes — um com foco em **RPA e Automação** e o outro em **Ciência de Dados** — o projeto combina **web scraping, uso de APIs, banco de dados relacional** e **visualização interativa de informações**.

A nova versão substitui os arquivos JSON por um banco de dados **PostgreSQL**, garantindo maior **persistência, escalabilidade e integridade dos dados**. Também foi implementado um scraper mais eficiente para a KaBuM, agora baseado diretamente em sua **API pública**.

---

## 🚦 Status do Projeto

🟡 **Em desenvolvimento**  
- [x] Definição do escopo  
- [x] Estrutura inicial de diretórios  
- [x] Substituição de JSON por banco PostgreSQL  
- [x] Implementação de coleta via API (KaBuM)  
- [ ] Scrapers para outras lojas (Amazon, Magalu, etc.)  
- [ ] Interface com Streamlit para visualização  
- [ ] Lógica de comparação de preços  
- [ ] Deploy da aplicação (Docker + Streamlit Cloud)

---

## 🧱 Estrutura Atual do Projeto

```bash
Precinho/
├── interface/
│   └── app.py               # Interface principal (Streamlit)
│
├── scraping/
│   ├── kabum.py             # Coletor da KaBuM via API
│   └── amazon.py            # Em desenvolvimento (scraping)
│
├── database/
│   ├── db.py                # Conexão e funções auxiliares para PostgreSQL
│   └── models.sql           # Scripts de criação de tabelas
│
├── shared/
│   └── utils.py             # Funções de formatação, limpeza etc.
│
├── assets/                  # Logos, ícones e imagens (opcional)
├── export/                  # Exportações futuras (CSV, Excel)
├── config/
│   └── streamlit.config     # Configurações visuais e gerais
│
├── README.md                # Este arquivo :)
├── LICENSE                  # Licença MIT
├── requirements.txt         # Dependências do projeto
```

---

## 🔄 Principais Atualizações

- 📦 **Migração de JSON para PostgreSQL**  
  Agora os dados de preços são armazenados diretamente no banco de dados, facilitando consultas e análises posteriores.

- ⚙️ **Scraper da KaBuM via API Pública**  
  O coletor foi refeito utilizando a API oficial da KaBuM, tornando a coleta mais rápida e confiável, além de reduzir riscos de bloqueio.

- 🧠 **Planejamento da Interface com Streamlit**  
  A visualização dos preços será feita por meio de gráficos e filtros interativos, com atualização em tempo real a partir do banco de dados.

---

## 👨‍💻 Colaboradores

- **Jonatha** – RPA, Automação e Desenvolvimento da Interface  
- **Wollace** – Coleta de Dados (Scraping) e Análise

---

## 📄 Licença

Este projeto está licenciado sob os termos da **MIT License**.  
Veja mais no arquivo [`LICENSE`](LICENSE).
