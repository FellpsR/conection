<h1 align="center">Conection Finance</h1>

## Descrição do Projeto

A solução basicamente funciona sendo aplicação em Python que utiliza o framework Flask para criar uma aplicação web. A aplicação tem um formulário que aceita datas de início e fim, e um tipo de consulta. Os dados inseridos no formulário são utilizados para fazer consultas em um banco de dados PostgreSQL. Os resultados das consultas são então processados e inseridos ou atualizados em outra tabela do banco de dados. Assim, com as "planilhas" de dados na tabela do BD Finance, ocorrerá uma comparação entre as duas em campos específicos, resultando na conciliação dos valores retornados anteriormente às tabelas. A solução terá validações de data, número de controle externo, protocolo ONR, duplicidade de lançamento, etc.


✅ Badges
![Static Badge](https://img.shields.io/badge/release-v0.0.1-blue)


✅ Tabela de Conteúdos
=================
<!--ts-->
   * [Sobre](#Sobre)
   * [Tabela de Conteudo](#tabela-de-conteudo)
   * [Instalação](#instalacao)
   * [Como usar](#como-usar)
      * [Pre Requisitos](#pre-requisitos)
      * [Local files](#local-files)
      * [Remote files](#remote-files)
      * [Multiple files](#multiple-files)
      * [Combo](#combo)
   * [Tests](#testes)
   * [Tecnologias](#tecnologias)
<!--te-->

✅ Instalação

✅ Pre Requisitos

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas:
[Git](https://git-scm.com).
[Python](https://www.python.org/downloads/).
Além disto é bom ter um editor para trabalhar com o código como [VSCode](https://code.visualstudio.com/)

### 🎲 Rodando o Back End (servidor)

```bash
# Clone este repositório
$ git clone <https://github.com/FellpsR/conection>

# Acesse a pasta do projeto no terminal/cmd
$ cd conection

# Vá para a pasta server
$ cd server

# Instale os pacotes:
$ pip install flask
$ pip install python-decouple
$ pip install flask_sqlalchemy
$ pip install psycopg2
$ pip install alembic
$ pip install pandas
$ pip install python-dotenv

# Crie a base finance no SGBD de escolha, no caso é o PostgreSQL:
$ sudo -u postgres psql postgres
$ create database finance; ## ou nome que desejar


# O servidor inciará na porta:5000 - acesse <http://localhost:5000/consulta>

##

```

✅ Tecnologias

As seguintes ferramentas foram utilizadas neste projeto:

-[Python] (https://www.python.org/)
-[CSS] (https://css3.com/about/)
-[PostgreSQL] (https://www.postgresql.org/)

✅ Contribuições

<table>
  <tr>
    <td align="center"><a href="https://github.com/FellpsR"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/149281400" width="100px;" alt=""/><br /><sub><b>Felipe "Fellps" Rodrigues</b></sub></a><br /><a href="https://github.com/FellpsR" title="Rocketseat">👨‍🚀</a></td>
    <td align="center"><a href="https://github.com/michael-rafael"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/22911710?v=4" width="100px;" alt=""/><br /><sub><b>Michael Rafael</b></sub></a><br /><a href="https://github.com/michael-rafael" title="Rocketseat">👨‍🚀</a></td>
    <td align="center"><a href="https://github.com/fejunior"><img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/57399312" width="100px;" alt=""/><br /><sub><b>Fernando "Junonn" Junior</b></sub></a><br /><a href="https://github.com/fejunior" title="Rocketseat">👨‍🚀</a></td>
  </tr>
</table>

✅ Licença

MIT License

Copyright (c) <2020> <Fellps>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.