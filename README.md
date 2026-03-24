# Gerenciador de Ingressos

## Descrição
Um sistema de gerenciamento de ingressos que permite aos usuários comprar e gerenciar ingressos para eventos de forma eficiente, aproveitando as últimas tecnologias disponíveis.

## Recursos
- Compra de ingressos online
- Confirmação de pagamento via Stripe
- Interface responsiva utilizando Bootstrap 5
- Dashboard para usuários e administradores

## Tecnologias
- Django 5.2.7
- Bootstrap 5
- Asaas API para pagamentos

## Instruções de Instalação
1. Clone este repositório:
   ```bash
   git clone https://github.com/WaldembergDev/gerenciador-ingressos.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd gerenciador-ingressos
   ```
3. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   ```
4. Ative o ambiente virtual:
   - No Windows:
   ```bash
   venv\Scripts\activate
   ```
   - No macOS/Linux:
   ```bash
   source venv/bin/activate
   ```
5. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Uso
- Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```
- Acesse o sistema em seu navegador através do endereço `http://127.0.0.1:8000/`.

## Estrutura do Projeto
```
gerenciador_ingressos/
├── manage.py
├── gerenciador_ingressos/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── app_inicial/
│   ├── models.py
│   ├── views.py
│   └── templates/
└── static/
```

## Visão Geral das Dependências
- **Django**: Framework web de alto nível que promove o desenvolvimento rápido.
- **Asaas**: Solução de pagamento que fornece a capacidade de realizar transações de forma segura.

## Diretrizes de Contribuição
1. Faça o fork do projeto
2. Crie um branch para a sua feature:
   ```bash
   git checkout -b minha-feature
   ```
3. Faça commit das suas alterações:
   ```bash
   git commit -m 'Adiciona minha feature'
   ```
4. Envie para o branch:
   ```bash
   git push origin minha-feature
   ```
5. Abra um Pull Request.

## Licença
Este projeto é licenciado sob a Licença MIT. Consulte o arquivo LICENSE para mais detalhes.