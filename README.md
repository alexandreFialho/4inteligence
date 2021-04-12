## Execute o seguinte comando na raiz do projeto 
```./compose.sh```

## Execute o seguinte comando para rodar os tests
```./compose.sh exec backend poetry run pytest -rP -vv```

### Para acessar a interface da api via swagger, basta digitar o ip esternalizado do docker caso sua máquina seja mac/windows ou o ip local se for linux.
A aplicação esta levantada na porta ```8002``` e a documentação esta apontada no end-point raiz da aplicação 
