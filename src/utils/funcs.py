
def animate_gif(label, frames, frame_counter):
 
    label.config(image=frames[frame_counter[0]])
    frame_counter[0] = (frame_counter[0] + 1) % len(frames)
    label.after(100, animate_gif, label, frames, frame_counter)