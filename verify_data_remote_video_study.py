# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 14:11:00 2021

@author: Michal
"""

import os
import util
import event_messages
import re
import pandas as pd

#%% Set variables

#data_directory = (r"E:\emteq-data-science\VR\python\data_preprocessing_scripts\michal\data\filip_panchevski")
expected_number_of_all_files = 14
expected_number_of_event_files = expected_number_of_all_files/2
minimum_expected_signal_quality = 8
# Setting this to true will print more messages
is_debug = False
create_quality_csv_output_file = True
df = pd.DataFrame(columns = ["participant_number", "slow_movement_signal_quality", "fast_movement_signal_quality", "video_movement_signal_quality", "protocol"])

#%% define methods

def __check_slow_movement_event_data(slow_movement_event_data):
    slow_movement_study_issues_found = False;
    if(is_debug):
        print("\nCHECKING SLOW MOVEMENT SEGMENT")
    if __is_segment_signal_quality_good(slow_movement_event_data[1]['Event'], "Slow movement segment") == False:
        slow_movement_study_issues_found = True
    if slow_movement_event_data[0]['Event'] != event_messages.SLOW_MOVEMENT_SIGNAL_CHECK_MESSAGE:
        util.message_not_found(event_messages.SLOW_MOVEMENT_SIGNAL_CHECK_MESSAGE)
        slow_movement_study_issues_found = True
    else:
        if(is_debug):
            util.message_found(event_messages.SLOW_MOVEMENT_SIGNAL_CHECK_MESSAGE)
    if slow_movement_event_data[len(slow_movement_event_data)-1]['Event'] != event_messages.SLOW_MOVEMENT_FINISHED_MESSAGE:
        util.message_not_found(event_messages.SLOW_MOVEMENT_FINISHED_MESSAGE)
        slow_movement_study_issues_found = True
    else:
        if(is_debug):
            util.message_found(event_messages.SLOW_MOVEMENT_FINISHED_MESSAGE)
    if slow_movement_study_issues_found:
        print("!!!!!!!!SLOW MOVEMENT SEGMENT ISSUE!!!!!!!!")
    else:
        if(is_debug):
            print("SLOW MOVEMENT SEGMENT OK")
        
def __check_fast_movement_event_data(fast_movement_event_data):
    fast_movement_study_issues_found = False;
    if(is_debug):
        print("\nCHECKING FAST MOVEMENT SEGMENT")
    if __is_segment_signal_quality_good(fast_movement_event_data[1]['Event'], "Fast movement segment") == False:
        fast_movement_study_issues_found = True
    if fast_movement_event_data[0]['Event'] != event_messages.FAST_MOVEMENT_SIGNAL_CHECK_MESSAGE:
        util.message_not_found(event_messages.FAST_MOVEMENT_SIGNAL_CHECK_MESSAGE)
        fast_movement_study_issues_found = True
    else:
        if(is_debug):
            util.message_found(event_messages.FAST_MOVEMENT_SIGNAL_CHECK_MESSAGE)
    if fast_movement_event_data[len(fast_movement_event_data)-1]['Event'] != event_messages.FAST_MOVEMENT_FINISHED_MESSAGE:
        util.message_not_found(event_messages.FAST_MOVEMENT_FINISHED_MESSAGE)
        fast_movement_study_issues_found = True
    else:
        if(is_debug):
            util.message_found(event_messages.FAST_MOVEMENT_FINISHED_MESSAGE)
    if fast_movement_study_issues_found:
        print("!!!!!!!!FAST MOVEMENT SEGMENT ISSUE!!!!!!!!")
    else:
        if(is_debug):
            print("FAST MOVEMENT SEGMENT OK")
        
def __check_video_segment_1_event_data(video_segment_1_event_data):
    video_segment_1_issues_found = False;
    if(is_debug):
        print("\nCHECKING VIDEO SEGMENT 1")
    if __is_segment_signal_quality_good(video_segment_1_event_data[1]['Event'], "Video segment") == False:
        video_segment_1_issues_found = True
    if video_segment_1_event_data[0]['Event'] != event_messages.VIDEO_SIGNAL_CHECK_MESSAGE:
        util.message_not_found(event_messages.VIDEO_SIGNAL_CHECK_MESSAGE)
        video_segment_1_issues_found = True
    else:
        if(is_debug):
            util.message_found(event_messages.VIDEO_SIGNAL_CHECK_MESSAGE)
    
    for event in video_segment_1_event_data:
        category_sequence_names = re.search('Category sequence:(.*)', event['Event'])
        if(category_sequence_names is not None):
            if(is_debug):
                print(category_sequence_names.group(1)) 
        category_sequence_numbers = re.search('Category sequence array numbers:(.*)', event['Event'])
        if(category_sequence_numbers is not None):
            if(is_debug):
                print(category_sequence_numbers.group(1))
            category_sequence_list = category_sequence_numbers.group(1).split()
            # for category in category_sequence_list:
            #     category_sequence_list[category] = int(category.replace(',', ''))
            for i in range(len(category_sequence_list)):
                category_sequence_list[i] = int(category_sequence_list[i].replace(',', ''))
    
    if video_segment_1_issues_found:
        print("!!!!!!!!VIDEO SEGMENT 1 ISSUE!!!!!!!!")
    else:
        if(is_debug):
            print("VIDEO SEGMENT 1 OK")
    return category_sequence_list
        
def __check_video_segment_2_event_data(video_segment_2_event_data, segment_2_video_category):
    if(is_debug):
        print("\nCHECKING VIDEO SEGMENT 2")
    video_segment_2_issues_found = __check_video_segment_generic(video_segment_2_event_data, segment_2_video_category)
    if video_segment_2_issues_found:
        print("!!!!!!!!VIDEO SEGMENT 2 ISSUE!!!!!!!!")
    else:
        if(is_debug):
            print("VIDEO SEGMENT 2 OK")
    
def __check_video_segment_3_event_data(video_segment_3_event_data, segment_3_video_category):
    if(is_debug):
        print("\nCHECKING VIDEO SEGMENT 3")
    video_segment_3_issues_found = __check_video_segment_generic(video_segment_3_event_data, segment_3_video_category)
    if video_segment_3_issues_found:
        print("!!!!!!!!VIDEO SEGMENT 3 ISSUE!!!!!!!!")
    else:
        if(is_debug):
            print("VIDEO SEGMENT 3 OK")

def __check_video_segment_4_event_data(video_segment_4_event_data, segment_4_video_category):
    if(is_debug):
        print("\nCHECKING VIDEO SEGMENT 4")
    video_segment_4_issues_found = __check_video_segment_generic(video_segment_4_event_data, segment_4_video_category)
    if video_segment_4_issues_found:
        print("!!!!!!!!VIDEO SEGMENT 4 ISSUE!!!!!!!!")
    else:
        if(is_debug):
            print("VIDEO SEGMENT 4 OK")

def __check_video_segment_5_event_data(video_segment_5_event_data):
    video_segment_5_issues_found = False;
    playing_rest_video = False
    finished_playing_rest_video = False
    finished_playing_all_videos = False
    finished_video_ratings_study = False
    if(is_debug):
        print("\nCHECKING VIDEO SEGMENT 5")    
    for event in video_segment_5_event_data:
        event_string = event['Event']
        if playing_rest_video == False:
            if event_string == event_messages.VIDEO_PLAYING_REST_VIDEO:
                playing_rest_video = True
                if(is_debug):
                    util.message_found(event_messages.VIDEO_PLAYING_REST_VIDEO)
        if finished_playing_rest_video == False:
            if event_string == event_messages.VIDEO_FINISHED_PLAYING_REST_VIDEO:
                finished_playing_rest_video = True
                if(is_debug):
                    util.message_found(event_messages.VIDEO_FINISHED_PLAYING_REST_VIDEO)
        if finished_playing_all_videos == False:
            if event_string == event_messages.VIDEO_FINISHED_PLAYING_ALL_VIDEOS:
                finished_playing_all_videos = True
                if(is_debug):
                   util.message_found(event_messages.VIDEO_FINISHED_PLAYING_ALL_VIDEOS)
        if finished_video_ratings_study == False:
            if event_string == event_messages.VIDEO_FINISHED_STUDY:
                finished_video_ratings_study = True
                if(is_debug):
                    util.message_found(event_messages.VIDEO_FINISHED_STUDY)
                
    if playing_rest_video == False:
        util.message_not_found(event_messages.VIDEO_PLAYING_REST_VIDEO)
        video_segment_5_issues_found = True
    if finished_playing_rest_video == False:
        util.message_not_found(event_messages.VIDEO_FINISHED_PLAYING_REST_VIDEO)
        video_segment_5_issues_found = True
    if finished_playing_all_videos == False:
        util.message_not_found(event_messages.VIDEO_FINISHED_PLAYING_ALL_VIDEOS)
        video_segment_5_issues_found = True
    if finished_video_ratings_study == False:
        util.message_not_found(event_messages.VIDEO_FINISHED_STUDY)
        video_segment_5_issues_found = True
                             
    if video_segment_5_issues_found:
        print("!!!!!!!!VIDEO SEGMENT 5 ISSUE!!!!!!!!")
    else:
        if(is_debug):
            print("VIDEO SEGMENT 5 OK")

def __check_video_segment_generic(video_segment_event_data, expected_video_category_number):
    playing_rest_video = False
    finished_playing_rest_video = False
    playing_category = False
    category_name = ""
    category_number = 0
    playing_video_number_counter = 0
    expected_video_number_counter = 10
    category_finished = False
    video_segment_issue = False
    
    for event in video_segment_event_data:
        event_string = event['Event']
        if playing_rest_video == False:
            if event_string == event_messages.VIDEO_PLAYING_REST_VIDEO:
                playing_rest_video = True
                if(is_debug):
                    util.message_found(event_messages.VIDEO_PLAYING_REST_VIDEO)
        if finished_playing_rest_video == False:
            if event_string == event_messages.VIDEO_FINISHED_PLAYING_REST_VIDEO:
                finished_playing_rest_video = True
                if(is_debug):
                    util.message_found(event_messages.VIDEO_FINISHED_PLAYING_REST_VIDEO)
        if playing_category == False:
            playing_category_found = re.search('Playing category number:(.*)', event_string)
            if(playing_category_found is not None):
                category_number = int(re.search('Playing category number:(.*\d)', event_string).group(1))
                category_name = re.search('Category name:(.*)', event_string).group(1)
                if(is_debug):
                    print("Video category: ", category_number, " - ", category_name)
                playing_category = True
        if playing_video_number_counter < expected_video_number_counter:
            if(re.search('Finished playing video number:(.*)', event_string) is not None):
                playing_video_number_counter+= 1
        if category_finished == False:
            if event_string == event_messages.VIDEO_CATEGORY_FINISHED:
                category_finished = True
                if(is_debug):
                    util.message_found(event_messages.VIDEO_CATEGORY_FINISHED)
            
    if playing_rest_video == False:
        util.message_not_found(event_messages.VIDEO_PLAYING_REST_VIDEO)
        video_segment_issue = True
    if finished_playing_rest_video == False:
        util.message_not_found(event_messages.VIDEO_FINISHED_PLAYING_REST_VIDEO)
        video_segment_issue = True
    if category_finished == False:
        util.message_not_found(event_messages.VIDEO_CATEGORY_FINISHED)
        video_segment_issue = True
    if playing_video_number_counter < expected_video_number_counter:
        print("Not all videos finished playing. Played: ", playing_video_number_counter,"Expected: ", expected_video_number_counter)
    else:
        if(is_debug):
            print("All videos for this segment finished playing. Played: ", playing_video_number_counter, "Expected: ",  expected_video_number_counter)
    if category_number != expected_video_category_number:
        print("Unexpected category of videos played. Played: ", category_number, "Expected:", expected_video_category_number)
        video_segment_issue = True
    else:
        if(is_debug):
            print("Video category played: ", category_number, " Expected category: ", expected_video_category_number)
        
    return video_segment_issue
        
              
def __is_segment_signal_quality_good(signal_check_message, segment_name):
    # signal_fit_value = re.search('= (\d)', data[1]['Event'])
    signal_fit_value = re.search('= (\d)', signal_check_message)
    if(signal_fit_value is None):
        print("No signal quality obtained for ", segment_name, "value: ", signal_fit_value, "expected: ", minimum_expected_signal_quality)
        return False
    else:
        signal_fit_value = int(signal_fit_value.group(1))
        if("Slow" in segment_name):
            df.at[0, "slow_movement_signal_quality"] = signal_fit_value
        elif("Fast" in segment_name):
             df.at[0, "fast_movement_signal_quality"] = signal_fit_value
        elif("Video" in segment_name):
             df.at[0, "video_movement_signal_quality"] = signal_fit_value
    if signal_fit_value < minimum_expected_signal_quality:
        print("Low signal quality was found for: ", segment_name, "value: ", signal_fit_value, "expected: ", minimum_expected_signal_quality)
        return False
    else: 
        if(is_debug):
            print("Good signal quality was found for: ", segment_name, "value: ", signal_fit_value, "expected: ", minimum_expected_signal_quality)
        return True
    
def __get_event_files(list_of_all_files):
    event_files = []
    for file in list_of_all_files:
        if file.endswith(".json"):
            event_files.append(file)
    return sorted(event_files,  key=len)
    
#%% Verify data files

#main_wd = os.getcwd()
def verify_remote_data(data_directory):
    print(" Running data check for: ", data_directory)
    participant_number = data_directory.split("participant_")[1]
    if "v2" in participant_number:
        df.at[0, "protocol"] = "v2"
    else:
        df.at[0, "protocol"] = "v1"    
    df.at[0, "participant_number"] = participant_number[0:3]
    participant_data_files_list = os.listdir(data_directory)
    event_files = __get_event_files(participant_data_files_list)
    number_of_files = len(event_files)
    if number_of_files == expected_number_of_event_files:
        if(is_debug):
            print("\nCorrect number of event files was found: ", number_of_files)
        # Check events files for expected events for a finished study
        #for file_index in range(6):
        for file_index in range(7):
          file_to_check = data_directory + "/" + event_files[file_index]
          data = util.read_jsonfile(file_to_check)
          if event_files[file_index] == "slow_movement.json":
              __check_slow_movement_event_data(data)
          elif event_files[file_index] == "fast_movement.json":
              __check_fast_movement_event_data(data)
          elif event_files[file_index] == "video_1.json":
              category_sequence_list = __check_video_segment_1_event_data(data)
          elif event_files[file_index] == "video_2.json":
              __check_video_segment_2_event_data(data, category_sequence_list[0])
          elif event_files[file_index] == "video_3.json":
              __check_video_segment_3_event_data(data, category_sequence_list[1])
          elif event_files[file_index] == "video_4.json":
              __check_video_segment_4_event_data(data, category_sequence_list[2])
          elif event_files[file_index] == "video_5.json":
              __check_video_segment_5_event_data(data)
          else:
              print("test")
    else:
        print("FILES MISSING! FOUND: ", number_of_files, "EXPECTED: ", expected_number_of_event_files)
    if(is_debug):    
        print("\n FINISHED DATA CHECK FOR: ", data_directory)
    return df
