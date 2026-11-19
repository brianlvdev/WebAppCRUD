from CRUD import *

def exibir_menu():
    print("\n" + "=" * 30)
    print("      SISTEMA DE CADASTRO")
    print("=" * 30)
    print("1 - Cadastrar Pessoa")
    print("2 - Listar Pessoas")
    print("3 - Atualizar Pessoa")
    print("4 - Excluir Pessoa")
    print("5 - Buscar por nome")
    print("0 - Sair")
    print("=" * 30)

def main():
    
    #cadastro_em_massa() # Execute apenas uma vez.
    
    if not criar_banco():
        print("Algum problema aconteceu ")
        raise SystemExit
    
    while True:
        exibir_menu()
        opcao = input("Escolha uma opcao: ").strip()
        
        match opcao:
            case "1":  # cadastrar pessoa
                
                sair = input("Deseja prosseguir? (s/n): ").strip().lower()
                if sair == 'n' or sair == 'nao':
                    continue 
                      
                if not Cadastrar_Pessoa():
                    print("\n ERROU *** Pressione [ENTER] para voltar...") 
                else:
                    print("\nPressione [ENTER] para voltar...")
            case "2":   # listar pessoa
                if not Listar_Pessoas():
                    print("\nPressione [ENTER] para voltar...")
                else:
                    print("\nPressione [ENTER] para voltar...")
            case "3":   # atualizar pessoa
                
                sair = input("Deseja prosseguir? (s/n): ").strip().lower()
                if sair == 'n' or sair == 'nao' or sair == 'N':
                    continue
                    
                if not Atualizar_Pessoa():
                    print("\nPressione [ENTER] para voltar...")
                else:
                    print("\nPressione [ENTER] para voltar...")    
                     
            case "4":   # excluir pesssoa
                
                sair = input("Deseja prosseguir? (s/n): ").strip().lower()
                if sair == 'n' or sair == 'nao' or sair == 'N':
                    continue
                    
                if not Excluir_Pessoa():
                    print("\nPressione [ENTER] para voltar...")
                else:
                    print("\nPressione [ENTER] para voltar...")
            case "5":   # buscar nome
                
                sair = input("Deseja prosseguir? (s/n): ").strip().lower()
                if sair == 'n' or sair == 'nao' or sair == 'N':
                    continue
                    
                if not Buscar_por_nome():
                    print("\nPressione [ENTER] para voltar...") 
                else:
                    print("\nPressione [ENTER] para voltar...")   
            case "0":   # sair
                print("\nEncerrando sistema..")
                break
            case _:
                print("\n[ERROR] Opcao invalida, escolha uma opcao valida.")
                print("\nPressione [ENTER] para continuar...")            
        input("")   
            
           

if __name__ == "__main__":
    main()