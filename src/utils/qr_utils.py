import logging
from typing import Optional

import cv2
import qrcode

logger = logging.getLogger(__name__)


def print_qr_to_terminal(image_path: str):
    """将二维码打印到终端
    Args:
        image_path(str): 图片路径
    """
    qr_content = decode_qr_from_image(image_path)

    print("\n" + "=" * 50)
    print("  请使用微信扫描下方二维码")
    print("=" * 50)
    print()

    if qr_content:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=2,
            border=2,
        )
        qr.add_data(qr_content)
        qr.make(fit=True)
        qr.print_ascii(invert=True)

        print()
        print("=" * 50)
        print(f"  二维码内容: {qr_content}")
        print("=" * 50 + "\n")
    else:
        logger.warning("二维码解码失败")


def decode_qr_from_image(image_path: str) -> Optional[str]:
    """从图片中解码二维码内容
    Args:
        image_path (str): 图片路径

    Returns:
        Optional[str]: 解码成功的二维码内容，或None如果解码失败
    """
    img = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)
    return data if data else None
