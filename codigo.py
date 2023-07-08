import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

current_file = None  # Caminho do arquivo atualmente aberto
text_modified = False  # Indica se o texto foi modificado

def save_text():
    global current_file, text_modified
    if current_file:
        text = text_entry.get("1.0", "end-1c")  # Obtém o texto inserido
        if current_file.endswith(".ste"):
            encrypted_text = encrypt_text(text)  # Encripta o texto
            with open(current_file, "w") as file:
                file.write(encrypted_text)  # Salva o texto encriptado no arquivo
        else:
            with open(current_file, "w") as file:
                file.write(text)  # Salva o texto no arquivo
        text_modified = False
        messagebox.showinfo("Guardar", "Texto guardado com sucesso!")
    else:
        save_text_as()

def save_text_as():
    global current_file, text_modified
    text = text_entry.get("1.0", "end-1c")  # Obtém o texto inserido
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=(("Arquivos de Texto", "*.txt"),
                                                        ("Simple Text Editor", "*.ste")))
    # Abre a caixa de diálogo para selecionar o arquivo com tipos de arquivo permitidos
    if file_path:
        if file_path.endswith(".ste"):
            encrypted_text = encrypt_text(text)  # Encripta o texto
            with open(file_path, "w") as file:
                file.write(encrypted_text)  # Salva o texto encriptado no arquivo
        else:
            with open(file_path, "w") as file:
                file.write(text)  # Salva o texto no arquivo
        current_file = file_path
        text_modified = False
        messagebox.showinfo("Guardar Como", "Texto guardado com sucesso!")

def open_text():
    global current_file, text_modified
    if text_modified:
        answer = messagebox.askquestion("Guardar Alterações", "Você quer guardar este Ficheiro?")
        if answer == "yes":
            save_text()
        elif answer == "cancel":
            return
    file_path = filedialog.askopenfilename(filetypes=(("Arquivos de Texto", "*.txt"),
                                                      ("Simple Text Editor", "*.ste")))
    # Abre a caixa de diálogo para selecionar o arquivo a ser aberto
    if file_path:
        with open(file_path, "r") as file:
            if file_path.endswith(".ste"):
                encrypted_text = file.read()
                text = decrypt_text(encrypted_text)  # Desencripta o texto
            else:
                text = file.read()  # Lê o conteúdo do arquivo
            text_entry.delete("1.0", "end")  # Limpa o campo de entrada de texto
            text_entry.insert("1.0", text)  # Insere o conteúdo do arquivo no campo de entrada de texto
        current_file = file_path
        text_modified = False

def clear_text():
    global text_modified
    if text_modified:
        answer = messagebox.askquestion("Guardar Alterações", "Você quer guardar este Ficheiro?")
        if answer == "yes":
            save_text()
        elif answer == "cancel":
            return
    text_entry.delete("1.0", "end")  # Limpa o campo de entrada de texto
    text_modified = False

def text_changed(event):
    global text_modified
    text_modified = True

def show_about_window():
    about_window = tk.Toplevel(root)
    about_window.title("Sobre")
    about_window.resizable(False, False)
    
    # Texto com as informações do programa e versão
    program_name = "Simple Text Editor"
    program_version = "Versão: 0.1"
    os_version = platform.system()
    if os_version == "Windows":
        os_version = platform.win32_ver()[1]
    credits = "Créditos: ChatGPT e JogosGo"
    info_text = f"{program_name}\n\n{program_version}\n\nSistema Operacional: {os_version}\n\n{credits}"
    info_label = tk.Label(about_window, text=info_text)
    info_label.pack(padx=20, pady=20)

    # Botão "OK" para fechar a janela de sobre
    ok_button = tk.Button(about_window, text="OK", width=10, command=about_window.destroy)
    ok_button.pack(pady=10)

    about_window.mainloop()

def encrypt_text(text):
    encrypted_text = ""
    for char in text:
        encrypted_char = chr(ord(char) + 3)  # Desloca o caractere 3 posições para a frente na tabela ASCII
        encrypted_text += encrypted_char
    return encrypted_text

def decrypt_text(text):
    decrypted_text = ""
    for char in text:
        decrypted_char = chr(ord(char) - 3)  # Desloca o caractere 3 posições para trás na tabela ASCII
        decrypted_text += decrypted_char
    return decrypted_text

root = tk.Tk()
root.title("Simple Text Editor")

file_menu = tk.Menu(root, tearoff=False)
file_menu.add_command(label="Novo", command=clear_text)
file_menu.add_command(label="Guardar Como", command=save_text_as)
file_menu.add_command(label="Guardar", command=save_text)
file_menu.add_command(label="Abrir", command=open_text)

help_menu = tk.Menu(root, tearoff=False)
help_menu.add_command(label="Sobre", command=show_about_window)

menu = tk.Menu(root)
menu.add_cascade(label="Ficheiro", menu=file_menu)
menu.add_cascade(label="Ajuda", menu=help_menu)

root.config(menu=menu)

text_entry = tk.Text(root)
text_entry.pack(fill="both", expand=True)
text_entry.bind("<<Modified>>", text_changed)
text_entry.configure(font=("Segoe UI", 12))  # Define a fonte padrão do editor como a fonte do Notepad do Windows

root.mainloop()

