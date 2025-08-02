
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import zipfile

st.set_page_config(page_title="Clarity Editor", layout="centered")

# Branding
st.image("https://raw.githubusercontent.com/openai/clarity-brand-assets/main/clarity_logo_banner.png", width=300)
st.title("✨ Clarity Editor")
st.markdown("**Create with Clarity. Share with Purpose.**")
st.markdown("---")

avatar = st.file_uploader("Upload avatar or image (JPG/PNG)", type=["jpg", "png"])
subtitle = st.text_area("Enter your clarity quote or subtitle")

if avatar and subtitle:
    image = Image.open(avatar).convert("RGBA")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    text_position = (20, image.height - 60)
    draw.text(text_position, subtitle, fill="white", font=font)

    # Add watermark (bottom-right corner)
    logo = Image.open("clarity_watermark.png").convert("RGBA")
    logo.thumbnail((100, 100))
    image.paste(logo, (image.width - logo.width - 10, image.height - logo.height - 10), logo)

    st.image(image, caption="🔍 Preview with Watermark", use_column_width=True)

    # Save PNG
    output = io.BytesIO()
    image.save(output, format="PNG")
    st.download_button("📥 Download Preview Image", output.getvalue(), file_name="clarity_preview.png")

    # Save Clarity Kit ZIP
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr("subtitle.txt", subtitle)
        output.seek(0)
        zip_file.writestr("clarity_preview.png", output.read())
    zip_buffer.seek(0)
    st.download_button("📦 Download Clarity Kit (.zip)", zip_buffer, file_name="clarity_kit.zip")
else:
    st.info("Upload an image and enter a quote to begin.")
