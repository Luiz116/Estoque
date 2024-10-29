<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <title>Previsão de Estoque</title>
</head>
<body>
    <div class="container mt-5">
        <h2 class="text-center">Sistema de Previsão de Estoque</h2>
        <form action="modelo.php" method="post" enctype="multipart/form-data">
            <div class="form-group">
                <label for="entradas">Selecionar entradas.csv:</label>
                <input type="file" class="form-control-file" id="entradas" name="entradas" required>
            </div>
            <div class="form-group">
                <label for="produtos">Selecionar produtos.csv:</label>
                <input type="file" class="form-control-file" id="produtos" name="produtos" required>
            </div>
            <div class="form-group">
                <label for="saidas">Selecionar saidas.csv:</label>
                <input type="file" class="form-control-file" id="saidas" name="saidas" required>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Enviar</button>
        </form>
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
