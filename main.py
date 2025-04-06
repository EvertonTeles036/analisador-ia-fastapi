
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTML Formulário com barra de progresso e notificações
html_form = """
<!DOCTYPE html>
<html lang='pt-BR'>
<head>
  <meta charset='UTF-8'>
  <title>Envio de Áudios</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 30px; }
    h1 { color: #444; }
    .progresso { width: 100%; background-color: #f3f3f3; border-radius: 10px; margin: 10px 0; display: none; }
    .barra { width: 0%; height: 20px; background-color: #4CAF50; border-radius: 10px; }
    .notificacao { margin-top: 10px; padding: 10px; border-radius: 5px; display: none; }
    .sucesso { background-color: #d4edda; color: #155724; }
    .erro { background-color: #f8d7da; color: #721c24; }
  </style>
</head>
<body>
  <h1>Envio Individual de Áudio</h1>
  <form id='form-individual' enctype='multipart/form-data'>
    <input type='file' name='arquivo' required>
    <button type='submit'>Enviar</button>
  </form>
  <div class='progresso'><div class='barra' id='barra-individual'></div></div>
  <div id='notificacao-individual' class='notificacao'></div>

  <hr>

  <h1>Envio Múltiplo de Áudios (até 50 arquivos)</h1>
  <form id='form-multiplo' enctype='multipart/form-data'>
    <input type='file' name='arquivos' multiple required>
    <button type='submit'>Enviar</button>
  </form>
  <div class='progresso'><div class='barra' id='barra-multipla'></div></div>
  <div id='notificacao-multipla' class='notificacao'></div>

  <script>
    async function enviarArquivo(formData, endpoint, barraId, notificacaoId) {
      const barra = document.getElementById(barraId);
      const notificacao = document.getElementById(notificacaoId);
      barra.style.width = "0%";
      barra.parentElement.style.display = "block";
      notificacao.style.display = "none";

      try {
        const resposta = await fetch(endpoint, {
          method: "POST",
          body: formData
        });

        for (let i = 0; i <= 100; i += 10) {
          await new Promise(resolve => setTimeout(resolve, 80));
          barra.style.width = i + "%";
        }

        const dados = await resposta.json();
        notificacao.style.display = "block";

        if (resposta.ok) {
          notificacao.className = "notificacao sucesso";
          let texto = "Transcrição realizada com sucesso!";
          if (dados.link_pdf) {
            texto += ` <a href="\${dados.link_pdf}" target="_blank">Baixar PDF</a>`;
          }
          notificacao.innerHTML = texto;
        } else {
          notificacao.className = "notificacao erro";
          notificacao.innerText = dados.detail || "Erro ao processar o arquivo.";
        }
      } catch (erro) {
        notificacao.style.display = "block";
        notificacao.className = "notificacao erro";
        notificacao.innerText = "Erro no envio: " + erro.message;
      } finally {
        barra.parentElement.style.display = "none";
      }
    }

    document.getElementById("form-individual").addEventListener("submit", function (e) {
      e.preventDefault();
      const formData = new FormData(this);
      enviarArquivo(formData, "/transcrever", "barra-individual", "notificacao-individual");
    });

    document.getElementById("form-multiplo").addEventListener("submit", function (e) {
      e.preventDefault();
      const arquivos = this.querySelector('input[name="arquivos"]').files;
      const formData = new FormData();

      if (arquivos.length > 50) {
        const notif = document.getElementById("notificacao-multipla");
        notif.style.display = "block";
        notif.className = "notificacao erro";
        notif.innerText = "Erro: limite de 50 arquivos excedido.";
        return;
      }

      for (let i = 0; i < arquivos.length; i++) {
        formData.append("arquivos", arquivos[i]);
      }

      enviarArquivo(formData, "/transcrever-multiplos", "barra-multipla", "notificacao-multipla");
    });
  </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def serve_form():
    return html_form
