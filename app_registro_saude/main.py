from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from datetime import datetime

# Carregar o arquivo KV
Builder.load_file('app.kv')

class AppSaude(App):
    def build(self):
        # Criar a tela principal do aplicativo
        self.tela = Tela()

        # Carregar o histórico existente do arquivo
        self.carregar_historico()

        return self.tela

    def carregar_historico(self):
        try:
            # Tentar abrir o arquivo histórico para leitura
            with open('historico.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    # Ler cada linha do arquivo e dividir o timestamp e o registro
                    parts = line.strip().split('|')
                    if len(parts) == 2:
                        timestamp, registro = parts
                        # Criar labels para mostrar o timestamp e o registro
                        label_data = Label(text=timestamp, size_hint_y=None, height=30, font_size='20sp', color=(0.5, 0.5, 0.5, 1))
                        label_registro = Label(text=registro, size_hint_y=None, height=40, font_size='20sp')
                        
                        # Adicionar os labels ao layout de histórico na tela
                        self.tela.ids.layout_historico.add_widget(label_data)
                        self.tela.ids.layout_historico.add_widget(label_registro)
        except FileNotFoundError:
            pass  # Se o arquivo não existir, apenas continuar sem mostrar histórico
        except Exception as e:
            print(f'Erro ao carregar histórico: {e}')

    def salvar_registro(self, registro):
        # Função para salvar um novo registro no arquivo histórico
        try:
            with open('historico.txt', 'a', encoding='utf-8') as file:
                file.write(registro + '\n')
        except Exception as e:
            print(f'Erro ao salvar registro: {e}')

    def apagar_historico(self):
        # Função para apagar todo o conteúdo do arquivo histórico e limpar o layout de histórico na tela
        try:
            with open('historico.txt', 'w', encoding='utf-8') as file:
                file.truncate(0)  # Apagar o conteúdo do arquivo
            
            # Limpar widgets do layout de histórico na interface
            self.tela.ids.layout_historico.clear_widgets()
        except Exception as e:
            print(f'Erro ao apagar histórico: {e}')

class Tela(BoxLayout):
    def armazenar_dados(self):
        # Método para armazenar os dados de pressão arterial e glicemia
        pressao = self.ids.input_pressao.text
        glicemia = self.ids.input_glicemia.text
        
        if pressao and glicemia:
            try:
                # Obter timestamp atual
                timestamp = datetime.now().strftime('%d/%m/%Y - %H:%M')
                
                # Formatar registro com timestamp, pressão e glicemia
                registro = f'{timestamp} | Pressão: {pressao}  Glicemia: {glicemia}'
                
                # Salvar registro no arquivo e exibir na interface
                App.get_running_app().salvar_registro(registro)
                
                # Criar labels para mostrar os dados registrados
                label_data = Label(text=timestamp, size_hint_y=None, height=30, font_size='20sp', color=(0.5, 0.5, 0.5, 1))
                label_registro = Label(text=f'Pressão: {pressao}  Glicemia: {glicemia}', size_hint_y=None, height=40, font_size='20sp')
                
                # Adicionar labels ao layout de histórico na tela
                self.ids.layout_historico.add_widget(label_data)
                self.ids.layout_historico.add_widget(label_registro)
                
                # Limpar campos de entrada após registrar os dados
                self.ids.input_pressao.text = ''
                self.ids.input_glicemia.text = ''
            except Exception as e:
                print(f'Erro ao armazenar dados: {e}')

    def apagar_historico(self):
        # Método para chamar a função de apagar histórico no AppSaude
        App.get_running_app().apagar_historico()

# Executar o aplicativo
if __name__ == '__main__':
    AppSaude().run()
