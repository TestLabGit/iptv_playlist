set APP=%~dp0run.py
call workon pl_m3u_gen
call python3 %APP%
call cd ../src