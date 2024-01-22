from PIL import Image


def crop_image(input_image, output_image, start_x, start_y, width, height):
    input_img = Image.open(input_image)
    box = (start_x, start_y, start_x + width, start_y + height)
    output_img = input_img.crop(box)
    output_img.save(output_image + ".png")


def combine(images, output_path):
    # Open all images
    image_list = [Image.open(image) for image in images]

    # Get the width and height of the first image
    width, height = image_list[0].size

    # Create a new image with a width that can accommodate all images
    combined_image = Image.new("RGB", (width * len(image_list), height))

    # Paste each image horizontally
    for i, img in enumerate(image_list):
        combined_image.paste(img, (i * width, 0))

    # Save the combined image
    combined_image.save(output_path)


# if __name__ == "__main__":
#     images = []
#     for i in range(131):
#         FilePath = "data\\img" + str(i) + ".png"
#         Engine = 2
#         crop_image(
#             FilePath, "data\\img" + str(i) + "-cropped", 200 - 136, 200 - 120, 95, 80
#         )
#         images.append("data\\img" + str(i) + "-cropped" + ".png")
#     combine(images, "combined.png")
𝔩=[]
𝔱=𝔩==𝔩
print((bin(~𝔱)))
