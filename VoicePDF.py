from elevenlabs import generate, play
import pyfiglet
import os.path
from PyPDF2 import PdfReader
from elevenlabs import set_api_key

# Estilo do painel
class Painel:

    def __init__(self):
        print("#" * 60)
        titulo = pyfiglet.figlet_format("VoicePDF", font="doom")
        print(titulo)
        print("#" * 60)

    # Recebe o caminho e verifica se o PDF existe
    def pdf(self):
        try:
            # Verifica o caminho
            caminho_pdf = input("Informe o caminho do PDF: ")
            if os.path.exists(caminho_pdf):
                return caminho_pdf
            
            else:
                print("\nDesculpa, arquivo não encontrado.")
                return None
        except:
            print(f"Erro")
            return None

    # Leitura do PDF
    def ler_pdf(self, caminho_pdf):
        try:
            pdf = PdfReader(caminho_pdf)
            numero_de_paginas = len(pdf.pages)
            print(f'O PDF possui {numero_de_paginas} páginas.')
            texto = []

            # Extraindo texto
            for pagina in pdf.pages:
                texto.append(pagina.extract_text())
            return texto

        except:
            print(f"Erro ao ler o PDF")
            return None

    # Função de geração de voz
    def gerar_voz(self, texto):
        try:
            set_api_key("SUA API KEY ELEVENLABS")  # Substitua pela sua chave da ElevenLab
            
            num_caracteres_por_request = 500
            inicio_caracter = 0
            fim_caracter = num_caracteres_por_request

            while inicio_caracter < len(texto):
                parte_texto = texto[inicio_caracter:fim_caracter]

                audio = generate(
                    text=parte_texto,
                    voice="Bella",
                    model="eleven_multilingual_v2"
                )
                play(audio)
                inicio_caracter = fim_caracter
    
                fim_caracter = min(fim_caracter + num_caracteres_por_request, len(texto))
        except:
            print(f"Erro ao gerar a voz:")


if __name__ == "__main__":
    painel = Painel()

    # Obter o caminho do PDF
    caminho_do_pdf = painel.pdf()

    #se obteve o caminho, texto das paginas recebe a função ler 
    if caminho_do_pdf:
        texto_das_paginas = painel.ler_pdf(caminho_do_pdf)

    #recebe o texto das paginas e da um join
    if texto_das_paginas:
        texto_completo = "\n".join(texto_das_paginas)

        # Processar o texto em partes de 500 caracteres por request, mas esta lento deve ser melhorado 
        painel.gerar_voz(texto_completo)

