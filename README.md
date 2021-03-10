## Execute o seguinte comando na raiz do projeto 
```docker-compose -f docker-compose.yml -f docker-compose-test.yml up --build -d```

Esse comando ira levantar os container da aplicação como também o container do banco para tests da aplicação

## Execute o seguinte comando para rodar os tests
```docker exec web_api pytest -rP -vv```

### Para acessar a interface da api via swagger, basta digitar o ip esternalizado do docker caso sua máquina seja mac ou ip local caso seja linux.
A aplicação esta levantada na porta ```8002``` e a documentação esta apontada no end-point raiz da aplicação 

### Para realizar qualquer requisição, informar o seguinte paramentro no header da solicitação
```x-token:coneofsilence```
