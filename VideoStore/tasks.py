from celery import shared_task
import cv2
import uuid


@shared_task
def add(x, y):
    return x + y

@shared_task
def generate_thumbnails(path):
    print("generate_thumbnails open")
    print(path)
    new_path = path.split('/')[-1]
    print(new_path)
    
    vidcap = cv2.VideoCapture(f'public/static/videos/{new_path}')
    success , image = vidcap.read()
    generated_images = []
    count = 0
    try:
        while success:
            vidcap.set(cv2.CAP_PROP_POS_MSEC , (count * 10000))
            success, image = vidcap.read()
            if success:
                image_name = uuid.uuid4()
                cv2.imwrite(f'public/static/images/{image_name}.jpg', image)
                generated_images.append(f'media/images/{image_name}.jpg')
                count+=5

            if len(generated_images) > 5:
                break
    
    except Exception as e:
        print(e)

    print("generate_thumbnails close")

    return generated_images
    