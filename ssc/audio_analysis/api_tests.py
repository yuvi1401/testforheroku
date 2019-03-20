import sys

from ssc.audio_analysis.acr_api_requests import identify_audio

print(identify_audio('/home/oliver/Desktop/wombats.mp3'))
# print(upload_audio(sys.argv[1], 'ssc_bucket', 'new_song', '123456'))
#
# if identify_audio(sys.argv[1])["status"]["msg"] == 'Success':
#     print('This audio file already exists please choose another')
