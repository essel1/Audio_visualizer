import glfw
from OpenGL.GL import glViewport


vertex_shader = """
                    #version 330 core
                    layout(location = 0) in vec2 aPos;
                    
                    void main(){
                        gl_Position = vec4(aPos.x, aPos.y, 0.0, 1.0);
                    }
    
    
    """
    
fragment_shader = """
                    #version 330 core
                    out vec4 frag_color;
                    
                    void main(){
                        frag_color = vec4(1.0, 1.0, 1.0, 1.0);
                    }

                    """
    
    
def framesize_callback(window,width,height):
    glViewport(0,0,width,height)
    
    
def processInput(window):
    if(glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS):
        glfw.window_should_close(window,True)