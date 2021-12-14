import torch
import utils
import transformer
import os
from torchvision import transforms
import time
import cv2

#STYLE_TRANSFORM_PATH = "transforms/lazy.pth"
STYLE_TRANSFORM_PATH = "C:/Users/A1234/Documents/INF573/project/fast-neural-style-pytorch/transforms/wave.pth"
#change this !!!!!

#PRESERVE_COLOR = False

def stylize(preserve_color):
    # Device
    device = ("cuda" if torch.cuda.is_available() else "cpu")

    # Load Transformer Network
    net = transformer.TransformerNetwork()
    net.load_state_dict(torch.load(STYLE_TRANSFORM_PATH))
    net = net.to(device)

    with torch.no_grad():
        while(1):
            torch.cuda.empty_cache()


            print("Stylize Image~ Press Ctrl+C and Enter to close the program")
            content_image_path = input("Enter the image path: ")



            content_image = utils.load_image(content_image_path)
            starttime = time.time()
            content_tensor = utils.itot(content_image).to(device)
            generated_tensor = net(content_tensor)
            generated_image = utils.ttoi(generated_tensor.detach())
            #if (PRESERVE_COLOR):
            if (preserve_color):
                generated_image = utils.transfer_color(content_image, generated_image)
            print("Transfer Time: {}".format(time.time() - starttime))
            utils.show(generated_image)
            utils.saveimg(generated_image, "helloworld.jpg")

def stylize_folder_single(style_path, content_folder, save_folder, preserve_color):
    """
    Reads frames/pictures as follows:

    content_folder
        pic1.ext
        pic2.ext
        pic3.ext
        ...

    and saves as the styled images in save_folder as follow:

    save_folder
        pic1.ext
        pic2.ext
        pic3.ext
        ...
    """
    # Device
    device = ("cuda:0" if torch.cuda.is_available() else "cpu")
    print('device: ', device)

    # Load Transformer Network
    net = transformer.TransformerNetwork()
    net.load_state_dict(torch.load(style_path))
    net = net.to(device)

    # Stylize every frame
    images = [img for img in os.listdir(content_folder) if img.endswith(".jpg")]
    with torch.no_grad():
        #print(images)
        for image_name in images:
            # Free-up unneeded cuda memory
            torch.cuda.empty_cache()
            
            # Load content image
            #content_image = utils.load_image(content_folder + image_name)
            content_image = utils.load_image(os.path.join(content_folder, image_name))
            content_tensor = utils.itot(content_image).to(device)

            # Generate image
            generated_tensor = net(content_tensor)
            generated_image = utils.ttoi(generated_tensor.detach())
            if (preserve_color):
                generated_image = utils.transfer_color(content_image, generated_image)
            # Save image
            utils.saveimg(generated_image, os.path.join(save_folder,image_name))

#stylize()
