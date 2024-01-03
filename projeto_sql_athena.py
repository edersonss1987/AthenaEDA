# -*- coding: utf-8 -*-
"""ProjetoSQL.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zg1BTf-l10m1dfOZXPo96nmpZOWxniqp

## **Realização da atividade no links abaixo, além do notebook a disposição**

Link da atividade no kaggle [link](https://www.kaggle.com/code/edersonsantossilva/athena-aws)

Link da atividade no GitHub [link](https://github.com/edersonss1987/AthenaEDA/tree/main)

# **Athena AWS - Análise de Dados de Crédito no SQL**
*Esse notebook faz parte do meu portifólio pessoal.*

# Sobre os Dados:
Eles representam informações de clientes de um banco,onde trataremos o seu conjunto de informações no Athena **AWS**, essa base de dados foi particionada no bucket **"bucket-eder-projeto"**, no intuito de consumir menor volume de na *AWS*, contendo as seguintes colunas e seus tipos:
```sql
idade = idade do cliente
sexo = sexo do cliente (F ou M)
dependentes = número de dependentes do cliente
escolaridade = nível de escolaridade do clientes
salario_anual = faixa salarial do cliente
tipo_cartao = tipo de cartao do cliente
qtd_produtos = quantidade de produtos comprados nos últimos 12 meses
iteracoes_12m = quantidade de iterações/transacoes nos ultimos 12 meses
meses_inativo_12m = quantidade de meses que o cliente ficou inativo
limite_credito = limite de credito do cliente
valor_transacoes_12m = valor das transações dos ultimos 12 meses
qtd_transacoes_12m = quantidade de transacoes dos ultimos 12 meses

A tabela foi criada no AWS Athena junto com o S3 Bucket.
```
```sql
CREATE EXTERNAL TABLE IF NOT EXISTS default.credito (
  `idade` int,
  `sexo` string,
  `dependentes` int,
  `escolaridade` string,
  `estado_civil` string,
  `salario_anual` string,
  `tipo_cartao` string,
  `qtd_produtos` bigint,
  `iteracoes_12m` int,
  `meses_inativo_12m` int,
  `limite_credito` float,
  `valor_transacoes_12m` float,
  `qtd_transacoes_12m` int
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'serialization.format' = ',',
  'field.delim' = ','
) LOCATION 's3://bucket-eder-projeto/'
TBLPROPERTIES ('has_encrypted_data'='false');
```



# **Analise exploratótio dos Dados (EDA):**
# O que é (EDA)?
*Em inglês chamado de Exploratory Data Analysis (EDA)*, a **Análise Exploratória de Dados** é uma forma de abordagem usada para analisar e investigar dados.

**Quanto ao EDA**

**OBS:** Os dados aqui tratados, são apenas uma amostra.

1° Faremos uma Analise exploratória a fim de conher os dados, e pensar quais insigts podemos tirar a partir do mesmo.

**Query**
```sql
select * from credito limit 10;
```
Selecionando as 10 primeiras linhas da base de dados, apenas para conhecer nossas colunas e dados contidos em cada uma delas, assim já podemos nos questionar sobre quais informações podemos absorver, questionar e separar só o que fará sentido ao longo do processo.

![](https://github.com/edersonss1987/AthenaEDA/blob/main/tudo_limit10.png?raw=true)



*consulta da quantidade de linhas na nossa base de dados.*

**Query**

```sql
select count(*) from credito
```
*Saída*
![](https://github.com/edersonss1987/AthenaEDA/blob/main/total%20de%20linhas%20na%20consulta.png?raw=true)


**Query**

```sql
SELECT DISTINCT escolaridade FROM credito
```
Após consulta, conseguimos identificar qu existem informações de "Escolaridade não informada".

*Saída*
![](https://github.com/edersonss1987/AthenaEDA/blob/main/agregacao%20de%20total%20por%20escolaridade.png?raw=true)



**Verificano os tipos de dados que estão dispostos na nossa base de dados**

**Query:**
```sql
DESCRIBE credito
```
*Saída*

![](https://github.com/edersonss1987/AthenaEDA/blob/main/describ.png?raw=true)



*Verificando a quais são os valores distintos na tabela*

**Query**

```sql
SELECT DISTINCT tipo_cartao FROM credito
```
*Saída*

![](https://github.com/edersonss1987/AthenaEDA/blob/main/SELECT%20DISTINCT%20tipo_cartao%20FROM%20credito.png?raw=true)



A intenção dessa consulta é verificar o Tóp10, de maiores créditos concedidos a partir do sexo.

**Query**

```sql
select max(limite_credito) as limite_credito, escolaridade, tipo_cartao, sexo from credito
where escolaridade != 'na' and tipo_cartao != 'na'
group by escolaridade, tipo_cartao, sexo
order by limite_credito desc
limit 10
```
Saída

![](https://github.com/edersonss1987/AthenaEDA/blob/main/top10_credito.png?raw=true)



*Realizando uma consulta, para entender a relação entre tipo de cartão e escolaridade.*

**Query**

```sql
select count(tipo_cartao) as total_de_cartoes_por_escolaridade, escolaridade,tipo_cartao from credito
where tipo_cartao = 'platinum' or tipo_cartao = 'gold'
and escolaridade != 'na' and salario_anual != 'na'
group by tipo_cartao, escolaridade
order by tipo_cartao;
```
Saída

![](https://github.com/edersonss1987/AthenaEDA/blob/main/relacao_tipocartao_escolaridade.png?raw=true)

**Query**

```sql
select tipo_cartao, valor_transacoes_12m, qtd_transacoes_12m, limite_credito from credito
group by tipo_cartao, valor_transacoes_12m, qtd_transacoes_12m, limite_credito
order by qtd_transacoes_12m desc limit 10;
```

Saída

![](https://github.com/edersonss1987/AthenaEDA/blob/main/tipo%20de%20carta%20que%20mais%20movimenta.png?raw=true)



# **Conclusão baseada nas analises**

* 1° os maiores valores de créditos concedidos são para Homens

* 2º conforme analise, podemos identificar que escolaridade e tipo de cartão influenciam em uma tomada de decisão, quando se diz respeito ao tipo de  cartão, onde Platinum foi adquirido para uma pessoa com  mestrado e outro com doutorado.

* 3º O cartão que faz maiores movimentações e geraram maiores valores é do tipo Blue, ou seja, cartão que possuí menores privilégios e créditos,    giraram pouco mais que 4 MILHÕES, representando 96% de um total.

* 4° A escolaridade não influencia no limite do cartão.
"""