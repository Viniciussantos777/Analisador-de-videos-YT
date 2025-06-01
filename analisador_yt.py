from pytubefix import YouTube
import os
import whisper
import google.generativeai as genai
# ~~~~~~~~~~~~~~~~~~~~~~~Imports~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# URL do vídeo que vai ser transcrito:
yt = YouTube(input('Coloque aqui a Url do vídeo do You Tube:'))
print(yt.title)
print("-" * 100)

genai.configure(api_key= input('Coloque aqui sua chave API do Gemini: '))
print("-" * 100)

# Pasta destino do áudio:
pasta_destino=os.path.join(os.getcwd(),'audios_vid')

# Download do áudio do vídeo:
print(f'Fazendo download do vídeo {yt.title}')
ys = yt.streams.get_audio_only()
ys.download(output_path=pasta_destino,filename='meu_audio.m4a')
print("-" * 100)

# Local do áudio na pasta:
caminho_audio = 'C:\\Users\\Vinícius Almeida\\OneDrive\\Área de Trabalho\\analisador_yt\\audios_vid\\meu_audio.m4a'

# Verifica se o arquivo existe
if not os.path.exists(caminho_audio):
    print(f"Arquivo '{caminho_audio}' não encontrado. Verifique o nome ou o caminho.")
else:
    try:
        print("Carregando modelo...")
        model = whisper.load_model("base")  # ou "small", "medium", "large"

        print("Transcrevendo áudio...")
        resultado = model.transcribe(caminho_audio, language='Portuguese')

        print("\n Transcrição concluída:")
        print("-" * 100)
        texto = resultado["text"]

    # Gerando resumo com Gemini
        print("\nGerando resumo com Gemini...")
        modelo_gemini = genai.GenerativeModel(model_name='models/gemini-1.5-pro')
        resposta = modelo_gemini.generate_content(f"Resuma o seguinte conteúdo em português:\n\n{texto}")

        print("\nResumo gerado pelo Gemini:\n")
        print(resposta.text)

        # Caminho para salvar o resumo em .txt
        caminho_resumo = os.path.join(os.getcwd(), 'resumo.txt')

        with open(caminho_resumo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(resposta.text)

        print(f"\nResumo do vídeo {yt.title} salvo em: {caminho_resumo}")


    except Exception as e:
        print(f"Erro ao transcrever ou resumir o áudio: {e}")
print("-" * 100)