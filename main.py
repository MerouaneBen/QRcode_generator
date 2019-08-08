"""

Code for generating promotionnal QR Codes.

"""
import qrcode
from PIL import Image
from pyshorteners import Shortener
import os
import time
import imgkit

BASE_URL = 'https://www.google.com/search?q='
LIST_PROMOCODES  = ['awesome','clear','make']
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_PATH = PROJECT_PATH + '/images/templates'
OUTPUT_PATH = PROJECT_PATH + '/images/outputs'
shortener = Shortener('Tinyurl',  timeout=2)

def build_urls():
    """build url and return them in a list"""
    full_url_list = []
    for element in LIST_PROMOCODES: 
        full_url_list.append(BASE_URL+element)
    return full_url_list

def generate_qrcode(data, body_size, border, fill_color, back_color):
    """
    generate codes.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=body_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    return img


def load_image(image_name):
    """
    load a image template
    """
    try: 
        # open image from Path 
        img = Image.open( TEMPLATE_PATH + '/' + image_name) 
        width, height = img.size
        print('Template width:', width, 'Template height:', height) 

        return img
    except IOError: 
        pass

def copy_image_in_image(template_image, image, x_position, y_position):
    """
    copy qr image in 
    """
    template_image.paste(image, (x_position, y_position)) 
    return  template_image 

def save_image(image_object, image_name):

    """Saved in the same relative location """

    image_object.save(OUTPUT_PATH + '/' + image_name + ".jpg")
    

def build_link_image(url):
    """takes url string and return an image."""
    html_file = open(TEMPLATE_PATH + '/' + "link_html_template.html").read().format(short_url=url,)
    imgkit.from_string(html_file, TEMPLATE_PATH + '/' + 'url_image.jpg')
    
    # resize the text image.
    """ img = Image.open(TEMPLATE_PATH + '/' + 'url_image.jpg')
    width, height = img.size
    img = img.resize((int(width/2), int(height))) 
    img.save(TEMPLATE_PATH + '/' + 'url_image.jpg') """ 

def main(template_name, x_qr_position, y_qr_position, output_file_prefix, 
         qr_body_size, qr_border, qr_fill_color, qr_back_color, url_x_position, url_y_position):
    """buid the qr code inside the template """
    urls = build_urls()
    template = load_image(template_name)
    
    index = 1
    for url in urls : 
        qr_code = generate_qrcode(url,qr_body_size,qr_border,qr_fill_color,qr_back_color)
        file_name = output_file_prefix + '_' + str(index) 
        template_with_qr = copy_image_in_image(template, qr_code, x_qr_position, y_qr_position)
        short_url = shortener.short(url)
        build_link_image(short_url)
        # sleep to generate the text image and save it on disk 
        time.sleep(1)
        url_image = load_image('url_image.jpg')
        final_image = copy_image_in_image(template_with_qr, url_image,url_x_position, url_y_position)
        save_image(final_image, file_name)
        # time sleep for tuny url api, is free and public but timesout a lot
        time.sleep(3)
        index += 1

if __name__ == '__main__':
    template_name = 'Template_qr_code.jpg' 
    output_file_prefix = 'eva_promo_code'
    x_qr_position = 700
    y_qr_position = 200
    url_x_position = 710
    url_y_position = 530
    qr_body_size = 10
    qr_border = 4
    qr_fill_color = 'black'
    qr_back_color = 'white'

    main(template_name, x_qr_position, y_qr_position, output_file_prefix, 
         qr_body_size, qr_border, qr_fill_color, qr_back_color, url_x_position, url_y_position)