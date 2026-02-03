import io
import qrcode


class QrService:
    @staticmethod
    def generate_qr_bytes(data: str) -> bytes:
        """
        Генерирует QR-код и возвращает изображение в виде bytes
        """
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer.getvalue()