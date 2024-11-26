import streamlit as st
import qrcode
from PIL import Image

def generate_qr_with_logo(link, logo_path=None):
    # Generar el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    if logo_path:
        try:
            # Cargar el logo
            logo = Image.open(logo_path)

            # Redimensionar el logo
            qr_width, qr_height = qr_image.size
            logo_size = int(qr_width * 0.2)  # El logo ocupará el 20% del QR
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

            # Fusionar el logo con el QR
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            qr_image.paste(logo, pos, mask=logo.convert("RGBA").split()[3])  # Usar transparencia
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

if st.button("Generar QR"):
    if link:
        qr_image = generate_qr_with_logo(link, logo_path=logo_file)
        
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
