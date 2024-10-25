# Projeto: API Simples com Flask e Docker

## Descrição do Projeto

Este projeto é uma API RESTful simples desenvolvida em Python usando o framework Flask e containerizada com Docker. A API gerencia um recurso chamado "tarefas" (todos), permitindo operações CRUD (Create, Read, Update, Delete) para gerenciar as tarefas.

### Tecnologias Envolvidas

- **Python**: Uma linguagem de programação de alto nível, amplamente usada para desenvolvimento web, automação, análise de dados, entre outros.
- **Flask**: Um microframework para Python que facilita o desenvolvimento de aplicações web. É leve e permite que você crie APIs de forma rápida.
- **Docker**: Uma plataforma que permite a criação, implementação e execução de aplicações em containers. Os containers são unidades padrão de software que empacotam o código e todas as suas dependências, garantindo que a aplicação seja executada rapidamente e de forma confiável em diferentes ambientes.
- **Docker Compose**: Uma ferramenta para definir e executar aplicações Docker multi-container. Com o Docker Compose, você pode usar um arquivo YAML para configurar os serviços da sua aplicação.

---

## Estrutura do Projeto

A estrutura do projeto é a seguinte:

```
flask-docker-api/
│
├── app/
│   ├── __init__.py
│   ├── app.py
│   └── requirements.txt
│
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### Detalhamento dos Arquivos

1. **app/**: Diretório que contém o código da aplicação.

   - **`__init__.py`**: Este arquivo indica que a pasta `app` é um pacote Python. Embora neste projeto específico o arquivo esteja vazio, ele é necessário para que você possa importar o módulo `app` corretamente em outros arquivos.

   - **`app.py`**: Este é o arquivo principal da aplicação Flask. Ele contém a lógica para gerenciar as tarefas. Vamos descrever seu conteúdo:

     ```python
     from flask import Flask, jsonify, request

     app = Flask(__name__)

     tasks = []

     @app.route('/tasks', methods=['GET'])
     def get_tasks():
         return jsonify(tasks)

     @app.route('/tasks', methods=['POST'])
     def add_task():
         task = request.json
         tasks.append(task)
         return jsonify(task), 201

     @app.route('/tasks/<int:task_id>', methods=['PUT'])
     def update_task(task_id):
         task = next((t for t in tasks if t.get('id') == task_id), None)
         if task is None:
             return jsonify({'error': 'Task not found'}), 404
         updated_task = request.json
         task.update(updated_task)
         return jsonify(task)

     @app.route('/tasks/<int:task_id>', methods=['DELETE'])
     def delete_task(task_id):
         global tasks
         tasks = [t for t in tasks if t.get('id') != task_id]
         return jsonify({'result': 'Task deleted'})

     if __name__ == '__main__':
         app.run(host='0.0.0.0', port=5000)
     ```

     - **Importações**: A API importa as classes necessárias do Flask, incluindo `Flask`, `jsonify` e `request`.
     - **Instanciação do Flask**: `app = Flask(__name__)` cria uma nova aplicação Flask.
     - **Lista de Tarefas**: `tasks` é uma lista que armazena as tarefas (simulando um banco de dados).
     - **Rotas**:
       - `GET /tasks`: Retorna todas as tarefas.
       - `POST /tasks`: Adiciona uma nova tarefa à lista.
       - `PUT /tasks/<task_id>`: Atualiza uma tarefa existente com base no `task_id`.
       - `DELETE /tasks/<task_id>`: Remove uma tarefa com base no `task_id`.

   - **`requirements.txt`**: Este arquivo lista as dependências do projeto que o Python precisa instalar. Para este projeto, você precisa do Flask. O conteúdo do arquivo é:

     ```plaintext
     Flask==2.3.3
     ```

2. **`Dockerfile`**: Este arquivo contém as instruções necessárias para construir a imagem Docker da sua aplicação. Vamos analisar seu conteúdo:

   ```Dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY app/requirements.txt .

   RUN pip install --no-cache-dir -r requirements.txt

   COPY app/ .

   CMD ["python", "app.py"]
   ```

   - **FROM**: Especifica a imagem base a ser usada. Aqui, estamos usando uma versão leve do Python 3.9.
   - **WORKDIR**: Define o diretório de trabalho dentro do container como `/app`.
   - **COPY**: Copia o arquivo `requirements.txt` para o diretório de trabalho.
   - **RUN**: Executa o comando para instalar as dependências listadas em `requirements.txt`.
   - **COPY**: Copia todo o código da pasta `app` para o diretório de trabalho do container.
   - **CMD**: Define o comando padrão a ser executado quando o container é iniciado. Neste caso, inicia a aplicação Flask.

3. **`docker-compose.yml`**: Este arquivo define os serviços da sua aplicação Docker. O conteúdo é:

   ```yaml
   version: '3.8'

   services:
     flask-app:
       build: .
       ports:
         - "5000:5000"
       volumes:
         - ./app:/app
   ```

   - **version**: A versão do Docker Compose utilizada (opcional, pode ser removida).
   - **services**: Define os serviços que a aplicação irá utilizar.
   - **flask-app**: Nome do serviço.
     - **build**: Indica que o Docker deve construir a imagem a partir do Dockerfile no diretório atual (`.`).
     - **ports**: Mapeia a porta 5000 do container para a porta 5000 da máquina host, permitindo que você acesse a API através de `http://localhost:5000`.
     - **volumes**: Mapeia o diretório local `./app` para o diretório `/app` do container, permitindo que alterações feitas no código local sejam refletidas no container em tempo real.

### Como Executar o Projeto

1. **Instale o Docker:**
   - Se ainda não tiver o Docker instalado, siga as instruções específicas para seu sistema operacional (Windows, macOS ou Linux).

2. **Clone o Repositório:**
   - Clone o repositório do projeto em sua máquina local.

3. **Navegue até o Diretório do Projeto:**
   ```bash
   cd /caminho/para/seu/projeto/flask-docker-api
   ```

4. **Execute o Docker Compose:**
   - Execute o comando a seguir para construir a imagem e iniciar os serviços:
   ```bash
   docker-compose up --build
   ```

5. **Teste a API:**
   - Use uma ferramenta como Postman ou cURL para testar os endpoints:
     - **Obter todas as tarefas:**
       ```bash
       curl http://localhost:5000/tasks
       ```
     - **Adicionar uma nova tarefa:**
       ```bash
       curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d '{"id": 1, "title": "Tarefa 1"}'
       ```
     - **Atualizar uma tarefa existente:**
       ```bash
       curl -X PUT http://localhost:5000/tasks/1 -H "Content-Type: application/json" -d '{"title": "Tarefa Atualizada"}'
       ```
     - **Excluir uma tarefa:**
       ```bash
       curl -X DELETE http://localhost:5000/tasks/1
       ```

### Considerações Finais

Este projeto serve como uma boa base para entender como funcionam as APIs RESTful, o framework Flask e como usar o Docker para containerizar aplicações. Você pode expandir este projeto adicionando funcionalidades como persistência de dados usando um banco de dados (como SQLite ou PostgreSQL), autenticação de usuários, ou mesmo interface gráfica.