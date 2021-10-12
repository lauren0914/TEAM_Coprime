import os

from bokeh.embed import components
from bokeh.models import Range1d
from bokeh.plotting import figure, ColumnDataSource
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect


# Create your views here.

# image upload
from can.predict import predict_image
from can.visionAPI import detect_text


def img_upload(request):
    return render(request, 'can/img_upload.html', {})

# save image & predict
def pred_img(request):

    uploaded_file = request.FILES['img_uploaded']
    fs = FileSystemStorage()
    uploaded_filename = fs.save(uploaded_file.name, uploaded_file)
    uploaded_file_url = fs.url(uploaded_filename) # "/media/~~~.jpg"

    # predict
    pred_result = predict_image(settings.MEDIA_ROOT_URL + uploaded_file_url)

    result_name = pred_result[0]
    result_value = pred_result[1]
    rank = pred_result[2]
    rank_value = pred_result[3]

    # audio source
    tts = settings.MEDIA_URL + "result.mp3"

    # bar graph
    source = ColumnDataSource(data=dict(
        rank_value=rank_value,
        rank=rank
    ))
    # hover
    TOOLTIPS = [
        ("Beverage", "@rank"),
        ("Predict value", "@rank_value{0.2f} %"),
    ]

    rank_bar = figure(y_range=rank, x_range=(0, 1), toolbar_location=None, tooltips=TOOLTIPS, title="Rank of TOP3")
    rank_bar.hbar(y='rank', right='rank_value', height=0.5, alpha=0.7, color='limegreen', source=source)
    # customizing
    rank_bar.x_range = Range1d(0, 100)
    rank_bar.width = 300
    rank_bar.height = 200
    rank_bar.xaxis.visible = False
    rank_bar.background_fill_alpha = 0
    rank_bar.border_fill_color = None
    rank_bar.axis.minor_tick_line_color = None
    rank_bar.outline_line_color = None
    rank_bar.xgrid.grid_line_color = None
    rank_bar.ygrid.grid_line_color = None

    script_rank, div_rank = components(rank_bar)

    context = {'uploaded_file_url': uploaded_file_url,
               'uploaded_file_name': uploaded_filename,
               'result_name': result_name,
               'result_value': round(result_value*100, 2),
               'rank': rank,
               'rank_value': rank_value,
               'script_rank': script_rank,
               'div_rank': div_rank,
               'tts': tts}

    return render(request, 'can/result.html', context)

# detecting text
def detect_img_text(request, file_name):

    detected_text = detect_text(settings.MEDIA_ROOT_URL + settings.MEDIA_URL + file_name)

    tts_2 = settings.MEDIA_URL + "text.mp3"

    context = {'uploaded_file_url': settings.MEDIA_URL+file_name,
    'uploaded_file_name': file_name,
    'text_list': detected_text,
    'tts_2': tts_2}

    return render(request, 'can/text_reader.html', context)


# delete image
def delete(request, file_name):
    fs = FileSystemStorage()
    fs.delete(file_name)
    os.remove("./media/result.mp3")
    if os.path.isfile("./media/text.mp3"):
        os.remove("./media/text.mp3")

    return redirect('main:index')