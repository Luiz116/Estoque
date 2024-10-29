<?php
// Script Python
$entradas_path = 'caminho/para/entradas.csv';
$produtos_path = 'caminho/para/produtos.csv';
$saidas_path = 'caminho/para/saidas.csv';
exec("python modelo.py $entradas_path $produtos_path $saidas_path");

// Resultados do arquivo
$resultados = file_get_contents('resultados.txt');

// Exibir resultados
echo "<h2>Resultados da Previsão de Estoque</h2>";
echo "<pre>$resultados</pre>";

// Exibir gráfico
echo "<h3>Gráfico de Previsões vs Valores Reais:</h3>";
echo "<img src='previsoes_vs_reais.png' class='img-fluid' alt='Gráfico'>";
