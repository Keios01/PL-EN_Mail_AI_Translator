from tkinter import *
from tkinter import messagebox, simpledialog
import openai
import pyperclip
import sys

# Ask user for API Key
user_api_key = simpledialog.askstring("OpenAi API Key", "Insert OpenAI API key:", show='*')
if user_api_key is None or user_api_key == "":
    sys.exit()
else:
    openai.api_key = user_api_key


# The code from OpenAI is responsible for translation.
def translate_mail(text):
    try:
        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Translate from polish to english: {text}",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.8,
        )

        translated_message = completions.choices[0].text
        return translated_message
    except Exception:
        messagebox.showerror("Error", "An error occurred during communication with OpenAI")
        root.destroy()
        return None


# Opens a new window with a new text prompt where the generated email appears.
def open_win(translation):
    # New window
    new_window = Toplevel(root)
    new_window.geometry("750x500")
    new_window.title("Generated")
    new_window.resizable(False, False)
    new_window.iconbitmap("mail_icon.ico")

    # Widgets
    generated_mail = translation
    mail_text_box = Text(new_window, height=20, width=66)
    mail_text_box.pack(expand=True)

    # Inserting the generated message
    mail_text_box.insert('end', "Hi %s \n %s \n Thanks in advance,\n %s" % (
        email_text_box.get("1.0", END), generated_mail, signature_text_box.get("1.0", END)))

    # More widgets
    mail_text_box.config(state='normal')
    mail_text_box.place(x=80, y=5)

    copy_button = Button(new_window, text="Copy", command=lambda: pyperclip.copy(mail_text_box.get("1.0", END)))
    copy_button.place(x=80, y=335)

    # End
    new_window.protocol("WM_DELETE_WINDOW", confirm_exit)


# Displays a prompt asking the user to close the program.
def confirm_exit():
    if messagebox.askyesno("Exit?", "Are you sure you want to exit?"):
        root.destroy()


# Code responsible for main window
root = Tk()

root.geometry("750x500")
root.title("AI Mail Translator")
root.config(bg='#ebebeb')
root.resizable(False, False)
root.iconbitmap("mail_icon.ico")

# Widgets
label = Label(root,
              text="Compose the message in Polish, include the recipient's name and mail content, then press Generate.",
              font=80, bg='#ebebeb')
label.place(relx=0.5, rely=0.05, anchor=CENTER)

email_addressee = 'Addressee'
email_text_box = Text(root, height=1, width=30)
email_text_box.pack(expand=False)
email_text_box.insert('end', email_addressee)
email_text_box.config(state='normal')
email_text_box.place(x=60, y=60)

content_message = 'Mail Contnet'
content_text_box = Text(root, height=15, width=70)
content_text_box.pack(expand=True)
content_text_box.insert('end', content_message)
content_text_box.config(state='normal')
content_text_box.place(x=60, y=90)

signature_message = "Your Signature"
signature_text_box = Text(root, height=1, width=30)
signature_text_box.pack(expand=False)
signature_text_box.insert('end', signature_message)
signature_text_box.config(state='normal')
signature_text_box.place(x=60, y=340)

button = Button(root, text="Generate", command=lambda: [open_win(translate_mail(content_text_box.get("1.0", END)))])
button.place(x=60, y=375)

# End
root.protocol("WM_DELETE_WINDOW", confirm_exit)
root.mainloop()
