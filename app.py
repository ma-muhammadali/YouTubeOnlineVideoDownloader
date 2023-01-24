# importing modules
from youtube_transcript_api import YouTubeTranscriptApi
from flask import Flask, render_template
from flask import render_template, request, redirect, url_for, flash, send_file, session, copy_current_request_context
#import mimetypes
from pytube import YouTube
from io import BytesIO
#from distutils.log import debug
#from fileinput import filename
import os, os.path
import logging
import threading
#import sys
#import time



app = Flask(__name__)

app.config['SECRET_KEY'] = 'helloworld'


@app.route('/')
def main():
    return render_template('index.html')
   
@app.route('/bulkdownload')
def bulkdownload():
    return render_template('bulkdownload.html')
    
@app.route('/audiodownload')
def audiodownload():
    return render_template('audiodownload.html')

@app.route('/transcript')
def transcript():
    return render_template('transcript.html')


@app.route("/", methods = ["GET", "POST"])
@app.route("/index", methods = ["GET", "POST"])
def index():
    """
    When the form is submitted, the video link is
    parsed and made ready for download.
    """
    if request.method == "POST":
        session['link'] = request.form.get('url')
        try:
            url = YouTube(session['link'])
            url.check_availability()

            def find_video_length():
                # Find the length of the video in hours, minutes, seconds
                duration = url.length
                
                hours = duration // 3600
                hours = int(hours)
                
                minutes = (duration - hours * 3600) // 60
                minutes = int(minutes)

                seconds = duration % 60
                seconds = int(seconds)

                if hours<10:
                    hours = str(0) + str(hours)
                
                if minutes<10:
                    minutes = str(0) + str(minutes)

                if seconds<10:
                    seconds = str(0) + str(seconds)

                
                video_length = str(hours) + ":" + str(minutes) + ":" + str(seconds)
                return video_length

            def get_video_file_size():
                # Convert file size of video to GB or MB
                file_size = url.streams.get_highest_resolution().filesize
                video_file_size_GB = round(file_size / (1024 * 1024 * 1024), 2)
                video_file_size_MB = round(file_size / (1024 * 1024), 2)
                best_video_file_size = str(video_file_size_GB) + ' GB' if video_file_size_GB > 1 else str(video_file_size_MB) + ' MB'
                return best_video_file_size
            
            video_duration = find_video_length()
            video_file_size = get_video_file_size()
            resolution = url.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()#.order_by('resolution').desc()
            #flash(f'Downloading {url.title}')
        except:
            flash('Error: invalid link or no link provided')
            return redirect(url_for('index'))

        return render_template(
            "videodownload.html",
            url=url,
            video_duration=video_duration,
            hightest_resolution=resolution.resolution,
            best_video_file_size=video_file_size)
    return render_template("index.html", title="Home")


@app.route("/audiodownload", methods = ["GET", "POST"])
def mp3download():
    """
    When the form is submitted, the video link is
    parsed and made ready for download.
    """
    if request.method == "POST":
        session['link'] = request.form.get('url')
        try:
            url = YouTube(session['link'])
            url.check_availability()

            def find_audio_length():
                # Find the length of the video in hours, minutes, seconds
                duration = url.length
                
                hours = duration // 3600
                hours = int(hours)
                
                minutes = (duration - hours * 3600) // 60
                minutes = int(minutes)

                seconds = duration % 60
                seconds = int(seconds)

                if hours<10:
                    hours = str(0) + str(hours)
                
                if minutes<10:
                    minutes = str(0) + str(minutes)

                if seconds<10:
                    seconds = str(0) + str(seconds)

                
                audio_length = str(hours) + ":" + str(minutes) + ":" + str(seconds)
                return audio_length

            def get_audio_file_size():
                # Convert file size of video to GB or MB
                file_size = url.streams.get_audio_only().filesize#filter(only_audio=True)#.get_highest_resolution().filesize
                audio_file_size_GB = round(file_size / (1024 * 1024 * 1024), 2)
                audio_file_size_MB = round(file_size / (1024 * 1024), 2)
                best_audio_file_size = str(audio_file_size_GB) + ' GB' if audio_file_size_GB > 1 else str(audio_file_size_MB) + ' MB'
                return best_audio_file_size
            
            audio_duration = find_audio_length()
            audio_file_size = get_audio_file_size()
            #resolution = url.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()#.order_by('resolution').desc()
            #flash(f'Downloading {url.title}')
        except:
            flash('Error: invalid link or no link provided')
            return redirect(url_for('index'))

        return render_template(
            "mp3download.html",
            url=url,
            audio_duration=audio_duration,
            best_audio_file_size=audio_file_size)
    return render_template("index.html", title="Home")


@app.route("/transcript", methods = ["GET", "POST"])
def downloadtrans():
    """
    When the form is submitted, the video link is
    parsed and made ready for download.
    """
    if request.method == "POST":
        session['link'] = request.form.get('url')
        try:
            url = YouTube(session['link'])
            url.check_availability()

            #srt = YouTubeTranscriptApi.get_transcript("SW14tOda_kI",languages=['en'])

            #logging.info("Hello Testing")

            #transcript_list = YouTubeTranscriptApi.list_transcripts("SW14tOda_kI")

            #for transcript in transcript_list:
             #   logging.info("Hello " + transcript)

            def find_audio_length():
                # Find the length of the video in hours, minutes, seconds
                duration = url.length
                
                hours = duration // 3600
                hours = int(hours)
                
                minutes = (duration - hours * 3600) // 60
                minutes = int(minutes)

                seconds = duration % 60
                seconds = int(seconds)

                if hours<10:
                    hours = str(0) + str(hours)
                
                if minutes<10:
                    minutes = str(0) + str(minutes)

                if seconds<10:
                    seconds = str(0) + str(seconds)

                
                audio_length = str(hours) + ":" + str(minutes) + ":" + str(seconds)
                return audio_length

            
            audio_duration = find_audio_length()
            #resolution = url.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()#.order_by('resolution').desc()
            #flash(f'Downloading {url.title}')
        except:
            flash('Error: invalid link or no link provided')
            return redirect(url_for('index'))

        return render_template(
            "transcriptdownload.html",
            url=url,
            audio_duration=audio_duration
            #best_audio_file_size=audio_file_size
            )
    return render_template("index.html", title="Home")



@app.route("/videodownload", methods = ["GET", "POST"])
def downloadvideo():
    """Downloads the video and saves it to the user's computer"""
    if request.method == "POST":
        buffer = BytesIO()
        url = YouTube(session['link'])
        file_name = url.title + ".mp4"
        #itag = request.form.get("itag")
        myvideo = url.streams.get_highest_resolution()#.get_by_itag(itag)
        #myvideo.download()
        myvideo.stream_to_buffer(buffer)
        buffer.seek(0)
        #flash(f'Downloading {url.title}')  
        return send_file(
            buffer,
            download_name=file_name,
            as_attachment=True, 
            mimetype='video/mp4'
        )
    return redirect(url_for("videodownload"))

@app.route("/index", methods = ["GET", "POST"])
def gobackhome():
    if request.method == "POST":
        return render_template("index.html")




@app.route("/mp3download", methods = ["GET", "POST"])
def downloadmp3():
    """Downloads the audio and saves it to the user's computer"""
    try:

        if request.method == "POST":
            buffer = BytesIO()
            url = YouTube(session['link'])
            file_name = url.title + ".mp3"
            #itag = request.form.get("itag")
            myaudio = url.streams.get_audio_only()#get_highest_resolution()#.get_by_itag(itag)
            #myvideo.download()
            myaudio.stream_to_buffer(buffer)
            buffer.seek(0)
            #flash(f'Downloading {url.title}') 
            #flash("Audio downloaded successfully. Please check your Downloads Folder")
            return send_file(
                buffer,
                download_name=file_name,
                as_attachment=True, 
                mimetype='audio/mp3'
            )
        #return redirect(url_for("mp3download"))
        return render_template('mp3download')
        

    except Exception as ex:
        logging.warning("Exception: " + ex)


@app.route("/transcriptdownload", methods = ["GET", "POST"])
def downloadtranscript():
    """Downloads the audio and saves it to the user's computer"""
    try:

        if request.method == "POST":
            buffer = BytesIO()
            url = YouTube(session['link'])
            file_name = url.title + "_Transcript.txt"
            #itag = request.form.get("itag")

            def find_audio_length():
                # Find the length of the video in hours, minutes, seconds
                duration = url.length
                
                hours = duration // 3600
                hours = int(hours)
                
                minutes = (duration - hours * 3600) // 60
                minutes = int(minutes)

                seconds = duration % 60
                seconds = int(seconds)

                if hours<10:
                    hours = str(0) + str(hours)
                
                if minutes<10:
                    minutes = str(0) + str(minutes)

                if seconds<10:
                    seconds = str(0) + str(seconds)

                
                audio_length = str(hours) + ":" + str(minutes) + ":" + str(seconds)
                return audio_length

            
            audio_duration = find_audio_length()

            
            #myaudio = url.streams.get_highest_resolution()#.get_by_itag(itag)
            #myvideo.download()
            #srt = YouTubeTranscriptApi.get_transcript()

            video_id = "\""+ url.video_id +"\""
            logging.warning("New Video Id: " + video_id)

            
            # For Testing Purpose
            # Video Id: SW14tOda_kI
            #srt = YouTubeTranscriptApi.get_transcript("SW14tOda_kI",languages=['en'])

            # For Testing Purpose
            # https://youtu.be/Nn_iCKa7neM
            srt = YouTubeTranscriptApi.get_transcript(url.video_id)#,languages=['en'])



            username = os.getlogin()
            
            # creating or overwriting a file "subtitles.txt" with
            # the info inside the context manager
            with open(f'C:/Users/{username}/Downloads/'+ url.title +" - Transcript.txt", "w") as f:
   
            # iterating through each element of list srt
                for i in srt:
                    # writing each element of srt on a new line
                    f.write("{}\n".format(i))
                    
                   
            #myaudio.stream_to_buffer(buffer)
            #buffer.seek(0)
            #flash(f'Downloading {url.title}') 
            logging.warning("Video ID: " + url.video_id)
            flash("Transcript downloaded successfully. Please check your Downloads Folder")
            #return send_file(
            #    buffer,
            #    download_name="subtitles.txt",
            #    as_attachment=True, 
            #    mimetype='text/txt'
            #)
            
            #return redirect(url_for("transcript"))

        

    except Exception as ex:
        flash("Trascript Not Found for this video.")
        logging.exception(ex)
    
    finally:
        return render_template(
            "transcriptdownload.html",
            url=url,
            audio_duration=audio_duration,
            #best_audio_file_size=0
            )





@app.route('/bulkdownload', methods = ["GET", 'POST'])  
def bulkdownloadvideo():  
    if request.method == 'POST':
        
        f = request.files['file']
        filename = f.filename
        f.save(f.filename) 

        logging.warning("file name: " + filename)

        download_flag = True

        @copy_current_request_context
        def background_task(link):
            try:
                logging.warning("In Thread")
                buffer = BytesIO()
                url = YouTube(link)
                logging.warning("URL "+link)
                logging.warning(url)
                file_name = url.title + ".mp4"
                myvideo = url.streams.get_highest_resolution()#.get_by_itag(itag)
                
                username = os.getlogin()
                myvideo.download(f'C:/Users/{username}/Downloads')
                flash(url.title + " is downloaded. Please check your Downloads folder")
                    
                myvideo.download()
                #return redirect(url_for("bulkdownload"))
                
                #myvideo.download()
                #myvideo.stream_to_buffer(buffer)
                #buffer.seek(0)
                #logging.warning("File size: "+ str(myvideo.filesize))
                
                #logging.warning(buffer)

                #send_file(
                #                  buffer,
                #                    download_name=file_name,
                #                    as_attachment=True, 
                #                    mimetype='video/mp4'
                                    
                #                )

            except Exception as ex:
                logging.warning("Exception: "+ str(ex))


        while download_flag:
            logging.warning("in while loop")
            try:
                with open(filename) as file:
                    for line in file:
                        link = str(line).strip()

                        #session['_flashes'].clear()
                        #session.pop("User", None)
                        #flash(link + " is downloading. Please check your Downloads folder")
                        
                        #logging.warning("Sleep 10 sec.")
                        #time.sleep(10)

                        th = threading.Thread(target=background_task, args=(link,))
                        th.daemon = True
                        th.start()
                        th.join()
                        

                        

                        #buffer = BytesIO()
                        #url = YouTube(link)
                        #file_name = url.title + ".mp4"
                        #itag = request.form.get("itag")
                        #myvideo = url.streams.get_highest_resolution()#.get_by_itag(itag)
                        
                        #username = os.getlogin()
                        #myvideo.download(f'C:/Users/{username}/Downloads')
                        #myvideo.download()
                        #myvideo.stream_to_buffer(buffer)
                        #buffer.seek(0)
                                
                        #send_file(
                         #           buffer,
                          #          download_name=file_name,
                           #         as_attachment=True, 
                            #        mimetype='video/mp4'
                             #   )
                        
                download_flag = False

            except Exception as ex:
                logging.warning("Exception: "+ str(ex))

            finally:
                download_flag = False

        #f.save(os.path.join(app.config['UPLOAD_FOLDER'], (f.filename)))
        return render_template("bulkdownload.html", name = f.filename)

if __name__=="__main__":
    app.run(debug=True)