# 🐼 barto.lomeu  
Um **encurtador de links** desenvolvido em **Python** com **Flask** e **Streamlit**, criado especialmente para um vídeo do canal [Codecon](https://www.youtube.com/@codecondev).

---

## 📌 Sobre o projeto  
O **barto.lomeu** é uma aplicação que permite transformar URLs longas em links curtos, simples e compartilháveis. Ele possui:  
- **Backend em Flask** para gerenciar e armazenar os links.  
- **Frontend em Streamlit** para uma interface simples e interativa.  
- **Banco de dados SQLite** para persistência dos dados.  

---

## 🚀 Tecnologias utilizadas  
- **Python 3.13**  
- **Flask 3.1.1**  
- **Streamlit 1.47.1**  
- **SQLite-utils 3.38**  
- **Requests 2.32.4**  
- **Streamlit Dynamic Filters 0.1.9**  
- **Python Dotenv 1.1.1**  
- **Validators 0.35.0**

---

## ⚙️ Instalação e Execução  

### 1️⃣ Clone o repositório  
```bash
git clone https://github.com/aliceborges/barto.lomeu.git
cd barto.lomeu
```

### 2️⃣ Crie e ative um ambiente virtual  
```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```

### 3️⃣ Instale as dependências  
```bash
pip install -r requirements.txt
```

---

## ▶️ Como executar  

Use o script principal para rodar backend e frontend juntos:

```bash
python main.py
```

- Backend Flask rodando em: http://localhost:80  
- Frontend Streamlit rodando em: http://localhost:8501

---

## ✅ Funcionalidades  
✔️ Encurtar URLs longas  
✔️ Redirecionamento para o link original  
✔️ Interface web simples e funcional  
✔️ Armazenamento em SQLite  

---

## 📺 Assista ao vídeo no canal  
Este projeto foi criado para um vídeo no canal **[Codecon](https://www.youtube.com/@codecondev)**.  
