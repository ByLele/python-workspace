import re
import ddddocr


def ocr(img) -> str:
    """
    通过带带弟弟库识别图片中的文本
    @param    img: 图片
    @return:  字符串
    """
    dddd = ddddocr.DdddOcr(show_ad=False)
    code = dddd.classification(img)
    return re.sub(r'\W+', '', code)
# 识别图像