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

    # Leitura do PDF a partir de uma página específica
    def ler_pdf(self, caminho_pdf, pagina_inicio):
        try:
            pdf = PdfReader(caminho_pdf)
            numero_de_paginas = len(pdf.pages)
            print(f'O PDF possui {numero_de_paginas} páginas.')
            print("\nAlguarde, leitura iniciada...")

            if pagina_inicio < 1 or pagina_inicio > numero_de_paginas:
                print("Número de página inválido.")
                return None

            texto = []

            # Extraindo texto a partir da página especificada
            for i in range(pagina_inicio - 1,numero_de_paginas):
                texto.append(pdf.pages[i].extract_text())
        
            return texto

        except Exception as e:
            print(f"Erro ao ler o PDF: {str(e)}")
            return None

    # Função de geração de voz
    def gerar_voz(self, texto):
        try:
            set_api_key(">>>>>>>>SUA API KEY<<<<<<<<<<<<<<")  # Substitua pela sua chave da ElevenLab
            
            num_caracteres_por_request = 200  #numero de caracteres para o request
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

    # Se obteve o caminho, solicitar a página de início
    if caminho_do_pdf:
        pdf = PdfReader(caminho_do_pdf)
        numero_de_paginas = len(pdf.pages)
        pagina_inicio = int(input(f'Digite o número da página de início (1-{numero_de_paginas}): '))
        texto_das_paginas = painel.ler_pdf(caminho_do_pdf, pagina_inicio)

    # Recebe o texto das páginas e dá um join
    if texto_das_paginas:
        texto_completo = "\n".join(texto_das_paginas)

        #gera o texto em 200 caracteres 
        painel.gerar_voz(texto_completo)

