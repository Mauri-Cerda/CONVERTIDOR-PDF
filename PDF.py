import streamlit as st
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        if hasattr(self, 'document_title'):
            self.set_font(family='Arial', style='B', size=15)
            self.cell(w=0, h=10, txt=self.document_title, border=0, ln=1, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font(family='Arial', style='I', size=8)
        self.cell(w=0, h=10, txt=f'Pagina {self.page_no()}', border=0, ln=0, align='C')

    def chapter_title(self, title, font='Arial', size=14):
        self.set_font(font, style='B', size=size)
        self.cell(w=0, h=10, txt=title, border=0, ln=1, align='L')
        self.ln(10)

    def chapter_body(self, body, font='Arial', size=12):
        self.set_font(font, size=size)
        self.multi_cell(w=0, h=10, txt=body)
        self.ln()

def create_pdf(filename, document_title, author, chapters, image_path=None):
    pdf = PDF()
    pdf.document_title = document_title
    pdf.add_page()
    if author:
        pdf.set_author(author)

    if image_path:
        pdf.image(image_path, x=10, y=25, w=pdf.w - 20)
        pdf.ln(120)

    for chapter in chapters:
        title, body, font, size = chapter
        pdf.chapter_title(title, font, size)
        pdf.chapter_body(body, font, size)

    pdf.output(filename)

def main():
    st.title("Generador de PDF con Python")
    st.header("Configuracion del Documento")
    document_title = st.text_input("Titulo del Documento", "Titulo del Documento")
    author = st.text_input("Autor", "")
    uploaded_image = st.file_uploader("Sube una imagen para el documento (opcional)", type=["jpg", "png", "jpeg"])

    st.header("Capitulos del Documento")
    chapters = []
    chapter_count = st.number_input("Numero de Capitulos", min_value=1, max_value=10, value=1)

    for i in range(chapter_count):
        st.subheader(f"Capitulo {i + 1}")
        title = st.text_input(f"Titulo del Capitulo {i + 1}", f"Titulo del Capitulo {i + 1}")
        body = st.text_area(f"Cuerpo del Capitulo {i + 1}", f"Contenido del Capitulo {i + 1}")
        font = st.selectbox(f"Fuente del Capitulo {i + 1}", ['Arial', 'Courier', 'Times'])
        size = st.slider(f"Tamaño de Fuente del Capitulo {i + 1}", 8, 24, 12)
        chapters.append((title, body, font, size))

    if st.button("Generar PDF"):
        image_path = uploaded_image.name if uploaded_image else None
        if image_path:
            with open(image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())

        create_pdf(filename="archivo.pdf", document_title=document_title, author=author, chapters=chapters, image_path=image_path)

        with open("archivo.pdf", "rb") as pdf_file:
            PDFbyte = pdf_file.read()

        st.download_button(label="Descargar PDF", data=PDFbyte, file_name="archivo.pdf", mime='application/octet-stream')

        st.success("PDF generado exitosamente")

if __name__ == "__main__":
    main()
