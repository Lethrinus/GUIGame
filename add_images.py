from PIL import Image, ImageTk

def add_image(canvas, images_dict, image_config):
    try:
        print(f"Loading image: {image_config['file']}")
        img = Image.open(image_config["file"])
        img = img.resize(tuple(image_config["resize"]))
        img_tk = ImageTk.PhotoImage(img)

        images_dict[image_config["name"]] = img_tk
        canvas.create_image(
            *image_config["position"],
            anchor=image_config["anchor"],
            image=img_tk
        )
    except Exception as e:
        print(f"Error adding image {image_config['name']}: {e}")

def load_interactive_image(canvas, image_path, resize, position, on_click_callback, instance):
    img = Image.open(image_path)
    img = img.resize(resize)
    img_tk = ImageTk.PhotoImage(img)

    image_id = canvas.create_image(*position, anchor="center", image=img_tk)
    canvas.image = img_tk

    canvas.tag_bind(image_id, "<Button-1>", lambda e: on_click_callback(instance))
