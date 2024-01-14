import time
import glfw
import librosa
import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader
from glContexts import vertex_shader,fragment_shader,framesize_callback,processInput
from coordinates import loading_fourier_data,audio_to_coordinates,normalize_coordinates
from audio_playback import initialize_audio,play_audio
    


def main():
    
    
    filepath = "./audio_files/queen.mp3"
    audio_data,sample_rate = librosa.load(filepath,sr=None)
    audio_data = np.array(audio_data,dtype=np.float32)
    CHUNK = int(sample_rate * 0.0907)
    # CHUNK = int(sample_rate * 0.01)
        
    start_position = 0
    end_position = CHUNK
    
    if not glfw.init():
        return
    
    window = glfw.create_window(600,480,"Audio Visualizer",None, None)
    glfw.make_context_current(window)
    
    glViewport(0,0,600,480)
    glfw.set_framebuffer_size_callback(window,framesize_callback)
    
    if not window:
        glfw.terminate()
    
    fourier_transform_full = loading_fourier_data(audio_data)
    audio_points_full = audio_to_coordinates(fourier_transform_full)
    
    RESOLUTION = max(audio_points_full)
    normalized_audio_points_full = normalize_coordinates(audio_points_full,RESOLUTION)
    
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER,vbo)
    glBufferData(GL_ARRAY_BUFFER, normalized_audio_points_full.nbytes, normalized_audio_points_full, GL_STREAM_DRAW)
    
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0,2,GL_FLOAT,GL_FALSE,8,None)
    
    compile_vertex = compileShader(vertex_shader,GL_VERTEX_SHADER)
    compile_fragment = compileShader(fragment_shader,GL_FRAGMENT_SHADER)
    shader_program = glCreateProgram()
    glAttachShader(shader_program,compile_vertex)
    glAttachShader(shader_program,compile_fragment)
    glLinkProgram(shader_program)
    glUseProgram(shader_program)
    
    initialize_audio(filepath)
    play_audio()
    
    while not glfw.window_should_close(window):
        
        processInput(window)
        
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glfw.set_time(0.0)
        start_time = glfw.get_time()
        
        if end_position <= len(audio_data):
            sub_buffer_data = loading_fourier_data(audio_data[start_position:end_position:1])
            audio_points = audio_to_coordinates(sub_buffer_data)
            normalized_audio_points = normalize_coordinates(audio_points,RESOLUTION)
            
            glBindBuffer(GL_ARRAY_BUFFER, vbo)
            glBufferSubData(GL_ARRAY_BUFFER,0,normalized_audio_points)
            
            glDrawArrays(GL_LINE_STRIP,0,len(normalized_audio_points) // 2 )
            # Update positions for the next sub-buffer
            start_position += CHUNK
            end_position += CHUNK
        
        end_time = glfw.get_time()   
        
        time.sleep(0.0465) 
        # time.sleep(0.01)
        glfw.poll_events()
        glfw.swap_buffers(window)
        
    pygame.mixer.music.stop()
    pygame.mixer.quit()        
                
    glfw.terminate()
    
if __name__ == "__main__":
    main()
    
    
     

