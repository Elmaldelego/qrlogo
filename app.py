import streamlit as st
import qrcode
from PIL import Image, ImageFilter

def generate_qr_with_logo(link, logo_path=None, corner_color="black"):
    # Generar el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    # Personalizar colores del QR
    qr_image = qr.make_image(fill_color=corner_color, back_color="white").convert("RGB")

    if logo_path:
        try:
            # Cargar el logo
            logo = Image.open(logo_path).convert("RGBA")  # Asegura transparencia
            qr_width, qr_height = qr_image.size
            logo_size = int(qr_width * 0.2)  # El logo ocupará el 20% del QR
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
            
            # Aplicar filtro para suavizar la imagen del logo
            logo = logo.filter(ImageFilter.SMOOTH)
            
            # Fusionar el logo con el QR
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            qr_image.paste(logo, pos, mask=logo)
        except Exception as e:
            st.error(f"Error al agregar el logo: {e}")

    return qr_image

# Interfaz de Streamlit
st.title("Generador de Códigos QR con Logo")
st.write("Sube un logo opcional y genera un código QR para tu página.")

# Entrada del enlace
link = st.text_input("Ingresa el enlace de tu página:", "https://www.tupagina.com")

# Subir logo opcional
logo_file = st.file_uploader("Sube un logo (opcional):", type=["png", "jpg", "jpeg"])

# Lista desplegable para elegir color
corner_color = st.selectbox(
    "Selecciona el color de las esquinas del QR:",
    options=["black", "blue", "green", "red", "purple"]
)

if st.button("Generar QR"):
    if link:
        qr_image = generate_qr_with_logo(link, logo_path=logo_file, corner_color=corner_color)
        
        # Mostrar y permitir descarga del QR
        st.image(qr_image, caption="Tu código QR", use_container_width=True)
        qr_image.save("codigo_qr_con_logo.png")
        with open("codigo_qr_con_logo.png", "rb") as file:
            st.download_button(
                label="Descargar QR",
                data=file,
                file_name="codigo_qr_con_logo.png",
                mime="image/png",
            )
    else:
        st.error("Por favor, ingresa un enlace válido.")
