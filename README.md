##### Covid Dashboard

O Objetivo desta ferramenta é coletar dados e promover análises pré configuradas dos dados da COVID-19, no Brasil.

------

###### Passo a passo instalação do projeto:

Obs.: Quando executar pela primeira vez usar o comando: 
````commandline
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migration
python manage.py runserver
````
Quando o serviço estiver rodando a chamada a API pode ser feita da seguinte forma:
- http://\<host\>/dashcovid/api/?country=brazil&end_date=20200612&state=PE&start_date=20200610

Obs.: Para executar os testes unitarios implementados: 
````commandline
python manage.py test --verbosity 3
````

Obs.: Para atualizar o requirements: 
````commandline
pip freeze > requirements.txt
````

--------
##### Principais dependencias
Fonte de dados: https://covid19-brazil-api-docs.now.sh/

