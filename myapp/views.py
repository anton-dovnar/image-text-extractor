from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponseBadRequest

from .text_extractor import handle_uploaded_file, check_file


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('upload_file')
        
        if uploaded_file is None:
            return HttpResponseBadRequest("No file uploaded")
        
        try:
            file_name = handle_uploaded_file(uploaded_file)
            extracted_text = check_file(file_name)
            
            if extracted_text:
                result_message = f"The extracted text is: {extracted_text}"
            else:
                result_message = "No text available to extract"

        except Exception as e:
            result_message = f"An error occurred: {str(e)}"
        
        return render(request, 'file_upload.html', {'text': result_message})
    return render(request, 'file_upload.html')
