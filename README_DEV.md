# App-With-Flet - Versão Refatorada

## 🚀 Sistema de Gestão Comercial Modernizado

Este projeto foi completamente refatorado para usar as versões mais atuais das bibliotecas Python, mantendo o design original mas com melhor performance e compatibilidade.

## ✨ Principais Melhorias

- **SQLAlchemy 2.0+**: ORM moderno com SQLite para desenvolvimento
- **Flet 0.24+**: Framework GUI atualizado
- **Dependências Atualizadas**: Todas as bibliotecas nas versões mais recentes
- **Ambiente Virtual**: Configuração isolada e reprodutível
- **Banco SQLite**: Sem necessidade de MySQL para desenvolvimento

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Flet** - Interface gráfica moderna
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados local (desenvolvimento)
- **bcrypt** - Criptografia de senhas
- **Cryptography** - Criptografia de dados

## 📋 Funcionalidades

- ✅ **Autenticação de Usuário**: Sistema de login seguro
- ✅ **Gestão de Usuários**: Cadastro e controle de acesso
- ✅ **Gestão de Clientes**: Cadastro completo com endereços
- ✅ **Gestão de Produtos**: Controle de estoque e categorias
- ✅ **Gestão de Vendas**: Registro de vendas e produtos vendidos
- ✅ **Dashboard**: Relatórios e métricas do negócio
- ✅ **Interface Moderna**: Design responsivo e intuitivo

## 🚀 Instalação Rápida

### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd App-With-Flet
```

### 2. Crie e ative o ambiente virtual
```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
# Linux/Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

### 3. Execute o script de configuração
```bash
python setup_dev.py
```

Este script irá:
- ✅ Atualizar o pip
- ✅ Instalar todas as dependências
- ✅ Criar o banco SQLite
- ✅ Inserir dados de exemplo
- ✅ Verificar a instalação

### 4. Execute a aplicação
```bash
python main.py
```

## 🔑 Credenciais Padrão

- **Usuário**: `admin`
- **Senha**: `admin123`

## 📁 Estrutura do Projeto

```
App-With-Flet/
├── main.py                 # Ponto de entrada da aplicação
├── InfostoreApp.py         # Classe principal da aplicação
├── models.py               # Modelos SQLAlchemy
├── database_config.py      # Configuração do banco
├── Database.py            # Classes de acesso a dados
├── Config.py              # Configurações do sistema
├── setup_dev.py           # Script de configuração
├── init_db.py             # Script de inicialização do banco
├── requirements.txt       # Dependências atualizadas
├── .venv/                 # Ambiente virtual
├── infostore_dev.db       # Banco SQLite (criado automaticamente)
└── Screens/               # Imagens das telas
```

## 🔧 Configuração Avançada

### Banco de Dados

O sistema usa SQLite por padrão para desenvolvimento. O arquivo `infostore_dev.db` é criado automaticamente.

Para usar MySQL em produção:
1. Configure as credenciais no arquivo `data.bin`
2. Execute os scripts SQL em `database_scripts/`

### Personalização

- **Empresa**: Edite `Config.py` para alterar dados da empresa
- **Tema**: Modifique cores e estilos em `main.py`
- **Funcionalidades**: Adicione novas telas seguindo o padrão existente

## 🐛 Solução de Problemas

### Erro de Importação
```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### Banco Corrompido
```bash
# Deletar e recriar banco
rm infostore_dev.db
python init_db.py
```

### Problemas de Ambiente Virtual
```bash
# Recriar ambiente virtual
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
python setup_dev.py
```

## 📊 Versões das Principais Bibliotecas

- **Flet**: 0.24.0+
- **SQLAlchemy**: 2.0.23+
- **bcrypt**: 4.1.0+
- **cryptography**: 42.0.0+
- **Pillow**: 10.0.0+

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para dúvidas ou suporte:
- 📧 Email: helio.card@yahoo.com.br
- 🐛 Issues: Use a aba Issues do GitHub

---

**Desenvolvido com ❤️ usando Python e Flet**
