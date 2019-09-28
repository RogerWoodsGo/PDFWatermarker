#coding = utf-8
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def create_stamp_pdf(options, width=960, height=540):
    pdfTemp = io.BytesIO()
    pdfDoc = canvas.Canvas(pdfTemp, pagesize=(width, height))
    pdfmetrics.registerFont(TTFont('simsun', 'simsun.ttf'))
    pdfDoc.setFont("simsun", options.font_size)
    pdfDoc.setFillColorRGB(*tuple(c / 255.0
                                  for c in hex_to_rgb(options.color)))
    pdfDoc.setFillAlpha(options.opacity)
    pdfDoc.translate(float(width / 2), float(height / 2))
    pdfDoc.rotate(options.rotate_angle)
    pdfDoc.drawCentredString(0, 0, options.watermark_string)
    pdfDoc.save()
    return pdfTemp


def add_one_page_watermark(page, options):
    page_width = page.mediaBox.lowerRight[0] - page.mediaBox.lowerLeft[0]
    page_height = page.mediaBox.upperLeft[1] - page.mediaBox.lowerLeft[1]
    stamp = create_stamp_pdf(options, page_width, page_height)
    pdf_watermark = PdfFileReader(io.BytesIO(stamp.getvalue()), strict=False)
    page.mergePage(pdf_watermark.getPage(0))
    page.compressContentStreams()


def add_watermark(options):
    try:
        input_stream = open(options.input_file, 'rb')
    except Exception as e:
        print("Input File Not Found", e)
        return
    pdf_input = PdfFileReader(input_stream, strict=False)
    pageNum = pdf_input.getNumPages()

    if pageNum == -1:
        print("PDF Object Not Found")
        return

    pdf_output = PdfFileWriter()
    for i in range(pageNum):
        print("Handling Page {}".format(i + 1))
        page = pdf_input.getPage(i)
        add_one_page_watermark(page, options)
        pdf_output.addPage(page)

    pdf_output.write(open(options.output_file, 'wb'))


def get_cli_options():
    import argparse
    parser = argparse.ArgumentParser("python pdf_watermark.py")
    parser.add_argument("--rotate_angle",
                        help="The watermark rotate_angle",
                        type=int,
                        default=45)
    parser.add_argument("--font_size",
                        help="The watermark size",
                        type=int,
                        default=48)
    parser.add_argument("--opacity",
                        help="The watermark opacity",
                        type=float,
                        default=0.5)
    parser.add_argument("--color",
                        help="The watermark color:eg. '#000000' or 000000",
                        type=str,
                        default="#808080")
    parser.add_argument("--watermark_string",
                        help="Watermark String",
                        type=str,
                        default="This Is Watermark")
    parser.add_argument("input_file", help="Input file name", type=str)
    parser.add_argument("output_file", help="Output file name", type=str)
    options = parser.parse_args()
    return options


if __name__ == "__main__":
    options = get_cli_options()
    add_watermark(options)
