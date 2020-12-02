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

