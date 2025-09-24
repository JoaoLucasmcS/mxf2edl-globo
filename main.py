from dotenv import load_dotenv
from utils.Logger import Logger
from workflow.get_streams import get_streams
from workflow.extract_streams import extrair_audio
import pymsgbox
import os


def main():
    logger = Logger()

    # Carrega variáveis de ambiente
    load_dotenv()
    arquivo_mxf = os.getenv("ARQUIVO_MXF")

    try:
        # Obter streams do arquivo MXF
        streams = get_streams(arquivo_mxf)

        if not streams:
            logger.registrar_erro("❌ Nenhum stream encontrado no arquivo MXF.")
            return

        logger.registrar_info(f"📊 Encontradas {len(streams)} streams no MXF.")

        # Processar apenas streams de áudio
        for stream in streams:
            if stream.get("codec_type") != "audio":
                continue

            indice = stream["index"]
            codec = stream["codec_name"]
            canais = stream.get("channels", "desconhecido")

            logger.registrar_info(
                f"\n🎤 Processando stream {indice} "
                f"({codec}, {canais} canais)..."
            )

            # Extrair áudio da stream
            wav_extraido = extrair_audio(indice, codec, canais)
            if not wav_extraido:
                logger.registrar_erro(f"Falha ao extrair stream {indice}")
                continue

    except Exception as e:
        logger.registrar_erro(f"❌ Erro inesperado: {e}")
        pymsgbox.alert("Erro ao tentar executar o processo.")
        return

    # Finalização
    logger.registrar_info("\n✅ Processamento concluído!")
    pymsgbox.alert("Processo finalizado com sucesso!")


if __name__ == "__main__":
    main()
