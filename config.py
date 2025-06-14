#
#yaml file
#  
audio_config:
  audio_output: true
  default_volume: 1.0
  min_time_bewteen_play: 1
  speed_rate: 180

base_config:
  robot_name: "RaspRover"
  module_type: 2
  sbc_version: 0.89

sbc_config:
  feedback_interval: 0.001
  disabled_http_log: true

args_config:
  max_speed: 0.65
  slow_speed: 0.3
  max_rate: 1.00
  mid_rate: 0.66
  min_rate: 0.30

cv:
  default_color: "blue"
  color_lower: [101, 50, 38]
  color_upper: [110, 255, 255]
  min_radius: 12
  sampling_rad: 25
  track_color_iterate: 0.023
  track_faces_iterate: 0.045
  track_spd_rate: 60
  track_acc_rate: 0.4
  aimed_error: 8

cmd_config:
  cmd_movition_ctrl: 1
  cmd_pwm_ctrl: 11
  cmd_gimbal_ctrl: 133
  cmd_gimbal_steady: 137
  cmd_gimbal_base_ctrl: 141
  cmd_set_servo_id: 501     #54
  cmd_servo_torque: 210     #55
  cmd_set_servo_mid: 502    #58

code:
  max_res: 10101
  mid_res: 10102
  min_res: 10103
  zoom_x1: 10104
  zoom_x2: 10105
  zoom_x4: 10106

  pic_cap: 10201
  vid_sta: 10202
  vid_end: 10203

  cv_none: 10301
  cv_moti: 10302
  cv_face: 10303
  cv_objs: 10304
  cv_clor: 10305
  cv_hand: 10306
  cv_auto: 10307
  mp_face: 10308
  mp_pose: 10309

  re_none: 10401
  re_capt: 10402
  re_reco: 10403
  led_off: 10404
  led_aut: 10405
  led_ton: 10406
  base_of: 10407
  base_on: 10408
  head_ct: 10409
  base_ct: 10410

  mc_lock: 10501
  mc_unlo: 10502

  s_panid: 10901
  release: 10902
  set_mid: 10903
  s_tilid: 10904

fb:
  detect_type:  101
  led_mode:     102
  detect_react: 103
  picture_size: 104
  video_size:   105
  cpu_load:     106
  cpu_temp:     107
  ram_usage:    108
  pan_angle:    109
  tilt_angle:   110
  wifi_rssi:    111
  base_voltage: 112
  video_fps:    113
  cv_movtion_mode:  114
  base_light:   115