from django.shortcuts import render
from PIL import Image
from django.conf import settings
import os
from django.http import HttpResponse
def home(request):
    return render(request, 'image_editor/home.html')

def edit_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        operation = request.POST.get('operation')

        if image is not None and operation is not None:
            # Save the uploaded image temporarily
            image_path = os.path.join(settings.MEDIA_ROOT, 'temp_image.jpg')
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            # Perform the specified image editing operation
            edited_img = None
            if operation == 'resize':
                width = int(request.POST.get('width', 0))
                height = int(request.POST.get('height', 0))
                if width > 0 and height > 0:
                    img = Image.open(image_path).convert('RGB')  # Convert image to RGB mode
                    edited_img = img.resize((width, height))

            elif operation == 'crop':
                left = int(request.POST.get('left', 0))
                upper = int(request.POST.get('upper', 0))
                right = int(request.POST.get('right', 0))
                lower = int(request.POST.get('lower', 0))
                if left < right and upper < lower and right > 0 and lower > 0:  # Check if the coordinates define a valid crop region
                    img = Image.open(image_path).convert('RGB')  # Convert image to RGB mode
                    edited_img = img.crop((left, upper, right, lower))

            # Delete the temporary uploaded image
            os.remove(image_path)

            if edited_img:
                # Save the edited image
                edited_img_path = os.path.join(settings.MEDIA_ROOT, 'edited_image.jpg')
                edited_img.save(edited_img_path)

                # Prepare the download link for the edited image
                download_link = settings.MEDIA_URL + 'edited_image.jpg'
                # Redirect to the result view
                return result(request, download_link, edited_img_path)

        # If form submission fails or no image or operation is provided, render the edit image page
        return render(request, 'image_editor/edit_image.html')
    # Render the edit image page for GET requests
    return render(request, 'image_editor/edit_image.html')
def result(request, download_link=None, edited_img_path=None):
    if download_link and edited_img_path:
        # Open the edited image file
        with open(edited_img_path, 'rb') as f:
            response = HttpResponse(f, content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="edited_image.jpg"'
        return response
    else:
        # Render the result template with the download link
        return render(request, 'image_editor/result.html', {'download_link': download_link})
