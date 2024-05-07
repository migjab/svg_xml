import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import svgwrite

# Variáveis globais para armazenar entradas de cadeiras e grupos
chair_values = []
group_entries = []

def add_group_entries():
    global group_entries
    num_groups = int(num_main_groups_entry.get())
    group_entries = []
    for widget in group_entries_frame.winfo_children():
        widget.destroy()
    for i in range(num_groups):
        ttk.Label(group_entries_frame, text=f"Quantas cadeiras no setor {i+1}?").grid(row=8, column=i+1)
        entry = ttk.Entry(group_entries_frame)
        entry.grid(row=9, column=i+1)
        group_entries.append(entry)

def add_chair_entries():
    global chair_values
    chair_values = []
    for widget in chair_entries_frame.winfo_children():
        widget.destroy()
    for i in range(len(group_entries)):
        num_lines = int(group_entries[i].get())
        ttk.Label(chair_entries_frame, text=f"Fileiras do setor {i+1}").grid(row=0, column=i*3)
        chair_values.append([])
        for j in range(num_lines):
            if letters_var.get():  # Verificar se a opção de letras está selecionada
                chair_label = chr(65 + j)  # Convertendo índices em letras (A, B, C, ...)
            else:
                chair_label = str(j + 1)  # Mantendo a numeração padrão (1, 2, 3, ...)
            ttk.Label(chair_entries_frame, text=f"Fileira {chair_label}").grid(row=j+1, column=i*3)
            entry = ttk.Entry(chair_entries_frame)
            entry.grid(row=j+1, column=i*3+1)
            chair_values[i].append(entry)

def generate_svg():
    try:
        # Coletando os valores dos parâmetros de entrada
        width = int(width_entry.get())
        height = int(height_entry.get())
        ellipse_radius = int(ellipse_radius_entry.get())
        spacing = int(spacing_entry.get())
        num_main_groups = int(num_main_groups_entry.get())
        add_numbering = numbering_var.get()
        use_letters = letters_var.get()
        project_name = project_name_entry.get()

        # Inicializar o desenho SVG
        dwg = svgwrite.Drawing(f"{project_name}.svg", width=f"{width}px", height=f"{height}px")

        file_spacing = 0  # Inicialização do espaçamento vertical total
        current_line_label = "A"  # Inicialização da etiqueta da linha

        for class_index in range(1, num_main_groups + 1):
            # Solicitar quantidade de fileiras no setor atual
            num_lines_per_sub_group = int(group_entries[class_index-1].get())
            file_spacing += num_lines_per_sub_group * spacing  # Atualização do espaçamento vertical total
            
            class_label = f"cla_{class_index}"
            class_group = dwg.g(id=class_label)
            
            class_group_offset = (class_index - 1) * file_spacing  # Deslocamento vertical para o grupo atual
            
            for line_index in range(1, num_lines_per_sub_group + 1):
                if letters_var.get():  # Verificar se a opção de letras está selecionada
                    line_label = chr(65 + line_index - 1)  # Convertendo índices em letras (A, B, C, ...)
                else:
                    line_label = str(line_index)  # Mantendo a numeração padrão (1, 2, 3, ...)
                    
                line_group_label = f"fil_{class_index}_{line_label}"
                line_group = dwg.g(id=line_group_label)
                
                current_x = spacing
                
                # Coletar a quantidade de cadeiras na fileira atual
                num_ellipses_per_line = int(chair_values[class_index-1][line_index-1].get())
                
                for ellipse_index in range(1, num_ellipses_per_line + 1):
                    cx = current_x
                    cy = class_group_offset + spacing * (line_index - 1)
                    
                    ellipse = dwg.ellipse(center=(cx, cy), r=(ellipse_radius, ellipse_radius), fill="#71c837")
                    ellipse_id = f"cad_{class_index}_{line_label}_{ellipse_index}"
                    ellipse['id'] = ellipse_id
                    line_group.add(ellipse)
                    
                    if add_numbering:
                        # Adicionar numeração às cadeiras dentro da elipse
                        text = dwg.text(str(ellipse_index), insert=(cx, cy), font_size="10px", fill="#000000",
                                        text_anchor="middle", dy="3")
                        line_group.add(text)
                    
                    current_x += spacing
                
                class_group.add(line_group)
                current_line_label = chr(ord(current_line_label) + 1)  # Atualização da etiqueta da linha
            
            dwg.add(class_group)

        # Centralizar o desenho horizontalmente
        dwg.viewbox(-spacing, 0, width, file_spacing * num_main_groups)
        dwg.save()

        # Mensagem de sucesso
        messagebox.showinfo("Sucesso", f"Arquivo SVG '{project_name}.svg' criado com sucesso.")
    except ValueError:
        # Mensagem de erro se algum valor inserido não for um número

        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")


# Configuração da janela principal
root = tk.Tk()
root.title("Gerador cadeira individual")
#root.geometry("1200x800")
#root.iconbitmap('icone.ico')
root.geometry("+100+50")  # Posiciona a janela 100 pixels à direita e 50 pixels abaixo do canto superior esquerdo da tela




# Frame para os parâmetros de entrada
input_frame = ttk.Frame(root, padding="20")
input_frame.pack(fill=tk.BOTH, expand=True)

# Entradas para os parâmetros
ttk.Label(input_frame, text="Nome do Projeto:").grid(column=0, row=5)
project_name_entry = ttk.Entry(input_frame)
project_name_entry.grid(column=1, row=5)
project_name_entry.insert(0, "Teatro")

ttk.Label(input_frame, text="Largura do SVG:").grid(column=0, row=0)
width_entry = ttk.Entry(input_frame)
width_entry.grid(column=1, row=0)
width_entry.insert(0, "910")

ttk.Label(input_frame, text="Altura do SVG:").grid(column=0, row=1)
height_entry = ttk.Entry(input_frame)
height_entry.grid(column=1, row=1)
height_entry.insert(0, "800")

ttk.Label(input_frame, text="Tamanho da elipse:").grid(column=0, row=2)
ellipse_radius_entry = ttk.Entry(input_frame)
ellipse_radius_entry.grid(column=1, row=2)
ellipse_radius_entry.insert(0, "10")

ttk.Label(input_frame, text="Espaçamento entre as cadeiras:").grid(column=0, row=3)
spacing_entry = ttk.Entry(input_frame)
spacing_entry.grid(column=1, row=3)
spacing_entry.insert(0, "24")

ttk.Label(input_frame, text="Quantidade de setores:").grid(column=0, row=4)
num_main_groups_entry = ttk.Entry(input_frame)
num_main_groups_entry.grid(column=1, row=4)
num_main_groups_entry.insert(0, "1")

numbering_var = tk.BooleanVar()
numbering_checkbox = ttk.Checkbutton(input_frame, text="Adicionar numeração (texto) aos lugares ?", variable=numbering_var)
numbering_checkbox.grid(column=0, row=6)
3
letters_var = tk.BooleanVar()
letters_checkbox = ttk.Checkbutton(input_frame, text="A-Z ? Padrão: 1-99", variable=letters_var)
letters_checkbox.grid(column=0, row=7)

# Botão para adicionar entradas para cada setor
add_group_button = ttk.Button(input_frame, text="Adicionar Fileiras", command=add_group_entries)
add_group_button.grid(column=3, row=7)

# Frame para as entradas de cada setor
group_entries_frame = ttk.Frame(input_frame)
group_entries_frame.grid(column=3, row=9)

# Botão para adicionar entradas para quantidade de cadeiras por fileira
add_chair_button = ttk.Button(input_frame, text="Adicionar Cadeiras", command=add_chair_entries)
add_chair_button.grid(column=3, row=10)

# Frame para as entradas de quantidade de cadeiras por fileira
chair_entries_frame = ttk.Frame(input_frame)
chair_entries_frame.grid(column=3, row=11)

# Botão para gerar o SVG
generate_button = ttk.Button(input_frame, text="Gerar SVG", command=generate_svg)
generate_button.grid(column=6, row=5)

root.mainloop()
