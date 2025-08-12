# 📝 Simulados Online

Sistema web para criação e execução de simulados online desenvolvido em Django, permitindo que usuários criem questões, montem simulados personalizados e respondam a avaliações de forma interativa.

### Principais Características:
- 🎯 Criação de questões por assunto com alternativas múltiplas
- 📊 Sistema de pesos para questões em simulados
- 👥 Gestão de usuários com autenticação segura
- 🔍 Filtros avançados para busca de simulados
- 📱 Interface responsiva e amigável
- ⚡ Validações em tempo real
- 📄 Paginação otimizada

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão |
|------------|--------|
| **Python** | 3.10+ |
| **Django** | 5.2.5 |
| **SQLite** | - |
| **HTML5/CSS3** | - |
| **JavaScript** | ES6+ |
| **Bootstrap** | - |

## 📁 Estrutura do Projeto

```
projsimulado/
├── manage.py                    # Script principal do Django
├── db.sqlite3                   # Banco de dados SQLite
├── projsimulado/               # Configurações do projeto
│   ├── __init__.py
│   ├── settings.py             # Configurações principais
│   ├── urls.py                 # URLs principais
│   ├── wsgi.py                 # Configuração WSGI
│   └── asgi.py                 # Configuração ASGI
└── simulado/                   # App principal
    ├── models.py               # Modelos de dados
    ├── admin.py                # Interface admin
    ├── forms.py                # Formulários
    ├── urls.py                 # URLs do app
    ├── utils.py                # Utilitários
    ├── migrations/             # Migrações do banco
    ├── services/               # Casos de uso/Serviços
    │   ├── casousousuario.py   # Lógica de usuários
    │   ├── casousoquestao.py   # Lógica de questões
    │   └── casousosimulado.py  # Lógica de simulados
    ├── views/                  # Views organizadas
    │   ├── index.py            # Página inicial
    │   ├── usuarios.py         # Views de usuários
    │   ├── questao.py          # Views de questões
    │   └── simulados.py        # Views de simulados
    ├── templates/              # Templates HTML
    │   └── simulado/
    ├── static/                 # Arquivos estáticos
    │   ├── css/                # Estilos
    │   └── js/                 # Scripts JavaScript
    └── templatetags/           # Tags customizadas
        └── pagination_tags.py  # Tags de paginação
```

### 🗃️ Modelos de Dados

- **Usuario**: Extensão do User do Django com nome personalizado
- **Questao**: Questões com enunciado, assunto e validações
- **Alternativa**: Alternativas das questões com flag de correta
- **Simulado**: Simulados temáticos com data de criação
- **Peso**: Relacionamento entre questões e simulados

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

### 1. Clone o repositório
```bash
git clone https://github.com/fonseca-plx/Simulados-Online.git
cd Simulados-Online
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv

# No Linux/Mac:
source venv/bin/activate

# No Windows:
venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados
```bash
cd projsimulado
python manage.py makemigrations
python manage.py migrate
```

### 5. Crie um superusuário (opcional)
```bash
python manage.py createsuperuser
```

### 6. Execute o servidor
```bash
python manage.py runserver
```

### 7. Acesse a aplicação
Abra seu navegador e acesse: `http://127.0.0.1:8000`

## 🤝 Contribuições

Contribuições são sempre bem-vindas! Para colaborar com o projeto:

### 🌟 Como Contribuir

1. **Faça um Fork do projeto**
   ```bash
   # Clique em "Fork" no GitHub
   ```

2. **Clone seu fork**
   ```bash
   git clone https://github.com/seu-usuario/Simulados-Online.git
   cd Simulados-Online
   ```

3. **Crie uma branch para sua feature**
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```

4. **Faça suas alterações e commit**
   ```bash
   git add .
   git commit -m "feat: adiciona nova funcionalidade"
   ```

5. **Push para sua branch**
   ```bash
   git push origin feature/nova-funcionalidade
   ```

6. **Abra um Pull Request**

### 📋 Diretrizes de Contribuição

- **Código**: Siga as convenções PEP 8 para Python
- **Commits**: Use conventional commits (feat, fix, docs, etc.)
- **Testes**: Adicione testes para novas funcionalidades
- **Documentação**: Atualize a documentação quando necessário

### 🐛 Reportando Bugs

1. Verifique se o bug já foi reportado nas [Issues](https://github.com/fonseca-plx/Simulados-Online/issues)
2. Crie uma nova issue com:
   - Descrição clara do problema
   - Passos para reproduzir
   - Comportamento esperado vs atual
   - Screenshots (se aplicável)

### 💡 Sugerindo Melhorias

- Abra uma issue com a tag "enhancement"
- Descreva claramente a melhoria proposta
- Explique por que seria útil para o projeto

### 🎯 Áreas para Contribuição

Veja [AQUI](docs/FEATURES.md)

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Pedro Fonseca** - [@fonseca-plx](https://github.com/fonseca-plx)

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no GitHub!
