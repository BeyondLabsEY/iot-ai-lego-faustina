# IOT AI Lego Boost Faustina

A equipe de engenharia do Wavespace elaborou uma prova de conceito de um robô assistente com Inteligência Artificial para controlar movimentos e ações do Lego Boost.
O robô que desenvolvemos se chama Faustina, pois durante o seu processo de desenvolvimento ela já interrompeu várias vezes os seus criadores enquanto eles estavam falando.

![](faustao.gif)

## Setup do robô

Nessa prova de conceito, utilizamos um kit Lego Boost conectado via bluetooth a um Raspberry Pi model 3.
Conectados ao Raspberry, colocamos uma caixa de som (entrada P2) e um microfone (entrada USB).

## Script

O script que controla o robô foi desenvolvido em Python 3, testado no Raspbian e Mac OS Mojave. Por conta dos drivers específicios, não garantimos o seu funcionamento em outros sistemas operacionais:

_Instalação do driver do portal audio_

Para Raspbian:

```sh
$ apt-get install portaudio19-dev
```

Para Mac OS:

```sh
$ brew install portaudio
```

_Instalação do ffmpeg_

Para Raspbian:

```sh
$ apt-get install ffmpeg
```

Para Mac OS:

```sh
$ brew install ffmpeg
```

_Instalação de bibliotecas a partir da pasta raiz do projeto_:

```sh
$ pip install -r requirements.txt
```

_Instalação da biblioteca de conexão com o Lego Boost_:

```sh
$ pip install https://github.com/undera/pylgbst/archive/0.10.tar.gz
```

_Configuração do Wit.ai_

Para a parte de Natural Language Understanding (NLU) da Faustina, estamos usando a biblioteca Wit.ai, desenvolvida pelo Facebook.
Acesse https://wit.ai, crie uma conta e um app a partir da pasta knowledge_base_backup, contida na raíz do projeto.
No final do processo de criação do app, será gerado um access token. Copie e cole-o no arquivo wit_client.py, no diretório raíz do projeto.

_Execução do script_

Antes de executar o script, verifique se o Lego Boost está ligado. Caso haja algum freezing na execução do código, provavelmente é devido a falta de conexão com o dispositivo. Nesse caso, verifique se ele não desligou automaticamente. Um indicativo de que o Lego Boost está conectado e operacional é uma luz azul no seu visor de cores.

Execute

```sh
$ python main.py
```

Em ambientes onde existem mais de uma vesão do Python, utilize os atalhos apropriados, por exemplo `pip3` e `python3`.


## Como interagir com a Faustina?

Para realizar perguntas a Faustina, espere que a luz verde seja exibida em seu visor de LED. Isso se dá, pois por simplicidade colocamos um intervalo de 5 segundos para a captura do áudio do usuário.


## Arquivos de voz e como evitar o delay na resposta

Para reduzir o delay entre uma pergunta realizada pelo usuário e a resposta em voz da faustina, criamos um mecanismo de cache de áudio, em que gravamos um arquivo por assunto que está cadastrado na base de conhecimento. Esses arquivos podem ser encontrados na pasta recordings, na raíz do projeto.

## Manutenção da base de conhecimento

O cadastro de novas intenções e entidades deve ser realizado no seu app do Wit.ai. Caso queira alterar algum texto da resposta, dirija-se ao arquivo knowledge_base.json.
Após a alteração da base de conhecimento ou da resposta, apague os arquivos da pasta recordings, pois isso forçará o serviço de TTS a gerar um novo áudio, já considerando a alteração feita.


## Indicativo de cores LED

| Cor  | Significado |
| ------------- | ------------- |
| Azul  | Conexão bluetooth com o Lego foi estabelecida com sucesso  |
| Branco  | Procurando conexões disponíveis  |
| Verde  | Robô está pronta para ouvir a pergunta do usuário  |
| Vermelho  | Robô está realizando algum processamento  |
| Amarelo  | Não foi identificado nenhuma pergunta  |


## Evoluções futuras

Em evoluções futuras, queremos que a Faustina seja capaz de realizar movimentos mais complexos e interagir com uma gama maior de dispositivos. Por exemplo, podemos acoplar uma webcam no Raspberry para realizar deteção facial e lembrar o nome da pessoa com quem a Faustina está falando.
Além disso, é oportuno melhorar o mecanismo de corte do áudio (hoje realizamos o corte a cada 5s). No futuro, podemos identificar o momento exato que o usuário parou de falar e realizar o corte do áudio. Podemos também testar outras ferramentas de NLU, TTS e STT visando fazer um benchmarking de assertividade das respostas.

