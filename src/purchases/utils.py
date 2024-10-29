import math
from pyppeteer import launch
import os
from django.template import loader
from django.http import FileResponse


def number_to_words(amount):
    def get_words_for_number(no):
        digit_1 = len(str(no))
        i = 0
        str_array = []

        while i < digit_1:
            if i == 2:
                divider = 10
            else:
                divider = 100

            number_part = no % divider
            no = no // divider
            i += 1 if divider == 10 else 2

            if number_part:
                counter = len(str_array)
                plural = "s" if counter and number_part > 9 else ""
                hundred = "and " if counter == 1 and str_array[0] else ""

                if number_part < 21:
                    str_array.append(
                        f"{words[str(number_part)]} {digits[counter]}{plural} {hundred}"
                    )
                else:
                    str_array.append(
                        f"{words[str(number_part // 10 * 10)]} {words[str(number_part % 10)]} {digits[counter]}{plural} {hundred}"
                    )
            else:
                str_array.append("")

        return "".join(reversed(str_array)).strip()

    words = {
        "0": "",
        "1": "One",
        "2": "Two",
        "3": "Three",
        "4": "Four",
        "5": "Five",
        "6": "Six",
        "7": "Seven",
        "8": "Eight",
        "9": "Nine",
        "10": "Ten",
        "11": "Eleven",
        "12": "Twelve",
        "13": "Thirteen",
        "14": "Fourteen",
        "15": "Fifteen",
        "16": "Sixteen",
        "17": "Seventeen",
        "18": "Eighteen",
        "19": "Nineteen",
        "20": "Twenty",
        "30": "Thirty",
        "40": "Forty",
        "50": "Fifty",
        "60": "Sixty",
        "70": "Seventy",
        "80": "Eighty",
        "90": "Ninety",
    }

    digits = ["", "Hundred", "Thousand", "Lakh", "Crore", "Arab", "Kharab"]

    # Split amount into whole number and fractional part
    no = int(math.floor(amount))
    point = round((amount - no) * 100)

    # Convert whole number part to words
    result = get_words_for_number(no)

    # Convert fractional part to words if there's a decimal part
    points = (
        f". {words[str(point // 10)]} {words[str(point % 10)]} Paisa" if point else ""
    )

    # Return the final result without "Paisa" if there's no fractional part
    return f"{result} Rupees{points} Only."


import asyncio
from django.views import View
from django.http import FileResponse, Http404
from pyppeteer import launch
from asgiref.sync import async_to_sync


import os
import asyncio
from django.views import View
from django.http import FileResponse, Http404
from pyppeteer import launch
from asgiref.sync import async_to_sync


class PdfView(View):
    template_name: str = ""
    size: str = "A4"
    file_name: str = "output"

    async def generate_pdf(self) -> str:
        try:
            # Launch the browser
            browser = await launch({"headless": True})
            page = await browser.newPage()

            # Construct the file path to the HTML template
            template_path = os.path.join(os.getcwd(), self.template_name)
            if not os.path.exists(template_path):
                raise Http404("Template not found")

            # Open the HTML template in the browser
            await page.goto(f"file://{template_path}")

            # Generate the PDF
            pdf_path = os.path.join(os.getcwd(), f"{self.file_name}.pdf")
            await page.pdf({"path": pdf_path, "format": self.size})

            # Close the browser
            await browser.close()

            return pdf_path

        except Exception as e:
            print(f"An error occurred: {e}")
            raise Http404("An error occurred while generating the PDF")

    def get(self, request, *args, **kwargs):
        return FileResponse(
            open(self.pdf_path, "rb"),
            as_attachment=True,
            filename=f"{self.file_name}.pdf",
        )
