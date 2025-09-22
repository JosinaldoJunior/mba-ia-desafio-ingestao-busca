from search import search_prompt
import sys

def main():

    print("🤖 Chat com IA - Sistema de Busca em Documentos 🤖")
    print("=" * 50)
    print("Digite suas perguntas sobre o documento.")
    print("Para sair, digite 'sair', 'quit' ou 'exit'")
    print("=" * 50)

    try:
        while True:
            # Solicitar pergunta do usuário
            user_input = input("\n❓ Sua pergunta: ").strip()
            
            # Verificar se o usuário quer sair
            if user_input.lower() in ['sair', 'quit', 'exit', 'q']:
                print("\n👋 Obrigado por usar o chat! Até logo!")
                break
            
            # Verificar se a pergunta não está vazia
            if not user_input:
                print("⚠️  Por favor, digite uma pergunta válida.")
                continue
            
            try:
                # Processar a pergunta usando a chain de busca
                print("\n🔍 Buscando informações...")
                response = search_prompt(user_input)

                if not response:
                    print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
                    return

                print("\n" + "-"*100)
                print(f"📝 PERGUNTA: {user_input}")
                print(f"🤖 RESPOSTA: " + response.content)
                print("-"*100)
                
            except Exception as e:
                print(f"\n❌ Erro ao processar sua pergunta: {e}")
                print("Tente novamente ou verifique se o sistema está configurado corretamente.")
                continue
                
    except KeyboardInterrupt:
        print("\n\n⚠️ Chat interrompido pelo usuário. Até logo!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()